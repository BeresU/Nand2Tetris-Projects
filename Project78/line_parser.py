from collections import namedtuple
from enum import Enum

ParseResults = namedtuple("ParseResults", ["command_type", "arg1", "arg2"])


class ParseResultsType(Enum):
    NONE = -1
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2


# example of commands:
# pop <variable_name> <number>
# push <variable_name> <number>
# <arithmetic_logic_command>

class LineParser:
    def parse_line(self, line):
        clean_line = self._remove_comment(line)

        if not clean_line or clean_line == "":
            return ParseResults(ParseResultsType.NONE, None, None)

        split = clean_line.split()

        if len(split) == 1:
            return ParseResults(ParseResultsType.C_ARITHMETIC, split[0], None)

        if split[0] == "push":
            return ParseResults(ParseResultsType.C_PUSH, split[1], int(split[2]))

        if split[0] == "pop":
            return ParseResults(ParseResultsType.C_POP, split[1], int(split[2]))

    @staticmethod
    def _remove_comment(line):
        return line.split("//")[0].strip()
