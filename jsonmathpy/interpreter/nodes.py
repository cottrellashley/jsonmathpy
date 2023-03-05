from dataclasses import dataclass

#########################################
######### SINGLE ARGUMENT NODES #########
#########################################

@dataclass
class PlusNode:
    """Represents a positive node."""

    value: any

    def __repr__(self):
        return f"(+{self.value})"

@dataclass
class MinusNode:
    """Represents a minus or negation node."""

    value: any

    def __repr__(self):
        return f"(-{self.value})"

@dataclass
class TensorNode:
    """Represents a tensor node."""

    value: any
    "Value representing the tensor. Usually a string."

    def __repr__(self):
        return f"({self.value})"

@dataclass
class VariableNode:
    """Represents a variable node."""

    value: any
    "Value represening the variable. Usually a string."

    def __repr__(self):
        return f"{self.value}"

@dataclass
class IntNode:
    """Represents a integer number node."""

    value: any
    "Value representing the integer number. Usually a string."

    def __repr__(self):
        return f"({self.value})"

@dataclass
class FloatNode:
    """Represents a floating point number node."""

    value: any
    "Value representing the Floting number node. Usually a string."

    def __repr__(self):
        return f"({self.value})"

@dataclass
class SimplifyNode:
    """Represents simplification function node."""

    value: any
    "The expression to be simplified."

    def __repr__(self):
        return f"simplify({self.value})"

@dataclass
class ExpandNode:
    """Represents expand function node."""

    value: any
    "The expression to expand."

    def __repr__(self):
        return f"expand({self.value})"


#########################################
######## SIMPLE ARITHMETIC NODES ########
#########################################

@dataclass
class AddNode:
    """Represents a addition node."""

    value_a: any
    value_b: any


    def __repr__(self):
        return f"({self.value_a} + {self.value_b})"

@dataclass
class SubNode:
    """Represents a subtraction node."""

    value_a: any
    value_b: any

    def __repr__(self):
        return f"({self.value_a} - {self.value_b})"

@dataclass
class MulNode:
    """Represents a multiplication node."""

    value_a: any
    value_b: any

    def __repr__(self):
        return f"({self.value_a} * {self.value_b})"

@dataclass
class PowNode:
    """Represents a exponentiation node."""

    value_a: any
    "The base expression of the exponent."

    value_b: any
    "The exponent of the expression."

    def __repr__(self):
        return f"({self.value_a} ^ {self.value_b})"

@dataclass
class DivNode:
    """Represents a division node."""

    value_a: any
    "The Nominator"

    value_b: any
    "The Denominator"

    def __repr__(self):
        return f"({self.value_a} / {self.value_b})"

#########################################
###### FUNCTION / OPERATION NODES #######
#########################################

@dataclass
class FunctionNode:

    value_a: any
    value_b: any

    def __repr__(self):
        return f"({self.value_a}, {self.value_b})"


@dataclass
class IntegrateNode:
    """Represents a integration node."""

    value_a: any
    "The integrand. The expression to integrate."

    value_b: list
    "List representing the measure (variables to integrate with respect to.)"

    def __repr__(self):
        return f"integrate({self.value_a}, {self.value_b})"

@dataclass
class DifferentialNode:
    """Represents a differentiation node."""

    value_a: any
    "The expression to differentiate."

    value_b: list
    "List of the variables to differentiate with respect to."

    def __repr__(self):
        return f"differential({self.value_a}, {self.value_b})"

@dataclass
class SolveNode:
    """Represents the solve function node."""

    value_a: any
    "The expression or list of expressions to be solved."

    value_b: any
    "Variables or list of the variables to solve expression with respect to."

    def __repr__(self):
        return f"solve({self.value_a}, {self.value_b})"


@dataclass
class LimitNode:
    """Represents the limit function node."""

    value_a: any
    "The expression whose limit needs to be evaluated."

    value_b: any
    "The independent variable of the expression."

    value_c: any
    "The point at which the limit needs to be evaluated."

    def __repr__(self):
        return f"limit({self.value_a}, {self.value_b}, {self.value_c})"


@dataclass
class SeriesNode:
    """Represents the taylor series function node."""

    value_a: any
    "The expression whose Taylor series needs to be computed."

    value_b: any
    "The point about which the Taylor series is being computed."

    value_c: any
    "The number of terms to compute in the Taylor series."

    def __repr__(self):
        return f"series({self.value_a}, {self.value_b}, {self.value_c})"

@dataclass
class NumericalNode:
    """Represents a numerical function node."""

    value_a: any
    "The expression to be evaluated numerically."

    value_b: any
    "The number of digits of precision to use in the numerical evaluation. This can be an integer or None (which means to use the default value of 15)."

    def __repr__(self):
        return f"numerical({self.value_a}, {self.value_b})"

@dataclass
class PlotNode:
    """Represents a plot function node."""

    value_a: any
    "The expression(s) to be plotted. This can be a single expression or a list of expressions."

    value_b: list
    "The range over which to plot the expression(s). This can be a tuple of the form (x, xmin, xmax) or a list of such tuples."

    def __repr__(self):
        return f"plot({self.value_a}, {self.value_b})"

@dataclass
class EqualsNode: # Currenctly not used/implemented
    """Represents assignment node. Value assigned to a key in local memory."""

    value_a: any
    "Value of the key, assigned value."

    value_b: any
    "Value the key will return when called."

    def __repr__(self):
        return f"{self.value_a} = {self.value_b}"


@dataclass
class ArrayNode:
    "Node representing an array."

    value: list
    "List of values in the list."
        
    def __repr__(self):
        return f"[{self.value}]"

#########################################
######### TRIGONOMETRIC NODES ###########
#########################################

@dataclass
class BaseTrigFunction:
    """ Base class of trig function nodes."""

    value: any
    "Argument of the trig function."
        
    def __repr__(self):
        func_name = type(self).__name__
        return f"{func_name}({self.value})"

@dataclass
class SinNode(BaseTrigFunction):
    pass

@dataclass
class CosNode(BaseTrigFunction):
    pass

@dataclass
class TanNode(BaseTrigFunction):
    pass

@dataclass
class ASinNode(BaseTrigFunction):
    pass

@dataclass
class ACosNode(BaseTrigFunction):
    pass

@dataclass
class ATanNode(BaseTrigFunction):
    pass

#########################################
########### HYPERBOLIC NODES ############
#########################################


@dataclass
class BaseHyperbolicFunction:
    """ Base class of hyperbolic node."""

    value: any
    "Argument of the hyperbolic function."
        
    def __repr__(self):
        func_name = type(self).__name__
        return f"{func_name}({self.value})"

@dataclass
class SinhNode(BaseHyperbolicFunction):
    pass

@dataclass
class CoshNode(BaseHyperbolicFunction):
    pass

@dataclass
class TanhNode(BaseHyperbolicFunction):
    pass

@dataclass
class ASinhNode(BaseHyperbolicFunction):
    pass

@dataclass
class ACoshNode(BaseHyperbolicFunction):
    pass

@dataclass
class ATanhNode(BaseHyperbolicFunction):
    pass
