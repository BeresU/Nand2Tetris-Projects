from line_parser import ParseResultsType


class AssemblyWriter:
    STACK_BASE_ADDR = 256
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
    assembly_arr = []
    function_trace = []
    label_count_dict = dict()

    def set_file_name(self, file_name):
        self.file_name = file_name

    def write_init_code(self):
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"M={AssemblyWriter.STACK_BASE_ADDR}")

    def translate_to_assembly(self, parse_results):
        match parse_results.command_type:
            case ParseResultsType.C_POP:
                self._pop(parse_results.arg1, parse_results.arg2)
            case ParseResultsType.C_PUSH:
                self._push(parse_results.arg1, parse_results.arg2)
            case ParseResultsType.C_ARITHMETIC:
                self._do_logic_arithemetic(parse_results.arg1)
            case ParseResultsType.C_LABEL:
                self._write_label(parse_results.arg1)
            case ParseResultsType.C_GOTO:
                self._write_goto(parse_results.arg1)
            case ParseResultsType.C_IF:
                self._write_if(parse_results.arg1)
            case ParseResultsType.C_CALL:
                self._write_call(parse_results.arg1, parse_results.arg2)
            case ParseResultsType.C_FUNCTION:
                self.function_trace.append(parse_results)
                self._write_function(parse_results.arg1, parse_results.arg2)
            case ParseResultsType.C_RETURN:
                self._write_return()
                self.function_trace.pop()

    def _push(self, value_type, value):
        match value_type:
            case "local" | "argument" | "this" | "that":
                self._push_regular_value(AssemblyWriter.KEYWORDS_MAP[value_type], value)
            case "constant":
                self._push_constant(value)
            case "static":
                self._push_static(self.file_name, value)
            case "pointer":
                self._push_pointer(value)
            case "temp":
                self._push_temp(value)

    def _pop(self, value_type, value):
        match value_type:
            case "local" | "argument" | "this" | "that":
                self._pop_regular_value(AssemblyWriter.KEYWORDS_MAP[value_type], value)
            case "static":
                self._pop_static(self.file_name, value)
            case "pointer":
                self._pop_pointer(value)
            case "temp":
                self._pop_temp(value)

    def _do_logic_arithemetic(self, method_type):
        self._write_comment(f"do {method_type}")
        match method_type:
            case "add" | "sub" | "and" | "or":
                expression = "D+M" if method_type == "add" else "M-D" if method_type == "sub" else "D&M" if method_type == "and" else "D|M"
                self._do_logic_arithmetic_2_values(expression)
            case "not" | "neg":
                expression = "-M" if method_type == "neg" else "!M"
                self._do_logic_arithmetic_1_value(expression)
            case "eq":
                self._do_eq()
            case "gt" | "lt":
                jump_expression = "JGT" if method_type == "gt" else "JLT"
                label_name = "SET_GREATER_THEN" if method_type == "gt" else "SET_LOWER_THEN"
                self._do_boolean_logic(jump_expression, label_name)

    def _push_regular_value(self, value_type, value):
        self._write_comment(f"push: {value_type} {value}")

        self._write_assembly(f"@{value_type}")

        if value > 0:
            self._write_assembly(f"D=M")
            self._write_assembly(f"@{value}")
            self._write_assembly(f"A=D+A")
        else:
            self._write_assembly(f"A=M")

        self._write_assembly(f"D=M")
        self._push_to_stack()

    def _push_constant(self, value):
        self._write_comment(f"push: constant: {value}")

        self._write_assembly(f"@{value}")
        self._write_assembly(f"D=A")
        self._push_to_stack()

    def _push_static(self, static_name, value):
        self._write_comment(f"push static: {static_name}.{value}")

        self._write_assembly(f"@{static_name}.{value}")
        self._write_assembly(f"D=M")
        self._push_to_stack()

    def _push_pointer(self, value):
        pointer_type = AssemblyWriter._get_pointer_type(value)

        self._write_comment(f"push pointer: {pointer_type}")

        self._write_assembly(f"@{pointer_type}")
        self._write_assembly(f"D=M")
        self._push_to_stack()

    def _push_temp(self, value):
        self._write_comment(f"push temp: {value}")

        self._point_at_temp_addr(value)
        self._write_assembly(f"D=M")
        self._push_to_stack()

    def _push_to_stack(self, comp="D"):
        self._write_comment(f"RAM[{AssemblyWriter.SP_KEYWORD}] = {comp}, {AssemblyWriter.SP_KEYWORD}++")

        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"AM=M+1")
        self._write_assembly(f"A=A-1")
        self._write_assembly(f"M={comp}")

    def _pop_regular_value(self, value_type, value):
        self._write_comment(f"pop: {value_type} {value}")
        self._write_assembly(f"@{value_type}")
        self._write_assembly(f"D=M")

        if value > 0:
            self._write_assembly(f"@{value}")
            self._write_assembly(f"D=D+A")

        self._write_assembly(f"@R13")
        self._write_assembly(f"M=D")
        self._pop_stack()
        self._write_assembly(f"@R13")
        self._write_assembly(f"A=M")
        self._write_assembly(f"M=D")

    def _pop_static(self, static_name, value):
        self._write_comment(f"pop static: {static_name}.{value}")
        self._pop_stack()

        self._write_assembly(f"@{static_name}.{value}")
        self._write_assembly(f"M=D")

    def _pop_pointer(self, value):
        pointer_type = AssemblyWriter._get_pointer_type(value)
        self._write_comment(f"pop pointer: {pointer_type}")
        self._pop_stack()
        self._write_assembly(f"@{pointer_type}")
        self._write_assembly(f"M=D")

    def _pop_temp(self, value):
        self._write_comment(f"pop temp: {value}")
        self._pop_stack()
        self._point_at_temp_addr(value)
        self._write_assembly(f"M=D")

    @staticmethod
    def _get_pointer_type(value):
        return AssemblyWriter.THIS_KEYWORD if value == 0 else AssemblyWriter.THAT_KEYWORD

    def _do_logic_arithmetic_1_value(self, expression):
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"A=M-1")
        self._write_assembly(f"M={expression}")

    def _do_logic_arithmetic_2_values(self, expression):
        self._pop_stack()
        self._write_assembly(f"A=A-1")
        self._write_assembly(f"M={expression}")

    def _do_boolean_logic(self, jump_expression, label_name):
        full_label_name = f"{self._get_full_label_name(label_name)}_{self.get_label_count(label_name)}"
        continue_label = f"{self._get_full_label_name('CONTINUE')}_{self.get_label_count('CONTINUE')}"

        self._pop_stack()
        self._write_assembly(f"A=A-1")
        self._write_assembly(f"D=M-D")
        self._write_assembly(f"@{full_label_name}")
        self._write_assembly(f"D;{jump_expression}")

        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"A=M-1")
        self._write_assembly(f"M=0")
        self._write_assembly(f"@{continue_label}")
        self._write_assembly(f"0;JMP")
        self._write_assembly(f"({full_label_name})")
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"A=M-1")
        self._write_assembly(f"M=-1")
        self._write_assembly(f"({continue_label})")

    def _do_eq(self):
        self._pop_stack()
        self._write_assembly(f"A=A-1")
        self._write_assembly(f"D=M-D")
        self._write_assembly(f"D=D+1")
        self._write_assembly(f"@1")
        self._write_assembly(f"D=D&A")
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"A=M-1")
        self._write_assembly(f"M=-D")

    def _pop_stack(self):
        self._write_comment(f"{AssemblyWriter.SP_KEYWORD}--")
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"AM=M-1")
        self._write_assembly(f"D=M")

    def _point_at_temp_addr(self, value):
        temp_addr = AssemblyWriter.TEMP_BASE_ADDR + value
        self._write_assembly(f"@{temp_addr}")

    def _write_comment(self, comment):
        if AssemblyWriter.GENERATE_COMMENTS:
            self._write_assembly(f"\n// {comment}")

    def _write_assembly(self, assembly_code):
        self.assembly_arr.append(assembly_code)

    def _get_full_label_name(self, label_name):
        func_name = ""

        if len(self.function_trace) > 0:
            func_name = f".{self.function_trace[-1].arg1}"

        return f"{self.file_name}{func_name}${label_name}"

    def get_label_count(self, label_name):
        full_name = self._get_full_label_name(label_name)
        label_count = self.label_count_dict.get(full_name, 0)
        self.label_count_dict[full_name] = label_count + 1
        return label_count

    def _write_label(self, label_name):
        full_label_name = self._get_full_label_name(label_name)
        self._write_assembly(f"({full_label_name})")

    def _write_goto(self, label_name):
        self._write_comment(f"goto {label_name}")

        full_label_name = self._get_full_label_name(label_name)
        self._write_assembly(f"@{full_label_name}")
        self._write_assembly(f"0;JMP")

    def _write_if(self, label_name):
        full_label_name = self._get_full_label_name(label_name)
        self._write_comment(f"if-goto {full_label_name}")
        self._pop_stack()
        self._write_assembly(f"@{full_label_name}")
        self._write_assembly(f"D;JNE")

    def _write_call(self, function_name, args_count):
        pass

    def _write_function(self, function_name, vars_count):
        self._write_comment(f"start function: {function_name}, vars: {vars_count}")

        self._write_assembly(f"@({self.file_name}.{function_name})")
        self._write_comment(f"LCL=SP")
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@{AssemblyWriter.LCL_KEYWORD}")
        self._write_assembly(f"M=D")

        for _ in vars_count:
            self._push_to_stack("0")

    def _write_return(self):
        pass
