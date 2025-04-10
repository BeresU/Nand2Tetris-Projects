from symbol_table import SymbolTable
import io_module
import symbol_extractor
import assembler
import concurrent.futures


def parse_and_create_file(file_lines, file_name):
    table = SymbolTable()
    symbol_extractor.extract_symbols(file_lines, table)
    parsed_content = assembler.parse_file(file_lines, table)
    io_module.create_hack_file(file_name, parsed_content)


asm_input_files = io_module.get_asm_file_lines()

with concurrent.futures.ThreadPoolExecutor(8) as executor:
    futures = {
        executor.submit(
            parse_and_create_file, asm_input_file.data, asm_input_file.file_name
        ): asm_input_file
        for asm_input_file in asm_input_files
    }

    for future in concurrent.futures.as_completed(futures):
        future.result()
