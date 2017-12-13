class PureCheckVisitor:
    def __init__(self):
        self.isPure = True

    def visit(self, tree):
        self.isPure = tree.accept(self)
        print(self.isPure)

    def visit_number(self, number):
        return True

    def visit_reference(self, reference):
        return True

    def visit_conditional(self, conditional):
        if conditional.condition.accept(self) is False:
            return False

        for expr in conditional.if_true:
            if expr.accept(self) is False:
                return False

        for expr in conditional.if_false:
            if expr.accept(self) is False:
                return False

        return True

    def visit_read(self, read):
        return False

    def visit_print(self, print):
        return False

    def visit_function_definition(self, function_definition):
        f = function_definition.function
        for expr in f.body:
            if expr.accept(self) is False:
                return False
        return True

    def visit_function_call(self, function_call):
        return True

    def visit_unary_operation(self, unary_operation):
        return unary_operation.expr.accept(self)

    def visit_binary_operation(self, binary_operation):
        if binary_operation.lhs.accept(self) and binary_operation.rhs.accept(self):
            return True
        else:
            return False
