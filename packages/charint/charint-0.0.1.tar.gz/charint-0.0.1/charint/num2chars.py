from chars import CHARS_RADIXES


def convert(num: int, char_type_name) -> str:
    """整数を文字列に変換

    Args:
        num (int): 変換したい整数
        char_type_name (type): CHAR_TYPES に定義済みの文字列のタイプ

    Returns:
        str: 変換された数値文字列

    """
    base_chars = CHARS_RADIXES.get_chars(char_type_name)
    radix = len(base_chars)

    converted = _calc(num, radix, base_chars)
    return converted


def _calc(
    num: int,
    radix: int,
    base_chars: str,
    chars: str =''
) -> str:
    """整数から文字を計算

    Args:
        num (int): 文字列に変換される整数
        radix (int): 進数 ( 文字の種類数 )
        base_chars (str): 変換先の文字の種類
        chars (str): 前の桁の計算結果の文字列

    Returns:
        str: 整数から変換された文字
        int: 余り

    """
    div_result = int(num / radix) - 1
    rem_result = num % radix

    if div_result > -1:
        chars = _calc(div_result, radix, base_chars, chars) + chars

    chars += base_chars[rem_result]

    return chars
