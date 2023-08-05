import re
from ..util.functional import shift_with_wrap, keygen


def __encrypt_str(plaintext: str, keyword: str) -> str:
    ciphertext = ""

    _pt_stripped = (re.sub(r'[^a-zA-Z0-9]', "", plaintext)).upper()
    autokey = keyword.upper() + _pt_stripped

    keytext = keygen(autokey)
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
    ciphertext = ""

    plaintext = (re.sub(r'[^a-zA-Z0-9]', "", plaintext)).upper()
    autokey = keyword.upper() + plaintext

    keytext = keygen(autokey)
    for _pt_char in plaintext:
        _key_char_ord = ord(next(keytext))
        ciphertext += shift_with_wrap(_pt_char, (_key_char_ord % 65))

    return ciphertext


def encrypt(plaintext: str, keyword: str, strip_frmt=False) -> str:
    if strip_frmt:
        return __encrypt_strip_frmt(plaintext, keyword)
    else:
        return __encrypt_str(plaintext, keyword)


def __build_autokey(keyword: str, ciphertext: str) -> str:
    autokey = (re.sub(r'[^a-zA-Z0-9]', "", keyword)).upper()

    for _i in range(len(ciphertext)):
        _key_char_ord = ord(autokey[_i])
        autokey += shift_with_wrap(ciphertext[_i], (_key_char_ord % 65) * -1)

    return autokey


def __decrypt_str(ciphertext: str, autokey: str) -> str:
    plaintext = ""
    keytext = keygen(autokey)

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


def __decrypt_strip_frmt(ciphertext: str, autokey: str) -> str:
    plaintext = ""
    keytext = keygen(autokey)
    ciphertext = (re.sub(r'[^a-zA-Z0-9]', "", ciphertext)).upper()

    for _ct_char in ciphertext:
        _key_char_ord = ord(next(keytext))
        plaintext += shift_with_wrap(_ct_char, (_key_char_ord % 65) * -1)

    return plaintext


def decrypt(ciphertext: str, keyword: str, strip_frmt=False) -> str:
    autokey = __build_autokey(keyword, ciphertext)

    if strip_frmt:
        return __decrypt_strip_frmt(ciphertext, autokey)
    else:
        return __decrypt_str(ciphertext, autokey)
