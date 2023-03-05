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
    SOLVE                   = 15    # The `solve` function keyword
    FUNCTION                = 16    # A function name
    EQUALS                  = 17    # The `=` symbol for assignment or comparison
    COMMA                   = 18    # The `,` symbol for function arguments or tensor indices
    POW                     = 19    # The `**` symbol for exponentiation
    OPEN_SQUARE_BRACE       = 20    # An open square braces '['
    CLOSED_SQUARE_BRACE     = 21    # An closed square braces ']'
    CONTEXT_VARIABLE        = 22    # A type variable, but is contextual to the function it belongs to. (integral meausre variable vs differential w.r.t variable)
    SIN                     = 23    # Sin function.
    COS                     = 24    # Cos function.
    TAN                     = 25    # Tan function.
    SINH                    = 26    # Sinh function.
    COSH                    = 27    # Cosh function.
    TANH                    = 28    # Tanh function.
    ASIN                    = 29    # Arcsin function.
    ACOS                    = 30    # Arccos function.
    ATAN                    = 31    # Arctan function.
    ASINH                   = 32    # Arcsinh function.
    ACOSH                   = 33    # Arccosh function.
    ATANH                   = 34    # Arctanh function.
    LIMIT                   = 35    # Limit function.
    SIMPLIFY                = 36    # Simplify function.
    EXPAND                  = 37    # Expand function.
    SERIES                  = 38    # Series function.
    NUMERICAL               = 39    # Numerical function.
    PLOT                    = 40    # Plot function.
    PI                      = 41    # Pi constant


TRIG_FUNCTIONS = (
                    TokenType.SIN, 
                    TokenType.COS,
                    TokenType.TAN, 
                    TokenType.ASIN,
                    TokenType.ACOS,
                    TokenType.ATAN
                )

HYPERBOLIC_FUNCTIONS = (
                        TokenType.SINH, 
                        TokenType.COSH,
                        TokenType.TANH, 
                        TokenType.ASINH,
                        TokenType.ACOSH,
                        TokenType.ATANH
                    )