from symbol_table import SymbolTable
import io_module
from io_module import AsmData

import symbol_extractor
import parser


table = SymbolTable()

asm_input_files = io_module.get_asm_file_lines()[0]

symbol_extractor.extract_symbols(asm_input_files.data, table)

parsed_lines = parser.parse_lines(asm_input_files.data, table)
io_module.create_hack_file(asm_input_files.file_name, parsed_lines)
