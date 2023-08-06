import unittest
from unittest import mock

import cashaccount.payment as pay
import cashaccount.registration as rgstr


class TestNameValidation(unittest.TestCase):
    def test_returns_valid_names(self):
        self.assertEqual(rgstr.validate_name('lower'), 'lower')
        self.assertEqual(rgstr.validate_name('UPPER'), 'UPPER')
        self.assertEqual(rgstr.validate_name('mixedCASE'), 'mixedCASE')
        self.assertEqual(rgstr.validate_name('mixedWITH01234'), 'mixedWITH01234')
        self.assertEqual(rgstr.validate_name('mixedWITH__01234'), 'mixedWITH__01234')
        max_length_name = 'a' * 99
        self.assertEqual(rgstr.validate_name(max_length_name), max_length_name)

    def test_raises_ValueError_for_invalid_names(self):
        with self.assertRaises(ValueError):
            rgstr.validate_name('nonalphabet文字')
        with self.assertRaises(ValueError):
            rgstr.validate_name('hyphens-not-allowed')
        with self.assertRaises(ValueError):
            too_long = 'a' * 100
            rgstr.validate_name(too_long)


class TestConverters(unittest.TestCase):
    def test_to_hex(self):
        assert rgstr.to_hexlike('emergent_reasons') == '656d657267656e745f726561736f6e73'

    def test_from_hex(self):
        assert rgstr.from_hexlike('656d657267656e745f726561736f6e73') == 'emergent_reasons'


class TestOpPush(unittest.TestCase):
    def test_minpush_works_for_short_data(self):
        self.assertEqual(rgstr._minpush_for('00' * 1), '01')  # minimum push
        self.assertEqual(rgstr._minpush_for('00' * 9), '09')
        self.assertEqual(rgstr._minpush_for('00' * 30), '1e')
        self.assertEqual(rgstr._minpush_for('00' * 75), '4b')  # max specific push code

    def test_minpush_works_for_var_data(self):
        self.assertEqual(rgstr._minpush_for('00' * 76), '764c')  # min push 1 byte
        self.assertEqual(rgstr._minpush_for('00' * (2**8-1)), '76ff')  # max push 1 byte

    def test_minpush_raises_exception_for_invalid_lengths(self):
        with self.assertRaises(Exception):
            rgstr._minpush_for('')
        with self.assertRaises(Exception):
            rgstr._minpush_for('00' * 2**8)


class TestTxOutputs(unittest.TestCase):
    def setUp(self):
        name = 'emergent_reasons'
        keyhash_info = pay.PaymentKeyHash('bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9')
        self.keyhash_registration = rgstr.Registration(name, keyhash_info)

    def test_electron_markdown_with_key_hash(self):
        expected = '<push><hex>01010101' \
                   '<push><hex>656d657267656e745f726561736f6e73' \
                   '<push><hex>01f793fe8539aa546e579954d43af6a76229f28e4e'

        self.assertEqual(rgstr.electron_markdown(self.keyhash_registration), expected)

    def test_opreturn_hex_with_key_hash(self):
        expected = ''.join([
            '04',                                           # OP_RETURN
            '01010101',                                     # cash account protocol
            '10',                                           # push x bytes of name
            '656d657267656e745f726561736f6e73',             # name
            '15',                                           # push 0x15 (21) bytes of payment info
            '01f793fe8539aa546e579954d43af6a76229f28e4e'    # 01 payment type + info
        ])
        self.assertEqual(rgstr.opreturn_hexlike(self.keyhash_registration), expected)


class TestString(unittest.TestCase):
    def test_has_useful_info(self):
        expected = 'name: emergent_reasons\n' \
                   'payment info:\n' \
                   '  some lines\n' \
                   '  of payment info'
        name = 'emergent_reasons'
        payment_info_mock = mock.MagicMock()
        payment_info_mock.__str__.return_value = 'some lines\nof payment info'
        registration = rgstr.Registration(name, payment_info_mock)
        self.assertEqual(str(registration), expected)
