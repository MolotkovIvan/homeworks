from yat.model import *
from yat.static_analyzer import *

print(PureCheckVisitor().visit(FunctionDefinition("foo", Function(["x", "y", "z"], [Reference("x"), Number(5)]))))
#p.visit(FunctionCall(Reference("foo"), [Number(5), Number(2), BinaryOperation(Reference("a"), "+", Reference("b"))]))
prog1 = Conditional(BinaryOperation(Number(4), "=", Print(Number(5))), [
    Number(123),
], [
    Number(456),
])
prog2 = Conditional(BinaryOperation(Number(4), "=", Number(5)), [
    Print(Number(123)),
], [
    Number(456),
])
print(PureCheckVisitor().visit(prog1))
print(PureCheckVisitor().visit(prog2))