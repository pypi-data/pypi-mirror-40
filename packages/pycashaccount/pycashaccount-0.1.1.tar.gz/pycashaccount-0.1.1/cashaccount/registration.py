import re
import textwrap


NAME_REGEX = r'^[a-zA-Z0-9_]{1,99}$'
OP_PUSHDATA1 = '76'
OP_PUSHDATA2 = '77'
OP_PUSHDATA4 = '78'


class Registration:
    def __init__(self, name, payment_info):
        self.name = validate_name(name)
        self.payment_info = payment_info

    def __str__(self):
        info = textwrap.indent(str(self.payment_info), '  ')
        return 'name: {}\n' \
               'payment info:\n{}' \
               ''.format(self.name, info)


def validate_name(n):
    if re.match(NAME_REGEX, n):
        return n
    raise ValueError(r'name ({name}) does not meet requirements ({regex})'
                     r''.format(name=n, regex=NAME_REGEX))


def electron_markdown(registration):
    template = '<push><hex>01010101' \
               '<push><hex>{hex_name}' \
               '<push><hex>{payment_info}'
    return template.format(hex_name=to_hexlike(registration.name),
                           payment_info=registration.payment_info.hexlike())


def opreturn_hexlike(registration):
    name_hex = to_hexlike(registration.name)
    info_hex = registration.payment_info.hexlike()
    result = ''.join([
        '04',  # OP_RETURN
        '01010101',  # cash account protocol
        _minpush_for(name_hex),  # push code for name
        name_hex,
        _minpush_for(info_hex),  # push code for payment info
        info_hex,
    ])
    return result


def to_hexlike(s):
    return s.encode('utf-8').hex()


def from_hexlike(hexlike_string):
    return bytes.fromhex(hexlike_string).decode('utf-8')


def _minpush_for(hexlike):
    bytelen = len(hexlike) // 2
    assert len(hexlike) % 2 == 0
    if bytelen < 76:
        return '{:02x}'.format(bytelen)
    elif bytelen < 2**8:
        return OP_PUSHDATA1 + '{:02x}'.format(bytelen)
    elif bytelen < 2**16:
        return OP_PUSHDATA2 + '{:04x}'.format(bytelen)
    elif bytelen < 2**32:
        return OP_PUSHDATA4 + '{:08x}'.format(bytelen)
    raise ValueError('provided value is too many bytes to push ({}, max {})'.format(bytelen, 2**32))
