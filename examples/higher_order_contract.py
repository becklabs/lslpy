from lslpy.contracts import contract, check_contract
from lslpy.contracts.primitives import Function, List
from lslpy.contracts.derived import Any, String, Integer, Boolean


@contract(
    Function(
        arguments=(Function(arguments=[Any()], result=Any()), List()), result=List()
    )
)
def general_map(f, lst):
    res = []
    for e in lst:
        res.append(f(e))
    return res


check_contract(general_map)


@contract(
    Function(
        arguments=[Function(arguments=[String()], result=Integer()), List(String())],
        result=List(Integer()),
    )
)
def string_to_int_map(f, lst):
    res = []
    for e in lst:
        res.append(f(e))
    return res


check_contract(string_to_int_map)


@contract(
    Function(
        arguments=(Function(arguments=[Integer()], result=Boolean()), List(Integer())),
        result=List(Integer()),
    )
)
def integer_filter(f, lst):
    res = []
    for e in lst:
        if f(e):
            res.append(e)
    return res


check_contract(integer_filter)


@contract(
    Function(
        arguments=(
            Function(arguments=(Integer(), Integer()), result=Integer()),
            Integer(),
            List(Integer()),
        ),
        result=Integer(),
    )
)
def fold_int(f, acc, lst):
    for e in lst:
        acc = f(e, acc)
    return acc


check_contract(fold_int)
