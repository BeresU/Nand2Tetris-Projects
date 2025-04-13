from io_module import JackFileData
import jack_tokenizer
from tokens_xml_handler import TokenXmlHandler


class CompilationEngine:

    def __init__(self, file_data: JackFileData, output_path: str):
        self.file_data = file_data
        self.output_path = output_path
        self.tokens_xml_handler = TokenXmlHandler()

    # main method
    # write to xml (token and final)
    # TODO: create class to handle xml writing in a more clean way?
    # TODO: need to create tokens xml, should handle this in a different class?
    # TODO: need to handle the term case where let x = foo can be either a variable assignment or an array (foo[]) or a method call (foo.bar)
    def compile(self):
        for line in self.file_data.content:
            token_data = jack_tokenizer.tokenize_data(line)

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
