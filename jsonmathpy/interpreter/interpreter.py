from jsonmathpy.interpreter.math_json import MathJSON

class Interpreter:

    def visit(self, node):
        if isinstance(node, list):
            return [getattr(self, f"visit_{type(i).__name__}")(i).dict for i in node]
        else:
            method_name = f"visit_{type(node).__name__}"
            method = getattr(self, method_name)
            return method(node)

    def visit_IntNode(self, node) -> MathJSON:
        return MathJSON({}).build_int(node.value)

    def visit_ArrayNode(self, node) -> MathJSON:
        return MathJSON({}).array(self.visit(node.node))

    def visit_MinusNode(self, node) -> MathJSON:
        return MathJSON({}).build_minus(self.visit(node.value))

    def visit_FloatNode(self, node) -> MathJSON:
        return MathJSON({}).build_float(node.value)

    def visit_TensorNode(self, node) -> MathJSON:
        return MathJSON({}).build_tensor(node.value)

    def visit_VariableNode(self, node) -> MathJSON:
        return MathJSON({}).build_variable(node.value)

    def visit_PowNode(self, node) -> MathJSON:
        return MathJSON(self.visit(node.node_a).dict) ** MathJSON(self.visit(node.node_b).dict)

    def visit_AddNode(self, node) -> MathJSON:
        return MathJSON(self.visit(node.node_a).dict) + MathJSON(self.visit(node.node_b).dict)

    def visit_SubNode(self, node) -> MathJSON:
        return MathJSON(self.visit(node.node_a).dict) - MathJSON(self.visit(node.node_b).dict)

    def visit_MulNode(self, node) -> MathJSON:
        return MathJSON(self.visit(node.node_a).dict) * MathJSON(self.visit(node.node_b).dict)

    def visit_DivNode(self, node) -> MathJSON:
        return MathJSON(self.visit(node.node_a).dict) / MathJSON(self.visit(node.node_b).dict)

    def visit_DifferentialNode(self, node) -> MathJSON:
        return MathJSON(self.visit(node.node_a).dict).differentiate(MathJSON(self.visit(node.node_b)))

    def visit_IntegrateNode(self, node) -> MathJSON:
        return MathJSON(self.visit(node.node_a).dict).integrate(MathJSON(self.visit(node.node_b)))

    def visit_FunctionNode(self, node) -> MathJSON:
        return MathJSON(self.visit(node.node_a).dict).function(MathJSON(self.visit(node.node_b)))

