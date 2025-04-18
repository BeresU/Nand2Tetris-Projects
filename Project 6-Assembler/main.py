import argparse
import os
from pathlib import Path
from symbol_table import SymbolTable
import io_module
import symbol_extractor
import assembler
import concurrent.futures


def parse_and_create_file(file_lines, file_name):
    table = SymbolTable()
    symbol_extractor.extract_symbols(file_lines, table)
    parsed_content = assembler.parse_file(file_lines, table)
    io_module.create_hack_file(file_name, parsed_content, output_path)

parser = argparse.ArgumentParser(description="Process a file path.")
parser.add_argument("path", type=str, help="The path to the file")
parser.add_argument("-o", "--output", type=str, help="The output file path")

args = parser.parse_args()
full_path = os.path.abspath(args.path)
input_path_obj = Path(full_path)

output_path = input_path_obj if args.output is None else args.output

print(f"Args: input path: {input_path_obj}, output path: {output_path}")

asm_files_data = io_module.get_files_data(input_path_obj)

with concurrent.futures.ThreadPoolExecutor(8) as executor:
    futures = {
        executor.submit(
            parse_and_create_file, asm_input_file.data, asm_input_file.file_name
        ): asm_input_file
        for asm_input_file in asm_files_data
    }

    for future in concurrent.futures.as_completed(futures):
        future.result()
