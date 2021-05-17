from django.test import TestCase

# Create your tests here.
code_src =  """

def hello_world():
    print('Hello inner world!')
    return printed

print('Hello outer world!') # print a string

print(hello_world())        # print return of function

results = printed          # fetch printed in a global

"""
test_code = """test_text = str(input("Введите число: "))
    test_number = int(test_text)
    print ("Введенное число: ", test_number)
    """