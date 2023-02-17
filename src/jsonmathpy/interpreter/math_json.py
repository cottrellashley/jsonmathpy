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
            "operation": "MINUS",
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
