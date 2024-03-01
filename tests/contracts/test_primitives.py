import unittest

from lslpy.contracts.derived import Boolean, Integer, Natural, true
from lslpy.contracts.primitives import (AllOf, Function, Immediate, List,
                                        OneOf, Tuple)


class TestPrimitiveContracts(unittest.TestCase):
    def test_immediate(self):
        contract = Immediate(check=lambda x: x is True, generate=lambda fuel: True)
        self.assertTrue(contract.check(True))
        self.assertFalse(contract.check(False))
        self.assertEqual(contract.generate(0), True)

    def test_function(self):
        contract = Function(arguments=(Boolean(),), result=true())
        contract.visit(lambda x: x)
        self.assertTrue(contract(True))
        with self.assertRaises(Exception):
            contract(False)

    def test_list(self):
        contract = List(Natural())
        self.assertTrue(contract.check([1, 2, 3]))
        self.assertFalse(contract.check([1, -2, 3]))

    def test_tuple(self):
        contract = Tuple(Natural(), Boolean())
        self.assertTrue(contract.check((1, True)))
        self.assertFalse(contract.check((1, 2)))

    def test_oneof(self):
        contract = OneOf(Natural(), Boolean())
        self.assertTrue(contract.check(1))
        self.assertTrue(contract.check(True))
        self.assertFalse(contract.check("string"))

    def test_allof(self):
        contract = AllOf(Natural(), Integer())
        self.assertTrue(contract.check(1))
        self.assertFalse(contract.check(-1))


if __name__ == "__main__":
    unittest.main()
