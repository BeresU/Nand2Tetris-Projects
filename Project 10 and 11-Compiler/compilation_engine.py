from pathlib import Path
from xml.etree.ElementTree import Element
from tokens_xml_handler import TokenXmlHandler
from jack_tokenizer import JackTokenizer
import xml.etree.ElementTree as ET
from constants import Constants
from jack_tokenizer import TokenType


class CompilationEngine:
    tokens_xml_handler: TokenXmlHandler
    output_path: str
    file_path: str
    tokenizer: JackTokenizer
    xml_root_element: Element

    CLASS_VAR_DEC = "classVarDec"
    SUBROUTINE_DEC = "subroutineDec"
    PARAMETER_LIST = "parameterList"
    SUBROUTINE_BODY = "subroutineBody"
    VAR_DEC = "varDec"
    STATEMENTS = "statements"
    IF_STATEMENT = "ifStatement"
    EXPRESSION = "expression"
    WHILE_STATEMENT = "whileStatement"
    LET_STATEMENT = "letStatement"
    DO_STATEMENT = "doStatement"
    RETURN_STATEMENT = "returnStatement"
    TERM = "term"
    EXPRESSION_LIST = "expressionList"

    def __init__(self, file_path: str, output_path: str):
        self.file_path = file_path
        self.output_path = output_path
        self.tokens_xml_handler = TokenXmlHandler()
        self.tokenizer = JackTokenizer(file_path)

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
        self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, self.xml_root_element)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, self.xml_root_element)

        self._compile_class_var_dec(self.xml_root_element)

        while self.tokenizer.current_token.value in {Constants.FUNCTION, Constants.METHOD, Constants.CONSTRUCTOR}:
            self._compile_subroutine(self.xml_root_element)

        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, self.xml_root_element)

        self._on_finish()

    def _compile_class_var_dec(self, xml_element: Element):
        current_token = self.tokenizer.current_token

        if current_token.value not in {Constants.FIELD, Constants.STATIC}: return

        element = ET.SubElement(xml_element, CompilationEngine.CLASS_VAR_DEC)
        self._process(current_token.value, TokenType.KEYWORD, element)

        while self.tokenizer.current_token.value != Constants.SEMICOLON:
            current_token = self.tokenizer.current_token
            self._process(current_token.value, current_token.token_type, element)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, element)
        self._compile_class_var_dec(xml_element)

    def _compile_subroutine(self, xml_element: Element):
        current_token = self.tokenizer.current_token
        element = ET.SubElement(xml_element, CompilationEngine.SUBROUTINE_DEC)

        self._process(current_token.value, TokenType.KEYWORD, element)

        expected_token_type = TokenType.IDENTIFIER if current_token.value == Constants.CONSTRUCTOR else TokenType.KEYWORD
        self._process(self.tokenizer.current_token.value, expected_token_type, element)
        self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, element)
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, element)
        self._compile_parameter_list(element)
        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, element)
        self._compile_subroutine_body(element)

    def _compile_parameter_list(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.PARAMETER_LIST)

        while self.tokenizer.current_token.value != Constants.RIGHT_BRACKET:
            current_token = self.tokenizer.current_token
            self._process(current_token.value, TokenType.KEYWORD, element)
            self._process(current_token.value, TokenType.IDENTIFIER, element)

            if self.tokenizer.current_token.value == Constants.RIGHT_BRACKET: break
            self._process(Constants.COMMA, TokenType.SYMBOL, element)

    def _compile_subroutine_body(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.SUBROUTINE_BODY)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, element)

        while self.tokenizer.current_token.value == Constants.VAR:
            self._compie_var_dec(element)

        self._compile_statements(element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, element)

    def _compie_var_dec(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.VAR_DEC)
        self._process(Constants.VAR, TokenType.KEYWORD, element)

        while self.tokenizer.current_token.value != Constants.SEMICOLON:
            current_token = self.tokenizer.current_token
            self._process(current_token.value, current_token.token_type, element)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, element)

    def _compile_statements(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.STATEMENTS)

        statement_keywords = {
            Constants.LET, Constants.IF, Constants.WHILE, Constants.DO, Constants.RETURN
        }

        while self.tokenizer.current_token.value in statement_keywords:
            token_value = self.tokenizer.current_token.value

            if token_value == Constants.IF: self._compile_if(element)
            if token_value == Constants.LET: self._compile_let(element)
            if token_value == Constants.WHILE: self._compile_while(element)
            if token_value == Constants.DO: self._compile_do(element)
            if token_value == Constants.RETURN: self._compile_return(element)

    def _compile_if(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.IF_STATEMENT)
        self._process(Constants.IF, TokenType.KEYWORD, element)
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, element)

        self._compile_expression(element)

        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, element)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, element)
        self._compile_statements(element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, element)

        if self.tokenizer.current_token.value != Constants.ELSE: return
        self._process(Constants.ELSE, TokenType.KEYWORD, element)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, element)
        self._compile_statements(element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, element)

    def _compile_let(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.LET_STATEMENT)
        self._process(Constants.LET, TokenType.KEYWORD, element)
        self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, element)

        if self.tokenizer.current_token.value == Constants.EQUAL:
            self._process(Constants.EQUAL, TokenType.SYMBOL, element)
            self._compile_expression(element)

        elif self.tokenizer.current_token.value == Constants.LEFT_SQUARE_BRACKET:
            self._process_array(element)
            self._process(Constants.EQUAL, TokenType.SYMBOL, element)
            self._compile_expression(element)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, element)  # END

    def _compile_while(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.WHILE_STATEMENT)
        self._process(Constants.WHILE, TokenType.KEYWORD, element)
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, element)
        self._compile_expression(element)
        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, element)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, element)
        self._compile_statements(element)
        self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, element)

    def _compile_do(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.DO_STATEMENT)
        self._process(Constants.DO, TokenType.KEYWORD, element)
        self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, element)
        self._process_subroutine_call(element)
        self._process(Constants.SEMICOLON, TokenType.SYMBOL, element)

    def _compile_return(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.RETURN_STATEMENT)
        self._process(Constants.RETURN, TokenType.KEYWORD, element)

        if self.tokenizer.current_token.value != Constants.SEMICOLON:
            self._compile_expression(element)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, element)

    def _compile_expression_list(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.EXPRESSION_LIST)
        if self.tokenizer.current_token.value == Constants.RIGHT_BRACKET: return

        self._compile_expression(element)

        while self.tokenizer.current_token.value == Constants.COMMA:
            self._process(Constants.COMMA, TokenType.SYMBOL, element)
            self._compile_expression(element)

    def _compile_expression(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.EXPRESSION)
        self._compile_term(element)

        op_set = {Constants.PLUS, Constants.MINUS, Constants.ASTERISK, Constants.FORWARD_SLASH, Constants.AND,
                  Constants.OR, Constants.LESS_THAN, Constants.GREATER_THAN, Constants.EQUAL}

        while self.tokenizer.current_token.value in op_set:
            self._process(self.tokenizer.current_token.value, TokenType.SYMBOL, element)
            self._compile_term(element)

    def _compile_term(self, xml_element: Element):
        element = ET.SubElement(xml_element, CompilationEngine.TERM)
        current_token = self.tokenizer.current_token
        self._process(current_token.value, current_token.token_type, element)

        if current_token.value == Constants.LEFT_BRACKET:
            self._compile_expression(element)
            self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, element)
        elif current_token.value in {Constants.TILDA, Constants.MINUS}:
            self._compile_term(element)
        elif self.tokenizer.current_token.value == Constants.LEFT_SQUARE_BRACKET:
            self._process_array(element)
        elif self.tokenizer.current_token.value == Constants.POINT:
            self._process_subroutine_call(element)

    def _process_array(self, xml_element: Element):
        self._process(Constants.LEFT_SQUARE_BRACKET, TokenType.SYMBOL, xml_element)
        self._compile_expression(xml_element)
        self._process(Constants.RIGHT_SQUARE_BRACKET, TokenType.SYMBOL, xml_element)

    def _process_subroutine_call(self, xml_element: Element):
        if self.tokenizer.current_token.value == Constants.LEFT_BRACKET:
            self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, xml_element)
            self._compile_expression_list(xml_element)
            self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, xml_element)
        else:
            self._process(Constants.POINT, TokenType.SYMBOL, xml_element)
            self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, xml_element)
            self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, xml_element)
            self._compile_expression_list(xml_element)
            self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, xml_element)

    def _process(self, token_value: str, token_type: TokenType, xml_element: Element):
        current_token = self.tokenizer.current_token

        if current_token.token_type != token_type:
            self.raise_error(
                f"Got: {current_token.token_type.name} expected: {token_type.name}, "
                f"token value: {current_token.value}, line:{self.tokenizer.line_count}, file: {self.file_path}")

        if current_token.token_type in {TokenType.KEYWORD, TokenType.SYMBOL} and current_token.value != token_value:
            self.raise_error(
                f"Got: {current_token.value}, expected: {token_value}, line:{self.tokenizer.line_count},  file: {self.file_path}")

        element = ET.SubElement(xml_element, current_token.token_type.value)
        element.text = f" {current_token.value} "  # add spaces since the compare file has spaces

        self.tokens_xml_handler.write_to_xml(current_token)
        self.tokenizer.advance()

    def raise_error(self, error_message: str):
        self._on_finish()
        raise ValueError(error_message)
