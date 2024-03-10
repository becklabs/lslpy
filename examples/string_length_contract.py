from lslpy import contract, check_contract
from lslpy.contracts import Natural, String

@contract
def string_length(s: String) -> Natural:
    return len(s)

check_contract(string_length)