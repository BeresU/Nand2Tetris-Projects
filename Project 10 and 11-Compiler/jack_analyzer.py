import io_module
import  compilation_engine

def analyze(input_path: str, output_path: str):
    io_module.create_output_folder(output_path)
    files_data = io_module.get_files_data(input_path)

    for file_data in files_data:
        compilation_engine.compile_class(file_data, output_path)