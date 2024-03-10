from lslpy.contracts import contract
from lslpy import verify_contract
from lslpy.contracts.aliases import Integer, Constant

@contract
def bad_mult(x: Integer, y: Integer) -> Integer:
    return 0 if x == 10456 else (x * y)

@contract
def bad_mult_prop(x: Integer, y: Integer) -> Constant[True]:
    return bad_mult(x, y) == x * y

@contract
def contracted_foo(x: Integer, y: Integer) -> Constant[1]:
    return x + y

verify_contract(contracted_foo, global_vars=globals())


