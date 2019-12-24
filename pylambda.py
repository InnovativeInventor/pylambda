import sys

class UntypedLambda():
    """
    A simple untyped lambda calculus interpreter.
    This is the BNF form of the grammar that this interpreter expects.
        <alpha>      := a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z
        <var>        := <alpha><var> 
        <expression> := <var> | <expression> ( <expression> ) | λ <var> . [ <expression> }
    """
    def __init__(self, filename = None, expression = None):
        sys.setrecursionlimit(10000) # not usually needed
        if filename:
            self.filename = filename
            self.read()
        elif expression:
            if isinstance(expression, list):
                self.expression = expression
            else:
                self.expression = expression.split()

    def check(self):
        return self.wffchecker(self.expression)

    def read(self):
        with open(self.filename, "r") as f:
            expression = str(f.readline()).split()
        
        # Clean up lambda expression (may not be necessary)
        self.expression = list(filter(None, expression))
        print(self.expression) # debug

    def wffchecker(self, expression: list):
        if len(expression) == 1:
            return expression[0].isalpha()
        elif expression[-1] == ")":
            index = len(expression) - list(reversed(expression)).index("(")
            expr_1 = expression[:index]
            expr_2 = expression[index:-1]
            return self.wffchecker(expr_1) and self.wffchecker(expr_2)
        elif expression[0] == "λ" and expression[2] == "." and expression[3] == "[":
            var = expression[1]
            expr = expression[1]
            return self.wffchecker(var) and self.wffchecker(expr)
        else:
            raise ValueError("Ill-formed lambda expression!")

