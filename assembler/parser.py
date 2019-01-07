import enum
import tokenizer


def take_while(s, e):
    idx = 0
    for v in s:
        idx += 1
        if not e(v):
            break
    return s[:idx], s[idx:]


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
        s = take_while(self.tokens, lambda t: t.token_type != tokenizer.TokenType.Equal)
        dest, rest = s[0][:1], s[1]
        # if len(dest) > 1:
        #     rest = dest[1:]
        #     dest = dest[0]
        print(s, dest, rest)
        s = take_while(rest, lambda t: t.token_type != tokenizer.TokenType.SemiColon)
        comp, jump = s[0], s[1]
        print([t.value for t in self.tokens], [t.value for t in dest], [t.value for t in comp], [t.value for t in jump])
        return Op(OpType.C, self.address, dest, comp, jump)
