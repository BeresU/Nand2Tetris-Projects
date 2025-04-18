from pathlib import Path
from collections import namedtuple

AsmData = namedtuple("AsmData", ["file_name", "data"])


def get_files_data(path):
    files_data = []

    data_path = Path(path)

    if data_path.is_file():
        vm_file_data = get_asm_file(path)
        files_data.append(vm_file_data)
    else:
        vm_files = list(data_path.glob("*.asm"))

        for vm_file in vm_files:
            vm_file_data = get_asm_file(vm_file)
            files_data.append(vm_file_data)

    return files_data


def get_asm_file(path):
    file_path = Path(path)
    print(f"opening: ${file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return AsmData(file_path.stem, file.readlines())


def create_hack_file(file_name, lines, output_path):
    output_path_obj = Path(output_path) / f"{file_name}.hack"

    counter = 0
    while output_path_obj.exists():
        output_path_obj = Path(output_path) / f"{file_name}_{counter}.hack"
        counter += 1

    output_path_obj.parent.mkdir(parents=True, exist_ok=True)

    output_path_obj.write_text("\n".join(lines), encoding="utf-8")
