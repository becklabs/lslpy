import ast
import inspect
from .verification.transformer import Z3Transformer
from .verification.prover import prove


from .contracts import Callable, contract, check_contract, contract_generate
from .contracts.exceptions import ContractViolation
from .contracts.util import format_func


def verify_contract(func: Callable, global_vars: dict):
        func_ast = ast.parse(inspect.getsource(func.func))
        func_symbolic = Z3Transformer(local_vars={}, global_vars=global_vars).visit(func_ast)
        proved, counterexample = prove(func_symbolic)
        if not proved:
            raise ContractViolation(
                f"Found counterexample: {format_func(func.func)}({counterexample})")