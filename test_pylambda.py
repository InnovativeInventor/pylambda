import pylambda
import pytest
import os
from collections import OrderedDict

STRING = "λ x . [ x ]  ( λ y . [ λ z . [ z ] ] )"
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
    assert interpreter.find_parens() == (OrderedDict([(3, 5), (14, 16), (10, 17), (6, 18)]), [3, 14, 10, 6])

def test_eval():
    interpreter = pylambda.UntypedLambda(expression = STRING)
    assert interpreter.eval(expression = STRING.split()) == ['λ', 'y', '.', '[', 'λ', 'z', '.', '[', 'z', ']', ']']
    assert interpreter.eval(expression = STRING) == ['λ', 'y', '.', '[', 'λ', 'z', '.', '[', 'z', ']', ']']

def test_eval_1():
    interpreter = pylambda.UntypedLambda(expression = STRING)
    assert interpreter.eval() == ['λ', 'y', '.', '[', 'λ', 'z', '.', '[', 'z', ']', ']']

def test_eval_1():
    interpreter = pylambda.UntypedLambda()
    assert interpreter.eval(expression = STRING) == ['λ', 'y', '.', '[', 'λ', 'z', '.', '[', 'z', ']', ']']

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

def test_ill_formed_error_3():
    with pytest.raises(IndexError) as error:
        interpreter = pylambda.UntypedLambda()
        interpreter.eval(expression = ["λ", "x"])

def test_ill_formed_error_4():
    with pytest.raises(ValueError) as error:
        interpreter = pylambda.UntypedLambda(expression = ["]", ")"])
        interpreter.wffchecker(expression = ["]", ")"])

def test_ill_formed_error_5():
    with pytest.raises(ValueError) as error:
        interpreter = pylambda.UntypedLambda()
        interpreter.wffchecker(expression = [])

def test_tokenize():
    interpreter = pylambda.UntypedLambda()
    assert interpreter.tokenize(expression = "λx") == ["λ", "x"]

def test_tokenize_auto():
    interpreter = pylambda.UntypedLambda(expression = "λx")
    assert interpreter.tokenize() == ["λ", "x"]

def test_tokenize_ignore():
    interpreter = pylambda.UntypedLambda(expression = "λx")
    assert interpreter.tokenize(expression = ["λ", "x"]) == ["λ", "x"]
