from jsonmathpy.interpreter.nodes import *
from jsonmathpy.interpreter.types import TokenType
from jsonmathpy.interpreter.types import TRIG_FUNCTIONS
from jsonmathpy.interpreter.types import HYPERBOLIC_FUNCTIONS
from more_itertools import peekable

def function_map(key):
    return {
        "SIN" : lambda arg : SinNode(arg),
        "COS" : lambda arg : CosNode(arg),
        "TAN" : lambda arg : TanNode(arg),
        "ASIN" : lambda arg : ASinNode(arg),
        "ACOS" : lambda arg : ACosNode(arg),
        "ATAN" : lambda arg : ATanNode(arg),
        "SINH" : lambda arg : SinhNode(arg),
        "COSH" : lambda arg : CoshNode(arg),
        "TANH" : lambda arg : TanhNode(arg),
        "ASINH" : lambda arg : ASinhNode(arg),
        "ACOSH" : lambda arg : ACoshNode(arg),
        "ATANH" : lambda arg : ATanhNode(arg)
    }[key]

class Parser:

    def __init__(self, tokens):
        """
        Constructor for Parser class.

        Args:
            tokens: a list of tokens representing the input expression to parse
        """
        self.tokens = peekable(tokens)
        self.advance()

    def raise_error(self, error_message):
        """
        Helper method to raise exceptions with a custom error message.

        Args:
            error_message: a string representing the error message to raise
        """
        raise Exception(error_message)

    def advance(self):
        """
        Helper method to advance to the next token in the input.
        """
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        """
        Parse the input expression.

        Returns:
            The resulting expression tree if the input was valid, None otherwise.
        """
        if self.current_token == None:
            return None
        result = self.expr()
        if self.current_token != None:
            self.raise_error("Syntax Error")
        return result

    def expr(self):
        """
        Parse an expression.

        Returns:
            An expression tree that represents the input expression.
        """
        # Look for a term and store it in X
        X = self.term()
        # Look for additional terms after (PLUS|MINUS) tokens and then construct expression tree
        while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                X = AddNode(X, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                X = SubNode(X, self.term())
        return X

    def term(self):
        """
        Parse a term.

        Returns:
            A term node that represents the input term.
        """
        # Look for a factor and store it in result
        result = self.power()
        # Look for additional factors after (MUL|DIV) tokens and then construct term node
        while self.current_token != None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = MulNode(result, self.power())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivNode(result, self.power())
        return result

    def power(self):
        """
        Parse a power.

        Returns:
            A power node that represents the input power.
        """
        result = self.object()
        # Look for additional powers and construct power node
        while self.current_token != None and self.current_token.type == TokenType.POW:
            self.advance()
            result = PowNode(result, self.object())
        return result

    def object(self):
        """
        Parse an object.

        Returns:
            An object node that represents the input object.
        """
        token = self.current_token
        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()
            if self.current_token.type != TokenType.RPAREN:
                self.raise_error("Syntax Error, expecting a LPAREN token.")
            self.advance()
            return result
        elif token.type == TokenType.FLOAT:
            self.advance()
            return FloatNode(token.value)
        elif token.type == TokenType.INTEGER:
            self.advance()
            return IntNode(token.value)
        elif token.type == TokenType.TENSOR:
            self.advance()
            return TensorNode(token.value)
        elif token.type == TokenType.VARIABLE:
            self.advance()
            return VariableNode(token.value)
        elif token.type == TokenType.PLUS:
            self.advance()
            return PlusNode(self.object())
        elif token.type == TokenType.MINUS:
            self.advance()
            return MinusNode(self.object())
        elif token.type == TokenType.INTEGRAL:
            self.advance()
            return self.integral_node()
        elif token.type == TokenType.SOLVE:
            self.advance()
            return self.solve_node()
        elif token.type == TokenType.LIMIT:
            self.advance()
            return self.limit_node()
        elif token.type == TokenType.PLOT:
            self.advance()
            return self.plot_node()
        elif token.type == TokenType.NUMERICAL:
            self.advance()
            return self.numerical_node()
        elif token.type == TokenType.SERIES:
            self.advance()
            return self.series_node()
        elif token.type == TokenType.SIMPLIFY:
            self.advance()
            return self.simplify_node()
        elif token.type == TokenType.EXPAND:
            self.advance()
            return self.expand_node()
        elif token.type == TokenType.DIFFERENTIAL:
            self.advance()
            return self.differential_node()
        elif token.type == TokenType.FUNCTION:
            func_name = token.value
            self.advance()
            return self.function_node(func_name)
        elif token.type == TokenType.OPEN_SQUARE_BRACE:
            self.advance()
            return self.array_node()
        elif (token.type in TRIG_FUNCTIONS) or (token.type in HYPERBOLIC_FUNCTIONS):
            function_name = token.type.name
            self.advance()
            return self.trig_function_node(function_name)
        self.raise_error("Syntax Error")

    ########################################################################
    ############################# HELPERS ##################################
    ########################################################################

    def integral_node(self):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression_to_integrate = self.expr()
        if self.current_token.type != TokenType.COMMA:
            self.raise_error("Syntax Error, expecting a COMMA token.")
        self.advance()
        wrt_variables = self.find_context_variables()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return IntegrateNode(expression_to_integrate, wrt_variables)

    def differential_node(self):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression_to_integrate = self.expr()
        if self.current_token.type != TokenType.COMMA:
            self.raise_error("Syntax Error, expecting a COMMA token.")
        self.advance()
        wrt_variables = self.find_context_variables()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return DifferentialNode(expression_to_integrate, wrt_variables)

    def function_node(self, func_name):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        if self.current_token.type != TokenType.VARIABLE:
            self.raise_error("Expected a variable here.")
        wrt_variables = self.find_context_variables()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return FunctionNode(VariableNode(func_name), wrt_variables)

    def solve_node(self):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression_to_integrate = self.expr()
        if self.current_token.type != TokenType.COMMA:
            self.raise_error("Syntax Error, expecting a COMMA token.")
        self.advance()
        wrt_variables = self.find_context_variables()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return IntegrateNode(expression_to_integrate, wrt_variables)

    def limit_node(self):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression_to_integrate = self.expr()
        if self.current_token.type != TokenType.COMMA:
            self.raise_error("Syntax Error, expecting a COMMA token.")
        self.advance()
        wrt_variables = self.find_context_variables()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return IntegrateNode(expression_to_integrate, wrt_variables)
    
    def plot_node(self):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression_to_integrate = self.expr()
        if self.current_token.type != TokenType.COMMA:
            self.raise_error("Syntax Error, expecting a COMMA token.")
        self.advance()
        wrt_variables = self.find_context_variables()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return IntegrateNode(expression_to_integrate, wrt_variables)

    def numerical_node(self):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression_to_integrate = self.expr()
        if self.current_token.type != TokenType.COMMA:
            self.raise_error("Syntax Error, expecting a COMMA token.")
        self.advance()
        wrt_variables = self.find_context_variables()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return IntegrateNode(expression_to_integrate, wrt_variables)

    def series_node(self):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression_to_integrate = self.expr()
        if self.current_token.type != TokenType.COMMA:
            self.raise_error("Syntax Error, expecting a COMMA token.")
        self.advance()
        wrt_variables = self.find_context_variables()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return IntegrateNode(expression_to_integrate, wrt_variables)

    def simplify_node(self):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression = self.expr()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return SimplifyNode(expression)

    def expand_node(self):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression = self.expr()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return ExpandNode(expression)

    def trig_function_node(self, function_name):
        if self.current_token.type != TokenType.LPAREN:
            self.raise_error("Syntax Error, expecting a LPAREN token.")
        self.advance()
        expression = self.expr()
        if self.current_token.type != TokenType.RPAREN:
            self.raise_error("Syntax Error, expecting a RPAREN token.")
        self.advance()
        return function_map(function_name)(expression)

    def array_node(self):
        elements = []
        if self.current_token.type != TokenType.CLOSED_SQUARE_BRACE:
            elements.append(self.expr())
            while self.current_token != None and self.current_token.type == TokenType.COMMA:
                self.advance()
                elements.append(self.expr())
        if self.current_token.type != TokenType.CLOSED_SQUARE_BRACE:
            self.raise_error("Syntax Error, expecting a CLOSED_SQUARE_BRACE token.")
        self.advance()
        return ArrayNode(elements)

    def find_context_variables(self):
        """
        Helper method to find and extract variables from the input.

        Returns:
            A list of VariableNodes representing the extracted variables.
        """
        tokens = []
        if self.current_token.type != TokenType.VARIABLE:
            self.raise_error("Syntax Error, expecting a VARIABLE token.")
        tokens.append(self.object())
        while self.current_token != None and self.current_token.type == TokenType.COMMA:
            self.advance()
            if self.current_token.type != TokenType.VARIABLE:
                self.raise_error("Syntax Error, expecting a VARIABLE token.")
            tokens.append(self.object())
        return tokens
