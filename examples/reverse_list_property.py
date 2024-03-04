from lslpy.contracts import check_contract, contract
from lslpy.contracts.aliases import  List, Integer, Constant


@contract
def my_reverse(l: List[Integer]) -> List[Integer]:
    l.reverse()
    return l


check_contract(my_reverse)


@contract
def my_reverse_prop(l1: List[Integer], l2: List[Integer]) -> Constant[True]:
    return my_reverse(l1 + l2) == my_reverse(l2) + my_reverse(l1)


check_contract(my_reverse_prop)
