import unittest

from lslpy.contracts.aliases import (
    AllOf,
    Boolean,
    Callable,
    Constant,
    Integer,
    List,
    Natural,
    OneOf,
    Tuple,
)
from lslpy.contracts.exceptions import ContractViolation, GenerateError
from lslpy.contracts.primitives import Immediate


class TestPrimitiveContracts(unittest.TestCase):
    def test_immediate(self):
        contract = Immediate(check=lambda x: x is True, generate=lambda fuel: True)
        self.assertTrue(contract.check(True))
        self.assertFalse(contract.check(False))
        self.assertEqual(contract.generate(0), True)

    def test_function(self):
        contract = Callable[[Boolean], Constant[True]]
        contract.visit(lambda x: x)
        self.assertTrue(contract(True))
        with self.assertRaises(ContractViolation):
            contract(False)

        with self.assertRaises(ContractViolation):
            contract(True, True)
        
        generated_func = contract.generate(0)
        self.assertTrue(generated_func(True))
        self.assertTrue(generated_func(False))

        # Wrong argument contract
        with self.assertRaises(ContractViolation):
            generated_func(1)

        # Wrong number of arguments
        with self.assertRaises(ContractViolation):
            generated_func(False, False)
        

    def test_list(self):
        contract = List[Natural]
        self.assertTrue(contract.check([1, 2, 3]))
        self.assertFalse(contract.check([1, -2, 3]))

    def test_tuple(self):
        contract = Tuple[Natural, Boolean]
        self.assertTrue(contract.check((1, True)))
        self.assertFalse(contract.check((1, 2)))

    def test_oneof(self):
        contract = OneOf[Natural, Boolean]
        self.assertTrue(contract.check(1))
        self.assertTrue(contract.check(True))
        self.assertFalse(contract.check("string"))

    def test_allof(self):
        contract = AllOf[Natural, Integer]
        contract2 = AllOf[Natural, Constant[-1]]
        self.assertTrue(contract.check(1))
        self.assertFalse(contract.check(-1))
        with self.assertRaises(GenerateError):
            contract2.generate(100)


if __name__ == "__main__":
    unittest.main()
