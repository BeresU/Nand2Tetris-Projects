from collections import namedtuple
from enum import Enum

ParseResults = namedtuple("ParseResults", ["command_type", "arg1", "arg2"])


class ParseResultsType(Enum):
    NONE = -1
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8


def parse_line(line):
    clean_line = _remove_comment(line)

    if not clean_line or clean_line == "":
        return ParseResults(ParseResultsType.NONE, None, None)

    split = clean_line.split()

    match split[0]:
        case "add" | "sub" | "neg" | "eq" | "gt" | "lt" | "and" | "or" | "not":
            return ParseResults(ParseResultsType.C_ARITHMETIC, split[0], None)
        case "push":
            return ParseResults(ParseResultsType.C_PUSH, split[1], int(split[2]))
        case "pop":
            return ParseResults(ParseResultsType.C_POP, split[1], int(split[2]))
        case "label":
            return ParseResults(ParseResultsType.C_LABEL, split[1], None)
        case "goto":
            return ParseResults(ParseResultsType.C_GOTO, split[1], None)
        case "if-goto":
            return ParseResults(ParseResultsType.C_IF, split[1], None)
        case "function":
            return ParseResults(ParseResultsType.C_FUNCTION, split[1], int(split[2]))
        case "return":
            return ParseResults(ParseResultsType.C_RETURN, None, None)
        case "call":
            return ParseResults(ParseResultsType.C_CALL, split[1], int(split[2]))

    return ParseResults(ParseResultsType.NONE, None, None)


def _remove_comment(line):
    return line.split("//")[0].strip()
