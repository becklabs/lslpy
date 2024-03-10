import textwrap
import unittest
from lslpy.verification.transformer import Z3Transformer
from lslpy.contracts.aliases import Integer, Constant
from lslpy.contracts import contract
import ast
import inspect
import z3


def get_value(node: ast.Module):
    return node.body[0].value


def evaluate(expr, variables):
    s = z3.Solver()
    s.add(expr)
    for name, val in variables.items():
        s.add(name == val)
    return s.check() == z3.sat


class TestZ3Transformer(unittest.TestCase):

    def setUp(self):
        self.global_vars = {}
        self.local_vars = {}
        self.transformer = Z3Transformer(self.global_vars, self.local_vars)

    def test_visit_Module(self):
        tree = ast.parse("False")
        result = self.transformer.visit_Module(tree)
        self.assertEqual(result, z3.BoolVal(False))

    def test_visit_Expr(self):
        tree = ast.parse("False").body[0]
        result = self.transformer.visit_Expr(tree)
        self.assertEqual(result, z3.BoolVal(False))

    def test_visit_Return(self):
        x = z3.Int("x")

        @contract
        def foo(x: Integer) -> Constant[1]:
            return x

        tree = (
            ast.parse(textwrap.dedent(inspect.getsource(foo.func))).body[0].body[0]
        )  # get the return statement

        transformer = Z3Transformer(local_vars={"x": x}, global_vars={"foo": foo})
        result = transformer.visit_Return(tree)
        self.assertEqual(result, x)

        with self.assertRaises(ValueError):
            transformer = Z3Transformer(local_vars={}, global_vars={"foo": foo})
            result = transformer.visit_Return(tree)

    def test_visit_FunctionDef(self):
        x = z3.Int("x")
        y = z3.Int("y")

        @contract
        def foo(x: Integer, y: Integer) -> Constant[1]:
            return x + y

        transformer = Z3Transformer(local_vars={}, global_vars={"foo": foo})
        tree = ast.parse(textwrap.dedent(inspect.getsource(foo.func))).body[0]

        result = transformer.visit_FunctionDef(tree)  # x + y == 1
        self.assertTrue(evaluate(result, {x: 1, y: 0}))
        self.assertTrue(evaluate(result, {x: 0, y: 1}))
        self.assertFalse(evaluate(result, {x: 1, y: 1}))

        @contract
        def bar(x: Integer) -> Constant[True]:
            return foo(x, x) == x**2

        transformer = Z3Transformer(local_vars={}, global_vars={"foo": foo, "bar": bar})

        tree = ast.parse(textwrap.dedent(inspect.getsource(bar.func))).body[0]

        result = transformer.visit_FunctionDef(tree)  # (x + x == x ** 2) == True
        self.assertTrue(evaluate(result, {x: 2}))
        self.assertFalse(evaluate(result, {x: 3}))

        def uncontracted_bar(x: Integer) -> Constant[True]:
            return foo(x, x) == x**2

        @contract
        def multi_expr_bar(x: Integer) -> Constant[True]:
            result = foo(x, x) == x**2
            return result

        # Test that functions without contracts are not allowed
        with self.assertRaises(ValueError):
            transformer = Z3Transformer(
                local_vars={},
                global_vars={"foo": foo, "uncontracted_bar": uncontracted_bar},
            )
            tree = ast.parse(textwrap.dedent(inspect.getsource(uncontracted_bar))).body[
                0
            ]
            transformer.visit_FunctionDef(tree)

        # Test that multi-expression functions are not allowed
        with self.assertRaises(NotImplementedError):
            transformer = Z3Transformer(
                local_vars={},
                global_vars={"foo": foo, "multi_expr_bar": multi_expr_bar},
            )
            tree = ast.parse(
                textwrap.dedent(inspect.getsource(multi_expr_bar.func))
            ).body[0]
            transformer.visit_FunctionDef(tree)

    def test_visit_Call(self):
        def foo(x, y):
            return x + y

        transformer = Z3Transformer(local_vars={}, global_vars={"foo": foo})

        tree = get_value(ast.parse("foo(1, 2)"))
        result = transformer.visit_Call(tree)
        self.assertEqual(result, z3.IntVal(1) + z3.IntVal(2))

        # Test that variables are being correctly substituted
        x = z3.Int("x")
        y = z3.Int("y")
        transformer = Z3Transformer(
            local_vars={"x": x, "y": y}, global_vars={"foo": foo}
        )

        tree = get_value(ast.parse("foo(x + 1, y)"))
        result = transformer.visit_Call(tree)
        self.assertEqual(result, x + 1 + y)

        # Test that we can parse a function decorated with a contract
        @contract
        def contracted_foo(x: Integer, y: Integer) -> Integer:
            return x + y

        transformer = Z3Transformer(
            local_vars={}, global_vars={"contracted_foo": contracted_foo}
        )

        tree = get_value(ast.parse("contracted_foo(1, 2)"))
        result = transformer.visit_Call(tree)
        self.assertEqual(result, z3.IntVal(1) + z3.IntVal(2))

        def bar(x, y):
            res = x + y
            return res

        transformer = Z3Transformer(local_vars={}, global_vars={"bar": bar})

        # Test that multi-expression functions are not allowed
        with self.assertRaises(NotImplementedError):
            tree = get_value(ast.parse("bar(1, 2)"))
            transformer.visit_Call(tree)

    def test_visit_BinOp(self):
        x = z3.Int("x")
        y = z3.Int("y")
        transformer = Z3Transformer(local_vars={"x": x, "y": y}, global_vars={})

        tree = get_value(ast.parse("x + y"))
        result = transformer.visit_BinOp(tree)
        self.assertEqual(result, x + y)

        tree = get_value(ast.parse("x - y"))
        result = transformer.visit_BinOp(tree)
        self.assertEqual(result, x - y)

        tree = get_value(ast.parse("x * y"))
        result = transformer.visit_BinOp(tree)
        self.assertEqual(result, x * y)

        tree = get_value(ast.parse("x / y"))
        result = transformer.visit_BinOp(tree)
        self.assertEqual(result, x / y)

        with self.assertRaises(NotImplementedError):
            tree = get_value(ast.parse("x @ y"))
            transformer.visit_BinOp(tree)

    def test_visit_Name(self):
        x = z3.Int("x")
        y = z3.Int("y")
        transformer = Z3Transformer(local_vars={"x": x, "y": y}, global_vars={})
        tree = get_value(ast.parse("x"))
        result = transformer.visit_Name(tree)
        self.assertEqual(result, x)

    def test_visit_IfExp(self):
        x = z3.Int("x")
        y = z3.Int("y")
        transformer = Z3Transformer(local_vars={"x": x, "y": y}, global_vars={})
        tree = get_value(ast.parse("x if x > y else y"))
        result = transformer.visit_IfExp(tree)
        self.assertEqual(result, z3.If(x > y, x, y))

    def test_visit_Compare(self):
        x = z3.Int("x")
        y = z3.Int("y")
        transformer = Z3Transformer(local_vars={"x": x, "y": y}, global_vars={})
        eq_tree = get_value(ast.parse("x == y"))
        eq_result = transformer.visit_Compare(eq_tree)
        self.assertEqual(eq_result, x == y)

        noteq_tree = get_value(ast.parse("x != y"))
        noteq_result = transformer.visit_Compare(noteq_tree)
        self.assertEqual(noteq_result, x != y)

        lt_tree = get_value(ast.parse("x < y"))
        lt_result = transformer.visit_Compare(lt_tree)
        self.assertEqual(lt_result, x < y)

        lte_tree = get_value(ast.parse("x <= y"))
        lte_result = transformer.visit_Compare(lte_tree)
        self.assertEqual(lte_result, x <= y)

        gt_tree = get_value(ast.parse("x > y"))
        gt_result = transformer.visit_Compare(gt_tree)
        self.assertEqual(gt_result, x > y)

        gte_tree = get_value(ast.parse("x >= y"))
        gte_result = transformer.visit_Compare(gte_tree)
        self.assertEqual(gte_result, x >= y)

        with self.assertRaises(NotImplementedError):
            tree = get_value(ast.parse("x is y"))
            transformer.visit_Compare(tree)

        with self.assertRaises(NotImplementedError):
            tree = get_value(ast.parse("x > y > x"))
            transformer.visit_Compare(tree)

    def test_visit_BoolOp(self):
        x = z3.Bool("x")
        y = z3.Bool("y")
        transformer = Z3Transformer(local_vars={"x": x, "y": y}, global_vars={})
        or_tree = get_value(ast.parse("x or y"))
        or_result = transformer.visit_BoolOp(or_tree)
        self.assertEqual(or_result, z3.Or(x, y))

        and_tree = get_value(ast.parse("x and y"))
        and_result = transformer.visit_BoolOp(and_tree)
        self.assertEqual(and_result, z3.And(x, y))

        with self.assertRaises(NotImplementedError):
            tree = get_value(ast.parse("x or y or z"))
            transformer.visit_BoolOp(tree)

    def test_visit_Constant(self):
        tree = get_value(ast.parse("False"))
        result = self.transformer.visit_Constant(tree)
        self.assertEqual(result, z3.BoolVal(False))

        tree = get_value(ast.parse("True"))
        result = self.transformer.visit_Constant(tree)
        self.assertEqual(result, z3.BoolVal(True))

        tree = get_value(ast.parse("42"))
        result = self.transformer.visit_Constant(tree)
        self.assertEqual(result, z3.IntVal(42))

        tree = get_value(ast.parse("'hello'"))
        result = self.transformer.visit_Constant(tree)
        self.assertEqual(result, z3.StringVal("hello"))


if __name__ == "__main__":
    unittest.main()
