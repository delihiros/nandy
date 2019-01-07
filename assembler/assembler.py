import sys
import tokenizer
import symbol_table
import parser
import generator


class Assembler:
    def assemble(self, asms):

        self.tokenizer = tokenizer.Tokenizer()
        token_lines = [self.tokenizer.tokenize(asm) for asm in asms]
        self.parser = parser.Parser()
        parsed_lines = self.parser.parse(token_lines)
        for p in parsed_lines:
            print(p)
        # self.symbol_table = symbol_table.SymbolTable()
        # self.symbol_table.generate(parsed_lines)
        # self.generator = generator.Generator(self.symbol_table)
        # codes = self.generator.generate(parsed_lines)


    def assemble_file(self, asm_filename):
        asms = []
        with open(asm_filename, 'r') as f:
            for line in f:
                asms.append(line)
        self.assemble(asms)


assembler = Assembler()
assembler.assemble_file('./test.nandy')
