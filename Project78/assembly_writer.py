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
    _current_function = ""
    _label_count_dict = dict()

    def set_file_name(self, file_name):
        self.file_name = file_name

    def write_init_code(self):
        self._write_assembly(f"@{AssemblyWriter.STACK_BASE_ADDR}")
        self._write_assembly(f"D=A")
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"M=D")

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
                self._current_function = parse_results.arg1
                self._write_function(parse_results.arg1, parse_results.arg2)
            case ParseResultsType.C_RETURN:
                self._write_return()

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
                jump_expression = "JLE" if method_type == "gt" else "JGE"
                label_name = "GREATER_THEN" if method_type == "gt" else "LOWER_THEN"
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
        end_label_name = f"END_{label_name}"
        full_label_name = f"{end_label_name}_{self.get_label_count(end_label_name)}"

        self.increase_label_count(end_label_name)

        self._pop_stack()
        self._write_assembly(f"A=A-1")
        self._write_assembly(f"D=M-D")
        self._write_assembly(f"M=0")

        self._write_assembly(f"@{full_label_name}")
        self._write_assembly(f"D;{jump_expression}")

        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"A=M-1")
        self._write_assembly(f"M=-1")

        self._write_assembly(f"\n({full_label_name})")

    def _do_eq(self):
        self._write_comment("EQ")
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
            self._write_assembly(f"// {comment}")

    def _write_assembly(self, assembly_code):
        self.assembly_arr.append(assembly_code)

    def _get_full_label_name(self, label_name):
        func_name = f".{self._current_function}" if self._current_function != "" else ""

        return f"{self.file_name}{func_name}${label_name}"

    @staticmethod
    def get_return_label(function_name):
        return f"{function_name}$ret"

    def get_label_count(self, label_name):
        full_name = self._get_full_label_name(label_name)
        return self._label_count_dict.get(full_name, 1)

    def increase_label_count(self, label_name):
        full_name = self._get_full_label_name(label_name)
        label_count = self._label_count_dict.get(full_name, 1)
        self._label_count_dict[full_name] = label_count + 1

    def _write_label(self, label_name):
        full_label_name = self._get_full_label_name(label_name)
        self._write_assembly(f"\n({full_label_name})")

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
        self._write_comment(f"call function: {function_name}, args: {args_count}")
        return_label = self.get_return_label(function_name)
        count = self._label_count_dict.get(return_label, 1)
        full_return_label = f"{return_label}.{count}"
        self._label_count_dict[return_label] = count + 1

        self._write_comment(f"save return address")
        self._write_assembly(f"@{full_return_label}")
        self._write_assembly(f"D=A")
        self._push_to_stack()

        self._write_comment(f"push LCL of current segment")
        self._write_assembly(f"@{AssemblyWriter.LCL_KEYWORD}")
        self._write_assembly(f"D=M")
        self._push_to_stack()

        self._write_comment(f"push ARG of current segment")
        self._write_assembly(f"@{AssemblyWriter.ARG_KEYWORD}")
        self._write_assembly(f"D=M")
        self._push_to_stack()

        self._write_comment(f"push THIS of current segment")
        self._write_assembly(f"@{AssemblyWriter.THIS_KEYWORD}")
        self._write_assembly(f"D=M")
        self._push_to_stack()

        self._write_comment(f"push THAT of current segment")
        self._write_assembly(f"@{AssemblyWriter.THAT_KEYWORD}")
        self._write_assembly(f"D=M")
        self._push_to_stack()

        self._write_comment(f"ARG=SP-5-{args_count}")
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@5")
        self._write_assembly(f"D=D-A")

        if args_count > 0:
            self._write_assembly(f"@{args_count}")
            self._write_assembly(f"D=D-A")

        self._write_assembly(f"@{AssemblyWriter.ARG_KEYWORD}")
        self._write_assembly(f"M=D")

        self._write_comment(f"LCL=SP")
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@{AssemblyWriter.LCL_KEYWORD}")
        self._write_assembly(f"M=D")

        self._write_assembly(f"@{function_name}")
        self._write_assembly(f"0;JMP")

        self._write_assembly(f"\n({full_return_label})")

    def _write_function(self, function_name, vars_count):
        self._write_comment(f"FUNCTION: {function_name}, vars: {vars_count}")
        self._write_assembly(f"\n({function_name})")

        for _ in range(vars_count):
            self._push_to_stack("0")

    def _write_return(self):
        self._write_comment(f"RETURN: current function: {self._current_function}")
        self._write_comment(f"Put endframe (LCL) in temp variable")
        self._write_assembly(f"@{AssemblyWriter.LCL_KEYWORD}")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@R14")
        self._write_assembly(f"M=D")

        self._write_comment(f"Set return address (endframe-5)")
        self._write_assembly(f"@5")
        self._write_assembly(f"A=D-A")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@R13")
        self._write_assembly(f"M=D")

        self._write_comment(f"put return value in ARG")
        self._pop_stack()
        self._write_assembly(f"@{AssemblyWriter.ARG_KEYWORD}")
        self._write_assembly(f"A=M")
        self._write_assembly(f"M=D")

        self._write_comment(f"reposition SP, SP=ARG+1 to return value")
        self._write_assembly(f"@{AssemblyWriter.ARG_KEYWORD}")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@{AssemblyWriter.SP_KEYWORD}")
        self._write_assembly(f"M=D+1")

        self._write_comment(f"restore THAT = (endframe-1)")
        self._write_assembly(f"@R14")
        self._write_assembly(f"A=M-1")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@{AssemblyWriter.THAT_KEYWORD}")
        self._write_assembly(f"M=D")

        self._write_comment(f"restore THIS = (endframe-2)")
        self._write_assembly(f"@R14")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@2")
        self._write_assembly(f"A=D-A")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@{AssemblyWriter.THIS_KEYWORD}")
        self._write_assembly(f"M=D")

        self._write_comment(f"restore ARG = (endframe-3)")
        self._write_assembly(f"@R14")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@3")
        self._write_assembly(f"A=D-A")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@{AssemblyWriter.ARG_KEYWORD}")
        self._write_assembly(f"M=D")

        self._write_comment(f"restore LCL = (endframe-4)")
        self._write_assembly(f"@R14")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@4")
        self._write_assembly(f"A=D-A")
        self._write_assembly(f"D=M")
        self._write_assembly(f"@{AssemblyWriter.LCL_KEYWORD}")
        self._write_assembly(f"M=D")

        self._write_comment(f"return to caller")
        self._write_assembly(f"@R13")
        self._write_assembly(f"A=M")
        self._write_assembly(f"A;JMP")
