#!/usr/bin/env python3
import unittest
from ..ciphers.autokey import encrypt


# shoutout to https://en.wikipedia.org/wiki/Autokey_cipher
class TestAutokeyEncryptMethods(unittest.TestCase):

    def test_autokey_encrypt_pt_and_key_lowercase(self):
        res = encrypt("attack", "queenly")
        self.assertEqual(res, "qnxepv", f"Expected 'qnxepv'. Got '{res}'.")
        res_strip = encrypt("attack", "queenly", strip_frmt=True)
        self.assertEqual(res_strip, "QNXEPV", f"Expected 'QNXEPV'. Got '{res_strip}'.")

    def test_autokey_encrypt_pt_longer_key(self):
        res = encrypt("applejuice", "queenly")
        self.assertEqual(res, "qjtprusirt", f"Expected 'qjtprusirt'. Got '{res}'.")
        res_strip = encrypt("applejuice", "queenly", strip_frmt=True)
        self.assertEqual(res_strip, 'QJTPRUSIRT', f"Expected 'QJTPRUSIRT'. Got '{res_strip}'.")


if __name__ == '__main__':
    unittest.main()
