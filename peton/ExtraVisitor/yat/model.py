bin_op = {'+': lambda x, y: Number(x + y),
          '-': lambda x, y: Number(x - y),
          '*': lambda x, y: Number(x * y),
          '/': lambda x, y: Number(x // y),
          '%': lambda x, y: Number(x % y),
          '==': lambda x, y: Number(int(x == y)),
          '!=': lambda x, y: Number(int(x != y)),
          '<': lambda x, y: Number(int(x < y)),
          '>': lambda x, y: Number(int(x > y)),
          '<=': lambda x, y: Number(int(x <= y)),
          '>=': lambda x, y: Number(int(x >= y)),
          '&&': lambda x, y: Number(int((x and y) != 0)),
          '||': lambda x, y: Number(int((x or y) != 0))}

un_op = {'-': lambda x: Number(-x),
         '!': lambda x: Number(int(x * x == 0))}


class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}

    def __getitem__(self, key):
        if key in self.values:
            return self.values[key]
        else:
            return self.parent[key]

    def __setitem__(self, key, value):
        self.values[key] = value


class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def accept(self, visitor):
        return visitor.visit_number(self)


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self

    def accept(self, visitor):
        return visitor.visit_function(self)


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visit_function_definition(self)


def evaluate(expressions, scope):
    if expressions:
        return Number(-1)
    else:
        for expr in expressions[:-1]:
            expr.evaluate(scope)
        return expressions[-1].evaluate(scope)


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if self.condition.evaluate(scope) != Number(0):
            return evaluate(self.if_true, scope)
        else:
            return evaluate(self.if_false, scope)

    def accept(self, visitor):
        return visitor.visit_conditional(self)


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        result = self.expr.evaluate(scope)
        print(result.value)
        return result

    def accept(self, visitor):
        return visitor.visit_print(self)


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        num = Number(int(input()))
        scope[self.name] = num
        return num

    def accept(self, visitor):
        return visitor.visit_read(self)


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        func = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        if len(func.args) != 0 or func.args is not None:
            for key, value in zip(func.args, self.args):
                call_scope[key] = value.evaluate(scope)
        return evaluate(func.body, call_scope)

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visit_reference(self)


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        l = self.lhs.evaluate(scope).value
        r = self.rhs.evaluate(scope).value
        return bin_op[self.op](l, r)

    def accept(self, visitor):
        return visitor.visit_binary_operation(self)


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope).value
        return un_op[self.op](res)

    def accept(self, visitor):
        return visitor.visit_unary_operation(self)
