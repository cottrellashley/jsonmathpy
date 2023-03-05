from enum import Enum

class TokenType(Enum):
    """An enumeration of token types used in a lexer or parser."""

    NUMBER                  = 0     # Number Token
    PLUS                    = 1     # Addition operator
    MINUS                   = 2     # Subtraction operator
    MULTIPLY                = 3     # Multiplication operator
    DIVIDE                  = 4     # Division operator
    VARIABLE                = 5     # A variable name
    OPERATOR                = 6     # A mathematical operator
    OBJECT                  = 7     # A generic object name
    LPAREN                  = 8     # Left parenthesis
    RPAREN                  = 9     # Right parenthesis
    TENSOR                  = 10    # A tensor name
    FLOAT                   = 11    # A floating-point number
    INTEGER                 = 12    # An integer number
    INTEGRAL                = 13    # The `int` function keyword
    DIFFERENTIAL            = 14    # The `diff` symbol for differentiation
    SOLVER                  = 15    # The `solve` function keyword
    FUNCTION                = 16    # A function name
    EQUALS                  = 17    # The `=` symbol for assignment or comparison
    COMMA                   = 18    # The `,` symbol for function arguments or tensor indices
    POW                     = 19    # The `**` symbol for exponentiation
    OPEN_SQUARE_BRACE       = 20
    CLOSED_SQUARE_BRACE     = 21
