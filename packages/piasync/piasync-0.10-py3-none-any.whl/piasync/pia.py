import socket
import argparse
import getpass
import io
import ipaddress
import logging
import re
import unicodedata
import zipfile
from pathlib import Path

import countrynames
import requests
from jeepney import DBusAddress, new_method_call
from jeepney.integrate.blocking import connect_and_authenticate

from . import PROJECT_DESCRIPTION
from .dbus import decode


OPENVPN_URL = 'https://www.privateinternetaccess.com/openvpn/openvpn.zip'
REMOTE_RE = re.compile(r'^remote(\s+)(?P<fqdn>[a-z0-9.-]+)')
ENDPOINT_RE = re.compile(r'^(?P<display_name>[\s\S]+)\.ovpn$')
OPENVPN_DNS = (
    '209.222.18.218',
    '209.222.18.222',
)
#
NM_BUSNAME = 'org.freedesktop.NetworkManager'
NM_SETTINGS_MANAGER = '/org/freedesktop/NetworkManager/Settings'
NM_SETTINGS_INTERFACE = 'org.freedesktop.NetworkManager.Settings'
NM_CONNECTION_INTERFACE = 'org.freedesktop.NetworkManager.Settings.Connection'

logger = logging.getLogger(__name__.split('.')[0])
logger.setLevel(logging.INFO)
term_handler = logging.StreamHandler()
logger.addHandler(term_handler)


class InvalidOVPNFile(Exception):
    pass


class PIAEndpoint(object):
    def __init__(self, name, fqdn):
        self._name = name
        self._fqdn = fqdn

    def __repr__(self):
        return f"{self._name}: {self._fqdn}"

    def __hash__(self):
        return hash((self._name, self._fqdn))

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return self._fqdn > other._fqdn

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self._name, self._fqdn) == (other._name, other._fqdn)
        return False

    @property
    def country(self):
        name_tokens = self._name.split()
        first_token_match = countrynames.to_code(name_tokens[0])
        if first_token_match is not None:
            return first_token_match
        return countrynames.to_code(self._name)

    @property
    def connection_params(self):
        # Jeepney is actually OK with handling dicts as input
        flag = ''.join(
            unicodedata.lookup(f'REGIONAL INDICATOR SYMBOL LETTER {char}')
            for char in self.country
        )
        connection_params = {
            'type': ('s', 'vpn'),
            'id': ('s', f'{flag} PIA {self._name}'),
            'autoconnect': ('b', 0),
            'metered': ('i', 2),
        }

        dns_addresses = [
            socket.htonl(int(ipaddress.IPv4Address(a))) for a in OPENVPN_DNS
        ]
        ipv4_params = {
            'address-data': ('aa{sv}', []),
            'addresses': ('aau', []),
            'dns': ('au', dns_addresses),
            'dns-search': ('as', []),
            'method': ('s', 'auto'),
            'route-data': ('aa{sv}', []),
            'routes': ('aau', []),
        }

        proxy_params = {}

        vpn_params = {
            'data': ('a{ss}', {
                'remote': self._fqdn,
                'auth': 'SHA256',
                'cipher': 'AES-256-CBC',
                'comp-lzo': 'no-by-default',
                # TODO Do something clever with secrets?
                'connection-type': 'password',
                'dev-type': 'tun',
                'password-flags': '1',
                'port': '501',
                'proto-tcp': 'yes',
            }),
            'service-type': ('s', 'org.freedesktop.NetworkManager.openvpn'),
        }

        return ({
            'connection': connection_params,
            'proxy': proxy_params,
            'vpn': vpn_params,
            'ipv4': ipv4_params,
        },)


class NMPIAConnection(object):

    def __init__(self, fqdn, uuid):
        self._fqdn = fqdn
        self._uuid = uuid

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._fqdn == other._fqdn
        return False

    def __hash__(self):
        return hash(self._fqdn)

    def __repr__(self):
        return f"{self._uuid}: {self._fqdn}"


