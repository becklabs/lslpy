from .base import Contract

def format_contract(c: Contract):
    from .derived import Constant
    from .primitives import Function, List, Tuple, OneOf, AllOf
    if isinstance(c, Function):
        return f"({', '.join([format_contract(arg) for arg in c.arguments])}) -> {format_contract(c.result)}"

    elif isinstance(c, List):
        return f"List({format_contract(c.contract)})"

    elif isinstance(c, Tuple):
        return f"Tuple({', '.join([format_contract(arg) for arg in c.contracts])})"
    
    elif isinstance(c, OneOf):
        return f"OneOf({', '.join([format_contract(arg) for arg in c.disjuncts])})"

    elif isinstance(c, AllOf):
        return f"AllOf({', '.join([format_contract(arg) for arg in c.conjuncts])})"

    elif isinstance(c, Constant):
        return f"Constant({str(c.value)})"
    
    else:
        return c.__class__.__name__

