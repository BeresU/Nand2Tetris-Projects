from enum import Enum
from typing import TextIO

from constants import Constants


class SegmentType(Enum):
    NONE = "none"
    CONSTANT = "constant"
    ARGUMENT = Constants.ARGUMENT
    LOCAL = "local"
    STATIC = Constants.STATIC
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


class ArithmeticCommandType(Enum):
    NONE = "none"
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
    def __init__(self, file_path: str):
        self._stream = open(f"{file_path}", "w", encoding="utf-8")

    def dispose(self):
        self._stream.close()

    def write_push(self, segment: SegmentType, index: int):
        self._write(f"\tpush {segment.value} {index}")

    def write_pop(self, segment: SegmentType, index: int):
        self._write(f"\tpop {segment.value} {index}")

    def write_arithmetic(self, arithmetic_command: ArithmeticCommandType):
        self._write(f"\t{arithmetic_command.value}")

    def write_label(self, label: str):
        self._write(f"label {label}")

    def write_goto(self, label: str):
        self._write(f"\tgoto {label}")

    def write_if(self, label: str):
        self._write(f"\tif-goto {label}")

    def write_call(self, name: str, n_args: int):
        self._write(f"\tcall {name} {n_args}")

    def write_function(self, name: str, n_vars: int):
        self._write(f"\nfunction {name} {n_vars}")

    def write_return(self):
        self._write("\treturn")

    def _write(self, text: str):
        self._stream.write(f"{text}\n")
