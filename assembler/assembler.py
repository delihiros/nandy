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
        self.symbol_table = symbol_table.SymbolTable()
        self.symbol_table.generate(parsed_lines)
        self.generator = generator.Generator()
        codes = self.generator.generate(parsed_lines, self.symbol_table)
        return codes


    def assemble_file(self, asm_filename):
        asms = []
        with open(asm_filename, 'r') as f:
            for line in f:
                asms.append(line)
        self.assemble(asms)


assembler = Assembler()
assembler.assemble_file('./test.nandy')
