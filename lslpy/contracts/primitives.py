import random

from .base import Contract
from .exceptions import ContractViolation, GenerateError
from .util import format_contract


class Immediate(Contract):
    def __init__(
        self,
        check: callable,
        generate: callable,
    ):
        self.check = check
        self.generate = generate

    def check(self, x) -> bool:
        return self.check(x)

    def generate(self, fuel):
        return self.generate(fuel)


class Function(Contract):
    def __init__(
        self, arguments: tuple[Contract], result: Contract, raises: BaseException | None = None
    ):
        self.arguments = arguments
        self.result = result
        self.raises = raises
        self.func: callable | None = None

    def visit(self, func: callable):
        self.func = func

    def __call__(self, *args):
        # TODO: Implement support for keyword args
        for arg, contract in zip(args, self.arguments):
            if not contract.check(arg):
                # TODO: Improve contract violation messages
                raise ContractViolation(f"{self.func} expected ({', '.join([format_contract(c) for c in self.arguments])}), got ({', '.join(args)})")
        try:
            result = self.func(*args)
            if not self.result.check(result):
                raise ContractViolation(f"{self.func} returned {result}, expected {format_contract(self.result)}")


        except Exception as e:
            if self.raises is not None and not isinstance(e, self.raises):
                raise ContractViolation(f"{self.func} returned {e}, expected {self.raises}") from e
            else:
                raise e

        return result

    def check(self, x):
        self.visit(x)
        return True

    def generate(self, fuel):
        return lambda *args: self.result.generate(fuel)
    

class List(Contract):
    def __init__(self, contract):
        self.contract = contract

    def check(self, x):
        # TODO: decide whether to check if type == list here
        return all([self.contract.check(e) for e in x])

    def generate(self, fuel):
        return [self.contract.generate(fuel) for _ in range(fuel)]


class Tuple(Contract):
    def __init__(self, *contracts):
        self.contracts = contracts

    def check(self, x):
        return all([contract.check(e) for e, contract in zip(x, self.contracts)])

    def generate(self, fuel):
        return (contract.generate(fuel) for contract in self.contracts)


class OneOf(Contract):
    def __init__(self, *disjuncts):
        self.disjuncts = disjuncts

    def check(self, x):
        return any([contract.check(x) for contract in self.disjuncts])

    def generate(self, fuel):
        return random.choice(self.disjuncts).generate(fuel)


class AllOf(Contract):
    def __init__(self, *conjuncts):
        self.conjuncts = conjuncts

    def check(self, x):
        return all([contract.check(x) for contract in self.conjuncts])

    def generate(self, fuel):
        for _ in range(fuel):
            x = random.choice(self.conjuncts).generate(fuel)
            if all([contract.check(x) for contract in self.conjuncts]):
                return x
            raise GenerateError(f"AllOf({' '.join([str(i) for i in self.conjuncts])})")

class Struct(Contract): ...


class All(Contract): ...


class Exists(Contract): ...
