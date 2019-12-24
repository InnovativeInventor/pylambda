import pylambda
import os

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
