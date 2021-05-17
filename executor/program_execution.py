from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython import compile_restricted, compile_restricted_exec
from RestrictedPython import safe_builtins
import sys
import builtins

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
    return query.split(sep=">")[1].split(sep="<")[0].replace("&quot;", '"')


def execution(form):
    """test_text = str(input("Введите число: "))
    test_number = int(test_text)
    print ("Введенное число: ", test_number)
    """
    loc ={
    "_print_" : SafePrintCollector,
    "_getattr_": getattr
    }
    safe_builtins["input"] = getattr(builtins, "input")

    code_src = extract_data(str(form["code"]))
    input_field = extract_data(str(form["input"])).replace('\n', '', 1)

    if input_field:
        with open('inputfile.txt', 'w') as f:
            f.write(input_field)
        with open('log.txt', 'a') as f:
            f.write(" inp:" + input_field)
        sys.stdin = open('inputfile.txt')

    try:
        code = compile_restricted(code_src, '<string>', 'exec')
        exec(code, {'__builtins__': safe_builtins}, loc)
    except Exception as error:
        with open('log.txt', 'a') as f:
            f.write(str(error))
        return "", str(error)

    result = str(loc['_print'].txt)
    with open('log.txt', 'a') as f:
        f.write(result)
    loc['_print'].txt = []
    return result, ""