class PIAManager(object):

    def __init__(self, args):
        self.network = set()
        self.current_connections = set()
        self._dbus_connection = None
        self._args = args

    def parse_bundle_member(self, bundle_archive, member_zipinfo):
        if not member_zipinfo.filename.endswith('.ovpn'):
            raise InvalidOVPNFile
        # TODO Display a progress bar
        logger.debug("Parsing %s", member_zipinfo.filename)
        name_matches = ENDPOINT_RE.match(member_zipinfo.filename)
        if not name_matches:
            raise InvalidOVPNFile
        endpoint_name = name_matches.group('display_name')

        with bundle_archive.open(member_zipinfo) as ovpn_file:
            for line in ovpn_file:
                line = line.decode('utf8').strip()
                matches = REMOTE_RE.match(line)
                if matches:
                    endpoint = PIAEndpoint(
                        endpoint_name, matches.group('fqdn')
                    )
                    self.network.add(endpoint)

    def fetch(self):
        openvpn_bundle_response = requests.get(OPENVPN_URL)
        if not openvpn_bundle_response.ok:
            # TODO Do something more clever
            raise ValueError

        with io.BytesIO(openvpn_bundle_response.content) as raw_bundle:
            with zipfile.ZipFile(raw_bundle, mode='r') as bundle_zip:
                for member in bundle_zip.infolist():
                    try:
                        self.parse_bundle_member(bundle_zip, member)
                    except InvalidOVPNFile:
                        logger.debug("%s not an OVPN file", member.filename)
                        continue

    @property
    def connection(self):
        if self._dbus_connection is None:
            try:
                self._dbus_connection = connect_and_authenticate(bus='SYSTEM')
            except Exception:
                raise SystemError
        return self._dbus_connection

    def enumerate_connections(self):
        settings_manager_address = DBusAddress(
            NM_SETTINGS_MANAGER, bus_name=NM_BUSNAME,
            interface=NM_SETTINGS_INTERFACE
        )
        enumeration_request = new_method_call(
            settings_manager_address, 'ListConnections'
        )
        enumeration_response = self.connection.send_and_get_reply(
            enumeration_request
        )
        for settings_object_path in enumeration_response[0]:
            settings_address = DBusAddress(
                settings_object_path, bus_name=NM_BUSNAME,
                interface=NM_CONNECTION_INTERFACE
            )
            settings_request = new_method_call(
                settings_address, 'GetSettings',
            )
            # The response's type is a{sa{sv}}
            settings_response = self.connection.send_and_get_reply(
                settings_request
            )
            connection_settings = decode('a{sa{sv}}', settings_response[0])[0]
            if self._is_pia_connection(connection_settings):
                pia_connection = NMPIAConnection(
                    connection_settings['vpn']['data']['remote'],
                    connection_settings['connection']['uuid'],
                )
                self.current_connections.add(pia_connection)

    @staticmethod
    def _is_pia_connection(connection_settings):
        if 'vpn' == connection_settings['connection']['type']:
            # TODO Use a regex or maybe even something that involves DNSSEC
            return connection_settings['vpn']['data']['remote'].endswith(
                'privateinternetaccess.com'
            )
        return False

    def sync_from_remote(self):
        # These are sets of NMPIAConnection
        endpoints_by_fqdn = {
            endpoint._fqdn: endpoint for endpoint in self.network
        }
        current_fqdns = set(
            connection._fqdn for connection in self.current_connections
        )

        # We need to access both the NM connection and the endpoint for udpates
        conn_to_modify = set(
            (extant, endpoints_by_fqdn[extant._fqdn])
            for extant in self.current_connections
            if extant._fqdn in endpoints_by_fqdn
        )
        conn_to_delete = (
            self.current_connections - set(c[0] for c in conn_to_modify)
        )

        # This is a set of PIAEndpoint
        endpoints_to_create = set(
            endpoint for endpoint in self.network if endpoint._fqdn not in
            current_fqdns
        )

        if conn_to_delete:
            logger.info("Deleting stale NM connections")
            for conn in conn_to_delete:
                self.delete_connection(conn)

        if endpoints_to_create:
            logger.info("Creating new NM connections")
            for endpoint in endpoints_to_create:
                self.create_connection(endpoint)

        if conn_to_modify:
            logger.info("Updating existing NM connections")
            for (conn, endpoint) in conn_to_modify:
                self.update_connection(conn, endpoint)

    def delete_connection(self, conn):
        logger.debug("Deleting stale connection %r", conn)
        settings_manager_address = DBusAddress(
            NM_SETTINGS_MANAGER, bus_name=NM_BUSNAME,
            interface=NM_SETTINGS_INTERFACE
        )
        get_connection_request = new_method_call(
            settings_manager_address, 'GetConnectionByUuid', 's',
            (conn._uuid,),
        )
        get_connection_response = self.connection.send_and_get_reply(
            get_connection_request
        )
        connection_address = DBusAddress(
            decode('o', get_connection_response)[0],
            bus_name=NM_BUSNAME,
            interface=NM_CONNECTION_INTERFACE,
        )
        delete_connection_request = new_method_call(
            connection_address, 'Delete',
        )
        self.connection.send_and_get_reply(
            delete_connection_request
        )

    @staticmethod
    def _inject_user_permission(connection_params):
        current_user_perm = f'user:{getpass.getuser()}:'
        connection_params[0]['connection']['permissions'] = (
            'as', [current_user_perm],
        )

    def _inject_username(self, connection_params):
        connection_params[0]['vpn']['data'][1]['username'] = \
            self._args.username

    def _inject_ca_cert(self, connection_params):
        cert_path = Path(self._args.cert).resolve()
        connection_params[0]['vpn']['data'][1]['ca'] = str(cert_path)

    def create_connection(self, endpoint):
        settings_manager_address = DBusAddress(
            NM_SETTINGS_MANAGER, bus_name=NM_BUSNAME,
            interface=NM_SETTINGS_INTERFACE
        )
        creation_params = endpoint.connection_params
        # Inject a user permission setting unless told not to
        if not self._args.all_users:
            self._inject_user_permission(creation_params)
        self._inject_username(creation_params)
        self._inject_ca_cert(creation_params)

        creation_request = new_method_call(
            settings_manager_address, 'AddConnection', 'a{sa{sv}}',
            # encode('a{sa{sv}}', endpoint.connection_params),
            endpoint.connection_params,
        )
        logger.debug("Creating NM connection for %s", endpoint._name)
        # The response's type is o (the DBus path of the new connection)
        self.connection.send_and_get_reply(
            creation_request
        )

    def update_connection(self, conn, endpoint):
        logger.debug("Updating NM connection for %s", conn._fqdn)
        settings_manager_address = DBusAddress(
            NM_SETTINGS_MANAGER, bus_name=NM_BUSNAME,
            interface=NM_SETTINGS_INTERFACE
        )
        get_connection_request = new_method_call(
            settings_manager_address, 'GetConnectionByUuid', 's',
            (conn._uuid,),
        )
        get_connection_response = self.connection.send_and_get_reply(
            get_connection_request
        )
        connection_address = DBusAddress(
            decode('o', get_connection_response)[0],
            bus_name=NM_BUSNAME,
            interface=NM_CONNECTION_INTERFACE,
        )
        update_params = endpoint.connection_params

        # Inject a user permission setting unless told not to
        if not self._args.all_users:
            self._inject_user_permission(update_params)
        self._inject_username(update_params)
        self._inject_ca_cert(update_params)

        # We need to inject the existing UUID into the updated params, else NM
        # will have a fit
        update_params[0]['connection']['uuid'] = ('s', conn._uuid)
        update_connection_request = new_method_call(
            connection_address, 'Update', 'a{sa{sv}}',
            update_params,
        )
        self.connection.send_and_get_reply(
            update_connection_request
        )


def setup_parser():
    parser = argparse.ArgumentParser(
        description=PROJECT_DESCRIPTION,
    )
    parser.add_argument(
        'username', help='Username to use for the VPN connections',
    )
    parser.add_argument(
        'cert', help='Path to the PIA root CA',
    )
    parser.add_argument(
        '-n', '--dry-run', action='store_true',
        help='Do not manipulate the NetworkManager configuration'
    )
    parser.add_argument(
        '-a', '--all-users', action='store_true',
        help='Make the connections available to all users'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Output debug information'
    )
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    logger.debug("CLI args: %r", args)
    manager = PIAManager(args)
    logger.info("Loading current PIA endpoints")
    manager.fetch()
    logger.info("Enumerating current NM connections")
    manager.enumerate_connections()
    logger.info("Syncing NM connections")
    manager.sync_from_remote()
