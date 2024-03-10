import ast
import inspect
import textwrap

from ..contracts.primitives import _Function
from z3 import And, BoolVal, If, IntVal, Or, StringVal



class Z3Transformer(ast.NodeVisitor):
    def __init__(self, global_vars: dict, local_vars: dict):
        self.global_vars = global_vars
        self.local_vars = local_vars

    def visit_Module(self, node):
        if len(node.body) != 1:
            raise NotImplementedError("Only single expression functions are supported.")
        return self.visit(node.body[0])

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Return(self, node):
        return self.visit(node.value)

    def visit_FunctionDef(self, node):
        func_def = self.global_vars[node.name]
        if not isinstance(func_def, _Function):
            raise ValueError(f"No contract given for {func_def}")
        func_def = func_def.func

        annotations = inspect.get_annotations(func_def)
        result = annotations.pop("return")
        local_vars = {
            name: contract.symbolic(name) for name, contract in annotations.items()
        }
        for name, value in local_vars.items():
            self.local_vars[name] = value
        if len(node.body) != 1:
            raise NotImplementedError(
                f"Only single expression functions are supported, blaming {func_def}"
            )
        func_body = node.body[0]
        return self.visit(func_body) == result.symbolic()

    def visit_Call(self, node):
        func_def = self.global_vars[node.func.id]
        if isinstance(func_def, _Function):
            func_def = func_def.func
        func_def_node = ast.parse(textwrap.dedent(inspect.getsource(func_def)))

        call_args = node.args
        func_args = func_def_node.body[0].args.args
        if len(func_def_node.body[0].body) != 1:
            raise NotImplementedError(
                f"Only single expression functions are supported, blaming {func_def}"
            )
        func_body = func_def_node.body[0].body[0]

        new_env = {
            func_arg.arg: self.visit(ast.parse(call_arg))
            for call_arg, func_arg in zip(call_args, func_args)
        }

        return Z3Transformer(global_vars=self.global_vars, local_vars=new_env).visit(
            func_body
        )

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right
        elif isinstance(node.op, ast.Mod):
            return left % right
        elif isinstance(node.op, ast.Pow):
            return left ** right
        else:
            raise NotImplementedError(f"Operation {type(node.op)} not implemented.")

    def visit_Name(self, node):
        if node.id not in self.local_vars:
            raise ValueError(f"Variable {node.id} not define in local_vars")
        return self.local_vars[node.id]

    def visit_IfExp(self, node):
        test = self.visit(node.test)
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        return If(test, body, orelse)

    def visit_Compare(self, node):
        if len(node.ops) != 1 or len(node.comparators) != 1:
            raise NotImplementedError("Complex comparisons not implemented.")
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        if isinstance(node.ops[0], ast.Eq):
            return left == right
        elif isinstance(node.ops[0], ast.NotEq):
            return left != right
        elif isinstance(node.ops[0], ast.Lt):
            return left < right
        elif isinstance(node.ops[0], ast.LtE):
            return left <= right
        elif isinstance(node.ops[0], ast.Gt):
            return left > right
        elif isinstance(node.ops[0], ast.GtE):
            return left >= right
        else:
            raise NotImplementedError(
                f"Comparison {type(node.ops[0])} not implemented."
            )

    def visit_BoolOp(self, node):
        if len(node.values) != 2:
            raise NotImplementedError("Complex boolean operations not implemented.")
        left = self.visit(node.values[0])
        right = self.visit(node.values[1])
        if isinstance(node.op, ast.And):
            return And(left, right)
        elif isinstance(node.op, ast.Or):
            return Or(left, right)
        else:
            raise NotImplementedError(
                f"Boolean operation {type(node.op)} not implemented."
            )

    def visit_Constant(self, node):
        if node.value is True:
            return BoolVal(True)
        elif node.value is False:
            return BoolVal(False)
        elif isinstance(node.value, int):
            return IntVal(node.value)
        elif isinstance(node.value, str):
            return StringVal(node.value)
        else:
            raise NotImplementedError(f"NameConstant {node.value} not implemented.")
