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
    NAME = 'Key Hash (P2PKH)'

    def __init__(self, address_string):
        address_string = _loose_address(address_string)
        self._validate_address(address_string)
        try:
            address = cashaddress.convert.Address.from_string(address_string)
        except cashaddress.convert.InvalidAddress as e:
            raise ValueError('unable to interpret address as p2pkh: {}'.format(e))
        self.data = _hash160(address)

    @staticmethod
    def _validate_address(address_string):
        # for addresses, we just need to separate p2pkh and p2sh since they are different in cash accounts
        first_char = address_string.replace('bitcoincash:', '')[0]
        if first_char not in ['q', '1']:
            raise ValueError('expected address to start with q or 1 but got {}'.format(first_char))


class PaymentScriptHash(PaymentKeyHash):
    TYPE = 2
    NAME = 'Script Hash (P2SH)'

    @staticmethod
    def _validate_address(address_string):
        # for addresses, we just need to separate p2pkh and p2sh since they are different in cash accounts
        first_char = address_string.replace('bitcoincash:', '')[0]
        if first_char not in ['p', '3']:
            raise ValueError('expected address to start with p or 3 but got {}'.format(first_char))


def _loose_address(address_string):
    if _looks_like_cashaddr_without_prefix(address_string):
        address_string = 'bitcoincash:{}'.format(address_string)
    return address_string


def _looks_like_cashaddr_without_prefix(s):
    if s[0] not in ['p', 'q']:
        return False
    if len(s) != 42:
        return False
    return True


def _hash160(address):
    legacy = address.legacy_address()
    return base58.b58decode_check(legacy).hex()[2:]
