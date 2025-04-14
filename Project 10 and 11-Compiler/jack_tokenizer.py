from dataclasses import dataclass
from enum import Enum
from constants import Constants
import re


class TokenType(Enum):
    NONE = "none"
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"


KEYWORDS = [
    Constants.CLASS,
    Constants.CONSTRUCTOR,
    Constants.FUNCTION,
    Constants.METHOD,
    Constants.FIELD,
    Constants.STATIC,
    Constants.VAR,
    Constants.INT,
    Constants.CHAR,
    Constants.BOOLEAN,
    Constants.VOID,
    Constants.TRUE,
    Constants.FALSE,
    Constants.NULL,
    Constants.THIS,
    Constants.LET,
    Constants.DO,
    Constants.IF,
    Constants.ELSE,
    Constants.WHILE,
    Constants.RETURN
]

SYMBOLS = [
    Constants.LEFT_CURLY_BRACKET,
    Constants.RIGHT_CURLY_BRACKET,
    Constants.LEFT_BRACKET,
    Constants.RIGHT_BRACKET,
    Constants.LEFT_SQUARE_BRACKET,
    Constants.RIGHT_SQUARE_BRACKET,
    Constants.POINT,
    Constants.COMMA,
    Constants.SEMICOLON,
    Constants.PLUS,
    Constants.MINUS,
    Constants.ASTERISK,
    Constants.FORWARD_SLASH,
    Constants.AND,
    Constants.OR,
    Constants.LESS_THAN,
    Constants.GREATER_THAN,
    Constants.EQUAL,
    Constants.TILDA,
]


@dataclass
class TokenData:
    token_type: TokenType
    value: str


def tokenize_data(data: str) -> list[TokenData]:
    clean_data = _clean_string(data)
    split_data = _split_data(clean_data)
    return [_create_token_data(data_string) for data_string in split_data]

def _clean_string(code: str) -> str:
    pattern = r"""
        /\*\*.*?\*/        # block comments like /** ... */
        |^\s*\*.*$         # lines that start with '*'
        |//.*              # single-line // comments
        |/\*\*.*           # dangling /** without */
    """
    return re.sub(pattern, '', code, flags=re.DOTALL | re.MULTILINE | re.VERBOSE)


    return code


def _split_data(data: str) -> list[str]:
    symbols = r'[\{\}\(\)\[\]\.\,\;\+\-\*\/\&\|\<\>\=\~]'
    pattern = rf'"[^"]*"|\w+|{symbols}'

    return re.findall(pattern, data)


def _create_token_data(data: str) -> TokenData:
    token_type = _get_token_type(data)
    return TokenData(token_type, _get_token_value(token_type, data))


def _get_token_value(token_type: TokenType, data: str) -> str:
    if token_type == TokenType.STRING_CONST: return data.strip('"')
    return data


def _get_token_type(data: str) -> TokenType:
    if data in KEYWORDS: return TokenType.KEYWORD
    if data in SYMBOLS: return TokenType.SYMBOL
    if data.startswith('"'): return TokenType.STRING_CONST
    if data.isdigit(): return TokenType.INT_CONST
    if not data[0].isdigit(): return TokenType.IDENTIFIER

    return TokenType.NONE
