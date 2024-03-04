# from typing import List
# from lslpy.contracts import contract
# from lslpy.contracts.aliases import *

class Test:
    def __getitem__(self, params):
        return params

def test(*args):
    print(args)

test(1)


# @check
def func1(x: int, y: bool) -> True:
    return x, y


