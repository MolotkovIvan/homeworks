class PureCheckVisitor:
    def visit_array(self, expressions):
        if not expressions:
            return True
        return all(expr.accept(self) for expr in expressions)

    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, number):
        return True

    def visit_reference(self, reference):
        return True

    def visit_conditional(self, conditional):
        return (conditional.condition.accept(self) and
                self.visit_array(conditional.if_true) and
                self.visit_array(conditional.if_false))

    def visit_read(self, read):
        return False

    def visit_print(self, print):
        return False

    def visit_function(self, function):
        return self.visit_array(function.body)

    def visit_function_definition(self, function_definition):
        return self.visit_array(function_definition.function.body)

    def visit_function_call(self, function_call):
        return (self.visit_array(function_call.args) and
                function_call.fun_expr.accept(self))

    def visit_unary_operation(self, unary_operation):
        return unary_operation.expr.accept(self)

    def visit_binary_operation(self, binary_operation):
        return (binary_operation.lhs.accept(self) and
                binary_operation.rhs.accept(self))


class NoReturnValueCheckVisitor:
    def visit_body(self, expressions):
        ans = False
        for expr in expressions or []:
            ans = expr.accept(self)
        return ans

    def visit_function_arguments(self, expressions):
        ans = True
        for expr in expressions:
            if not expr.accept(self):
                ans = False
        return ans

    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, number):
        return True

    def visit_reference(self, reference):
        return True

    def visit_conditional(self, conditional):
        cond1 = self.visit_body(conditional.if_true)
        cond2 = self.visit_body(conditional.if_false)
        conditional.condition.accept(self)
        return cond1 and cond2

    def visit_read(self, read):
        return True

    def visit_print(self, print):
        print.expr.accept(self)
        return True

    def visit_function(self, function):
        return self.visit_body(function.body)

    def visit_function_definition(self, function_definition):
        if not function_definition.function.accept(self):
            print(function_definition.name)
        return True

    def visit_function_call(self, function_call):
        cond1 = function_call.fun_expr.accept(self)
        cond2 = self.visit_function_arguments(function_call.args)
        return cond1 and cond2

    def visit_unary_operation(self, unary_operation):
        unary_operation.expr.accept(self)
        return True

    def visit_binary_operation(self, binary_operation):
        binary_operation.lhs.accept(self)
        binary_operation.rhs.accept(self)
        return True
