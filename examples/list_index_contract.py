from lslpy.contracts import contract, check_contract

from lslpy.contracts.aliases import  List, Integer, OneOf, Natural, Constant


@contract
def my_list_index(lst: List[Integer], value: Integer) -> OneOf[Natural, Constant[False]]:
    if value in lst:
        return lst.index(value)
    else:
        return False

@contract
def my_list_index_prop(lst: List[Integer], value: Integer) -> Constant[True]:
    res = my_list_index(lst, value)
    if value in lst and lst[res] == value:
        return True
    else:
        return not res

check_contract(my_list_index_prop)




