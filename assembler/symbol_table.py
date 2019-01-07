import parser
import tokenizer

class SymbolTable:
    def __init__(self):
        self.var_address = 1024 # 0x0010
        self.table = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SCREEN': 0x4000,
            'KBD': 0x6000
        }

    def __repr__(self):
        out = ''
        for k, v in self.table.items():
            out += k + ': ' + str(bin(v)) + ' ' + str(v) + '\n'
        return out

    def add_var(self, symbol, address):
        if not self.get(symbol):
            if symbol.token_type == tokenizer.TokenType.VarSymbol:
                self.table[symbol.value] = self.var_address
                self.var_address += 1
            elif symbol.token_type == tokenizer.TokenType.LabelSymbol:
                self.table[symbol.value] = address

    def get(self, symbol):
        if symbol.value in ['A', 'D', 'M']:
            return True
        if symbol.token_type == tokenizer.TokenType.Number:
            return symbol.value
        return self.table.get(symbol.value)

    def generate(self, parsed_lines):
        for ast in parsed_lines:
            if ast.op_type == parser.OpType.Label:
                self.add_var(ast.additionals, ast.address)
            elif ast.op_type == parser.OpType.Assign:
                for c in ast.comp:
                    self.add_var(c, ast.address)
                self.add_var(ast.dest, ast.address)
