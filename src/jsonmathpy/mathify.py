from src.jsonmathpy.interpreter.interpreter import Interpreter
from src.jsonmathpy.interpreter.lexer import Lexer
from src.jsonmathpy.interpreter.parser_ import Parser



class Mathify:

    def __init__(self, string : str):
        self.string = string

    def __call__(self):
        lex = Lexer(self.string).generate_tokens()
        par = Parser(lex).parse()
        intt = Interpreter().visit(par)
        return intt.dict
