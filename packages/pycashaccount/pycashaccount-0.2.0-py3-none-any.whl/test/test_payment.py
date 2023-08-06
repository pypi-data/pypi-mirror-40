import unittest

import cashaccount.payment as pay


class TestKeyHashInfo(unittest.TestCase):
    CASHADDRESS = 'bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9'
    LEGACY = '1Pa5CCeYCpWXFJXRnhZpmhJRuFg184HGHz'
    HEX160 = 'f793fe8539aa546e579954d43af6a76229f28e4e'
    INFO = '01' + HEX160

    def test_works_for_cashaddress(self):
        self.assertEqual(pay.PaymentKeyHash(self.CASHADDRESS).hexlike(), self.INFO)
        # allow missing bitcoincash prefix
        self.assertEqual(pay.PaymentKeyHash(self.CASHADDRESS.replace('bitcoincash:', '')).hexlike(), self.INFO)

    def test_works_for_legacy(self):
        self.assertEqual(pay.PaymentKeyHash(self.LEGACY).hexlike(), self.INFO)

    def test_raises_ValueError_for_invalid_addresses(self):
        with self.assertRaises(ValueError):
            pay.PaymentKeyHash('invalid address')
        with self.assertRaises(ValueError):
            pay.PaymentKeyHash('qstillinvalid')

    def test_string_has_useful_info(self):
        expected = 'Key Hash (P2PKH)\n' \
                   'type: 1\n' \
                   'data: {}'.format(self.HEX160)
        info = pay.PaymentKeyHash(self.CASHADDRESS)
        self.assertEqual(str(info), expected)


class ScriptKeyHashInfo(unittest.TestCase):
    CASHADDRESS = 'bitcoincash:pp4d24pemra2k3mths8cjxpuu6yl3a5ctvcp8mdkm9'
    LEGACY = '3BRu7EhouApLkW1EZ64T9o9yMuX5Rexz6f'
    HEX160 = '6ad55439d8faab476bbc0f89183ce689f8f6985b'
    INFO = '02' + HEX160

    def test_works_for_cashaddress(self):
        self.assertEqual(pay.PaymentScriptHash(self.CASHADDRESS).hexlike(), self.INFO)
        # allow missing bitcoincash prefix
        self.assertEqual(pay.PaymentScriptHash(self.CASHADDRESS.replace('bitcoincash:', '')).hexlike(), self.INFO)

    def test_works_for_legacy(self):
        self.assertEqual(pay.PaymentScriptHash(self.LEGACY).hexlike(), self.INFO)

    def test_string_has_useful_info(self):
        expected = 'Script Hash (P2SH)\n' \
                   'type: 2\n' \
                   'data: {}'.format(self.HEX160)
        info = pay.PaymentScriptHash(self.CASHADDRESS)
        self.assertEqual(str(info), expected)
