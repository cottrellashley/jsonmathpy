

class MathJSONInterpreter:
    def __init__(self, operations = None):
        self.operations = operations
    
    def interpret(self, mathjson):
        if isinstance(mathjson, dict):
            operation = mathjson["operation"]
            arguments = mathjson["arguments"]
            if operation in self.operations:
                return self.operations[operation](*[self.interpret(arg) for arg in arguments])
        else:
            return mathjson
        
    def add(self, *args):
        return sum(args)
    
    def subtract(self, *args):
        return args[0] - sum(args[1:])
    
    def multiply(self, *args):
        result = 1
        for arg in args:
            result *= arg
        return result
    
    def divide(self, *args):
        result = args[0]
        for arg in args[1:]:
            result /= arg
        return result
    
    def power(self, *args):
        return args[0] ** args[1]
    
    def build_int(self, *arg):
        return int(''.join(arg))
    
    def build_float(self, *arg):
        return float(''.join(arg))

    def array(self, *args):
        return list(args)