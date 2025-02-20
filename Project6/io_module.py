from pathlib import Path
from collections import namedtuple

AsmData = namedtuple("AsmData", ["file_name", "data"])

def get_asm_file_lines():
    parent_path = Path(__file__).parent
    input_path = parent_path / "Input"
      
    files = [f for f in input_path.iterdir() if f.is_file()]
    asm_files_data = []

    for file_path in files:
        print(f"opening: ${file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            asm_data = AsmData(file_path.stem, file.readlines())
            asm_files_data.append(asm_data)

    return asm_files_data


def create_hack_file(file_name, lines):
    parent_path = Path(__file__).parent
    output_path = parent_path / "Output" / f"{file_name}.hack"
    output_path.parent.mkdir(parents=True, exist_ok=True) 
    
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

