class MathOperation:
    def __init__(self, *args):
        self.args = args

    @classmethod
    def from_json(cls, json_obj):
        args = [cls.from_json(arg) if isinstance(arg, dict) else arg for arg in json_obj['arguments']]
        return cls(*args)

    def evaluate(self):
        raise NotImplementedError

class Add(MathOperation):
    
    def evaluate(self):
        a, b = self.args
        return a + b

class Multiply(MathOperation):

    def evaluate(self):
        a, b = self.args
        return a * b

class Divition(MathOperation):

    def evaluate(self):
        a, b = self.args
        return a / b

class Pow(MathOperation):

    def evaluate(self):
        a, b = self.args
        return a ** b

class Int(MathOperation):

    def evaluate(self):
        a = ''.join(self.args)
        return int(a)

class Float(MathOperation):

    def evaluate(self):
        a = ''.join(self.args)
        return float(a)

DEFAULT_OPERATION_CLASSES = {
        "BUILD_INT" : Int,
        "BUILD_FLOAT" : Float,
        "ADD": Add,
        "MULTIPLY": Multiply,
        "DIVISION": Divition,
        "POWER" : Pow
    }

class MathInterpreter:

    DEFAULT_OPERATION_CLASSES = {
            "BUILD_INT" : Int,
            "BUILD_FLOAT" : Float,
            "ADD": Add,
            "MULTIPLY": Multiply,
            "DIVISION": Divition,
            "POWER" : Pow
        }

    def __init__(self, math_op, operation_classes=None):
        self.math_op = math_op
        self.operation_classes = operation_classes if operation_classes else DEFAULT_OPERATION_CLASSES

    def evaluate(self):
        if isinstance(self.math_op, dict):
            operation_name = self.math_op["operation"]
            operation_class = self.operation_classes[operation_name]
            if operation_class is None:
                raise ValueError(f"No operation class defined for {operation_name}")
            args = [self.__class__(arg, self.operation_classes).evaluate() if isinstance(arg, dict) else arg for arg in self.math_op["arguments"]]
            return operation_class(*args).evaluate()
        else:
            return self.math_op.evaluate()

    @classmethod
    def from_json(cls, json_obj):
        return cls(MathOperation.from_json(json_obj))
