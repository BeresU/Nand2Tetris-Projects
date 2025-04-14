import jack_tokenizer
from pathlib import Path
from tokens_xml_handler import TokenXmlHandler


class CompilationEngine:

    def __init__(self, file_path: str, output_path: str):
        self.file_path = file_path
        self.output_path = output_path
        self.tokens_xml_handler = TokenXmlHandler()

    # main method
    # write to xml (token and final)
    # TODO: create class to handle xml writing in a more clean way?
    # TODO: need to create tokens xml, should handle this in a different class?
    # TODO: need to handle the term case where let x = foo can be either a variable assignment or an array (foo[]) or a method call (foo.bar)
    def compile(self):
        input_path_obj = Path(self.file_path)

        with input_path_obj.open('r') as file:
            for line in file:
                results = jack_tokenizer.tokenize_data(line)
                self.tokens_xml_handler.write_to_xml(results)

        self.tokens_xml_handler.create_xml(self.output_path)

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
