import shutil
from pathlib import Path
from compilation_engine import CompilationEngine


def compile_jack_code(input_path: str, output_path: str):
    _create_output_folder(output_path)

    input_path_obj = Path(input_path)

    if input_path_obj.is_file():
        _process_file(input_path, output_path)
        return

    _process_multi_files(input_path_obj, output_path)


def _create_output_folder(path: str):
    output_path = Path(path)

    if output_path.exists():
        shutil.rmtree(path)

    output_path.mkdir(parents=True, exist_ok=False)


def _process_multi_files(input_path_obj: Path, output_path: str):
    jack_files = list(input_path_obj.glob("*.jack"))

    for file in jack_files:
        _process_file(file, output_path)


def _process_file(file_path: str, output_path: str):
    compilation_engine = CompilationEngine(file_path, output_path)
    compilation_engine.compile_class()
