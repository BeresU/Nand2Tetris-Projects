from assembly_writer import AssemblyWriter
from line_parser import LineParser, ParseResultsType


def translate_vm_code_multiple_files(file_data_array):
    writer = AssemblyWriter()

    if len(file_data_array) > 1:
        writer.write_init_code()

    for data in file_data_array:
        translate_vm_code(data.data, data.file_name, writer)

    return writer.assembly_arr


def translate_vm_code(file_data, file_name, writer):
    parser = LineParser()
    writer.set_file_name(file_name)

    for line in file_data:
        parse_results = parser.parse_line(line)

        if parse_results.command_type == ParseResultsType.NONE:
            continue

        writer.translate_to_assembly(parse_results)
