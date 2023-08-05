from typing import Generator


def shift_with_wrap(char_to_shift: str, shift_amt: int, offset=65) -> str:
    char_to_shift = char_to_shift.upper()
    return chr((((ord(char_to_shift) - offset) + shift_amt) % 26) + offset)


def keygen(keyword: str, retain_case=False) -> Generator[str, None, None]:
    """
    Initialize a generator that yields the next character in `:keyword:`,
    wrapping back to the beginning of the string when the end is reached.

    :param str keyword:
        the keyword whose characters should be yielded
    :param bool retain_case:
        whether or not to retain the original cases in `:keyword:` when yielding
    """
    pos = 0
    if not retain_case:
        keyword = keyword.upper()
    while True:
        if pos >= len(keyword):
            pos = 0
        yield keyword[pos]
        pos += 1
