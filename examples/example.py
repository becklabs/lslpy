from lslpy.contracts import contract
from lslpy.contracts.derived import (Boolean, Constant, Integer, Natural, Real,
                                     String, false, true)
from lslpy.contracts.primitives import AllOf, Function, List, OneOf, Tuple


@contract(Function(arguments=(Natural(), Natural()), result=Natural(), raises=IndexError))
def add(x, y):
    return x + y


print(add(1, 2)) # Good

print(add(1, -2)) # Contract violation

