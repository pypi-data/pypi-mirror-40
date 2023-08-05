import logging

logger = logging.getLogger('piasync')

SIMPLE_TYPES = {
    'b': lambda x: bool(int(x)),
    'y': int,
    'n': int,
    'q': int,
    'i': int,
    'u': int,
    'x': int,
    't': int,
    'd': float,
    's': str,
    'o': str,
}

ARRAY_TYPE = 'a'
VARIANT_TYPE = 'v'

DICT_ENTRY_START = '{'
DICT_ENTRY_END = '}'

STRUCT_ENTRY_START = '('
STRUCT_ENTRY_END = ')'


def _sig_iter(signature):
    remaining = str(signature)
    while remaining:
        character = remaining[0]
        remaining = remaining[1:]
        if character in SIMPLE_TYPES:
            yield character, remaining
        elif character == VARIANT_TYPE:
            yield character, remaining
        elif character == ARRAY_TYPE:
            array_type, remaining = next(_sig_iter(remaining))
            yield character + array_type, remaining
        elif character == DICT_ENTRY_START:
            # Return the whole {k, v}
            key_type, remaining = next(_sig_iter(remaining))
            value_type, remaining = next(_sig_iter(remaining))
            end_type, remaining = next(_sig_iter(remaining))
            assert end_type == DICT_ENTRY_END
            yield character + key_type + value_type + end_type, remaining
        elif character == STRUCT_ENTRY_START:
            struct_type = [character]
            while True:
                struct_member_type, remaining = next(_sig_iter(remaining))
                struct_type.append(struct_member_type)
                if struct_member_type == STRUCT_ENTRY_END:
                    break
            yield "".join(struct_type), remaining
        elif character == DICT_ENTRY_END:
            yield character, remaining
        elif character == STRUCT_ENTRY_END:
            yield character, remaining
        else:
            raise ValueError


def sig_iter(signature):
    for sig, remaining in _sig_iter(signature):
        yield(sig)


def decode_single(type_indication, element):
    result = None
    logger.debug("Single element %s: %r", type_indication, element)
    if type_indication.startswith(ARRAY_TYPE):
        result = decode_sequence(type_indication, element)
    elif type_indication == VARIANT_TYPE:
        result = decode_variant(element)
    else:
        result = decode_simple_type(type_indication, element)
    return result


def decode_sequence(type_indication, sequence):
    # Whether we're dealing with an array or dict, we must exhaust all
    # PDU elements
    decoded_sequence = None
    logger.debug("Decoding sequence of type %s: %r", type_indication, sequence)
    if type_indication[1] == DICT_ENTRY_START:
        kv_sig_iter = sig_iter(type_indication[2:-1])
        key_sig = next(kv_sig_iter)
        value_sig = next(kv_sig_iter)
        logger.debug("Dict-type sequence %s -> %s", key_sig, value_sig)
        decoded_sequence = {}
        for k_v in sequence:
            key = decode_simple_type(key_sig, k_v[0])
            # This causes single to be called twice?
            value = decode_single(value_sig, k_v[1])
            decoded_sequence.update({key: value})
    else:
        array_sig_iter = sig_iter(type_indication[1:])
        array_type = next(array_sig_iter)
        logger.debug("List-type sequence %s", array_type)
        # The problem with this is that p, being an element of the pdu
        # iterable may _itself_ be an iterable, that's how we end up
        # decoding 4 out of '45' (for sig 'i')
        decoded_sequence = [decode_single(array_type, p) for p in sequence]
    return decoded_sequence


def decode_simple_type(type_sig, encoded_type):
    logger.debug("Simple element %s: %r", type_sig, encoded_type)
    try:
        return SIMPLE_TYPES[type_sig](encoded_type)
    except KeyError:
        raise ValueError


def decode_variant(variant_value):
    assert isinstance(variant_value, tuple)
    assert 2 == len(variant_value)
    # import pdb
    # pdb.set_trace()
    # pass
    # The type in a variant may be an array!
    return decode_single(variant_value[0], variant_value[1])


