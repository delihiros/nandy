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
        return self.assemble(asms)



def __main__():
    assembler = Assembler()
    codes = assembler.assemble_file(sys.argv[1])
    print(codes)
    with open('out.bin', 'w') as f:
        for code in codes:
            if code != None:
                f.write('{:016b}\n'.format(code, 2))


if __name__ == '__main__':
    __main__()
