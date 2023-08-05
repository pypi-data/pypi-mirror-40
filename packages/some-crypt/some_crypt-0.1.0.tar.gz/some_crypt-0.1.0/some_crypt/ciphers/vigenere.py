import re
from ..util.functional import shift_with_wrap, keygen


def __encrypt_str(plaintext: str, keyword: str) -> str:
    """Encrypt a `str` using a vigenere cipher, retaining formatting"""
    ciphertext = ""

    keytext = keygen(keyword)
    for _pt_char in plaintext:
        if 65 <= ord(_pt_char) <= 90:
            # uppercase block
            _key_char_ord = ord(next(keytext))
            ciphertext += shift_with_wrap(_pt_char, (_key_char_ord % 65))
        elif 97 <= ord(_pt_char) <= 122:
            # lowercase block
            _key_char_ord = ord(next(keytext))
            ciphertext += shift_with_wrap(_pt_char.upper(), (_key_char_ord % 65)).lower()
        else:
            # any other block
            ciphertext += _pt_char

    return ciphertext


def __encrypt_strip_frmt(plaintext: str, keyword: str) -> str:
    """Encrypt a `str` using a vigenere cipher, stripping formatting"""
    ciphertext = ""

    keytext = keygen(keyword)
    plaintext = (re.sub(r'[^a-zA-Z0-9]', "", plaintext)).upper()

    for _pt_char in plaintext:
        _key_char_ord = ord(next(keytext))
        ciphertext += shift_with_wrap(_pt_char, (_key_char_ord % 65))

    return ciphertext


def encrypt(plaintext: str, keyword: str, strip_frmt=False) -> str:
    """
    Encrypt `:plaintext:` using a Vigenere cipher with a key formed from
    `:keyword:`.\n

    By default this method retains formatting (case, spaces, punctuation)
    when returning the ciphertext, though non-letters are simply ignored for
    the purposes of shifting and reinserted before returning. For example,
    `encrypt('Some words.', 'key')` => `Csko ambhq.`.\n

    If `:strip_frmt:` is `True`, instead, formatting is stripped, returning
    an all-caps, no-spaces, no-punctuation `str`. For example,
    `encrypt('Some words.', 'key', strip_frmt=True)` => `'CSKOAMBHQ'`.

    :param str plaintext:
        the text to be encrypted
    :param str keyword:
        the keyword to form the key from (repeated until `len(key) = len(plaintext)`
    :param bool strip_frmt:
        [opt; def=False] whether to strip formatting from `:plaintext:`

    :return:
        the encrypted `str`
    """
    if strip_frmt:
        return __encrypt_strip_frmt(plaintext, keyword)
    else:
        return __encrypt_str(plaintext, keyword)


def __decrypt_str(ciphertext: str, keyword: str) -> str:
    plaintext = ""

    keytext = keygen(keyword)
    for _ct_char in ciphertext:
        if 65 <= ord(_ct_char) <= 90:
            # uppercase block
            _key_char_ord = ord(next(keytext))
            plaintext += shift_with_wrap(_ct_char, (_key_char_ord % 65) * -1)
        elif 97 <= ord(_ct_char) <= 122:
            # lowercase block
            _key_char_ord = ord(next(keytext))
            plaintext += shift_with_wrap(_ct_char.upper(), (_key_char_ord % 65) * -1).lower()
        else:
            # any other block
            plaintext += _ct_char

    return plaintext


def __decrypt_strip_frmt(ciphertext: str, keyword: str) -> str:
    plaintext = ""

    keytext = keygen(keyword)
    ciphertext = (re.sub(r'[^a-zA-Z0-9]', "", ciphertext)).upper()

    for _ct_char in ciphertext:
        _key_char_ord = ord(next(keytext))
        plaintext += shift_with_wrap(_ct_char, (_key_char_ord % 65) * -1)

    return plaintext


def decrypt(ciphertext: str, keyword: str, strip_frmt=False) -> str:
    if strip_frmt:
        return __decrypt_strip_frmt(ciphertext, keyword)
    else:
        return __decrypt_str(ciphertext, keyword)
