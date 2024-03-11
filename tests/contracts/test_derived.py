import unittest

from lslpy.contracts.aliases import Any, Boolean, Integer, Natural, Real, String


class TestDerivedContracts(unittest.TestCase):

    def test_boolean(self):
        self.assertTrue(Boolean.check(True))
        self.assertTrue(Boolean.check(False))
        self.assertFalse(Boolean.check(1))
        self.assertFalse(Boolean.check(1.0))
        self.assertFalse(Boolean.check("False"))

    def test_natural(self):
        self.assertTrue(Natural.check(1))
        self.assertFalse(Natural.check(-1))
        self.assertFalse(Natural.check(1.5))
        self.assertTrue(Natural.generate(1) >= 0)

    def test_integer(self):
        self.assertTrue(Integer.check(1))
        self.assertTrue(Integer.check(-1))
        self.assertFalse(Integer.check(1.5))
        self.assertFalse(Integer.check(False))
        self.assertFalse(Integer.check(True))
        self.assertTrue(isinstance(Integer.generate(1), int))

    def test_real(self):
        self.assertTrue(Real.check(1.5))
        self.assertFalse(Real.check(1))
        self.assertFalse(Real.check("1.5"))
        self.assertTrue(isinstance(Real.generate(1), float))

    def test_string(self):
        self.assertTrue(String.check("test"))
        self.assertFalse(String.check(1))
        self.assertFalse(String.check(1.0))
        self.assertFalse(String.check(True))

    def test_any(self):
        self.assertTrue(Any.check(True))
        self.assertTrue(Any.check(False))
        self.assertTrue(Any.check(-1))
        self.assertTrue(Any.check(1))
        self.assertTrue(Any.check(1.0))
        self.assertTrue(Any.check("hello"))
        Any.generate(100)


if __name__ == "__main__":
    unittest.main()
