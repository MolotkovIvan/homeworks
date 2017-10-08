class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}

    def __getitem__(self, key):
        if key in self.values:
            return self.values[key]
        elif self.parent is not None:
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

    def get_value(self):
        return self.value


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self

    def get_args(self):
        return self.args

    def get_expr(self):
        return self.body


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if (self.condition).evaluate(scope) != Number(0):
            return self.if_true[len(self.if_true)-1].evaluate(scope)
        elif self.if_false != 0:
            return self.if_false[len(self.if_false)-1].evaluate(scope)


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        result = (self.expr).evaluate(scope)
        print(result.get_value())
        return result


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        func = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        args_name = func.get_args()
        expressions = func.get_expr()
        for i in range(len(self.args)):
            call_scope[args_name[i]] = (self.args)[i].evaluate(scope)
        for i in range(len(expressions)):
            expressions[i] = expressions[i].evaluate(call_scope)
        return expressions[len(expressions) - 1]


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        l = scope[self.lhs].get_value()
        r = scope[self.rhs].get_value()
        if self.op == "+":
            return Number(l + r)
        if self.op == "-":
            return Number(l - r)
        if self.op == "*":
            return Number(l * r)
        if self.op == "/":
            return Number(l // r)
        if self.op == "%":
            return Number(l % r)
        if self.op == "==":
            if l == r:
                return Number(1)
            else:
                return Number(0)
        if self.op == "!=":
            if l != r:
                return Number(1)
            else:
                return Number(0)
        if self.op == "<":
            if l < r:
                return Number(1)
            else:
                return Number(0)
        if self.op == ">":
            if l > r:
                return Number(1)
            else:
                return Number(0)
        if self.op == "<=":
            if l <= r:
                return Number(1)
            else:
                return Number(0)
        if self.op == ">=":
            if l >= r:
                return Number(1)
            else:
                return Number(0)
        if self.op == "&&":
            if l != 0 and r != 0:
                return Number(1)
            else:
                return Number(0)
        if self.op == "||":
            if l != 0 or r != 0:
                return Number(1)
            else:
                return Number(0)


class UnaryOperation:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope).get_value()
        if self.op == "-":
            return Number(res * (-1))
        if self.op == "!":
            if res == 0:
                return Number(1)
            else:
                return Number(0)
