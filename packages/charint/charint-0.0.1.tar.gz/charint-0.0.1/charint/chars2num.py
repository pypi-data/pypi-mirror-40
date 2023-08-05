from chars import CHARS_RADIXES


def convert(chars: str, char_type_name: str) -> int:
    base_chars = CHARS_RADIXES.get_chars(char_type_name)
    radix = len(base_chars)

    num = 0
    for index, char in enumerate(chars[::-1]):
        position = base_chars.find(char)
        if position == -1:
            raise Exception()
        num += (1 + position) * (radix ** index)
    return num - 1
