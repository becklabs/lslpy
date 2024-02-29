# lslpy

`lslpy` is a library that allows for contract-based and property-based randomized testing in Python, inspired by [LSL](https://docs.racket-lang.org/lsl/index.html).

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
from lslpy.contracts import check_contract, contract
from lslpy.contracts.derived import Integer, true
from lslpy.contracts.primitives import Function, List


@contract(Function(arguments=(List(Integer()),), result=List(Integer())))
def my_reverse(l):
    l.reverse()
    return l


check_contract(my_reverse)


@contract(Function(arguments=(List(Integer()), List(Integer())), result=true()))
def my_reverse_prop(l1, l2):
    return my_reverse(l1 + l2) == my_reverse(l2) + my_reverse(l1)


check_contract(my_reverse_prop)
```