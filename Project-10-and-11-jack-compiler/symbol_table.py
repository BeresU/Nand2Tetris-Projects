from dataclasses import dataclass
from enum import Enum
from constants import Constants


class SymbolKind(Enum):
    NONE = "none"
    STATIC = Constants.STATIC
    FIELD = Constants.THIS
    ARG = Constants.ARGUMENT
    VAR = "local"


class SymbolTable:
    @dataclass
    class _SymbolData:
        name: str
        type: str
        kind: SymbolKind
        index: int

    def __init__(self):
        self._class_table: dict[str, SymbolTable._SymbolData] = dict()
        self._subroutine_table: dict[str, SymbolTable._SymbolData] = dict()
        self._symbol_kind_table = {
            SymbolKind.STATIC: 0,
            SymbolKind.FIELD: 0,
            SymbolKind.ARG: 0,
            SymbolKind.VAR: 0,
        }

    def reset(self):
        self._subroutine_table.clear()

        for key in (k for k in self._symbol_kind_table if k in {SymbolKind.ARG, SymbolKind.VAR}):
            self._symbol_kind_table[key] = 0

    def define(self, name: str, symbol_type: str, kind: SymbolKind):
        kind_index = self._symbol_kind_table[kind]
        data = SymbolTable._SymbolData(name, symbol_type, kind, kind_index)
        self._symbol_kind_table[kind] = kind_index + 1
        symbol_table = self._class_table if kind in {SymbolKind.STATIC, SymbolKind.FIELD} else self._subroutine_table
        symbol_table[name] = data

    def var_count(self, kind: SymbolKind) -> int:
        return self._symbol_kind_table[kind]

    def kind_of(self, name: str) -> SymbolKind:
        return self._get_data(name).kind

    def type_of(self, name: str) -> str:
        return self._get_data(name).type

    def index_of(self, name: str) -> int:
        return self._get_data(name).index

    def _get_data(self, name: str) -> _SymbolData:
        if name in self._class_table:
            return self._class_table[name]
        elif name in self._subroutine_table:
            return self._subroutine_table[name]
        return SymbolTable._SymbolData(name, "", SymbolKind.NONE, -1)
