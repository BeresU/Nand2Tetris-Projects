from pathlib import Path
from collections import namedtuple

VmData = namedtuple("VmData", ["file_name", "data"])


def get_vm_file_data(path):
    file_path = Path(path)
    print(f"opening: ${file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return VmData(file_path.stem, file.readlines())


def create_assembly_file(file_name, lines, target_path):
    output_path = Path(target_path) / f"{file_name}.asm"
    counter = 0

    while output_path.exists():
        output_path = target_path / f"{file_name}{counter}.asm"
        counter += 1

    output_path.write_text("\n".join(lines), encoding="utf-8")
