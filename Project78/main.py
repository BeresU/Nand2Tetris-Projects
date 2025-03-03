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

file_data = io_module.get_vm_file_data(full_path)

print(f"file name: {file_data.file_name}, line count: {len(file_data.data)}")

assembly_code = vm_translator.translate_vm_code(file_data.data, file_data.file_name)

io_module.create_assembly_file(file_data.file_name, assembly_code, Path(full_path).parent)
