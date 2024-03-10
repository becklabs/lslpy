from lslpy import contract, check_contract
from lslpy.contracts import Integer, Natural, Constant


@contract(raises=BaseException)
def my_abs(x: Integer) -> Natural:
    if x < 0:
        return -x
    else:
        return x


check_contract(my_abs)


@contract
def my_abs_prop(x: Integer) -> Constant[True]:
    res = my_abs(x)
    return res >= x


check_contract(my_abs_prop)
