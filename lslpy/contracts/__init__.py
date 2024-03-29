import inspect
import typing

from .aliases import *
from .base import Contract
from .exceptions import ContractViolation
from .primitives import _Function
from .util import format_func

CHECK_CONTRACT_FUEL = 100


def contract(
    func: typing.Union[callable, None] = None,
    raises: BaseException | None = None,
    enabled: bool = True,
):
    """
    Decorates a python function to impose a contract
    """

    def wrapper(function: callable):
        arg_info = inspect.getfullargspec(function)
        annotations = {
            arg: arg_info.annotations.get(arg, None)
            for arg in arg_info.args + ["return"]
        }
        partial = not all(annotations.values())
        annotations = {
            arg: annotations[arg] if arg is not None else Any
            for arg in annotations
        }

        result = annotations.pop("return")
        function_contract = _Function(
            kwargs=annotations, result=result, raises=raises, enabled=enabled, partial=partial
        )
        function_contract.visit(function)
        return function_contract

    if func is not None:
        assert callable(func)
        return wrapper(func)
    else:
        return wrapper


def check_contract(func: Callable, attempts: int = 100):
    if func.partial:
        raise ValueError(f"Cannot check partial contract: {format_func(func.func)}")
    for _ in range(attempts):
        args = [arg.generate(CHECK_CONTRACT_FUEL) for arg in func.arg_contracts]
        try:
            func(*args)
        except Exception as e:
            if func.raises is not None and isinstance(e, func.raises):
                continue
            elif isinstance(e, ContractViolation):
                raise ContractViolation(
                    f"Found counterexample: {format_func(func.func)}({', '.join([str(a) for a in args])})"
                ) from e
            else:
                raise e


def contract_generate(c: Contract, fuel: int):
    return c.generate(fuel)
