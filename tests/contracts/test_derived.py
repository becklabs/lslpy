import unittest

from lslpy.contracts.derived import (Boolean, Integer, Natural, Real, String,
                                     false, true, Any)


class TestDerivedContracts(unittest.TestCase):
    def test_true(self):
        contract = true()
        self.assertTrue(contract.check(True))
        self.assertFalse(contract.check(False))
        self.assertEqual(contract.generate(0), True)

    def test_false(self):
        contract = false()
        self.assertTrue(contract.check(False))
        self.assertFalse(contract.check(True))
        self.assertEqual(contract.generate(0), False)

    def test_boolean(self):
        contract = Boolean()
        self.assertTrue(contract.check(True))
        self.assertTrue(contract.check(False))
        self.assertFalse(contract.check(1))

    def test_natural(self):
        contract = Natural()
        self.assertTrue(contract.check(1))
        self.assertFalse(contract.check(-1))
        self.assertFalse(contract.check(1.5))

    def test_integer(self):
        contract = Integer()
        self.assertTrue(contract.check(1))
        self.assertTrue(contract.check(-1))
        self.assertFalse(contract.check(1.5))

    def test_real(self):
        contract = Real()
        self.assertTrue(contract.check(1.5))
        self.assertFalse(contract.check(1))
        self.assertFalse(contract.check("1.5"))

    def test_string(self):
        contract = String()
        self.assertTrue(contract.check("test"))
        self.assertFalse(contract.check(1))
        self.assertFalse(contract.check(True))
    
    def test_any(self):
        contract = Any()
        self.assertTrue(contract.check(True))
        self.assertTrue(contract.check(False))
        self.assertTrue(contract.check(-1))
        self.assertTrue(contract.check(1))
        self.assertTrue(contract.check(1.0))
        self.assertTrue(contract.check("hello"))
        contract.generate(100)


if __name__ == "__main__":
    unittest.main()