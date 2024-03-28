from .base import Contract
from .util import format_contract, format_func

class ContractViolation(Exception):
    def __init__(self, message="Contract violation"):
        self.message = message
        super().__init__(self.message)
    
    @classmethod
    def from_invalid_args(cls, func: callable, call_args: list, call_contracts: list[Contract]) -> str:
        message = f"{format_func(func)} expected ({', '.join([format_contract(c) for c in call_contracts])}), got ({', '.join(map(str, call_args))})"
        return cls(message)
    
    @classmethod
    def from_invalid_return(cls, func: callable, func_result: any, result_contract: Contract):
        message = f"{format_func(func)} returned {func_result}, expected {format_contract(result_contract)}"
        return cls(message)

    @classmethod
    def from_invalid_exception(cls, func: callable, exc: any, expected_exc: Contract):
        message = f"{format_func(func)} returned {exc}, expected {expected_exc}"
        return cls(message)

    


class GenerateError(Exception):
    def __init__(self, contract) -> None:
        self.message = f"Cannot generate {contract}"
        super().__init__(self.message)
