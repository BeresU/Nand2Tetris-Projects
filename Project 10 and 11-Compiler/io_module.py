from dataclasses import dataclass
from pathlib import Path
import shutil


@dataclass
class JackFileData:
    file_name: str
    content: list[str]


def create_output_folder(path: str):
    output_path = Path(path)

    if output_path.exists():
        shutil.rmtree(path)

    output_path.mkdir(parents=True, exist_ok=False)

def get_files_data(path: str) -> list[JackFileData]:
    data = []

    data_path = Path(path)

    if data_path.is_file():
        jack_file_data = _get_jack_file_data(path)
        data.append(jack_file_data)
    else:
        jack_files = list(data_path.glob("*.jack"))

        for jack_file in jack_files:
            jack_file_data = _get_jack_file_data(jack_file)
            data.append(jack_file_data)

    return data


def _get_jack_file_data(path: str):
    file_path = Path(path)
    print(f"opening: ${file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return JackFileData(file_path.stem, file.readlines())
