import re
import textwrap


NAME_REGEX = r'^[a-zA-Z0-9_]{1,99}$'


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


def to_hexlike(s):
    return s.encode('utf-8').hex()


def from_hexlike(hexlike_string):
    return bytes.fromhex(hexlike_string).decode('utf-8')
