from pathlib import Path
from collections import namedtuple

VmData = namedtuple("VmData", ["file_name", "data"])


def get_files_data(path):
    files_data = []

    data_path = Path(path)

    if data_path.is_file():
        vm_file_data = get_vm_file_data(path)
        files_data.append(vm_file_data)
    else:
        vm_files = list(data_path.glob("*.vm"))

        for vm_file in vm_files:
            vm_file_data = get_vm_file_data(vm_file)
            files_data.append(vm_file_data)

    return files_data


def get_asm_file_name(input_path):
    path = Path(input_path)
    return path.stem


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
