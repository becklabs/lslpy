import z3

from .util import capture_stdout, parse_prove_result


def prove(expr) -> tuple[bool, str | None]:
    result_str = capture_stdout(call=lambda: z3.prove(expr))
    return parse_prove_result(result_str=result_str)
