import inspect
from .base import Contract
from .primitives import _Function
from .aliases import Callable
from .exceptions import ContractViolation

CHECK_CONTRACT_FUEL = 100


def contract(raises: BaseException | None = None):
    """
    Decorates a python function to impose a contract
    """

    def wrapper(function: callable):
        annotations = inspect.get_annotations(function)
        result = annotations.pop("return")
        arguments = tuple(annotations.values())
        function_contract = _Function(arguments=arguments, result=result, raises=raises)
        function_contract.visit(function)
        return function_contract
    
    return wrapper



def check_contract(func: Callable, attempts: int = 100):
    for _ in range(attempts):
        args = [arg.generate(CHECK_CONTRACT_FUEL) for arg in func.arguments]
        try:
            func(*args)
        except ContractViolation as e:
            raise ContractViolation(
                f"Found counterexample: {func.func}({', '.join([str(a) for a in args])})"
            ) from e


def contract_generate(c: Contract, fuel: int):
    return c.generate(fuel)
