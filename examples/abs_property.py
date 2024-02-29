from lslpy.contracts import contract, check_contract
from lslpy.contracts.derived import Integer, Natural, true
from lslpy.contracts.primitives import Function


@contract(Function(arguments=(Integer(),), result=Natural()))
def my_abs(x):
    if x < 0:
        return -x
    else:
        return x


check_contract(my_abs)


@contract(Function(arguments=(Integer(),), result=true()))
def my_abs_prop(x):
    res = my_abs(x)
    return res >= x


check_contract(my_abs_prop)
