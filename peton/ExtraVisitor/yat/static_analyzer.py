def check_array(expressions, visitor):
    if expressions:
        for expr in expressions:
            if not expr.accept(visitor):
                return False
    return True


class PureCheckVisitor:
    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, number):
        return True

    def visit_reference(self, reference):
        return True

    def visit_conditional(self, conditional):
        if conditional.condition.accept(self) is False:
            return False
        if (check_array(conditional.if_true, self) and check_array(conditional.if_false, self)):
            return True
        return False

    def visit_read(self, read):
        return False

    def visit_print(self, print):
        return False

    def visit_function(self, function):
        return check_array(function.body, self)

    def visit_function_definition(self, function_definition):
        return check_array(function_definition.function.body, self)

    def visit_function_call(self, function_call):
        return check_array(function_call.args, self)

    def visit_unary_operation(self, unary_operation):
        return unary_operation.expr.accept(self)

    def visit_binary_operation(self, binary_operation):
        if binary_operation.lhs.accept(self) and binary_operation.rhs.accept(self):
            return True
        else:
            return False
