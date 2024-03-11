from .base import Contract


def format_contract(c: Contract):
    from .derived import _Constant
    from .primitives import _Function, _List, _Tuple, _OneOf, _AllOf

    if isinstance(c, _Function):
        return f"({', '.join([format_contract(arg) for arg in c.arguments])}) -> {format_contract(c.result)}"

    elif isinstance(c, _List):
        return f"List({format_contract(c.contract)})"

    elif isinstance(c, _Tuple):
        return f"Tuple({', '.join([format_contract(arg) for arg in c.contracts])})"

    elif isinstance(c, _OneOf):
        return f"OneOf({', '.join([format_contract(arg) for arg in c.disjuncts])})"

    elif isinstance(c, _AllOf):
        return f"AllOf({', '.join([format_contract(arg) for arg in c.conjuncts])})"

    elif isinstance(c, _Constant):
        return f"Constant({str(c.value)})"

    else:
        return c.__class__.__name__


def format_func(func: callable):
    func_name = str(func)
    start = func_name.find("function ") + len("function ")
    end = func_name.find(" at")
    return func_name[start:end]


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
