from lslpy.contracts import contract, check_contract
from lslpy.contracts.primitives import Function, OneOf, List
from lslpy.contracts.derived import Integer, Constant, Natural, true


@contract(
    Function(
        arguments=(List(Integer()), Integer()), result=OneOf(Natural(), Constant(False))
    )
)
def my_list_index(lst, value):
    if value in lst:
        return lst.index(value)
    else:
        return False

@contract(
    Function(
        arguments=(List(Integer()), Integer()), result=true())
)
def my_list_index_prop(lst, value):
    res = my_list_index(lst, value)
    if value in lst and lst[res] == value:
        return True
    else:
        return not res

check_contract(my_list_index_prop)




