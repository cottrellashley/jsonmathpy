from jsonmathpy.interpreter.nodes import *
from jsonmathpy.interpreter.types import TokenType
from more_itertools import peekable

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

    def find_variables(self):
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
        #########################################
        # | BELLOW NEEDS IMPROVEMENT | From here on, there woll be a lot of repeated code, which can be wraped in a single function call.
        #########################################
        elif token.type == TokenType.INTEGRAL:
            self.advance()
            if self.current_token.type != TokenType.LPAREN:
                self.raise_error("Syntax Error, expecting a LPAREN token.")
            self.advance()
            expression_to_integrate = self.expr()
            if self.current_token.type != TokenType.COMMA:
                self.raise_error("Syntax Error, expecting a COMMA token.")
            self.advance()
            wrt_variables = self.find_variables()
            if self.current_token.type != TokenType.RPAREN:
                self.raise_error("Syntax Error, expecting a RPAREN token.")
            self.advance()
            return IntegrateNode(expression_to_integrate, wrt_variables)
        elif token.type == TokenType.DIFFERENTIAL:
            self.advance()
            if self.current_token.type != TokenType.LPAREN:
                self.raise_error("Syntax Error, expecting a LPAREN token.")
            self.advance()
            expression_to_integrate = self.expr()
            if self.current_token.type != TokenType.COMMA:
                self.raise_error("Syntax Error, expecting a COMMA token.")
            self.advance()
            wrt_variables = self.find_variables()
            if self.current_token.type != TokenType.RPAREN:
                self.raise_error("Syntax Error, expecting a RPAREN token.")
            self.advance()
            return DifferentialNode(expression_to_integrate, wrt_variables)
        elif token.type == TokenType.FUNCTION:
            func_name = token.value
            self.advance()
            if self.current_token.type != TokenType.LPAREN:
                self.raise_error("Syntax Error, expecting a LPAREN token.")
            self.advance()
            if self.current_token.type != TokenType.VARIABLE:
                self.raise_error("Expected a variable here.")
            wrt_variables = self.find_variables()
            if self.current_token.type != TokenType.RPAREN:
                self.raise_error("Syntax Error, expecting a RPAREN token.")
            self.advance()
            return FunctionNode(VariableNode(func_name), wrt_variables)
        elif token.type == TokenType.OPEN_SQUARE_BRACE:
            self.advance()
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
        self.raise_error("Syntax Error")