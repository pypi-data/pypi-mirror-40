# some_crypt
**DISCLAIMER: This package provides tools for incredibly basic encrypting and decrypting based on mostly-classical
ciphers. It by NO means provides any resources for cryptographically secure encryption/decryption and should not
be used to store data requiring any level of security.**

**_some_crypt_** is a simple utility package providing the tools for casually encrypting and decrypting strings and
text files using mostly-classical ciphers (e.g. Caesar, Vigenere, etc.).

## Contents
* some_crypt/ciphers - the ever-growing cipher implementation package; if there's a cool (mostly simple) cipher
that you'd like to see, let me know and I might add it
    * some_crypt.ciphers.autokey - [Autokey Cipher](https://en.wikipedia.org/wiki/Autokey_cipher)
    * some_crypt.ciphers.caesar - [Caesar Cipher](https://en.wikipedia.org/wiki/Caesar_cipher)
    * some_crypt.ciphers.vigenere - [Vigenere Cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
* some_crypt/util - utilities useful in cipher implementation
    * some_crypt.util.file_io - (deprecated) basic reading and writing of files; previously in use before its
    functionality was moved over to a standalone script
    * some_crypt.util.functional -
        * primarily keygen() (generator which yields the characters of the given key, repeating when necessary) and
        shift_with_wrap() (which contains the logic concerning shifting characters within the range of ASCII letter
        blocks)

## Installation
To install some_crypt, simply ```pip install some_crypt```.