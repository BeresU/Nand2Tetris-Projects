from dataclasses import dataclass
from enum import Enum
from typing import TextIO

from constants import Constants
from pathlib import Path

import re


class TokenType(Enum):
    NONE = "none"
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"


@dataclass
class TokenData:
    token_type: TokenType
    value: str


class JackTokenizer:
    _stream: TextIO
    _line_position = 0
    _line_data: list[TokenData]

    current_token: TokenData
    has_more_tokens: bool

    _KEYWORDS = [
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

    _SYMBOLS = [
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

    def __init__(self, file_path: str):
        input_path_obj = Path(file_path)
        self.has_more_tokens = True
        self._stream = input_path_obj.open('r')
        self._line_data = []
        self.advance()

    def dispose(self):
        self._stream.close()

    def advance(self):
        self._line_position += 1

        if self._line_position < len(self._line_data):
            self.current_token = self._line_data[self._line_position]
            return

        self._line_data = []

        while len(self._line_data) == 0:
            line_data = self._stream.readline()

            if line_data == "":
                self.has_more_tokens = False
                return

            self._line_data = self._tokenize_data(line_data)

        self._line_position = 0
        self.current_token = self._line_data[0]


    def _tokenize_data(self, data: str) -> list[TokenData]:
        clean_data = JackTokenizer._clean_string(data)
        split_data = JackTokenizer._split_data(clean_data)
        return [self._create_token_data(data_string) for data_string in split_data]

    @staticmethod
    def _clean_string(code: str) -> str:
        pattern = r"""
            /\*\*.*?\*/        # block comments like /** ... */
            |^\s*\*.*$         # lines that start with '*'
            |//.*              # single-line // comments
            |/\*\*.*           # dangling /** without */
        """
        return re.sub(pattern, '', code, flags=re.DOTALL | re.MULTILINE | re.VERBOSE)

    @staticmethod
    def _split_data(data: str) -> list[str]:
        symbols = r'[\{\}\(\)\[\]\.\,\;\+\-\*\/\&\|\<\>\=\~]'
        pattern = rf'"[^"]*"|\w+|{symbols}'

        return re.findall(pattern, data)

    def _create_token_data(self, data: str) -> TokenData:
        token_type = self._get_token_type(data)
        return TokenData(token_type, JackTokenizer._get_token_value(token_type, data))

    @staticmethod
    def _get_token_value(token_type: TokenType, data: str) -> str:
        if token_type == TokenType.STRING_CONST: return data.strip('"')
        return data

    def _get_token_type(self, data: str) -> TokenType:
        if data in self._KEYWORDS: return TokenType.KEYWORD
        if data in self._SYMBOLS: return TokenType.SYMBOL
        if data.startswith('"'): return TokenType.STRING_CONST
        if data.isdigit(): return TokenType.INT_CONST
        if not data[0].isdigit(): return TokenType.IDENTIFIER

        return TokenType.NONE
