import unittest

import cashaccount.payment as pay


class TestKeyHashInfo(unittest.TestCase):
    CASH_ADDR = 'bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9'
    LEGACY_ADDR = '1Pa5CCeYCpWXFJXRnhZpmhJRuFg184HGHz'
    EXPECTED_HASH160 = 'f793fe8539aa546e579954d43af6a76229f28e4e'
    EXPECTED_FULL_INFO = '01' + EXPECTED_HASH160

    def test_works_for_valid_addresses(self):
        self.assertEqual(pay.PaymentKeyHash(self.CASH_ADDR).hexlike(), self.EXPECTED_FULL_INFO)
        self.assertEqual(pay.PaymentKeyHash(self.LEGACY_ADDR).hexlike(), self.EXPECTED_FULL_INFO)

        no_prefix = self.CASH_ADDR.replace('bitcoincash:', '')
        self.assertEqual(pay.PaymentKeyHash(no_prefix).hexlike(), self.EXPECTED_FULL_INFO)

    def test_raises_some_exception_for_invalid_addresses(self):
        with self.assertRaises(Exception):
            pay.PaymentKeyHash('invalid address')
        with self.assertRaises(Exception):
            pay.PaymentKeyHash('qstillinvalid')

    def test_string_has_useful_info(self):
        expected = 'Key Hash\n' \
                   'type: 1\n' \
                   'data: {}'.format(self.EXPECTED_HASH160)
        info = pay.PaymentKeyHash(self.CASH_ADDR)
        self.assertEqual(str(info), expected)
