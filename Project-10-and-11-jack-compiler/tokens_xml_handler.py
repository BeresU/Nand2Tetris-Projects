from xml.etree.ElementTree import Element
from jack_tokenizer import TokenData
from jack_tokenizer import TokenType
import xml.etree.ElementTree as ET


class TokenXmlHandler:
    def __init__(self):
        self.root:Element = ET.Element("tokens")

    def write_to_xml(self, token_data: TokenData):
        if token_data.token_type == TokenType.NONE: return
        item = ET.SubElement(self.root, token_data.token_type.value)
        item.text = f" {token_data.value} " # add spaces since the compare file has spaces

    def create_xml(self, file_name: str, output_path: str):
        tree = ET.ElementTree(self.root)
        full_path = f"{output_path}/{file_name}T.xml"
        tree.write(full_path, encoding="utf-8", xml_declaration=True)
