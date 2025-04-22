from enum import Enum
from typing import TextIO

from constants import Constants


class SegmentType(Enum):
    NONE = "none",
    CONSTANT = "constant"
    ARGUMENT = Constants.ARGUMENT
    LOCAL = "local"
    STATIC = Constants.STATIC
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


class ArithmeticCommandType(Enum):
    NONE = "none",
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


class VmWriter:
    _stream: TextIO

    def __init__(self, file_path: str):
        self._stream = open(f"{file_path}.vm", "w", encoding="utf-8")

    def dispose(self):
        self._stream.close()

    def write_push(self, segment: SegmentType, index: int):
        pass

    def write_pop(self, segment: SegmentType, index: int):
        pass

    def write_arithmetic(self, arithmetic_command: ArithmeticCommandType):
        pass

    def write_label(self, label: str):
        pass

    def write_goto(self, label: str):
        pass

    def write_if(self, label: str):
        pass

    def write_call(self, name: str, n_args: int):
        pass

    def write_function(self, name: str, n_args: int):
        pass

    def write_return(self):
        pass

    def _write(self, text: str):
        self._stream.write(text)
