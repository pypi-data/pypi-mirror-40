#!/usr/bin/env python3
import unittest
from ..ciphers.caesar import encrypt, decrypt


class TestCaesarEncryptMethods(unittest.TestCase):

    def test_caesar_encrypt_min_key(self):
        res = encrypt("abc", 1)
        self.assertEqual(res, "bcd", f"Expected 'bcd'. Got '{res}'.")
        res_strip = encrypt("abc", 1, strip_frmt=True)
        self.assertEqual(res_strip, "BCD", f"Expected 'BCD'. Got '{res_strip}'.")

    def test_caesar_encrypt_zero_key(self):
        res = encrypt("abc", 0)
        self.assertEqual(res, "abc", f"Expected 'abc'. Got '{res}'.")
        res_strip = encrypt("abc", 0, strip_frmt=True)
        self.assertEqual(res_strip, "ABC", f"Expected 'ABC'. Got '{res_strip}'.")

    def test_caesar_encrypt_neg_key(self):
        res = encrypt("abc", -1)
        self.assertEqual(res, "zab", f"Expected 'abc'. Got '{res}'")
        res_strip = encrypt("abc", -1, strip_frmt=True)
        self.assertEqual(res_strip, "ZAB", f"Expected 'ZAB'. Got '{res_strip}'.")

    def test_caesar_encrypt_wrap_in_middle(self):
        res = encrypt("abc", 25)
        self.assertEqual(res, "zab", f"Expected 'zab'. Got '{res}'.")
        res_strip = encrypt("abc", 25, strip_frmt=True)
        self.assertEqual(res_strip, "ZAB", f"Expected 'ZAB'. Got '{res_strip}'.")

    def test_caesar_encrypt_wrap_from_start(self):
        res = encrypt("abc", 30)
        self.assertEqual(res, "efg", f"Expected 'efg'. Got '{res}'.")
        res_strip = encrypt("abc", 30, strip_frmt=True)
        self.assertEqual(res_strip, "EFG", f"Expected 'EFG'. Got '{res_strip}'.")

    def test_caesar_encrypt_with_space(self):
        res = encrypt("abc def", 1)
        self.assertEqual(res, "bcd efg", f"Expected 'bcd efg'. Got '{res}'.")
        res_strip = encrypt("abc def", 1, strip_frmt=True)
        self.assertEqual(res_strip, "BCDEFG", f"Expected 'BCDEFG'. Got '{res_strip}'.")


class TestCaesarDecryptMethods(unittest.TestCase):

    def test_caesar_decrypt_min_key(self):
        res = decrypt("bcd", 1)
        self.assertEqual(res, "abc", f"Expected 'abc'. Got '{res}'.")
        res_strip = decrypt("bcd", 1, strip_frmt=True)
        self.assertEqual(res_strip, "ABC", f"Expected 'ABC'. Got '{res_strip}'.")

    def test_caesar_decrypt_zero_key(self):
        res = decrypt("abc", 0)
        self.assertEqual(res, "abc", f"Expected 'abc'. Got '{res}'.")
        res_strip = decrypt("abc", 0, strip_frmt=True)
        self.assertEqual(res_strip, "ABC", f"Expected 'ABC'. Got '{res_strip}'.")

    def test_caesar_decrypt_neg_key(self):
        res = decrypt("zab", -1)
        self.assertEqual(res, "abc", f"Expected 'abc'. Got '{res}'")
        res_strip = decrypt("zab", -1, strip_frmt=True)
        self.assertEqual(res_strip, "ABC", f"Expected 'ABC'. Got '{res_strip}'.")

    def test_caesar_decrypt_wrap_in_middle(self):
        res = decrypt("zab", 25)
        self.assertEqual(res, "abc", f"Expected 'abc'. Got '{res}'.")
        res_strip = decrypt("zab", 25, strip_frmt=True)
        self.assertEqual(res_strip, "ABC", f"Expected 'ABC'. Got '{res_strip}'.")

    def test_caesar_decrypt_wrap_from_start(self):
        res = decrypt("efg", 30)
        self.assertEqual(res, "abc", f"Expected 'efg'. Got '{res}'.")
        res_strip = decrypt("efg", 30, strip_frmt=True)
        self.assertEqual(res_strip, "ABC", f"Expected 'ABC'. Got '{res_strip}'.")

    def test_caesar_decrypt_with_space(self):
        res = decrypt("bcd efg", 1)
        self.assertEqual(res, "abc def", f"Expected 'bcd efg'. Got '{res}'.")
        res_strip = decrypt("bcd efg", 1, strip_frmt=True)
        self.assertEqual(res_strip, "ABCDEF", f"Expected 'ABCDEF'. Got '{res_strip}'.")


if __name__ == '__main__':
    unittest.main()
