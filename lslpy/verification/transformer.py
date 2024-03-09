import inspect
import ast

from z3 import And, IntVal, BoolVal, Or, String, If

class Z3Transformer(ast.NodeVisitor):
    def __init__(self, global_vars: dict, local_vars: dict, depth: int = 0):
        print("Initializing Z3Transformer...")
        self.global_vars = global_vars
        self.local_vars = local_vars
        self.depth = depth
        print("Z3Transformer initialized with local_vars:", self.local_vars, "depth:", self.depth)

    def visit_Module(self, node):
        print("Visiting Module...")
        result = self.visit(node.body[0])
        print("Module visited, result:", result)
        return result

    def visit_Expr(self, node):
        print("Visiting Expr...")
        result = self.visit(node.value)
        print("Expr visited, result:", result)
        return result
    
    def visit_Return(self, node):
        print("Visiting Return...")
        result = self.visit(node.value)
        print("Return visited, result:", result)
        return result
    
    def visit_FunctionDef(self, node):
        print("Visiting FunctionDef...")
        func_def = self.global_vars[node.name].func
        annotations = inspect.get_annotations(func_def)
        result = annotations.pop("return")
        local_vars = {name: contract.symbolic(name) for name, contract in annotations.items()}
        for name, value in local_vars.items():
            self.local_vars[name] = value
        print("FunctionDef visited, local_vars updated:", self.local_vars, "return set", result.symbolic())
        return self.visit(node.body[0]) == result.symbolic()
    
    def visit_Call(self, node):
        print("Visiting Call...")
        # Retrieve the function definition from the global environment
        func_def = ast.parse(inspect.getsource(self.global_vars[node.func.id].func))

        new_env = {}
        for arg, param in zip(node.args, func_def.body[0].args.args):
            symbolic_arg = self.visit(ast.parse(arg))
            new_env[param.arg] = symbolic_arg
        print("Call visited, new environment created:", new_env)

        # Visit the body of the function with the new environment (supporting single expression funcs for now)
        return Z3Transformer(global_vars=self.global_vars, local_vars=new_env, depth = self.depth + 1).visit(func_def.body[0].body[0])

    def visit_BinOp(self, node):
        print("Visiting BinOp...")
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast.Add):
            print("BinOp visited, operation: addition")
            return left + right
        elif isinstance(node.op, ast.Sub):
            print("BinOp visited, operation: subtraction")
            return left - right
        elif isinstance(node.op, ast.Mult):
            print("BinOp visited, operation: multiplication")
            return left * right
        elif isinstance(node.op, ast.Div):
            print("BinOp visited, operation: division")
            return left / right
        else:
            raise NotImplementedError(f"Operation {type(node.op)} not implemented.")

    def visit_Num(self, node):
        print("Visiting Num...")
        result = IntVal(node.n)
        print("Num visited, result:", result)
        return result  
    
    def visit_Str(self, node):
        print("Visiting Str...")
        result = String(node.s)
        print("Str visited, result:", result)
        return result

    def visit_Name(self, node):
        print("Visiting Name...")
        if node.id not in self.local_vars:
            raise ValueError(f"Variable {node.id} not define in local_vars")
        result = self.local_vars[node.id]
        print("Name visited, result:", result)
        return result

    def visit_IfExp(self, node):
        print("Visiting IfExp...")
        test = self.visit(node.test)
        body = self.visit(node.body)
        orelse = self.visit(node.orelse)
        result = If(test, body, orelse)
        print("IfExp visited, result:", result)
        return result

    def visit_Compare(self, node):
        print("Visiting Compare...")
        if len(node.ops) != 1 or len(node.comparators) != 1:
            raise NotImplementedError("Complex comparisons not implemented.")
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        if isinstance(node.ops[0], ast.Eq):
            result = left == right
            print(f"Compare visited, operation: equality, left: {left}, right: {right}, result: {result}")
            return result
        elif isinstance(node.ops[0], ast.NotEq):
            result = left != right
            print(f"Compare visited, operation: inequality, left: {left}, right: {right}, result: {result}")
            return result
        elif isinstance(node.ops[0], ast.Lt):
            result = left < right
            print(f"Compare visited, operation: less than, left: {left}, right: {right}, result: {result}")
            return result
        elif isinstance(node.ops[0], ast.LtE):
            result = left <= right
            print(f"Compare visited, operation: less than or equal to, left: {left}, right: {right}, result: {result}")
            return result
        elif isinstance(node.ops[0], ast.Gt):
            result = left > right
            print(f"Compare visited, operation: greater than, left: {left}, right: {right}, result: {result}")
            return result
        elif isinstance(node.ops[0], ast.GtE):
            result = left >= right
            print(f"Compare visited, operation: greater than or equal to, left: {left}, right: {right}, result: {result}")
            return result
        else:
            raise NotImplementedError(f"Comparison {type(node.ops[0])} not implemented.")
    
    def visit_BoolOp(self, node):
        print("Visiting BoolOp...")
        if len(node.values) != 2:
            raise NotImplementedError("Complex boolean operations not implemented.")
        left = self.visit(node.values[0])
        right = self.visit(node.values[1])
        if isinstance(node.op, ast.And):
            print("BoolOp visited, operation: AND")
            return And(left, right)
        elif isinstance(node.op, ast.Or):
            print("BoolOp visited, operation: OR")
            return Or(left, right)
        else:
            raise NotImplementedError(f"Boolean operation {type(node.op)} not implemented.")
    
    def visit_NameConstant(self, node):
        print("Visiting NameConstant...")
        if node.value is True:
            print("NameConstant visited, value: True")
            return BoolVal(True)
        elif node.value is False:
            print("NameConstant visited, value: False")
            return BoolVal(False)
        else:
            raise NotImplementedError(f"NameConstant {node.value} not implemented.")