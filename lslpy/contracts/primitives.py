import random

from .base import Contract
from .exceptions import ContractViolation, GenerateError
from .util import format_contract, is_iterable


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


class _Function(Contract):
    def __init__(
        self,
        arguments: tuple[Contract] | None = None,
        result: Contract | None = None,
        raises: BaseException | None = None,
    ):
        self.arguments = arguments
        self.result = result
        self.raises = raises
        self.func: callable | None = None

    def visit(self, func: callable):
        self.func = func

    def __call__(self, *args, **kwargs):
        args = args + tuple(kwargs.values())
        if self.arguments is not None:
            for arg, contract in zip(args, self.arguments):
                if not contract.check(arg):
                    raise ContractViolation(
                        f"{self.func} expected ({', '.join([format_contract(c) for c in self.arguments])}), got ({', '.join(args)})"
                    )
            try:
                result = self.func(*args)
                if self.result is not None:
                    if not self.result.check(result):
                        raise ContractViolation(
                            f"{self.func} returned {result}, expected {format_contract(self.result)}"
                        )
            except Exception as e:
                if self.raises is not None and not isinstance(e, self.raises):
                    raise ContractViolation(
                        f"{self.func} returned {e}, expected {self.raises}"
                    ) from e
                else:
                    raise e
            return result

    def check(self, x):
        self.visit(x)  # Impose a check later
        return callable(x)

    def generate(self, fuel):
        return lambda *args: self.result.generate(fuel)

    def __getitem__(self, param):
        arguments = param[0]
        result = param[1]
        if len(param) == 3:
            raises = param[2]
        else:
            raises = None
        return _Function(arguments=arguments, result=result, raises=raises)


class _List(Contract):
    def __init__(self, contract: Contract | None = None):
        self.contract = contract

    def check(self, x):
        return is_iterable(x) and (
            self.contract is None or all([self.contract.check(e) for e in x])
        )

    def generate(self, fuel):
        return [self.contract.generate(fuel) for _ in range(random.randint(0, fuel))]

    def __getitem__(self, param: Contract):
        return _List(contract=param)


class _Tuple(Contract):
    def __init__(self, *contracts: Contract | None):
        self.contracts = contracts

    def check(self, x):
        return is_iterable(x) and (
            self.contracts == (None,)
            or all([contract.check(e) for e, contract in zip(x, self.contracts)])
        )

    def generate(self, fuel):
        return (contract.generate(fuel) for contract in self.contracts)

    def __getitem__(self, params: tuple[Contract]):
        return _Tuple(*params)


class _OneOf(Contract):
    def __init__(self, *disjuncts):
        self.disjuncts = disjuncts

    def check(self, x):
        return any([contract.check(x) for contract in self.disjuncts])

    def generate(self, fuel):
        return random.choice(self.disjuncts).generate(fuel)

    def __getitem__(self, params: tuple[Contract]):
        return _OneOf(*params)


class _AllOf(Contract):
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

    def __getitem__(self, params: tuple[Contract]):
        return _AllOf(*params)


class Struct(Contract): ...


class All(Contract): ...


class Exists(Contract): ...
