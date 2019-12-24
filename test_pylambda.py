import pylambda
import pytest
import os
from collections import OrderedDict

STRING = "λ x . [ x ]  ( λ y . [ λ z. [ z ] ] )"
FILENAME = "test.lbda"

def test_write():
    with open(FILENAME, "w") as f:
        f.write(STRING)
    interpreter = pylambda.UntypedLambda(FILENAME)
    assert interpreter.check() == True
    os.remove(FILENAME)

def test_write():
    with open(FILENAME, "w") as f:
        f.write(STRING)
    interpreter = pylambda.UntypedLambda(filename = FILENAME)
    assert interpreter.check() == True
    os.remove(FILENAME)

def test_expression_str():
    interpreter = pylambda.UntypedLambda(expression = STRING)
    assert interpreter.check() == True

def test_expression_str():
    interpreter = pylambda.UntypedLambda(expression = STRING.split())
    assert interpreter.check() == True

def test_find_paren():
    interpreter = pylambda.UntypedLambda(expression = STRING)

def test_eval():
    interpreter = pylambda.UntypedLambda(expression = STRING)
    assert interpreter.eval(expression = STRING.split()) == ['λ', 'y', '.', '[', 'λ', 'z.', '[', 'z', ']', ']']
    assert interpreter.eval(expression = STRING) == ['λ', 'y', '.', '[', 'λ', 'z.', '[', 'z', ']', ']']

def test_eval_1():
    interpreter = pylambda.UntypedLambda(expression = STRING)
    assert interpreter.eval() == ['λ', 'y', '.', '[', 'λ', 'z.', '[', 'z', ']', ']']

def test_eval_1():
    interpreter = pylambda.UntypedLambda()
    assert interpreter.eval(expression = STRING) == ['λ', 'y', '.', '[', 'λ', 'z.', '[', 'z', ']', ']']

def test_ill_formed_error():
    with pytest.raises(ValueError) as error:
        interpreter = pylambda.UntypedLambda(expression = ["a", ")"])
        interpreter.check()

def test_ill_formed_error_1():
    with pytest.raises(ValueError) as error:
        interpreter = pylambda.UntypedLambda(expression = ["]", ")"])
        interpreter.check()

def test_ill_formed_error_2():
    with pytest.raises(IndexError) as error:
        interpreter = pylambda.UntypedLambda()
        interpreter.eval(expression = ["]", ")"])

def test_ill_formed_error_2():
    with pytest.raises(IndexError) as error:
        interpreter = pylambda.UntypedLambda()
        interpreter.eval(expression = ["λ", "x"])
