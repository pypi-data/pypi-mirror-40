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


class TestElectronMarkdown(unittest.TestCase):
    def test_key_hash(self):
        expected = '<push><hex>01010101' \
                   '<push><hex>656d657267656e745f726561736f6e73' \
                   '<push><hex>01f793fe8539aa546e579954d43af6a76229f28e4e'

        name = 'emergent_reasons'
        payment_info = pay.PaymentKeyHash('bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9')
        registration = rgstr.Registration(name, payment_info)
        self.assertEqual(rgstr.electron_markdown(registration), expected)


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
