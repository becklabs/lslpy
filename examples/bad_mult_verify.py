from lslpy.contracts import contract
from lslpy import verify_contract
from lslpy.contracts.aliases import Integer, Constant

@contract
def func(x: Integer, y: Integer) -> Integer:
    return 0 if x == 10456 else (x * y)

@contract
def prop(x: Integer, y: Integer) -> Constant[True]:
    return func(x, y) == x * y

verify_contract(prop, global_vars=globals())


