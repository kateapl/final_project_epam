from django.test import TestCase
from django.test.client import Client

from . import forms, program_execution


class FinalProjectTests(TestCase):
    def setUp(self) -> None:
        self.single_print_code = 'print("test print")'

        self.function_print_code = """
def hello_world():
    return "Good news everyone!"
print(hello_world())"""

        self.print_code_with_input = """
test_text = str(input("print a number: "))
test_number = int(test_text)
print("Input: ", test_number)"""

        self.print_code_out_and_in = """
def hello_world():
    print("Hello inner world!")

print("Hello outer world!")
hello_world()"""

        self.security_check = """
code = "(lambda x: x).__globals__['__builtins__']['open'].__doc__[:100]"
print(eval(code, {}, {}))"""

        self.without_print = "a = 54"
        self.os_import_error = "import os"
        self.exec_error = 'exec(print("chill"))'
        self.eval_error = "eval(a= 2)"

    def test_single_print(self):
        data = {"code": self.single_print_code, "input": ""}
        form = forms.CodeInputForm(data=data)
        result = program_execution.execution(form)
        assert result == (["test print", "\n"], "")

    def test_print_function(self):
        data = {"code": self.function_print_code, "input": ""}
        form = forms.CodeInputForm(data=data)
        result = program_execution.execution(form)
        assert result == (["Good news everyone!", "\n"], "")

    def test_print_code_in_and_out_of_function(self):
        data = {"code": self.print_code_out_and_in, "input": ""}
        form = forms.CodeInputForm(data=data)
        result = program_execution.execution(form)
        assert result == (["Hello outer world!", "\n", "Hello inner world!", "\n"], "")

    def test_print_code_with_input(self):
        data = {"code": self.print_code_with_input, "input": "42"}
        form = forms.CodeInputForm(data=data)
        result = program_execution.execution(form)
        assert result == (["Input: ", " ", "42", "\n"], "")

    def test_os_import_error(self):
        data = {"code": self.os_import_error, "input": "42"}
        form = forms.CodeInputForm(data=data)
        result = program_execution.execution(form)
        assert result == ([], "__import__ not found")

    def test_exec_error(self):
        data = {"code": self.exec_error, "input": ""}
        form = forms.CodeInputForm(data=data)
        result = program_execution.execution(form)
        assert result == ([], "('Line 2: Exec calls are not allowed.',)")

    def test_eval_error(self):
        data = {"code": self.eval_error, "input": ""}
        form = forms.CodeInputForm(data=data)
        result = program_execution.execution(form)
        assert result == ([], "('Line 2: Eval calls are not allowed.',)")

    def test_security_check(self):
        data = {"code": self.security_check, "input": ""}
        form = forms.CodeInputForm(data=data)
        result = program_execution.execution(form)
        assert result == ([], "('Line 4: Eval calls are not allowed.',)")

    def test_without_print_in_code(self):
        data = {"code": self.without_print, "input": ""}
        form = forms.CodeInputForm(data=data)
        result = program_execution.execution(form)
        assert result == ([], "Nothing is printed")
