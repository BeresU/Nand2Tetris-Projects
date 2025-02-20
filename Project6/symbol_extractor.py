import line_parser
from line_parser import ParseResults

def extract_symbols(file_lines, symbol_table):
    line_number = 0
    for line in file_lines:
        results = line_parser.parse_line(line)

        if results.resultsType is ParseResultsType.LABEL:
            symbol_table.add(results.resultsData, line_number + 1)

        line_number += 1
        

