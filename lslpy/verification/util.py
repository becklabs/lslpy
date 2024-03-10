import io
import sys


def capture_stdout(call: callable) -> str:
    """
    Captures the stdout of the given call
    """
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    call()
    output = new_stdout.getvalue()
    sys.stdout = old_stdout
    return output


def parse_prove_result(result_str: str) -> tuple[bool, str | None]:
    """
    Parses the result string into a tuple of (proved?, counterexample)
    """
    lines = result_str.split("\n")
    result = lines[0]
    proved = result.strip() == "proved"
    if proved:
        counterexample = None
    else:
        counterexample = lines[1][1:-1]
    return proved, counterexample
