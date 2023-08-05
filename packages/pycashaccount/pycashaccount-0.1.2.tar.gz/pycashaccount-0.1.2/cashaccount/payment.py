import base58
import cashaddress


class Info:
    TYPE = None  # override
    NAME = None  # override
    data = None  # calculate

    def hexlike(self):
        """Return hex-like string for data as <Payment Type + Payment Data>."""
        return '{:02d}{}'.format(self.TYPE, self.data.lower())

    def __str__(self):
        return '{}\ntype: {}\ndata: {}'.format(self.NAME, self.TYPE, self.data)


class PaymentKeyHash(Info):
    TYPE = 1
    NAME = 'Key Hash'

    def __init__(self, address_string):
        address_string = _loose_address(address_string)
        try:
            address = cashaddress.convert.Address.from_string(address_string)
        except cashaddress.convert.InvalidAddress:
            raise ValueError('unable to interpret address as cashaddress or legacy ({})'
                             ''.format(address_string))
        self.data = _hash160(address)


def _loose_address(address_string):
    if _looks_like_cashaddr_without_prefix(address_string):
        address_string = 'bitcoincash:{}'.format(address_string)
    return address_string


def _looks_like_cashaddr_without_prefix(s):
    if s[0] != 'q':
        return False
    if len(s) != 42:
        return False
    return True


def _hash160(address):
    legacy = address.legacy_address()
    return base58.b58decode_check(legacy).hex()[2:]
