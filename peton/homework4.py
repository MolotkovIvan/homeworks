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


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self


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
            if self.if_true is not None and len(self.if_true) != 0:
                for expr in self.if_true[:-1]:
                    expr.evaluate(scope)
                return self.if_true[-1].evaluate(scope)
        elif self.if_false is not None:
            if len(self.if_false) != 0:
                for expr in self.if_false[:-1]:
                    expr.evaluate(scope)
                return self.if_false[-1].evaluate(scope)


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        result = (self.expr).evaluate(scope)
        print(result.value)
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
        args_name = func.args
        expressions = func.body
        for exp in expressions:
            print(exp, end=" ")
        for i in range(len(self.args)):
            call_scope[args_name[i]] = (self.args)[i].evaluate(scope)
        for i in range(len(expressions)):
            expressions[i] = expressions[i].evaluate(call_scope)
        for exp in expressions:
            print(exp.value, end=" ")
        return expressions[-1]


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
        l = self.lhs.evaluate(scope).value
        r = self.rhs.evaluate(scope).value
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
        res = self.expr.evaluate(scope).value
        if self.op == "-":
            return Number(res * (-1))
        if self.op == "!":
            if res == 0:
                return Number(1)
            else:
                return Number(0)

s = Scope()
Read("a").evaluate(s)
Read("b").evaluate(s)
Print(UnaryOperation("-", BinaryOperation(Reference("a"), "+", Reference("b")))).evaluate(s)
Print(Conditional(Number(0), [BinaryOperation(Reference("a"), "*", Reference("b"))], [Number(4)])).evaluate(s)

operation1 = FunctionDefinition("foo", Function(["a", "b"],
  [
    Print(BinaryOperation(Reference("a"), "+", Reference("b"))),
    BinaryOperation(Reference("a"), "+", Reference("b"))
  ]
))

operation2 = FunctionCall(Reference("foo"), [
  Number(1),
  BinaryOperation(Number(2), "+", Number(3))
])
#operation3 = FunctionCall(Reference("foo"), [
#  Number(1),
#  BinaryOperation(Number(2), "+", Number(3))
#])

operation1.evaluate(s)
operation2.evaluate(s)
operation2.evaluate(s)
