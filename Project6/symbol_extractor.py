import line_parser
from line_parser import ParseResultsType


def extract_symbols(file_lines, symbol_table):
    line_number = 0
    for line in file_lines:
        results = line_parser.parse_line(line)

        if results.resultsType is ParseResultsType.EMPTY:
            continue

        if results.resultsType is ParseResultsType.LABEL:
            symbol_table.add(results.resultsData, line_number)
            continue

        line_number += 1
