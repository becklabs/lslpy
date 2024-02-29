
from .primitives import Function, Immediate

class contract:
    """
    Decorates a python function to impose a contract
    """
    def __init__(self, function_contract: Function):
        self.contract = function_contract

    def __call__(self, val: callable):
        self.contract.visit(val)
        return self.contract