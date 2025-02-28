from enum import Enum
from collections import namedtuple
import re


class ParseResultsType(Enum):
    EMPTY = -1
    CONSTANT = 0
    VARIABLE = 1
    LABEL = 2
    C_INSTRUCTION = 3


ParseResults = namedtuple("ParseResults", ["resultsType", "resultsData"])


def parse_line(line):
    cleaned_line = _remove_comment(line)

    if not cleaned_line or cleaned_line.strip() == "":
        return ParseResults(ParseResultsType.EMPTY, None)

    if cleaned_line.startswith("@"):
        return ParseResults(
            (
                ParseResultsType.CONSTANT
                if _is_followed_by_digits(cleaned_line)
                else ParseResultsType.VARIABLE
            ),
            _extract_after(cleaned_line, "@"),
        )

    if cleaned_line.startswith("("):
        return ParseResults(
            ParseResultsType.LABEL, _extract_inside_parentheses(cleaned_line)
        )

    return ParseResults(ParseResultsType.C_INSTRUCTION, cleaned_line)


def _remove_comment(line):
    return line.split("//")[0].strip()


def _is_followed_by_digits(line):
    return bool(re.match(r"@\d+$", line))


def _extract_after(line, character):
    return line[1:] if line.startswith(f"{character}") else line


def _extract_inside_parentheses(line):
    start = line.find("(") + 1
    end = line.find(")")
    return line[start:end] if start > 0 and end > 0 else ""
