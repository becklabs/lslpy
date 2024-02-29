from lslpy.contracts import contract, check_contract
from lslpy.contracts.derived import Integer, true
from lslpy.contracts.primitives import Function, List


@contract(Function(arguments=(List(Integer()),), result=List(Integer())))
def my_reverse(l):
    l.reverse()
    return l

check_contract(my_reverse)

@contract(Function(arguments=(List(Integer()), List(Integer())), result=true()))
def my_reverse_prop(l1, l2):
    return my_reverse(l1 + l2) == my_reverse(l2) + my_reverse(l1)

check_contract(my_reverse_prop)
