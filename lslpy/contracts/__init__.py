
from .primitives import Function, Immediate
from .exceptions import ContractViolation

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

def check_contract(id: Function, maybe_attempts: int = 100):
    for _ in range(maybe_attempts):
        args = [arg.generate(CHECK_CONTRACT_FUEL) for arg in id.arguments]
        id(*args)