def decode(signature, pdu):
    result = []
    # Iterate on the sequence in the signature
    for type_indication, pdu_element in zip(sig_iter(signature), pdu):
        logger.debug(
            "Decoding PDU element %s: %r", type_indication, pdu_element
        )
        if type_indication[0] == ARRAY_TYPE:
            # decode_sequence can return a dict or a list
            decoded_element = decode_sequence(type_indication, pdu)
            result.append(decoded_element)
        elif type_indication == VARIANT_TYPE:
            decoded_element = decode_single(type_indication, pdu_element)
            result.append(decoded_element)
        else:
            decoded_element = decode_single(type_indication, pdu_element)
            result.append(decoded_element)
    return result


def encode_sequence(type_indication, sequence):
    # Whether we're dealing with an array or dict, we must exhaust all
    # PDU elements
    encoded_sequence = []
    logger.debug("Encoding sequence of type %s: %r", type_indication, sequence)
    if type_indication[1] == DICT_ENTRY_START:
        kv_sig_iter = sig_iter(type_indication[2:-1])
        key_sig = next(kv_sig_iter)
        value_sig = next(kv_sig_iter)
        logger.debug("Dict-type sequence %s -> %s", key_sig, value_sig)
        # ('ipv4',
        # [('address-data', ('aa{sv}', [])),
        # ('addresses', ('aau', [])),
        # ('dns', ('au', [])),
        # ('dns-search', ('as', [])),
        # ('method', ('s', 'auto')),
        # ('route-data', ('aa{sv}', [])),
        # ('routes', ('aau', []))]),

        # for k_v in sequence.items():
        #     key = encode_simple_type(key_sig, k_v[0])
        #     # We already have nice variants, let's pass them straight
        #     # value = encode_single(value_sig, k_v[1])
        #     encoded_sequence.append((key, k_v[1]))
        return list(sequence.items())
    else:
        array_sig_iter = sig_iter(type_indication[1:])
        array_type = next(array_sig_iter)
        logger.debug("List-type sequence %s", array_type)
        # The problem with this is that p, being an element of the pdu
        # iterable may _itself_ be an iterable, that's how we end up
        # encoding 4 out of '45' (for sig 'i')
        encoded_sequence = [encode_single(array_type, p) for p in sequence]
    return tuple(encoded_sequence)


def encode_simple_type(type_sig, native_type):
    logger.debug("Simple element %s: %r", type_sig, native_type)
    try:
        return str(native_type)
    except KeyError:
        raise ValueError


def encode_single(type_indication, element):
    result = None
    logger.debug("Single element %s: %r", type_indication, element)
    if type_indication.startswith(ARRAY_TYPE):
        result = encode_sequence(type_indication, element)
    elif type_indication == VARIANT_TYPE:
        result = encode_variant(type_indication, element)
    else:
        result = encode_simple_type(type_indication, element)
    return result


def encode_variant(type_indication, variant_value):
    # XXX Figure out something clever to determine the variant's type
    return ('s', encode_single('s', variant_value))


def encode(signature, pdu):
    result = []
    # Iterate on the sequence in the signature
    logger.debug("Encoding PDU packet %s: %r", signature, pdu)
    for type_indication, pdu_element in zip(sig_iter(signature), pdu.items()):
        logger.debug(
            "Encoding PDU element %s: %r", type_indication, pdu_element
        )
        if type_indication[0] == ARRAY_TYPE:
            encoded_element = encode_sequence(type_indication, pdu)
            result.append(encoded_element)
        elif type_indication == VARIANT_TYPE:
            encoded_element = encode_single(type_indication, pdu_element)
            result.append(encoded_element)
        else:
            encoded_element = encode_single(type_indication, pdu_element)
            result.append(encoded_element)
    return tuple(result)
