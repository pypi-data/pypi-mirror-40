from .grammar import grammar
from .parser import parser
from .expr import dice_expr
from .dice import Dice


def roll(query, with_query=False):
    if with_result:
        return parse.parse(query), query
    return parser.parse(query)

__all__ = ['parser']