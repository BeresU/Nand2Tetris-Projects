import jack_tokenizer
from pathlib import Path
from tokens_xml_handler import TokenXmlHandler
from jack_tokenizer import TokenData
from jack_tokenizer import JackTokenizer


class CompilationEngine:
    tokens_xml_handler: TokenXmlHandler
    output_path: str
    file_path: str
    tokenizer:JackTokenizer

    def __init__(self, file_path: str, output_path: str):
        self.file_path = file_path
        self.output_path = output_path
        self.tokens_xml_handler = TokenXmlHandler()
        self.tokenizer = JackTokenizer(file_path)

    # TODO: need to handle the term case where let x = foo can be either a variable assignment or an array (foo[]) or a method call (foo.bar)
    def compile(self):
        input_path_obj = Path(self.file_path)

        while self.tokenizer.has_more_tokens:
            data = self.tokenizer.current_data
            self.tokens_xml_handler.write_to_xml(data)
            self.tokenizer.advance()

        self.tokenizer.dispose()
        self.tokens_xml_handler.create_xml(input_path_obj.stem, self.output_path)

    def _handle_token_tesults(self, token_results: list[TokenData]):
        for result in token_results:
            pass

    def _compile_class_var_dec(self):
        pass

    def _compile_subroutine(self):
        pass

    def _compile_parameter_list(self):
        pass

    def _compile_subroutine_body(self):
        pass

    def _compie_var_dec(self):
        pass

    def _compile_statements(self):
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
