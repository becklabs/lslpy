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
from lslpy.contracts.aliases import  List, Integer, Constant


@contract()
def my_reverse(l: List[Integer]) -> List[Integer]:
    l.reverse()
    return l


check_contract(my_reverse)


@contract()
def my_reverse_prop(l1: List[Integer], l2: List[Integer]) -> Constant[True]:
    return my_reverse(l1 + l2) == my_reverse(l2) + my_reverse(l1)


check_contract(my_reverse_prop)
```