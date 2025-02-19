import binary_converter


class SymbolTable:

    def __init__(self):
        self.data = dict()
        self.free_address = 16
        self._add_predefined_elements()

    def _add_predefined_elements(self):
        dict = self.data

        dict["R0"] = binary_converter.convert_to_binary(0)
        dict["R1"] = binary_converter.convert_to_binary(1)
        dict["R2"] = binary_converter.convert_to_binary(2)
        dict["R3"] = binary_converter.convert_to_binary(3)
        dict["R4"] = binary_converter.convert_to_binary(4)
        dict["R5"] = binary_converter.convert_to_binary(5)
        dict["R6"] = binary_converter.convert_to_binary(6)
        dict["R7"] = binary_converter.convert_to_binary(7)
        dict["R8"] = binary_converter.convert_to_binary(8)
        dict["R9"] = binary_converter.convert_to_binary(9)
        dict["R10"] = binary_converter.convert_to_binary(10)
        dict["R11"] = binary_converter.convert_to_binary(11)
        dict["R12"] = binary_converter.convert_to_binary(12)
        dict["R13"] = binary_converter.convert_to_binary(13)
        dict["R14"] = binary_converter.convert_to_binary(14)
        dict["R15"] = binary_converter.convert_to_binary(15)
        dict["SCREEN"] = binary_converter.convert_to_binary(16384)
        dict["KBD"] = binary_converter.convert_to_binary(24576)
        dict["SP"] = binary_converter.convert_to_binary(0)
        dict["LCL"] = binary_converter.convert_to_binary(1)
        dict["ARG"] = binary_converter.convert_to_binary(2)
        dict["THIS"] = binary_converter.convert_to_binary(3)
        dict["THAT"] = binary_converter.convert_to_binary(4)

    def add(self, key, value):
        self.data[key] = binary_converter.convert_to_binary(value)

    def get(self, key):
        if key not in self.data:
            self.data[key] = binary_converter.convert_to_binary(self.free_address)
            self.free_address += 1

        return self.data[key]
