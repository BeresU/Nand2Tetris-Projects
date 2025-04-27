from pathlib import Path
from xml.etree.ElementTree import Element
from tokens_xml_handler import TokenXmlHandler
from jack_tokenizer import JackTokenizer, TokenData
import xml.etree.ElementTree as ET
from constants import Constants
from jack_tokenizer import TokenType
from symbol_table import SymbolTable
from symbol_table import SymbolKind
from vm_writer import VmWriter
from vm_writer import SegmentType
from vm_writer import ArithmeticCommandType


class CompilationEngine:
    _OP_COMMEND_DICT = {Constants.PLUS: ArithmeticCommandType.ADD,
                        Constants.MINUS: ArithmeticCommandType.SUB,
                        Constants.AND: ArithmeticCommandType.AND,
                        Constants.OR: ArithmeticCommandType.OR,
                        Constants.LESS_THAN: ArithmeticCommandType.LT,
                        Constants.GREATER_THAN: ArithmeticCommandType.GT,
                        Constants.EQUAL: ArithmeticCommandType.EQ,
                        Constants.TILDA: ArithmeticCommandType.NOT}

    _CLASS = "class"
    _SUBROUTINE = "subroutine"
    _EXPRESSION_USE = "expression use"
    _SET_ATTRIBUTES = True

    def __init__(self, file_path: str, output_path: str):
        self._file_path = file_path
        self._output_path = output_path
        self._tokens_xml_handler = TokenXmlHandler()
        self._tokenizer = JackTokenizer(file_path)
        self._symbol_table = SymbolTable()
        self._running_index = 0

        input_path_obj = Path(self._file_path)
        self._file_name = input_path_obj.stem
        full_vm_path = f"{self._output_path}/{self._file_name}.vm"
        self._vm_writer = VmWriter(full_vm_path)

    def _on_finish(self):
        self._tokenizer.dispose()
        self._tokens_xml_handler.create_xml(self._file_name, self._output_path)
        self._create_xml_file(self._file_name)
        self._vm_writer.dispose()

    def _create_xml_file(self, file_name: str):
        tree = ET.ElementTree(self._xml_root_element)
        full_path = f"{self._output_path}/{file_name}.xml"
        tree.write(full_path, encoding="utf-8", xml_declaration=False, short_empty_elements=False)

    def compile_class(self):
        self._xml_root_element = ET.Element(Constants.CLASS)
        self._process(Constants.CLASS, TokenType.KEYWORD, self._xml_root_element)

        self._process(self._tokenizer.current_token.value, TokenType.IDENTIFIER, self._xml_root_element, "class name")
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, self._xml_root_element)

        while self._tokenizer.current_token.value in {Constants.FIELD, Constants.STATIC}:
            self._compile_class_var_dec(self._xml_root_element)

        while self._tokenizer.current_token.value in {Constants.FUNCTION, Constants.METHOD, Constants.CONSTRUCTOR}:
            self._compile_subroutine(self._xml_root_element)

        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, self._xml_root_element)

        self._on_finish()

    def _compile_class_var_dec(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "classVarDec")

        # field\static keyword
        symbol_kind = SymbolKind[self._tokenizer.current_token.value.upper()]
        self._process(self._tokenizer.current_token.value, TokenType.KEYWORD, sub_element)

        # variable type (int\string\etc)
        symbol_type = self._tokenizer.current_token.value
        self._process(self._tokenizer.current_token.value, self._tokenizer.current_token.token_type, sub_element)

        # in case the variable declared with comma we loop
        while self._tokenizer.current_token.value != Constants.SEMICOLON:
            usage = None

            if self._tokenizer.current_token.value != Constants.COMMA:
                self._symbol_table.define(self._tokenizer.current_token.value, symbol_type, symbol_kind)
                usage = f"{symbol_kind.value} declaration"

            self._process(self._tokenizer.current_token.value, self._tokenizer.current_token.token_type, sub_element,
                          usage)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)

    def _compile_subroutine(self, xml_element: Element):
        current_token = self._tokenizer.current_token
        sub_element = ET.SubElement(xml_element, "subroutineDec")
        self._symbol_table.reset()

        subroutine_type = current_token.value

        if subroutine_type == Constants.METHOD:
            self._symbol_table.define("this", self._file_name, SymbolKind.ARG)

        self._process(current_token.value, TokenType.KEYWORD, sub_element)
        self._process(self._tokenizer.current_token.value, self._tokenizer.current_token.token_type, sub_element)

        subroutine_name = self._tokenizer.current_token.value
        self._process(self._tokenizer.current_token.value, TokenType.IDENTIFIER, sub_element, "subroutine declaration")
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, sub_element)

        self._compile_parameter_list(sub_element)
        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, sub_element)
        self._compile_subroutine_body(subroutine_name, subroutine_type, sub_element)

    def _compile_parameter_list(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "parameterList")

        if self._tokenizer.current_token.value == Constants.RIGHT_BRACKET: return

        self._compile_parameter(sub_element)

        while self._tokenizer.current_token.value == Constants.COMMA:
            self._process(Constants.COMMA, TokenType.SYMBOL, sub_element)
            self._compile_parameter(sub_element)

    def _compile_parameter(self, xml_element: Element):
        symbol_type = self._tokenizer.current_token.value
        self._process(self._tokenizer.current_token.value, self._tokenizer.current_token.token_type, xml_element)
        self._symbol_table.define(self._tokenizer.current_token.value, symbol_type, SymbolKind.ARG)
        self._process(self._tokenizer.current_token.value, TokenType.IDENTIFIER, xml_element, "parameter list")

    def _compile_subroutine_body(self, subroutine_name: str, subroutine_type: str, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "subroutineBody")
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

        while self._tokenizer.current_token.value == Constants.VAR:
            self._compie_var_dec(sub_element)

        local_var_count = self._symbol_table.var_count(SymbolKind.VAR)
        self._vm_writer.write_function(f"{self._file_name}.{subroutine_name}", local_var_count)

        if subroutine_type == Constants.CONSTRUCTOR:
            field_count = self._symbol_table.var_count(SymbolKind.FIELD)
            self._vm_writer.write_push(SegmentType.CONSTANT, field_count)
            self._vm_writer.write_call(Constants.OS_MEM_ALLOC, 1)
            self._vm_writer.write_pop(SegmentType.POINTER, 0)  # Set allocated memory address
        elif subroutine_type == Constants.METHOD:
            self._vm_writer.write_push(SegmentType.ARGUMENT, 0)
            self._vm_writer.write_pop(SegmentType.POINTER, 0)

        self._compile_statements(sub_element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

    def _compie_var_dec(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "varDec")
        self._process(Constants.VAR, TokenType.KEYWORD, sub_element)

        symbol_type = self._tokenizer.current_token.value
        self._process(self._tokenizer.current_token.value, self._tokenizer.current_token.token_type, sub_element)

        while self._tokenizer.current_token.value != Constants.SEMICOLON:
            if self._tokenizer.current_token.value != Constants.COMMA:
                self._symbol_table.define(self._tokenizer.current_token.value, symbol_type, SymbolKind.VAR)

            self._process(self._tokenizer.current_token.value, self._tokenizer.current_token.token_type, sub_element,
                          "subroutine variable declaration")

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)

    def _compile_statements(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "statements")

        statement_keywords = {
            Constants.LET, Constants.IF, Constants.WHILE, Constants.DO, Constants.RETURN
        }

        while self._tokenizer.current_token.value in statement_keywords:
            token_value = self._tokenizer.current_token.value

            if token_value == Constants.IF: self._compile_if(sub_element)
            if token_value == Constants.LET: self._compile_let(sub_element)
            if token_value == Constants.WHILE: self._compile_while(sub_element)
            if token_value == Constants.DO: self._compile_do(sub_element)
            if token_value == Constants.RETURN: self._compile_return(sub_element)

    def _compile_if(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "ifStatement")
        self._process(Constants.IF, TokenType.KEYWORD, sub_element)
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, sub_element)

        self._compile_expression(sub_element)  # expression

        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, sub_element)

        label = self._get_unique_label()
        self._vm_writer.write_arithmetic(ArithmeticCommandType.NOT)  # flip the expression output
        self._vm_writer.write_if(label)

        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)
        self._compile_statements(sub_element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

        if self._tokenizer.current_token.value == Constants.ELSE:
            else_label = label
            label = self._get_unique_label()
            self._vm_writer.write_goto(label)
            self._vm_writer.write_label(else_label)
            self._process(Constants.ELSE, TokenType.KEYWORD, sub_element)
            self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)
            self._compile_statements(sub_element)
            self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

        self._vm_writer.write_label(label)  # continue

    def _compile_let(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "letStatement")
        self._process(Constants.LET, TokenType.KEYWORD, sub_element)

        var_name = self._tokenizer.current_token.value
        self._process(self._tokenizer.current_token.value, TokenType.IDENTIFIER, sub_element, "let")

        if self._tokenizer.current_token.value == Constants.LEFT_SQUARE_BRACKET:
            self.handle_let_array(sub_element, var_name)
        else:
            self.handle_let_field(sub_element, var_name)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)

    def handle_let_array(self, xml_element: Element, array_field_name: str):
        self._compile_array(xml_element, array_field_name)
        self._process(Constants.EQUAL, TokenType.SYMBOL, xml_element)
        self._compile_expression(xml_element)

        # pop expression value to array[index]
        self._vm_writer.write_pop(SegmentType.TEMP, 0)  # TODO: need to see if need that...
        self._vm_writer.write_pop(SegmentType.POINTER, 1)  # last value before temp is the array address...
        self._vm_writer.write_push(SegmentType.TEMP, 0)
        self._vm_writer.write_pop(SegmentType.THAT, 0)

    def handle_let_field(self, xml_element: Element, var_name: str):
        self._process(Constants.EQUAL, TokenType.SYMBOL, xml_element)
        self._compile_expression(xml_element)
        field_data = self._get_vm_var_data(var_name)
        self._vm_writer.write_pop(field_data[0], field_data[1])

    def _compile_while(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "whileStatement")
        self._process(Constants.WHILE, TokenType.KEYWORD, sub_element)
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, sub_element)
        loop_label = f"loop_{self._get_unique_label()}"
        end_loop_label = f"end_loop_{self._get_unique_label()}"

        # loop condition expression
        self._vm_writer.write_label(loop_label)
        self._compile_expression(sub_element)
        self._vm_writer.write_arithmetic(ArithmeticCommandType.NOT)
        self._vm_writer.write_if(end_loop_label)

        # loop statements
        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, sub_element)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)
        self._compile_statements(sub_element)
        self._vm_writer.write_goto(loop_label)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

        self._vm_writer.write_label(end_loop_label)

    def _compile_do(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "doStatement")
        self._process(Constants.DO, TokenType.KEYWORD, sub_element)
        identifier_name = self._tokenizer.current_token.value
        self._process(identifier_name, TokenType.IDENTIFIER, sub_element, "do")
        self._compile_subroutine_call(identifier_name, sub_element)
        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)
        self._vm_writer.write_pop(SegmentType.TEMP, 0)  # dispose last variable in the stack

    def _compile_return(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "returnStatement")
        self._process(Constants.RETURN, TokenType.KEYWORD, sub_element)

        if self._tokenizer.current_token.value != Constants.SEMICOLON:
            self._compile_expression(sub_element)
        else:
            self._vm_writer.write_push(SegmentType.CONSTANT, 0)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)
        self._vm_writer.write_return()

    def _compile_expression_list(self, xml_element: Element) -> int:
        sub_element = ET.SubElement(xml_element, "expressionList")
        if self._tokenizer.current_token.value == Constants.RIGHT_BRACKET: return 0

        self._compile_expression(sub_element)
        var_count = 1

        while self._tokenizer.current_token.value == Constants.COMMA:
            self._process(Constants.COMMA, TokenType.SYMBOL, sub_element)
            self._compile_expression(sub_element)
            var_count += 1

        return var_count

    def _compile_expression(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "expression")
        self._compile_term(sub_element)

        op_set = {Constants.PLUS, Constants.MINUS, Constants.ASTERISK, Constants.FORWARD_SLASH, Constants.AND,
                  Constants.OR, Constants.LESS_THAN, Constants.GREATER_THAN, Constants.EQUAL}

        while self._tokenizer.current_token.value in op_set:
            op_symbol = self._tokenizer.current_token.value
            self._process(self._tokenizer.current_token.value, TokenType.SYMBOL, sub_element)
            self._compile_term(sub_element)
            self._write_op(op_symbol)

    def _compile_term(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "term")
        current_token = self._tokenizer.current_token

        self._process(current_token.value, current_token.token_type, sub_element, CompilationEngine._EXPRESSION_USE)

        if current_token.value == Constants.LEFT_BRACKET:
            self._compile_expression(sub_element)
            self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, sub_element)
        elif current_token.value in {Constants.TILDA, Constants.MINUS}:
            self._compile_term(sub_element)
            if current_token.value == Constants.MINUS:
                self._vm_writer.write_arithmetic(ArithmeticCommandType.NEG)
            else:
                self._write_op(current_token.value)
        elif self._tokenizer.current_token.value == Constants.LEFT_SQUARE_BRACKET:
            self._compile_array(sub_element, current_token.value)
            self._vm_writer.write_pop(SegmentType.POINTER, 1)
            self._vm_writer.write_push(SegmentType.THAT, 0)
        elif self._tokenizer.current_token.value == Constants.POINT:
            self._compile_subroutine_call(current_token.value, sub_element)
        else:
            self._push_var(current_token)

    def _push_var(self, token_data: TokenData):
        if token_data.token_type == TokenType.INT_CONST:
            self._vm_writer.write_push(SegmentType.CONSTANT, int(token_data.value))
        elif token_data.value in {Constants.NULL, Constants.FALSE}:
            self._vm_writer.write_push(SegmentType.CONSTANT, 0)
        elif token_data.value == Constants.TRUE:
            self._vm_writer.write_push(SegmentType.CONSTANT, 1)
            self._vm_writer.write_arithmetic(ArithmeticCommandType.NEG)
        elif token_data.value == Constants.THIS:
            self._vm_writer.write_push(SegmentType.POINTER, 0)
        elif token_data.token_type == TokenType.STRING_CONST:
            self._vm_writer.write_push(SegmentType.CONSTANT, len(token_data.value))
            self._vm_writer.write_call(Constants.OS_STRING_NEW, 1)
            for c in token_data.value:
                self._vm_writer.write_push(SegmentType.CONSTANT, ord(c))
                self._vm_writer.write_call(Constants.OS_STRING_APPEND, 2)
        else:
            var_data = self._get_vm_var_data(token_data.value)  # TODO: should handle this here?
            self._vm_writer.write_push(var_data[0], var_data[1])

    # push vm code that select index value: push: arr[i]
    # TODO: I really hope i'll work...
    # TODO: Need to check if its work for the other use case...
    # TODO: Rename method?
    def _compile_array(self, xml_element: Element, array_field_name: str):
        self._process(Constants.LEFT_SQUARE_BRACKET, TokenType.SYMBOL, xml_element)
        array_data = self._get_vm_var_data(array_field_name)
        self._vm_writer.write_push(array_data[0], array_data[1])  # push array base address
        self._compile_expression(xml_element)  # push index value
        self._vm_writer.write_arithmetic(ArithmeticCommandType.ADD)  # add addresses
        self._process(Constants.RIGHT_SQUARE_BRACKET, TokenType.SYMBOL, xml_element)

    def _compile_subroutine_call(self, identifier_name: str, xml_element: Element):
        if self._tokenizer.current_token.value == Constants.LEFT_BRACKET:
            identifier_name = f"{self._file_name}.{identifier_name}"  # This is an inner class call
            self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, xml_element)
            self._vm_writer.write_push(SegmentType.POINTER, 0)
            var_count = self._compile_expression_list(xml_element) + 1
            self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, xml_element)
        else:
            self._process(Constants.POINT, TokenType.SYMBOL, xml_element)

            subroutine_name = self._tokenizer.current_token.value

            self._process(self._tokenizer.current_token.value, TokenType.IDENTIFIER, xml_element,
                          CompilationEngine._EXPRESSION_USE)

            self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, xml_element)

            var_data = self._get_vm_var_data(identifier_name)
            var_count = 0

            # In case it's not a static call: SomeStaticClass.SomeMethod()
            if var_data[0] != SegmentType.NONE:
                self._vm_writer.write_push(var_data[0], var_data[1])
                var_count += 1  # +1 for address of the callee
                method_prefix = self._symbol_table.type_of(identifier_name)
            else:
                method_prefix = identifier_name

            var_count += self._compile_expression_list(xml_element)

            self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, xml_element)

            identifier_name = f"{method_prefix}.{subroutine_name}"

        self._vm_writer.write_call(identifier_name, var_count)

    def _write_op(self, op_symbol: str):
        if op_symbol == Constants.ASTERISK:
            self._vm_writer.write_call(Constants.OS_MULT, 2)
        elif op_symbol == Constants.FORWARD_SLASH:
            self._vm_writer.write_call(Constants.OS_DIV, 2)
        else:
            op_command = CompilationEngine._OP_COMMEND_DICT[op_symbol]
            self._vm_writer.write_arithmetic(op_command)

    def _process(self, token_value: str, token_type: TokenType, xml_element: Element, usage: str = None):
        current_token = self._tokenizer.current_token

        if current_token.token_type != token_type:
            self._raise_error(
                f"Got: {current_token.token_type.name} expected: {token_type.name}, "
                f"token value: {current_token.value}, line:{self._tokenizer.line_count}, file: {self._file_path}")

        if current_token.token_type in {TokenType.KEYWORD, TokenType.SYMBOL} and current_token.value != token_value:
            self._raise_error(
                f"Got: {current_token.value}, expected: {token_value}, line:{self._tokenizer.line_count},  file: {self._file_path}")

        sub_element = ET.SubElement(xml_element, current_token.token_type.value)
        sub_element.text = f" {current_token.value} "  # add spaces since the compare file has spaces

        self._tokens_xml_handler.write_to_xml(current_token)
        self._tokenizer.advance()

        if usage is not None and CompilationEngine._SET_ATTRIBUTES:
            self._add_attribute_to_identifier(sub_element, current_token, usage)

    def _raise_error(self, error_message: str):
        self._on_finish()
        raise ValueError(error_message)

    def _add_attribute_to_identifier(self, xml_element: Element, token_data: TokenData, usage: str):
        if token_data.token_type != TokenType.IDENTIFIER: return

        symbol_kind = self._symbol_table.kind_of(token_data.value)

        identifier_category = ""

        if symbol_kind == SymbolKind.NONE:
            if self._tokenizer.current_token.value in {Constants.POINT, Constants.LEFT_CURLY_BRACKET}:
                identifier_category = CompilationEngine._CLASS
            else:
                identifier_category = CompilationEngine._SUBROUTINE

        attributes = self._get_identifier_attributes(token_data.value, usage, identifier_category)
        xml_element.attrib.update(attributes)

    # TODO: remove this after finish with code writer
    def _get_identifier_attributes(self, name: str, usage: str, category: str = "") -> dict[str, str]:
        if category == "":
            category = self._symbol_table.kind_of(name).value
            if category == Constants.VAR:
                category = "local"

        attributes = {"category": category}

        symbol_index = self._symbol_table.index_of(name)

        if symbol_index != -1:
            attributes["index"] = f"{symbol_index}"

        attributes["usage"] = usage

        return attributes

    def _get_unique_label(self) -> str:
        index = self._running_index
        self._running_index += 1
        return f"{self._file_name}_{index}"

    def _get_vm_var_data(self, field_name) -> tuple[SegmentType, int]:
        array_field_index = self._symbol_table.index_of(field_name)
        segment_kind = self._symbol_table.kind_of(field_name)
        segment_type = SegmentType(segment_kind.value)
        return segment_type, array_field_index
