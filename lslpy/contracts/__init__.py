import inspect
from .base import Contract
from .primitives import _Function
from .aliases import Callable
from .exceptions import ContractViolation

CHECK_CONTRACT_FUEL = 100


def contract(raises: BaseException):
    """
    Decorates a python function to impose a contract
    """
    func_or_raises = raises
    return_wrapper = inspect.isclass(func_or_raises) and issubclass(func_or_raises, BaseException)

    def wrapper(function: callable):
        annotations = inspect.get_annotations(function)
        result = annotations.pop("return")
        arguments = tuple(annotations.values())
        function_contract = _Function(arguments=arguments, result=result, raises=func_or_raises if return_wrapper else None)
        function_contract.visit(function)
        return function_contract
    
    if return_wrapper:
        return wrapper
    else:
        return wrapper(func_or_raises)


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
