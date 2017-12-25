class PureCheckVisitor:
    def check_array(self, expressions):
        return all([expr.accept(self) for expr in expressions])

    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, number):
        return True

    def visit_reference(self, reference):
        return True

    def visit_conditional(self, conditional):
        return (conditional.condition.accept(self) and
                self.check_array(conditional.if_true) and
                self.check_array(conditional.if_false))

    def visit_read(self, read):
        return False

    def visit_print(self, print):
        return False

    def visit_function(self, function):
        return self.check_array(function.body)

    def visit_function_definition(self, function_definition):
        return self.check_array(function_definition.function.body)

    def visit_function_call(self, function_call):
        return (self.check_array(function_call.args) and
                function_call.fun_expr.accept(self))

    def visit_unary_operation(self, unary_operation):
        return unary_operation.expr.accept(self)

    def visit_binary_operation(self, binary_operation):
        return (binary_operation.lhs.accept(self) and
                binary_operation.rhs.accept(self))
