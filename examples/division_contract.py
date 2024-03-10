import random
from lslpy import contract, check_contract
from lslpy.contracts import  Natural, Real
from lslpy.contracts.primitives import  Immediate


@contract(raises=ZeroDivisionError)
def divide(x: Natural, y: Natural) -> Real:
    return x / y


# check_contract(divide) # No contract violations but throws an error

NonZeroInt = Immediate(
    check=lambda x: isinstance(x, int) and x > 0,
    generate=lambda fuel: random.randint(1, fuel),
)


@contract
def divide_safe(x: Natural, y: NonZeroInt) -> Real:
    return x / y


check_contract(divide_safe)
