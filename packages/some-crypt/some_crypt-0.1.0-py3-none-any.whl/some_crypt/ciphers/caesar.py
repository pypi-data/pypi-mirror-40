import re
from ..util.functional import shift_with_wrap


def __encrypt_str(plaintext: str, key: int) -> str:
    """Encrypt a `str` using a caesar shift, retaining formatting"""
    ciphertext = ""

    for letter in plaintext:
        if 65 <= ord(letter) <= 90:
            # uppercase block
            ciphertext += shift_with_wrap(letter, key)
        elif 97 <= ord(letter) <= 122:
            # lowercase block
            ciphertext += shift_with_wrap(letter, key).lower()
        else:
            # any other block
            ciphertext += letter

    return ciphertext


def __encrypt_strip_frmt(plaintext: str, key: int) -> str:
    """Encrypt a `str` using a caesar shift, stripping formatting"""
    ciphertext = ""
    plaintext = (re.sub(r'[^a-zA-Z0-9]', "", plaintext)).upper()

    for letter in plaintext:
        if 65 <= ord(letter) <= 122:
            ciphertext += shift_with_wrap(letter, key)
        else:
            ciphertext += letter

    return ciphertext


def encrypt(plaintext: str, key: int, strip_frmt=False) -> str:
    """
    Encrypt `:plaintext:` using a Caesar shift of size `:key:`.\n

    By default this method retains formatting (case, spaces, punctuation).
    For example, `encrypt('Some words.', 2)` => `'Uqog yqtfu.'`.\n

    If `:strip_frmt:` is `True`, instead, formatting is stripped, returning
    an all-caps, no-spaces, no-punctuation `str`. For example,
    `encrypt('Some words.', 2, strip_frmt=True)` => `'UQOGYQTFU'`.

    :param str plaintext:
        the text to be encrypted
    :param int key:
        the amount to shift `:plaintext:`
    :param bool strip_frmt:
        [opt; def=False] whether to strip formatting from `:plaintext:`

    :return:
        the encrypted `str`
    """
    if not isinstance(key, int):
        try:
            key = int(key)
        except ValueError:
            raise

    if strip_frmt:
        return __encrypt_strip_frmt(plaintext, key)
    else:
        return __encrypt_str(plaintext, key)


def __decrypt_str(ciphertext: str, key: int) -> str:
    """Decrypt a `str` that was encrypted using a Caesar shift of size `:key:`"""
    plaintext = ""
    key *= -1

    for letter in ciphertext:
        if 65 <= ord(letter) <= 90:
            plaintext += shift_with_wrap(letter, key)
        elif 97 <= ord(letter) <= 122:
            plaintext += shift_with_wrap(letter, key).lower()
        else:
            plaintext += letter

    return plaintext


def __decrypt_strip_frmt(ciphertext: str, key: int) -> str:
    """Decrypt a `str` that was encrypted using a Caesar shift of size `:key:`, stripping formatting"""
    plaintext = ""
    ciphertext = (re.sub(r'[^a-zA-Z0-9]', "", ciphertext)).upper()
    key *= -1

    for letter in ciphertext:
        if 65 <= ord(letter) <= 122:
            plaintext += shift_with_wrap(letter, key)
        else:
            plaintext += letter

    return plaintext


def decrypt(ciphertext: str, key: int, strip_frmt=False) -> str:
    """
    Decrypt `:ciphertext:` which was encrypted using a Caesar shift of size `:key:`.\n

    By default this method retains formatting (case, spaces, punctuation).
    For example `encrypt('Uqog yqtfu.', 2)` => `'Some Words.'`\n

    If `:strip_frmt:` is `True`, instead, formatting is stripped, returning
    an all-caps, no-spaces, no-punctuation `str`. For example,
    `decrypt('Uqog yqtfu.', 2, strip_frmt=True)` => `'SOMEWORDS'`.

    :param str ciphertext:
        the text to be decrypted
    :param int key:
        the amount that `:ciphertext:` was shifted by
    :param bool strip_frmt:
        [opt; def=False] whether to strip formatting from `:ciphertext:`

    :return:
        the decrypted `str`
    """
    if not isinstance(key, int):
        try:
            key = int(key)
        except ValueError:
            raise

    if strip_frmt:
        return __decrypt_strip_frmt(ciphertext, key)
    else:
        return __decrypt_str(ciphertext, key)
