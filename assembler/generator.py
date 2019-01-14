import tokenizer
import parser


comp_mnemonic = {
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',

    'M':   '1110000',
    '!M':  '1110001',
    '-M':  '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101'
}


d_mnemonic = {
    None:   '000',
    'M':    '001',
    'D':    '010',
    'MD':   '011',
    'A':    '100',
    'AM':   '101',
    'AD':   '110',
    'AMD':  '111'
}


j_mnemonic = {
    None:  '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}


def token_list2values(token_list):
    if token_list is None:
        return None
    return ''.join([str(t.value) for t in token_list])


class Generator:

    def generate(self, asts, symbol_table):
        self.symbol_table = symbol_table
        codes = [self._generate(ast) for ast in asts]
        return codes

    def _generate(self, ast):
        if ast.op_type == parser.OpType.Comment:
            return None
        elif ast.op_type == parser.OpType.A:
            return int('0b{:016b}'.format(self.symbol_table.get(ast.additionals)), 2)

        elif ast.op_type == parser.OpType.C:
            return int('0b111'
                       + comp_mnemonic[token_list2values(ast.comp)]
                       + d_mnemonic[token_list2values(ast.dest)]
                       + j_mnemonic[token_list2values(ast.jump)], 2)

        elif ast.op_type == parser.OpType.L:
            return None
