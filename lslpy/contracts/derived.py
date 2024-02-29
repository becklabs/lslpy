import random
import string

from .primitives import Immediate


class Constant(Immediate):
    def __init__(self, value):
        super().__init__(check=lambda x: x is value, generate=lambda fuel: value)


class true(Constant):
    def __init__(self) -> None:
        super().__init__(True)


class false(Constant):
    def __init__(self) -> None:
        super().__init__(False)


class Boolean(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: true().check(x) or false().check(x),
            generate=lambda fuel: random.choice([true(), false()]).generate(fuel),
        )


class Natural(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: isinstance(x, int) and x >= 0,
            generate=lambda fuel: random.randint(0, fuel),
        )


class Integer(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: isinstance(x, int),
            generate=lambda fuel: random.randint(-fuel, fuel),
        )


class Real(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: isinstance(x, float),
            generate=lambda fuel: random.uniform(-fuel, fuel),
        )


class String(Immediate):
    def __init__(self):
        super().__init__(
            check=lambda x: isinstance(x, str),
            generate=lambda fuel: "".join(
                random.choices(string.ascii_letters + string.digits, k=fuel)
            ),
        )
