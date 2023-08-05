from enum import Enum, unique
from functools import partial


@unique
class CHARS_RADIXES(Enum):
    """文字基数の列挙

    例 ) 0->A, 1->B, 2->C, ... , 25->Z, 26->AA, ...

    """

    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    @classmethod
    def get_all_type_names(cls) -> tuple:
        return tuple(type.name for type in cls)

    @classmethod
    def get_chars(cls, type_name) -> str:
        func = partial(
            lambda t, tn: t.name == tn,
            tn=type_name
        )

        _type = list(filter(func, cls))
        if len(_type) != 1:
            raise Exception('Chars radix not found ( {type_name} )'.format(
                type_name=type_name
            ))

        return _type[0].value
