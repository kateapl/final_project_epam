import builtins
import sys

from RestrictedPython import compile_restricted, safe_builtins
from RestrictedPython.PrintCollector import PrintCollector


def singleton(cls):
    _instance = {}

    def inner(t):
        if cls not in _instance:
            _instance[cls] = cls(t)
        return _instance[cls]

    return inner


@singleton
class SafePrintCollector(PrintCollector):
    pass


def extract_data(query: str) -> str:
    return (
        query.split(sep=">")[1]
        .split(sep="<")[0]
        .replace("&quot;", '"')
        .replace("&#x27", "'")
    )


def execution(form) -> tuple:
    loc = {"_print_": SafePrintCollector, "_getattr_": getattr}
    safe_builtins["input"] = getattr(builtins, "input")
    safeglobals = {"__builtins__": safe_builtins}
    safeglobals["_print_"] = SafePrintCollector

    code_src = extract_data(str(form["code"]))
    input_field = extract_data(str(form["input"])).replace("\n", "", 1)

    if input_field:
        with open("inputfile.txt", "w") as f:
            f.write(input_field)
        sys.stdin = open("inputfile.txt")

    try:
        code = compile_restricted(code_src, "<string>", "exec")
        exec(code, safeglobals, loc)
    except Exception as error:
        return [], str(error)
    try:
        result = loc["_print"].txt
    except KeyError as error:
        return [], "Nothing is printed"

    loc["_print"].txt = []
    return result, ""
