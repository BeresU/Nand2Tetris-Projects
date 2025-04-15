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

    # TODO: need to handle the term case where let x = foo can be either a variable assignment or an array (foo[]) or a method call (foo.bar)
    def compile_class(self):
        self.xml_root_element = ET.Element(Constants.CLASS)
        self._process(Constants.CLASS, TokenType.KEYWORD, self.xml_root_element)
        self._process("", TokenType.IDENTIFIER, self.xml_root_element)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, self.xml_root_element)

        self._compile_class_var_dec(self.xml_root_element)
        self._compile_subroutine(self.xml_root_element)

        # TODO: uncomment this when finish
        # self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, self.xml_root_element)

        self._on_finish()  # test

    # TODO: handle has more tokens here?
    def _process(self, token_value: str, token_type: TokenType, xml_element: Element):
        current_token = self.tokenizer.current_token

        if current_token.token_type != token_type:
            raise ValueError(
                f"Got: {current_token.token_type.name} expected: {token_type.name}, token value: {current_token.value}, file: {self.file_path}")

        if current_token.token_type in {TokenType.KEYWORD, TokenType.SYMBOL} and current_token.value != token_value:
            raise ValueError(f"Got: {current_token.value}, expected: {token_value}")

        element = ET.SubElement(xml_element, current_token.token_type.value)
        element.text = f" {current_token.value} "  # add spaces since the compare file has spaces

        self.tokens_xml_handler.write_to_xml(current_token)
        self.tokenizer.advance()

    def _compile_class_var_dec(self, xml_element: Element):
        current_token = self.tokenizer.current_token

        if current_token.value not in {Constants.FIELD, Constants.STATIC}: return

        element = ET.SubElement(xml_element, Constants.CLASS_VAR_DEC)
        self._process(current_token.value, TokenType.KEYWORD, element)

        while self.tokenizer.current_token.value != Constants.SEMICOLON:
            current_token = self.tokenizer.current_token
            self._process(current_token.value, current_token.token_type, element)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, element)
        self._compile_class_var_dec(xml_element)

    def _compile_subroutine(self, xml_element: Element):
        current_token = self.tokenizer.current_token
        if current_token.value not in {Constants.FUNCTION, Constants.METHOD, Constants.CONSTRUCTOR}: return

        element = ET.SubElement(xml_element, Constants.SUBROUTINE_DEC)

        self._process(current_token.value, TokenType.KEYWORD, element)

        expected_token_type = TokenType.IDENTIFIER if current_token.value == Constants.CONSTRUCTOR else TokenType.KEYWORD
        self._process(self.tokenizer.current_token.value, expected_token_type, element)
        self._process(self.tokenizer.current_token.value, TokenType.IDENTIFIER, element)
        self._process(Constants.LEFT_BRACKET, TokenType.SYMBOL, element)
        self._compile_parameter_list(element)
        self._process(Constants.RIGHT_BRACKET, TokenType.SYMBOL, element)
        self._compile_subroutine_body(element)
        # self._compile_subroutine(xml_element) #TODO: remove comment

    def _compile_parameter_list(self, xml_element: Element):
        element = ET.SubElement(xml_element, Constants.PARAMETER_LIST)

        while self.tokenizer.current_token.value != Constants.RIGHT_BRACKET:
            current_token = self.tokenizer.current_token
            self._process(current_token.value, TokenType.KEYWORD, element)
            self._process(current_token.value, TokenType.IDENTIFIER, element)
            if self.tokenizer.current_token.value == Constants.RIGHT_BRACKET: break
            self._process(Constants.COMMA, TokenType.SYMBOL, element)

    def _compile_subroutine_body(self, xml_element: Element):
        element = ET.SubElement(xml_element, Constants.SUBROUTINE_BODY)
        self._process(Constants.LEFT_CURLY_BRACKET, TokenType.SYMBOL, element)
        self._compie_var_dec(element)
        self._compile_statements(xml_element)
        # self._process(Constants.RIGHT_CURLY_BRACKET, TokenType.SYMBOL, element) # TODO: Remove comment

    def _compie_var_dec(self, xml_element: Element):
        if self.tokenizer.current_token.value != Constants.VAR: return
        element = ET.SubElement(xml_element, Constants.VAR_DEC)
        self._process(Constants.VAR, TokenType.KEYWORD, element)

        while self.tokenizer.current_token.value != Constants.SEMICOLON:
            current_token = self.tokenizer.current_token
            self._process(current_token.value, current_token.token_type, element)

        self._process(Constants.SEMICOLON, TokenType.SYMBOL, element)

        self._compie_var_dec(xml_element)

    def _compile_statements(self, xml_element: Element):
        element = ET.SubElement(xml_element, Constants.STATEMENTS)

        while self.tokenizer.current_token.value is {Constants.LET, Constants.IF, Constants.WHILE, Constants.DO,
                                                     Constants.RETURN}:
            pass

    def _compile_if(self):
        pass

    def _compile_let(self):
        pass

    def _compile_while(self):
        pass

    def compile_do(self):
        pass

    def compile_return(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass
