import random
from lslpy import contract, check_contract
from lslpy.contracts import  Natural, Real
from lslpy.contracts.primitives import  Immediate


@contract(raises=ZeroDivisionError)
def divide(x: Natural, y: Natural) -> Real:
    return x / y


check_contract(divide) 

NonZeroInt = Immediate(
    check=lambda x: isinstance(x, int) and x != 0,
    generate=lambda fuel: random.choice(list(range(1, fuel)) + list(range(-fuel, 0))),
)


@contract
def divide_safe(x: Natural, y: NonZeroInt) -> Real:
    return x / y


check_contract(divide_safe)
