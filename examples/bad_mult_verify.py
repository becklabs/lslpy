from lslpy import contract, verify_contract
from lslpy.contracts import Integer, Constant

@contract
def bad_mult(x: Integer, y: Integer) -> Integer:
    return 0 if x == 10456 else (x * y)

@contract
def bad_mult_prop(x: Integer, y: Integer) -> Constant[True]:
    return bad_mult(x, y) == x * y

verify_contract(bad_mult_prop, global_vars=globals())


