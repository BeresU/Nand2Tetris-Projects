from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    NONE = -1
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4


class KeywordType(Enum):
    NONE = -1
    CLASS = 0
    METHOD = 1
    FUNCTION = 2
    CONSTRUCTOR = 3
    INT = 4
    BOOLEAN = 5
    CHAR = 6
    VOID = 7
    VAR = 8
    STATIC = 9
    FIELD = 10
    LET = 11
    DO = 12
    IF = 13
    ELSE = 14
    WHILE = 15
    RETURN = 16
    TRUE = 17
    FALSE = 18
    NULL = 19
    THIS = 20


@dataclass
class ParseResults:
    token_type: TokenType
    keyword_type: KeywordType  # relevant only if token_type is KEYWORD
    symbol: str  # relevant only if token_type is SYMBOL
    identifier: str  # relevant only if token_type is IDENTIFIER
    int_val: int  # relevant only if token_type is INT_CONST
    string_val: str  # relevant only if token_type is STRING_CONST


def parse_code(line: str) -> ParseResults:
    pass


def _clean_string(line: str) -> str:
    return line.split("//")[0].strip()
