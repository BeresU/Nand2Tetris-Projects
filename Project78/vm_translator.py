from assembly_writer import AssemblyWriter
from line_parser import LineParser, ParseResultsType

def translate_vm_code_multiple_files(file_data_array):
    output = []
    for data in file_data_array:
        assembly_code = translate_vm_code(data.data, data.file_name)
        output.extend(assembly_code)

    return output

def translate_vm_code(file_data, file_name):
    output = []
    parser = LineParser()
    writer = AssemblyWriter(file_name)

    for line in file_data:
        parse_results = parser.parse_line(line)

        if parse_results.command_type == ParseResultsType.NONE:
            continue

        assembly_code = writer.translate_to_assembly(parse_results)
        output.extend(assembly_code)

    return output
