
from .base import Contract
from .primitives import Function

CHECK_CONTRACT_FUEL = 100

class contract:
    """
    Decorates a python function to impose a contract
    """
    def __init__(self, function_contract: Function):
        self.contract = function_contract

    def __call__(self, val: callable):
        self.contract.visit(val)
        return self.contract

def check_contract(id: Function, attempts: int = 100):
    for _ in range(attempts):
        args = [arg.generate(CHECK_CONTRACT_FUEL) for arg in id.arguments]
        id(*args)

def contract_generate(id: Contract, fuel: int):
    return id.generate(fuel)



