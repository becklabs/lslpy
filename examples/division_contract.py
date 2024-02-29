import random
from lslpy.contracts import contract, check_contract
from lslpy.contracts.derived import Natural, Real
from lslpy.contracts.primitives import Function, Immediate

@contract(Function(arguments=(Natural(), Natural()), result=Real(), raises=ZeroDivisionError))
def divide(x, y):
    return x / y

# check_contract(divide) # No contract violations but throws an error

NonZeroInt = Immediate(
    check=lambda x: isinstance(x, int) and x > 0,
    generate=lambda fuel: random.randint(1, fuel)
)

@contract(Function(arguments=(Natural(), NonZeroInt), result=Real()))
def divide_safe(x, y):
    return x / y

check_contract(divide_safe)
