# lslpy

`lslpy` is a library that enables contracts, property-based randomized testing, and verification via symbolic execution in Python, inspired by [LSL](https://docs.racket-lang.org/lsl/index.html).

## Installation

lslpy requires `python3.9` or higher.

1. Clone the repository and move into its directory:

```bash
git clone https://github.com/becklabs/lslpy.git && cd lslpy
```

2. Install the `pip` package:

```
pip3 install -e .
```

## Example Usage

Property-based testing of `reverse`:

```python
from lslpy import check_contract, contract
from lslpy.contracts import  List, Integer, Constant


@contract
def my_reverse(l: List[Integer]) -> List[Integer]:
    l.reverse()
    return l


check_contract(my_reverse)


@contract
def my_reverse_prop(l1: List[Integer], l2: List[Integer]) -> Constant[True]:
    return my_reverse(l1 + l2) == my_reverse(l2) + my_reverse(l1)


check_contract(my_reverse_prop)
```

Verification of `bad-mult` via symbolic execution:

```python
from lslpy import contract, verify_contract
from lslpy.contracts import Integer, Constant

@contract
def bad_mult(x: Integer, y: Integer) -> Integer:
    return 0 if x == 10456 else (x * y)

@contract
def bad_mult_prop(x: Integer, y: Integer) -> Constant[True]:
    return bad_mult(x, y) == x * y

verify_contract(bad_mult_prop, global_vars=globals())
```

This snippet will raise the following `ContractViolation`:
```
Found counterexample: bad_mult_prop(y = -7651, x = 10456)
```
