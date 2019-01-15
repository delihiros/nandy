import enum


def is_small_alpha(c):
    return 'a' <= c and c <= 'z'

def is_large_alpha(c):
    return 'A' <= c and c <= 'Z'

def is_alpha(c):
    return is_small_alpha(c) or is_large_alpha(c)

def is_num(c):
    return '0' <= c and c <= '9'

def is_space(c):
    return c in [' ', '\t', ',', '\n']


def is_symbol(c):
    return c in ['$', '_', '.']


class TokenType(enum.Enum):
    Number = 0
    VarSymbol = 1
    LabelSymbol = 2
    AtMark = 3
    Equal = 4
    Plus = 5
    Minus = 6
    SemiColon = 7
    Comment = 8


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return ' '.join(map(str, [self.value, self.token_type]))


class Tokenizer:
    def __init__(self):
        self.code = ''
        self.idx = 0
        self.max_idx = 0

    def tokenize(self, code):
        self.code = code
        self.idx = 0
        self.max_idx = len(code)
        tokens = []
        while self.idx < self.max_idx:
            if is_num(self.code[self.idx]):
                num = ''
                while self.idx < self.max_idx and is_num(self.code[self.idx]):
                    num += self.code[self.idx]
                    self.idx += 1
                tokens.append(Token(TokenType.Number, int(num)))
            elif is_alpha(self.code[self.idx]):
                symbol = ''
                while self.idx < self.max_idx and (is_alpha(self.code[self.idx]) or is_num(self.code[self.idx]) or is_symbol(self.code[self.idx])):
                    symbol += self.code[self.idx]
                    self.idx += 1
                tokens.append(Token(TokenType.VarSymbol, symbol))
            elif self.code[self.idx] == '@':
                tokens.append(Token(TokenType.AtMark, '@'))
                self.idx += 1
            elif self.code[self.idx] == '(':
                symbol = ''
                self.idx += 1
                while self.idx < self.max_idx and self.code[self.idx] != ')':
                    symbol += self.code[self.idx]
                    self.idx += 1
                tokens.append(Token(TokenType.LabelSymbol, symbol))
                self.idx += 1
            elif self.code[self.idx] == ';':
                tokens.append(Token(TokenType.SemiColon, ';'))
                self.idx += 1
            elif self.code[self.idx] == '=':
                tokens.append(Token(TokenType.Equal, '='))
                self.idx += 1
            elif self.code[self.idx] == '+':
                tokens.append(Token(TokenType.Plus, '+'))
                self.idx += 1
            elif self.code[self.idx] == '-':
                tokens.append(Token(TokenType.Minus, '-'))
                self.idx += 1
            elif self.code[self.idx] == '/':
                comment = ''
                self.idx += 2
                while self.idx < self.max_idx and self.code[self.idx] != '\n':
                    comment += self.code[self.idx]
                    self.idx += 1
                tokens.append(Token(TokenType.Comment, comment))
                self.idx += 1
            while self.idx < self.max_idx and is_space(self.code[self.idx]):
                self.idx += 1
        return tokens
