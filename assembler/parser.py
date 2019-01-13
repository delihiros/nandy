import enum
import tokenizer


def index_of_token(token_list, token_type):
    for index, token in enumerate(token_list):
        if token.token_type == token_type:
            return index
    return -1


class OpType(enum.Enum):
    Comment = 0
    A = 1
    C = 2
    L = 3

class Op:
    def __init__(self, op_type, address, dest, comp, jump, additionals = None):
        self.op_type = op_type
        self.address = address
        self.dest = dest
        self.comp = comp
        self.jump = jump
        self.additionals = additionals

    def __repr__(self):
        return ' '.join(map(str, [self.op_type, self.address, self.dest, self.comp, self.jump, self.additionals]))



class Parser:
    def parse(self, token_lines):
        self.address = -1
        asts = [self._parse(line) for line in token_lines]
        return asts

    def _parse(self, tokens):
        # syntax
        # lang ::= c_inst | a_inst
        # a_inst ::= '@' value
        # c_inst ::= comp
        #          | comp ';' jump
        #          | dest = comp
        #          | dest = comp ';' jump

        head = tokens[0]
        self.tokens = [tok for tok in tokens if tok.token_type != tokenizer.TokenType.Comment]

        if head.token_type == tokenizer.TokenType.Comment:
            return Op(OpType.Comment, None, None, None, None, additionals=head)
        elif head.token_type == tokenizer.TokenType.AtMark: # A
            self.address += 1
            return self._parse_a()
        elif head.token_type == tokenizer.TokenType.LabelSymbol:
            return self._parse_label()
        else: # C
            self.address += 1
            return self._parse_c()

    def _parse_a(self):
        return Op(OpType.A, self.address, None, None, None, additionals=self.tokens[1])

    def _parse_label(self):
        return Op(OpType.L, self.address+1, None, None, None, additionals=self.tokens[0])

    def _parse_c(self):
        equal_index = index_of_token(self.tokens, tokenizer.TokenType.Equal)
        semicolon_index = index_of_token(self.tokens, tokenizer.TokenType.SemiColon)
        if equal_index >= 0 and semicolon_index >= 0:
            #     | dest = comp ';' jump
            dest = self.tokens[0:equal_index]
            comp = self.tokens[equal_index+1:semicolon_index]
            jump = self.tokens[semicolon_index+1:]
            return Op(OpType.C, self.address, dest, comp, jump)
        if equal_index >= 0:
            #          | dest = comp
            dest = self.tokens[0:equal_index]
            comp = self.tokens[equal_index+1:]
            return Op(OpType.C, self.address, dest, comp, None)
        if semicolon_index >= 0:
            #          | comp ';' jump
            comp = self.tokens[0:semicolon_index]
            jump = self.tokens[semicolon_index+1:]
            return Op(OpType.C, self.address, None, comp, jump)
        return Op(OpType.C, self.address, None, self.tokens, None)

    def _parse_comp(self):
        return None
        return Op(OpType.C, self.address, None, self.tokens, None)
