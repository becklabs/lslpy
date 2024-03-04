from lslpy.contracts import contract, check_contract

from lslpy.contracts.aliases import Callable, Any, List, String, Integer, Boolean


@contract()
def general_map(f: Callable[[Any], Any], lst: List) -> List:
    res = []
    for e in lst:
        res.append(f(e))
    return res


check_contract(general_map)


@contract()
def string_to_int_map(f: Callable[[String], Integer], lst: List[String]) -> List[Integer]:
    res = []
    for e in lst:
        res.append(f(e))
    return res


check_contract(string_to_int_map)


@contract()
def integer_filter(f: Callable[[Integer], Boolean], lst: List[Integer]) -> List[Integer]:
    res = []
    for e in lst:
        if f(e):
            res.append(e)
    return res


check_contract(integer_filter)


@contract()
def fold_int(f: Callable[[Integer, Integer], Integer], acc: Integer, lst: List[Integer]) -> Integer:
    for e in lst:
        acc = f(e, acc)
    return acc


check_contract(fold_int)
