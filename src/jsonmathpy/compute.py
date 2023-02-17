class MathOperation:
    def __init__(self, *args):
        self.args = args

    @classmethod
    def from_json(cls, json_obj):
        args = [cls.from_json(arg) if isinstance(arg, dict) else arg for arg in json_obj['arguments']]
        return cls(*args)

    def evaluate(self):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError

class Add(MathOperation):
    
    def evaluate(self):
        a, b = self.args
        return a + b

    def to_json(self):
        return {
            "operation": "ADD",
            "arguments": [arg.to_json() for arg in self.args]
        }

class Multiply(MathOperation):

    def evaluate(self):
        a, b = self.args
        return a * b


    def to_json(self):
        return {
            "operation": "MULTIPLY",
            "arguments": [arg.to_json() for arg in self.args]
        }

class MathInterpreter:
    OPERATION_CLASSES = {
        "ADD": Add,
        "MULTIPLY": Multiply,
        # Add additional operation classes here
    }

    @classmethod
    def from_json(cls, json_obj):
        return cls(MathOperation.from_json(json_obj))

    def __init__(self, math_op):
        self.math_op = math_op

    def evaluate(self):
        if isinstance(self.math_op, dict):
            operation_name = self.math_op["operation"]
            operation_class = self.OPERATION_CLASSES[operation_name]
            args = [self.__class__(arg).evaluate() if isinstance(arg, dict) else arg for arg in self.math_op["arguments"]]
            return operation_class(*args).evaluate()
        else:
            return self.math_op.evaluate()

