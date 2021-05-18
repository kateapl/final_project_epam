from django.test import TestCase
import pytest
from . import program_execution
# Create your tests here.
code_src =  """

def hello_world():
    print('Hello inner world!')
    return "Good news everyone!"

print('Hello outer world!') # print a string

print(hello_world())        # print return of function
"""
test_code = """test_text = str(input("Введите число: "))
    test_number = int(test_text)
    print("Введенное число: ", test_number)
    """

def test_decorator_doc_parameter():
    form =
    assert (
        program_execution.execution()
        == """This function can sum any objects which have __add___"""
    )