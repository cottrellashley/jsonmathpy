import re
from jsonmathpy.interpreter.token import *
from jsonmathpy.interpreter.types import *
from more_itertools import peekable
from jsonmathpy.interpreter.shared import constants
from jsonmathpy.interpreter.shared.helpers import match_tensors

class Lexer:
    """
    A lexer class that generates tokens from a given text string.

    Attributes:
        text (str): the text string to be tokenized.
        tokens (List[Token]): the list of tokens generated from the text string.
    """
    def __init__(self, text : str) -> None:
        """
        Initializes the lexer object with the given text string.

        Args:
            text (str): the text string to be tokenized.

        """
        self.text = peekable(text + ' ') # Added space because peek() cannot peak the last string.
        self.advance()
        self.tokens = []


    def advance(self) -> None:
        """Advances to the next character in the text string."""
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self) -> list[Token]:
        """
        Generates a list of tokens from the given text string.

        Returns:
            List[Token]: the list of tokens generated from the text string.

        Raises:
            Exception: if the text string contains an illegal character.

        """
        while self.current_char != None:

            if self.current_char in constants.WHITESPACE:
                self.advance()

            elif self.current_char in constants.CHARS:
                self.generate_object()

            elif self.current_char in constants.DIGITS:
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

    def generate_number(self) -> None:
        """
        Generates a token of type INTEGER or FLOAT from the current character in the text string.

        Raises:
            Exception: if the current character represents an illegal number.

        """
        num = ''
        while self.current_char != None and (self.current_char in constants.DIGITS or self.current_char == '.'):
            num += self.current_char
            self.advance()
        count = num.count('.')
        if count == 0:
            self.tokens.append(Token(TokenType.INTEGER, num))
        elif count == 1:
            self.tokens.append(Token(TokenType.FLOAT, num))
        else:
            raise Exception(f"Illegal Character '{num}'")

    def generate_operation(self) -> None:
        """
        Generates a token of type MULTIPLY (*) or POW (**) from the current character in the text string.

        Raises:
            Exception: if the current character represents an illegal operation.

        """
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

    def generate_object(self) -> None:
        """Generates object tokens from the given text."""
        obj = ''
        while self.current_char != None and self.current_char in constants.OBJECT_CHARACTERS:
            if self.current_char in constants.CHARS and self.text.peek() == '(':
                obj += self.current_char
                self.advance()
                # TO DO: Create a method to hash these objects and wrap this logic in a python dictionary.
                if re.match(constants.re_integral, obj):
                    self.tokens.append(Token(TokenType.INTEGRAL, obj))
                elif re.match(constants.re_diff, obj):
                    self.tokens.append(Token(TokenType.DIFFERENTIAL, obj))
                elif re.match(constants.re_solve, obj):
                    self.tokens.append(Token(TokenType.SOLVE, obj))
                elif re.match(constants.re_series, obj):
                    self.tokens.append(Token(TokenType.SERIES, obj))
                elif re.match(constants.re_simplify, obj):
                    self.tokens.append(Token(TokenType.SIMPLIFY, obj))
                elif re.match(constants.re_limit, obj):
                    self.tokens.append(Token(TokenType.LIMIT, obj))
                elif re.match(constants.re_expand, obj):
                    self.tokens.append(Token(TokenType.EXPAND, obj))
                elif re.match(constants.re_numerical, obj):
                    self.tokens.append(Token(TokenType.NUMERICAL, obj))
                elif re.match(constants.re_plot, obj):
                    self.tokens.append(Token(TokenType.PLOT, obj))
                elif re.match(constants.re_sin, obj):
                    self.tokens.append(Token(TokenType.SIN, obj))
                elif re.match(constants.re_cos, obj):
                    self.tokens.append(Token(TokenType.COS, obj))
                elif re.match(constants.re_tan, obj):
                    self.tokens.append(Token(TokenType.TAN, obj))
                elif re.match(constants.re_asin, obj):
                    self.tokens.append(Token(TokenType.ASIN, obj))
                elif re.match(constants.re_acos, obj):
                    self.tokens.append(Token(TokenType.ACOS, obj))
                elif re.match(constants.re_atan, obj):
                    self.tokens.append(Token(TokenType.ATAN, obj))
                elif re.match(constants.re_sinh, obj):
                    self.tokens.append(Token(TokenType.SINH, obj))
                elif re.match(constants.re_cosh, obj):
                    self.tokens.append(Token(TokenType.COSH, obj))
                elif re.match(constants.re_tanh, obj):
                    self.tokens.append(Token(TokenType.TANH, obj))
                elif re.match(constants.re_asinh, obj):
                    self.tokens.append(Token(TokenType.ASINH, obj))
                elif re.match(constants.re_acosh, obj):
                    self.tokens.append(Token(TokenType.ACOSH, obj))
                elif re.match(constants.re_atanh, obj):
                    self.tokens.append(Token(TokenType.ATANH, obj))
                else:
                    self.tokens.append(Token(TokenType.FUNCTION, obj))
            elif self.text.peek() not in constants.OBJECT_CHARACTERS + '(':
                obj += self.current_char
                self.advance()
                if match_tensors(obj):
                    self.tokens.append(Token(TokenType.TENSOR, obj))
                elif re.match(constants.re_pi, obj):
                    self.tokens.append(Token(TokenType.PI, obj))
                elif re.match(constants.re_variable, obj):
                    self.tokens.append(Token(TokenType.VARIABLE, obj))
            else:
                obj += self.current_char
                self.advance()