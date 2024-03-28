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
            arg: arg_info.annotations.get(arg, Any)
            for arg in arg_info.args + ["return"]
        }
        result = annotations.pop("return")
        function_contract = _Function(
            kwargs=annotations, result=result, raises=raises, enabled=enabled
        )
        function_contract.visit(function)
        return function_contract

    if func is not None:
        assert callable(func)
        return wrapper(func)
    else:
        return wrapper


def check_contract(func: Callable, attempts: int = 100):
    for _ in range(attempts):
        args = [arg.generate(CHECK_CONTRACT_FUEL) for arg in func.arg_contracts]
        try:
            func(*args)
        except ContractViolation as e:
            raise ContractViolation(
                f"Found counterexample: {format_func(func.func)}({', '.join([str(a) for a in args])})"
            ) from e


def contract_generate(c: Contract, fuel: int):
    return c.generate(fuel)
