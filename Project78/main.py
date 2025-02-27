import argparse
import os
import io_module
from io_module import VmData
from pathlib import Path

parser = argparse.ArgumentParser(description="Process a file path.")
parser.add_argument("path", type=str, help="The path to the file")

args = parser.parse_args()
full_path = os.path.abspath(args.path)

print(f"Args: {full_path}")

file_data = io_module.get_vm_file_data(full_path)

print(f"file name: {file_data.file_name}, data count: {len(file_data.data)}")

demi_data = ["Udi", "Beres"]


io_module.create_assembly_file("test", demi_data, Path(full_path).parent)
