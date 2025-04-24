from pathlib import Path
from xml.etree.ElementTree import Element
from tokens_xml_handler import TokenXmlHandler
from jack_tokenizer import JackTokenizer, TokenData
import xml.etree.ElementTree as ET
from constants import Constants
from jack_tokenizer import TokenType
from symbol_table import SymbolTable
from symbol_table import SymbolKind


class CompilationEngine:
    tokens_xml_handler: TokenXmlHandler
    output_path: str
    file_path: str
    tokenizer: JackTokenizer
    xml_root_element: Element
    symbol_table: SymbolTable

    _CLASS = "class"
    _SUBROUTINE = "subroutine"
    _EXPRESSION_USE = "expression use"

    def __init__(self, file_path: str, output_path: str):
        self.file_path = file_path
        self.output_path = output_path
        self.tokens_xml_handler = TokenXmlHandler()
        self.tokenizer = JackTokenizer(file_path)
        self.symbol_table = SymbolTable()

    def _on_finish(self):
        self.tokenizer.dispose()
        input_path_obj = Path(self.file_path)
        file_name = input_path_obj.stem
        self.tokens_xml_handler.create_xml(file_name, self.output_path)
        self._create_xml_file(file_name)

    def _create_xml_file(self, file_name: str):
        tree = ET.ElementTree(self.xml_root_element)
        full_path = f"{self.output_path}/{file_name}.xml"
        tree.write(full_path, encoding="utf-8", xml_declaration=False, short_empty_elements=False)

    def compile_class(self):
        self.xml_root_element = ET.Element(Constants.CLASS)
        self._process(Constants.CLASS, TokenType.KEYWORD, self.xml_root_element)

        attributes = self._get_identifier_attributes("class name", CompilationEngine._CLASS)
        self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, self.xml_root_element, attributes)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, self.xml_root_element)

        while self.tokenizer.current_token.value in {Constants.FIELD, Constants.STATIC}:
            self._compile_class_var_dec(self.xml_root_element)

        while self.tokenizer.current_token.value in {Constants.FUNCTION, Constants.METHOD, Constants.CONSTRUCTOR}:
            self._compile_subroutine(self.xml_root_element)

        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, self.xml_root_element)

        self._on_finish()

    def _compile_class_var_dec(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "classVarDec")

        # field\static keyword
        symbol_kind = SymbolKind[self.tokenizer.current_token.value.upper()]
        self._process(self.tokenizer.current_token.value, TokenType.KEYWORD, sub_element)

        # variable type (int\string\etc)
        symbol_type = self.tokenizer.current_token.value
        self._process(self.tokenizer.current_token.value, self.tokenizer.current_token.token_type, sub_element)

        # in case the variable declared with comma we loop
        while self.tokenizer.current_token.value != Constants.SEMICOLON:
            attributes = None

            if self.tokenizer.current_token.value != Constants.COMMA:
                self.symbol_table.define(self.tokenizer.current_token.value, symbol_type, symbol_kind)
                usage = f"{symbol_kind.value} declaration"
                attributes = self._get_identifier_attributes(usage)

            self._process(self.tokenizer.current_token.value, self.tokenizer.current_token.token_type, sub_element,
                          attributes)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)

    def _compile_subroutine(self, xml_element: Element):
        current_token = self.tokenizer.current_token
        sub_element = ET.SubElement(xml_element, "subroutineDec")
        self.symbol_table.reset()
        self.symbol_table.define("this", Path(self.file_path).stem, SymbolKind.ARG)
        self._process(current_token.value, TokenType.KEYWORD, sub_element)

        expected_token_type = TokenType.IDENTIFIER if current_token.value == Constants.CONSTRUCTOR else TokenType.KEYWORD

        self._process(self.tokenizer.current_token.value, expected_token_type, sub_element)

        attributes = self._get_identifier_attributes("subroutine declaration", CompilationEngine._SUBROUTINE)

        self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, sub_element, attributes)
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, sub_element)

        self._compile_parameter_list(sub_element)
        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, sub_element)
        self._compile_subroutine_body(sub_element)

    def _compile_parameter_list(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "parameterList")

        if self.tokenizer.current_token.value == Constants.RIGHT_BRACKET: return

        self._compile_parameter(sub_element)

        while self.tokenizer.current_token.value == Constants.COMMA:
            self._process(Constants.COMMA, TokenType.SYMBOL, sub_element)
            self._compile_parameter(sub_element)

    def _compile_parameter(self, xml_element: Element):
        symbol_type = self.tokenizer.current_token.value
        self._process(self.tokenizer.current_token.value, self.tokenizer.current_token.token_type, xml_element)
        self.symbol_table.define(self.tokenizer.current_token.value, symbol_type, SymbolKind.ARG)
        attributes = self._get_identifier_attributes("parameter list")
        self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, xml_element, attributes)

    def _compile_subroutine_body(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "subroutineBody")
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

        while self.tokenizer.current_token.value == Constants.VAR:
            self._compie_var_dec(sub_element)

        self._compile_statements(sub_element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

    def _compie_var_dec(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "varDec")
        self._process(Constants.VAR, TokenType.KEYWORD, sub_element)

        symbol_type = self.tokenizer.current_token.value
        self._process(self.tokenizer.current_token.value, self.tokenizer.current_token.token_type, sub_element)

        while self.tokenizer.current_token.value != Constants.SEMICOLON:
            attributes = None
            if self.tokenizer.current_token.value != Constants.COMMA:
                self.symbol_table.define(self.tokenizer.current_token.value, symbol_type, SymbolKind.VAR)
                attributes = self._get_identifier_attributes("subroutine variable declaration")
            self._process(self.tokenizer.current_token.value, self.tokenizer.current_token.token_type, sub_element,
                          attributes)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)

    def _compile_statements(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "statements")

        statement_keywords = {
            Constants.LET, Constants.IF, Constants.WHILE, Constants.DO, Constants.RETURN
        }

        while self.tokenizer.current_token.value in statement_keywords:
            token_value = self.tokenizer.current_token.value

            if token_value == Constants.IF: self._compile_if(sub_element)
            if token_value == Constants.LET: self._compile_let(sub_element)
            if token_value == Constants.WHILE: self._compile_while(sub_element)
            if token_value == Constants.DO: self._compile_do(sub_element)
            if token_value == Constants.RETURN: self._compile_return(sub_element)

    def _compile_if(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "ifStatement")
        self._process(Constants.IF, TokenType.KEYWORD, sub_element)
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, sub_element)

        self._compile_expression(sub_element)

        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, sub_element)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)
        self._compile_statements(sub_element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

        if self.tokenizer.current_token.value != Constants.ELSE: return
        self._process(Constants.ELSE, TokenType.KEYWORD, sub_element)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)
        self._compile_statements(sub_element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

    def _compile_let(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "letStatement")
        self._process(Constants.LET, TokenType.KEYWORD, sub_element)

        attributes = self._get_identifier_attributes("let")
        self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, sub_element, attributes)

        if self.tokenizer.current_token.value == Constants.EQUAL:
            self._process(Constants.EQUAL, TokenType.SYMBOL, sub_element)
            self._compile_expression(sub_element)

        elif self.tokenizer.current_token.value == Constants.LEFT_SQUARE_BRACKET:
            self._compile_array(sub_element)
            self._process(Constants.EQUAL, TokenType.SYMBOL, sub_element)
            self._compile_expression(sub_element)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)  # END

    def _compile_while(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "whileStatement")
        self._process(Constants.WHILE, TokenType.KEYWORD, sub_element)
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, sub_element)
        self._compile_expression(sub_element)
        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, sub_element)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)
        self._compile_statements(sub_element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, sub_element)

    def _compile_do(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "doStatement")
        self._process(Constants.DO, TokenType.KEYWORD, sub_element)

        current_token = self.tokenizer.current_token
        self._process(current_token.value, TokenType.IDENTIFIER, sub_element)
        self._add_attribute_to_last_element(sub_element, current_token)
        self._compile_subroutine_call(sub_element)
        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)

    def _add_attribute_to_last_element(self,xml_element:Element, token_data: TokenData):
        if self.tokenizer.current_token.value == Constants.POINT:
            identifier_category = CompilationEngine._CLASS
        elif self.symbol_table.kind_of(token_data.value) == SymbolKind.NONE:
            identifier_category = CompilationEngine._SUBROUTINE
        else:
            identifier_category = ""

        attributes = self._get_identifier_attributes("do", identifier_category, name=token_data.value)

        element_child = xml_element.find(token_data.token_type.value)
        element_child.attrib.update(attributes)

    def _compile_return(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "returnStatement")
        self._process(Constants.RETURN, TokenType.KEYWORD, sub_element)

        # TODO; if the return has no value we need to push dummy value
        if self.tokenizer.current_token.value != Constants.SEMICOLON:
            self._compile_expression(sub_element)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, sub_element)

    def _compile_expression_list(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "expressionList")
        if self.tokenizer.current_token.value == Constants.RIGHT_BRACKET: return

        self._compile_expression(sub_element)

        while self.tokenizer.current_token.value == Constants.COMMA:
            self._process(Constants.COMMA, TokenType.SYMBOL, sub_element)
            self._compile_expression(sub_element)

    def _compile_expression(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "expression")
        self._compile_term(sub_element)

        op_set = {Constants.PLUS, Constants.MINUS, Constants.ASTERISK, Constants.FORWARD_SLASH, Constants.AND,
                  Constants.OR, Constants.LESS_THAN, Constants.GREATER_THAN, Constants.EQUAL}

        while self.tokenizer.current_token.value in op_set:
            # TODO: create a process method that handle syntax analyzing and vm writing for specific tasks? like op for example
            self._process(self.tokenizer.current_token.value, TokenType.SYMBOL, sub_element)
            self._compile_term(sub_element)
            # TODO: write vm code for op here

    def _compile_term(self, xml_element: Element):
        sub_element = ET.SubElement(xml_element, "term")
        current_token = self.tokenizer.current_token
        attributes = None

        if current_token.token_type == TokenType.IDENTIFIER:
            category_type = CompilationEngine._CLASS if self.symbol_table.kind_of(
                current_token.value) == SymbolKind.NONE else ""

            attributes = self._get_identifier_attributes(CompilationEngine._EXPRESSION_USE, category_type)

        self._process(current_token.value, current_token.token_type, sub_element, attributes)

        if current_token.value == Constants.LEFT_BRACKET:
            self._compile_expression(sub_element)
            self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, sub_element)
        elif current_token.value in {Constants.TILDA, Constants.MINUS}:
            self._compile_term(sub_element)
        elif self.tokenizer.current_token.value == Constants.LEFT_SQUARE_BRACKET:
            self._compile_array(sub_element)
        elif self.tokenizer.current_token.value == Constants.POINT:
            self._compile_subroutine_call(sub_element)

    def _compile_array(self, xml_element: Element):
        self._process(Constants.LEFT_SQUARE_BRACKET, TokenType.SYMBOL, xml_element)
        self._compile_expression(xml_element)
        self._process(Constants.RIGHT_SQUARE_BRACKET, TokenType.SYMBOL, xml_element)

    def _compile_subroutine_call(self, xml_element: Element):
        if self.tokenizer.current_token.value == Constants.LEFT_BRACKET:
            self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, xml_element)
            self._compile_expression_list(xml_element)
            self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, xml_element)
        else:
            self._process(Constants.POINT, TokenType.SYMBOL, xml_element)
            attributes = self._get_identifier_attributes(CompilationEngine._EXPRESSION_USE,
                                                         CompilationEngine._SUBROUTINE)

            self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, xml_element, attributes)
            self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, xml_element)
            self._compile_expression_list(xml_element)
            self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, xml_element)

    def _process(self, token_value: str, token_type: TokenType, xml_element: Element, attributes: dict = None):
        current_token = self.tokenizer.current_token

        if current_token.token_type != token_type:
            self._raise_error(
                f"Got: {current_token.token_type.name} expected: {token_type.name}, "
                f"token value: {current_token.value}, line:{self.tokenizer.line_count}, file: {self.file_path}")

        if current_token.token_type in {TokenType.KEYWORD, TokenType.SYMBOL} and current_token.value != token_value:
            self._raise_error(
                f"Got: {current_token.value}, expected: {token_value}, line:{self.tokenizer.line_count},  file: {self.file_path}")

        sub_element = ET.SubElement(xml_element, current_token.token_type.value,
                                    attrib={} if attributes is None else attributes)

        sub_element.text = f" {current_token.value} "  # add spaces since the compare file has spaces

        self.tokens_xml_handler.write_to_xml(current_token)
        self.tokenizer.advance()

    def _raise_error(self, error_message: str):
        self._on_finish()
        raise ValueError(error_message)

    def _get_identifier_attributes(self, usage: str, category="", name="") -> dict[str, str]:
        name = self.tokenizer.current_token.value if name == "" else name

        if category == "":
            category = self.symbol_table.kind_of(name).value
            if category == Constants.VAR:
                category = "local"

        attributes = {"category": category}

        symbol_index = self.symbol_table.index_of(name)

        if symbol_index != -1:
            attributes["index"] = f"{symbol_index}"

        attributes["usage"] = usage

        return attributes
