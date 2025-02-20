import binary_converter
import c_instruction_parser
import line_parser
from line_parser import ParseResults
from line_parser import ParseResultsType

def parse_lines(file_lines, symbol_table):
    parsed_lines = []

    for line in file_lines:
        line_results = line_parser.parse_line(line)

        match line_results.resultsType:
            case ParseResultsType.EMPTY | ParseResultsType.LABEL:
                continue
            case ParseResultsType.CONSTANT:
                constant_to_binary = binary_converter.convert_to_binary(int(line_results.resultsData))
                parsed_lines.append(constant_to_binary)
            case ParseResultsType.VARIABLE:
                variable_data = symbol_table.get(line_results.resultsData)
                parsed_lines.append(variable_data)
            case ParseResultsType.C_INSTRUCTION:
                c_instruction_results = c_instruction_parser.parse(line_results.resultsData)
                parsed_lines.append(c_instruction_results)

    return parsed_lines
