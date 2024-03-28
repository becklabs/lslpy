import random

from .base import Contract
from .exceptions import ContractViolation, GenerateError
from .util import (
    format_func,
    is_iterable,
)


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
        args: tuple[Contract] | None = None,
        kwargs: dict[str, Contract] | None = None,
        result: Contract | None = None,
        raises: BaseException | None = None,
    ):
        self.args = args
        self.kwargs = kwargs
        if self.args is not None:
            self.arg_contracts = args
        elif self.kwargs is not None:
            self.arg_contracts = tuple(kwargs.values())
        else:
            self.arg_contracts = ()
        self.result = result
        self.raises = raises
        self.func: callable | None = None

    def visit(self, func: callable):
        self.func = func

    def __call__(self, *args, **kwargs):
        call_contracts: list[Contract]
        call_args = args + tuple(kwargs.values())

        # Function was constructed with Callable
        if self.args is not None:
            call_contracts = self.args

        # Function was constructed with @contract decorator
        elif self.kwargs is not None:
            if len(args) > len(self.kwargs):
                raise TypeError(f"{format_func(self.func)}() takes {len(self.kwargs)} positional arguments but {len(args)} were given")
            call_contracts = list(self.kwargs.values())[: len(args)]
            for kwarg in kwargs:
                kwarg_contract = self.kwargs.get(kwarg, None)
                if kwarg_contract is None:
                    raise ValueError(f"Unexpected keyword argument '{kwarg}'")
                call_contracts.append(kwarg_contract)

        else:
            call_contracts = []

        if not (self.args is None and self.kwargs is None):
            if len(call_args) != len(call_contracts):
                raise ContractViolation.from_invalid_args(
                    func=self.func, call_args=call_args, call_contracts=call_contracts
                )

            for arg, contract in zip(call_args, call_contracts):
                if not contract.check(arg):
                    raise ContractViolation.from_invalid_args(
                        func=self.func,
                        call_args=call_args,
                        call_contracts=call_contracts,
                    )

        try:
            result = self.func(*args, **kwargs)
            if self.result is not None:
                if not self.result.check(result):
                    raise ContractViolation.from_invalid_return(
                        func=self.func,
                        func_result=result,
                        result_contract=self.result,
                    )
        except Exception as e:
            if self.raises is not None and not isinstance(e, self.raises):
                raise ContractViolation.from_invalid_exception(
                    func=self.func, exc=e, expected_exc=self.raises
                ) from e
            else:
                raise e
        return result

    def check(self, x):
        self.visit(x)  # Impose a check later
        return callable(x)

    def generate(self, fuel):
        def generated_func(*args, **kwargs):
            return self.result.generate(fuel)

        contract = _Function(
            args=self.args, kwargs=self.kwargs, result=self.result, raises=self.raises
        )
        contract.visit(generated_func)
        return contract

    def __getitem__(self, param):
        arguments = param[0]
        result = param[1]
        if len(param) == 3:
            raises = param[2]
        else:
            raises = None
        return _Function(args=arguments, result=result, raises=raises)


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
