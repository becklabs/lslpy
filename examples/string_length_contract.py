from lslpy.contracts import contract, check_contract
from lslpy.contracts.aliases import Natural, String

@contract()
def string_length(s: String) -> Natural:
    return len(s)

check_contract(string_length)