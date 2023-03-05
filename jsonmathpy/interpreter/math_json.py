class MathJSON:
    def __init__(self, dict):
        self.dict = dict
        
    def __add__(self, other):
        return MathJSON({
            "operation": "ADD",
            "arguments": [self.dict, other.dict]
        })
    
    def __mul__(self, other):
        return MathJSON({
            "operation": "MULTIPLY",
            "arguments": [self.dict, other.dict]
        })
    
    def __sub__(self, other):
        return MathJSON({
            "operation": "SUBTRACTION",
            "arguments": [self.dict, other.dict]
        })

    def __pow__(self, other):
        return MathJSON({
            "operation": "POWER",
            "arguments": [self.dict, other.dict]
        })
    
    def __truediv__(self, other):
        return MathJSON({
            "operation": "DIVISION",
            "arguments": [self.dict, other.dict]
        })

    def func(self, variables):
        return MathJSON({
            "operation": "FUNCTION",
            "arguments": [self.dict, variables.dict]
        })

    def integrate(self, measure):
        return MathJSON({
            "operation": "INTEGRAL",
            "arguments": [self.dict, measure.dict]
        })

    def differentiate(self, measure):
        return MathJSON({
            "operation": "DIFFERENTIAL",
            "arguments": [self.dict, measure.dict]
        })

    def function(self, measure):
        return MathJSON({
            "operation": "FUNCTION",
            "arguments": [self.dict, measure.dict]
        })

    def build_int(self, integer):
        return MathJSON({
            "operation": "BUILD_INT",
            "arguments": str(integer)
        })

    def build_float(self, float):
        return MathJSON({
            "operation": "BUILD_FLOAT",
            "arguments": str(float)
        })

    def build_tensor(self, tensor_repr):
        return MathJSON({
            "operation": "BUILD_TENSOR",
            "arguments": str(tensor_repr)
        })

    def build_variable(self, variable_repr):
        return MathJSON({
            "operation": "BUILD_VARIABLE",
            "arguments": str(variable_repr)
        })

    def build_minus(self, object):
        return MathJSON({
            "operation": "BUILD_MINUS",
            "arguments": [object.dict]
        })

    def array(self, objects):
        return MathJSON({
            "operation": "ARRAY",
            "arguments": objects
        })
