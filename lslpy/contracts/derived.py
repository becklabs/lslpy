import random
import string

from .primitives import Immediate


class _Constant(Immediate):
    def __init__(self, value):
        super().__init__(check=lambda x: x is value, generate=lambda fuel: value)
        self.value = value

    def __getitem__(self, param):
        return _Constant(param)


class _Boolean(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: _Constant(True).check(x) or _Constant(False).check(x),
            generate=lambda fuel: random.choice(
                [_Constant(True), _Constant(False)]
            ).generate(fuel),
        )


class _Natural(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: isinstance(x, int) and x >= 0,
            generate=lambda fuel: random.randint(0, fuel),
        )


class _Integer(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: isinstance(x, int),
            generate=lambda fuel: random.randint(-fuel, fuel),
        )


class _Real(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: isinstance(x, float),
            generate=lambda fuel: random.uniform(-fuel, fuel),
        )


class _String(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: isinstance(x, str),
            generate=lambda fuel: "".join(
                random.choices(
                    string.ascii_letters + string.digits, k=random.randint(0, fuel)
                )
            ),
        )


class _Any(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: True,
            generate=lambda fuel: random.choice(
                [_Boolean(), _Integer(), _Real(), _Natural(), _String()]
            ).generate(fuel),
        )
