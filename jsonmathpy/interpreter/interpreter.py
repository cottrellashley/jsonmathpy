from jsonmathpy.interpreter.math_json import MathJSON

class Interpreter:

    """
    This is a Python interpreter for a math expression language. 
    It defines an Interpreter class with a visit method that accepts a node from an expression tree and returns a MathJSON object, 
    which is a custom data type used to represent mathematical expressions in JSON format.

    The visit method uses dynamic dispatch to call a specific method based on the type of the input node. 
    Each method corresponds to a specific type of node in the expression tree and is responsible for evaluating that node and returning the result as a MathJSON object.

    For example, the visit_PowNode method evaluates a node representing a power operation (X^Y) 
    by calling the ** operator on the MathJSON objects corresponding to the X and Y operands. 
    Similarly, the visit_AddNode method evaluates a node representing an addition operation (X + Y) 
    by calling the + operator on the MathJSON objects corresponding to the X and Y operands.

    The Interpreter class uses the MathJSON object to build the resulting expression tree as a JSON object, 
    which can then be used for further processing or serialization.

    Overall, this interpreter provides a way to evaluate and manipulate mathematical expressions in a JSON format.
    """


    def visit(self, node):
        """
        visit method:
            This function is responsible for dispatching to the appropriate visit method based on the type of the given node. 
            If the node is a list, it calls the appropriate visit method for each element of the list and returns a list of the resulting MathJSON objects. 
            If the node is not a list, it calls the appropriate visit method for that type of node and returns the resulting MathJSON object.
        Args:
            node : Node
        """
        if isinstance(node, list):
            return [getattr(self, f"visit_{type(i).__name__}")(i).dict for i in node]
        else:
            method_name = f"visit_{type(node).__name__}"
            method = getattr(self, method_name)
            return method(node)

    def visit_IntNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing an integer value."""
        return MathJSON({}).build_int(node.value)

    def visit_ArrayNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing an array."""
        return MathJSON({}).array(self.visit(node.value))

    def visit_MinusNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing a negative value."""
        return MathJSON({}).build_minus(self.visit(node.value))

    def visit_FloatNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing a floating-point value."""
        return MathJSON({}).build_float(node.value)

    def visit_TensorNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing a tensor."""
        return MathJSON({}).build_tensor(node.value)

    def visit_VariableNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing a variable."""
        return MathJSON({}).build_variable(node.value)

    def visit_PowNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of raising one MathJSON object to the power of another."""
        return MathJSON(self.visit(node.value_a).dict) ** MathJSON(self.visit(node.value_b).dict)

    def visit_AddNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the sum of two MathJSON objects."""
        return MathJSON(self.visit(node.value_a).dict) + MathJSON(self.visit(node.value_b).dict)

    def visit_SubNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the difference between two MathJSON objects."""
        return MathJSON(self.visit(node.value_a).dict) - MathJSON(self.visit(node.value_b).dict)

    def visit_MulNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the product of two MathJSON objects."""
        return MathJSON(self.visit(node.value_a).dict) * MathJSON(self.visit(node.value_b).dict)

    def visit_DivNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the quotient of two MathJSON objects."""
        return MathJSON(self.visit(node.value_a).dict) / MathJSON(self.visit(node.value_b).dict)

    def visit_DifferentialNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of taking the derivative of one MathJSON object with respect to another."""
        return MathJSON(self.visit(node.value_a).dict).differentiate(MathJSON(self.visit(node.value_b)))

    def visit_IntegrateNode(self, node) -> MathJSON:
        """ This function creates a MathJSON object representing the result of integrating one MathJSON object with respect to another."""
        return MathJSON(self.visit(node.value_a).dict).integrate(MathJSON(self.visit(node.value_b)))

    def visit_FunctionNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of applying a function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value_a).dict).function(MathJSON(self.visit(node.value_b)))

    def visit_SinNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the sin function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).sin()

    def visit_CosNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the cos function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).cos()

    def visit_TanNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the tan function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).tan()

    def visit_ASinNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the asin function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).asin()

    def visit_ACosNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the acos function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).acos()

    def visit_ATanNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the atan function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).atan()

    def visit_SinhNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the sinh function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).sinh()

    def visit_CoshNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the cosh function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).cosh()

    def visit_TanhNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the tanh function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).tanh()

    def visit_ASinhNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the asinh function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).asinh()

    def visit_ACoshNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the acosh function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).acosh()

    def visit_ATanhNode(self, node) -> MathJSON:
        """This function creates a MathJSON object representing the result of the atanh function represented by one MathJSON object to another."""
        return MathJSON(self.visit(node.value).dict).atanh()

