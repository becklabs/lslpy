from lslpy.contracts import contract, check_contract
from lslpy.contracts.derived import String, Natural
from lslpy.contracts.primitives import Function

@contract(Function(arguments=(String(),), result=Natural()))
def string_length(s):
    return len(s)

check_contract(string_length)