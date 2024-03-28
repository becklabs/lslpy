import unittest
from lslpy import contract, check_contract

from lslpy.contracts.aliases import (
    Constant,
    Integer,
    Real,
    Natural,
)
from lslpy.contracts.exceptions import ContractViolation

class TestContract(unittest.TestCase):

    def test_check_contract(self):

        @contract
        def foo(a: Integer, b: Integer) -> Integer:
            return a + b

        @contract
        def bar(a: Integer, b: Integer) -> Constant[True]:
            if (a + b) % 2 == 0:
                return True
            else:
                return False

        check_contract(foo) 

        with self.assertRaises(ContractViolation):
            check_contract(bar, attempts=1000)
        
    
    def test_contract_raises(self):
        @contract(raises=ZeroDivisionError)
        def foo(x: Natural, y: Natural) -> Real:
            return x / y

        @contract(raises=ZeroDivisionError)
        def bar(x: Natural, y: Natural) -> Real:
            raise ValueError

        check_contract(foo)

        with self.assertRaises(ContractViolation):
            check_contract(bar, attempts=1)
    
    def test_contract_enabled(self):

        @contract(enabled=False)
        def foo() -> Constant[True]:
            return False

        @contract
        def bar() -> Constant[True]:
            return False
        
        check_contract(foo)

        with self.assertRaises(ContractViolation):
            check_contract(bar, attempts=1)

