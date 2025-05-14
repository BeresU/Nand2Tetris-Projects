import argparse
import os
import io_module
from pathlib import Path
import vm_translator

parser = argparse.ArgumentParser(description="Process a file path.")
parser.add_argument("path", type=str, help="The path to the file")

args = parser.parse_args()
full_path = os.path.abspath(args.path)

print(f"Args: {full_path}")

files_data = io_module.get_files_data(full_path)

assembly_code = vm_translator.translate_vm_code(files_data)

file_name = io_module.get_asm_file_name(args.path)

io_module.create_assembly_file(file_name, assembly_code, Path(full_path).parent)
