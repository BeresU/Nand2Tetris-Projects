from line_parser import ParseResultsType


class AssemblyWriter:
    # TODO: see where I initialize this addresses
    STACK_BASE_ADDR = 256
    LCL_BASE_ADDR = 300
    ARB_BASE_ADDR = 400
    THIS_BASE_ADDR = 3000
    THAT_BASE_ADDR = 3010
    TEMP_BASE_ADDR = 5

    SP_KEYWORD = "SP"
    LCL_KEYWORD = "LCL"
    ARG_KEYWORD = "ARG"
    THIS_KEYWORD = "THIS"
    THAT_KEYWORD = "THAT"

    KEYWORDS_MAP = {"local": LCL_KEYWORD,
                    "argument": ARG_KEYWORD,
                    "this": THIS_KEYWORD,
                    "that": THAT_KEYWORD}

    GENERATE_COMMENTS = True

    file_name = ""
    label_count = 0

    def __init__(self, file_name):
        self.file_name = file_name

    def translate_to_assembly(self, parse_results):
        assembly_code = []

        match parse_results.command_type:
            case ParseResultsType.C_POP:
                self._pop(assembly_code, parse_results.arg1, parse_results.arg2)
            case ParseResultsType.C_PUSH:
                self._push(assembly_code, parse_results.arg1, parse_results.arg2)
            case ParseResultsType.C_ARITHMETIC:
                self._do_logic_arithemetic(assembly_code, parse_results.arg1)

        return assembly_code

    def _push(self, assembly_arr, value_type, value):
        match value_type:
            case "local" | "argument" | "this" | "that":
                AssemblyWriter._push_regular_value(assembly_arr, AssemblyWriter.KEYWORDS_MAP[value_type], value)
            case "constant":
                AssemblyWriter._push_constant(assembly_arr, value)
            case "static":
                AssemblyWriter._push_static(assembly_arr, self.file_name, value)
            case "pointer":
                AssemblyWriter._push_pointer(assembly_arr, value)
            case "temp":
                AssemblyWriter._push_temp(assembly_arr, value)

    def _pop(self, assembly_arr, value_type, value):
        match value_type:
            case "local" | "argument" | "this" | "that":
                AssemblyWriter._pop_regular_value(assembly_arr, AssemblyWriter.KEYWORDS_MAP[value_type], value)
            case "static":
                AssemblyWriter._pop_static(assembly_arr, self.file_name, value)
            case "pointer":
                AssemblyWriter._pop_pointer(assembly_arr, value)
            case "temp":
                AssemblyWriter._pop_temp(assembly_arr, value)

    def _do_logic_arithemetic(self, assembly_arr, method_type):
        AssemblyWriter._write_comment(assembly_arr, f"do {method_type}")
        match method_type:
            case "add" | "sub" | "and" | "or":
                expression = "D+M" if method_type == "add" else "M-D" if method_type == "sub" else "D&M" if method_type == "and" else "D|M"
                AssemblyWriter._do_logic_arithmetic_2_values(assembly_arr, expression)
            case "not" | "neg":
                expression = "-M" if method_type == "neg" else "!M"
                AssemblyWriter._do_logic_arithmetic_1_value(assembly_arr, expression)
            case "eq":
                AssemblyWriter._do_eq(assembly_arr)
            case "gt" | "lt":
                jump_expression = "JGT" if method_type == "gt" else "JLT"
                label_name = "SET_GREATER_THEN" if method_type == "gt" else "SET_LOWER_THEN"
                AssemblyWriter._do_boolean_logic(assembly_arr, jump_expression, self.label_count, label_name)
                self.label_count += 1

    @staticmethod
    def _push_regular_value(assembly_arr, value_type, value):
        AssemblyWriter._write_comment(assembly_arr, f"push: {value_type} {value}")

        assembly_arr.append(f"@{value_type}")

        if value > 0:
            assembly_arr.append(f"D=M")
            assembly_arr.append(f"@{value}")
            assembly_arr.append(f"A=D+A")
        else:
            assembly_arr.append(f"A=M")

        assembly_arr.append(f"D=M")
        AssemblyWriter._push_to_stack(assembly_arr)

    @staticmethod
    def _push_constant(assembly_arr, value):
        AssemblyWriter._write_comment(assembly_arr, f"push: constant: {value}")

        assembly_arr.append(f"@{value}")
        assembly_arr.append(f"D=A")
        AssemblyWriter._push_to_stack(assembly_arr)

    @staticmethod
    def _push_static(assembly_arr, static_name, value):
        AssemblyWriter._write_comment(assembly_arr, f"push static: {static_name}.{value}")

        assembly_arr.append(f"@{static_name}.{value}")
        assembly_arr.append(f"D=M")
        AssemblyWriter._push_to_stack(assembly_arr)

    @staticmethod
    def _push_pointer(assembly_arr, value):
        pointer_type = AssemblyWriter._get_pointer_type(value)

        AssemblyWriter._write_comment(assembly_arr, f"push pointer: {pointer_type}")

        assembly_arr.append(f"@{pointer_type}")
        assembly_arr.append(f"D=M")
        AssemblyWriter._push_to_stack(assembly_arr)

    @staticmethod
    def _push_temp(assembly_arr, value):
        AssemblyWriter._write_comment(assembly_arr, f"push temp: {value}")

        AssemblyWriter._point_at_temp_addr(assembly_arr, value)
        assembly_arr.append(f"D=M")
        AssemblyWriter._push_to_stack(assembly_arr)

    @staticmethod
    def _push_to_stack(assembly_arr):
        AssemblyWriter._write_comment(assembly_arr,
                                      f"RAM[{AssemblyWriter.SP_KEYWORD}] = D, {AssemblyWriter.SP_KEYWORD}++")

        assembly_arr.append(f"@{AssemblyWriter.SP_KEYWORD}")
        assembly_arr.append(f"AM=M+1")
        assembly_arr.append(f"A=A-1")
        assembly_arr.append(f"M=D")

    @staticmethod
    def _pop_regular_value(assembly_arr, value_type, value):
        AssemblyWriter._write_comment(assembly_arr, f"pop: {value_type} {value}")
        assembly_arr.append(f"@{value_type}")
        assembly_arr.append(f"D=M")

        if value > 0:
            assembly_arr.append(f"@{value}")
            assembly_arr.append(f"D=D+A")

        assembly_arr.append(f"@R13")
        assembly_arr.append(f"M=D")
        AssemblyWriter._pop_stack(assembly_arr)
        assembly_arr.append(f"@R13")
        assembly_arr.append(f"A=M")
        assembly_arr.append(f"M=D")

    @staticmethod
    def _pop_static(assembly_arr, static_name, value):
        AssemblyWriter._write_comment(assembly_arr, f"pop static: {static_name}.{value}")
        AssemblyWriter._pop_stack(assembly_arr)

        assembly_arr.append(f"@{static_name}.{value}")
        assembly_arr.append(f"M=D")

    @staticmethod
    def _pop_pointer(assembly_arr, value):
        pointer_type = AssemblyWriter._get_pointer_type(value)
        AssemblyWriter._write_comment(assembly_arr, f"pop pointer: {pointer_type}")
        AssemblyWriter._pop_stack(assembly_arr)
        assembly_arr.append(f"@{pointer_type}")
        assembly_arr.append(f"M=D")

    @staticmethod
    def _pop_temp(assembly_arr, value):
        AssemblyWriter._write_comment(assembly_arr, f"pop temp: {value}")
        AssemblyWriter._pop_stack(assembly_arr)
        AssemblyWriter._point_at_temp_addr(assembly_arr, value)
        assembly_arr.append(f"M=D")

    @staticmethod
    def _get_pointer_type(value):
        return AssemblyWriter.THIS_KEYWORD if value == 0 else AssemblyWriter.THAT_KEYWORD

    @staticmethod
    def _do_logic_arithmetic_1_value(assembly_arr, expression):
        assembly_arr.append(f"@{AssemblyWriter.SP_KEYWORD}")
        assembly_arr.append(f"A=M-1")
        assembly_arr.append(f"M={expression}")

    @staticmethod
    def _do_logic_arithmetic_2_values(assembly_arr, expression):
        AssemblyWriter._pop_stack(assembly_arr)
        assembly_arr.append(f"A=A-1")
        assembly_arr.append(f"M={expression}")

    @staticmethod
    def _do_boolean_logic(assembly_arr, jump_expression, label_count, label_name):
        AssemblyWriter._pop_stack(assembly_arr)
        assembly_arr.append(f"A=A-1")
        assembly_arr.append(f"D=M-D")
        assembly_arr.append(f"@{label_name}_{label_count}")
        assembly_arr.append(f"D;{jump_expression}")

        assembly_arr.append(f"@{AssemblyWriter.SP_KEYWORD}")
        assembly_arr.append(f"A=M-1")
        assembly_arr.append(f"M=0")
        assembly_arr.append(f"@CONTINUE_{label_count}")
        assembly_arr.append(f"0;JMP")
        assembly_arr.append(f"({label_name}_{label_count})")
        assembly_arr.append(f"@{AssemblyWriter.SP_KEYWORD}")
        assembly_arr.append(f"A=M-1")
        assembly_arr.append(f"M=-1")
        assembly_arr.append(f"(CONTINUE_{label_count})")

    @staticmethod
    def _do_eq(assembly_arr):
        AssemblyWriter._pop_stack(assembly_arr)
        assembly_arr.append(f"A=A-1")
        assembly_arr.append(f"D=M-D")
        assembly_arr.append(f"D=D+1")
        assembly_arr.append(f"@1")
        assembly_arr.append(f"D=D&A")
        assembly_arr.append(f"@{AssemblyWriter.SP_KEYWORD}")
        assembly_arr.append(f"A=M-1")
        assembly_arr.append(f"M=-D")

    @staticmethod
    def _pop_stack(assembly_arr):
        AssemblyWriter._write_comment(assembly_arr, f"{AssemblyWriter.SP_KEYWORD}--")
        assembly_arr.append(f"@{AssemblyWriter.SP_KEYWORD}")
        assembly_arr.append(f"AM=M-1")
        assembly_arr.append(f"D=M")

    @staticmethod
    def _point_at_temp_addr(assembly_arr, value):
        temp_addr = AssemblyWriter.TEMP_BASE_ADDR + value
        assembly_arr.append(f"@{temp_addr}")

    @staticmethod
    def _write_comment(assembly_arr, comment):
        if AssemblyWriter.GENERATE_COMMENTS:
            assembly_arr.append(f"\n// {comment}")
