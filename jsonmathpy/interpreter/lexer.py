import re
from jsonmathpy.interpreter.token import *
from jsonmathpy.interpreter.types import *
from more_itertools import peekable

WHITESPACE         = ' \n\t'
DIGITS             = '0987654321'
LOWERCASES         = 'abcdefghijklmnopqrstuvwxyz'
UPPERCASES         = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CHARS              = UPPERCASES + LOWERCASES
CHARACTERS         = '{}_^=.:'
OBJECT_CHARACTERS  = CHARACTERS + UPPERCASES + LOWERCASES + DIGITS

re_float           = '^(\d+)(\.)(\d+)$'
re_integer         = '^(\d+)$'
regex_integral     = '^(integrate)$'
regex_diff         = '^(diff)$'
regex_solve        = '^(solve)$'
re_variable        = '[a-z]+'

def match_tensors(i):
    string = i
    rank = string.count('_') + string.count('^')
    if rank > 0:
        pattern = lambda x : "([a-zA-Z]+)([_^]\{[a-zA-Z]+\}|[_^]\{[a-zA-Z]+\=[0-9]}){" + str(x) + "}(?=(\*|\)|\+|\-|\/|$))"
        pattern2 = lambda x : "([a-zA-Z]+)([_^]\{[a-zA-Z]+\}|[_^]\{[a-zA-Z]+\:[0-9]}){" + str(x) + "}(?=(\*|\)|\+|\-|\/|$))"
        Total = re.match(pattern(rank), string)
        Total2 = re.match(pattern2(rank), string)
        return bool(Total) or bool(Total2)
    else:
        return False

class Lexer:
    def __init__(self, text):
        self.text = peekable(text + ' ')
        self.advance()
        self.tokens = []

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char != None:

            if self.current_char in WHITESPACE:
                self.advance()

            elif self.current_char in CHARS:
                self.generate_object()

            elif self.current_char in DIGITS:
                self.generate_number()

            elif self.current_char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, None))

            elif self.current_char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.CLOSED_SQUARE_BRACE, None))

            elif self.current_char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.OPEN_SQUARE_BRACE, None))

            elif self.current_char == '*':
                self.generate_operation()

            elif self.current_char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, None))

            elif self.current_char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, None))

            elif self.current_char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, None))

            elif self.current_char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, None))

            elif self.current_char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.EQUALS, None))
    
            elif self.current_char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, None))

            else:
                raise Exception(f"Illegal Character '{self.current_char}'")
        return self.tokens

    def generate_number(self):
        num = ''
        while self.current_char != None and (self.current_char in DIGITS or self.current_char == '.'):
            num += self.current_char
            self.advance()
        count = num.count('.')
        if count == 0:
            self.tokens.append(Token(TokenType.INTEGER, num))
        elif count == 1:
            self.tokens.append(Token(TokenType.FLOAT, num))
        else:
            raise Exception(f"Illegal Character '{num}'")

    def generate_operation(self):
        num = ''
        while self.current_char != None and self.current_char == '*':
            num += self.current_char
            self.advance()
        if num.count('*') == 1:
            self.tokens.append(Token(TokenType.MULTIPLY, None))
        elif num.count('*') == 2:
            self.tokens.append(Token(TokenType.POW, None))
        else:
            raise Exception(f"Illegal Character '{num}'")

    def generate_object(self):
        obj = ''
        while self.current_char != None and self.current_char in OBJECT_CHARACTERS:
            if self.current_char in CHARS and self.text.peek() == '(':
                obj += self.current_char
                self.advance()
                if re.match(regex_integral, obj):
                    self.tokens.append(Token(TokenType.INTEGRAL, obj))
                elif re.match(regex_diff, obj):
                    self.tokens.append(Token(TokenType.DIFFERENTIAL, obj))
                elif re.match(regex_solve, obj):
                    self.tokens.append(Token(TokenType.SOLVER, obj))
                else:
                    self.tokens.append(Token(TokenType.FUNCTION, obj))
            elif self.text.peek() not in OBJECT_CHARACTERS + '(':
                obj += self.current_char
                self.advance()
                if match_tensors(obj):
                    self.tokens.append(Token(TokenType.TENSOR, obj))
                elif re.match(re_variable, obj):
                    self.tokens.append(Token(TokenType.VARIABLE, obj))
            else:
                obj += self.current_char
                self.advance()
            