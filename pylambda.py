import sys
from collections import OrderedDict

class UntypedLambda():
    """
    A simple untyped lambda calculus interpreter.
    This is the BNF form of the grammar that this interpreter expects.
        <alpha>      := a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z
        <var>        := <alpha><var> 
        <expression> := <var> | <expression> ( <expression> ) | λ <var> . [ <expression> }
    No variable reuse is allowed.
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
        """
        This should eventually be made redundant by self.eval
        """
        # parens, parens_list = self.find_parens(expression)

        if len(expression) == 1:
            return expression[0].isalpha()
        elif expression[-1] == ")":
            index = len(expression) - list(reversed(expression)).index("(")
            expr_1 = expression[:index]
            expr_2 = expression[index:-1]
            return self.wffchecker(expr_1) and self.wffchecker(expr_2)
        elif expression[0] == "λ" and expression[2] == "." and expression[3] == "[":
            # index = expression.index("]")
            var = expression[1]
            # expr = expression[3:index] # not checking rn
            return self.wffchecker(var)
        else:
            raise ValueError("Ill-formed lambda expression!")

    def find_parens(self, expression = None):
        """
        Modified from https://stackoverflow.com/questions/29991917/indices-of-matching-parentheses-in-python
        """
        parens = OrderedDict() 
        pstack = []

        if not expression and self.expression:
            expression = self.expression
        elif not expression and not self.expression:
            return OrderedDict()

        for i, char in enumerate(expression):
            if char == '(' or char == "[":
                pstack.append(i)

            elif char == ')' or char == "]":
                if len(pstack) == 0:
                    raise IndexError("No matching closing parens at: " + str(i))

                parens[pstack.pop()] = i

        if len(pstack) > 0:
            raise IndexError("No matching opening parens at: " + str(pstack.pop()))

        return parens, list(parens)

    def eval(self, expression = None):
        """
        Evaluates the given lambda expression
        """
        # print(expression)

        if len(expression) == 1 and expression[0].isalpha():
            return expression[0]

        parens, parens_list = self.find_parens(expression)

        if expression[0] == "λ" and expression[2] == "." and expression[-1] == ")":
            index_appl = parens[parens_list[-1]]
            index_expr = parens[parens_list[0]]
            appl = expression[parens_list[-1]+1:index_appl]
            var = expression[1]
            expr = expression[parens_list[0]+1:index_expr]
            if self.wffchecker(var):
                # print("appl", appl)

                # replaces and *actually* evaluates lambda expression
                matches = [x in expr for x in var]
                eval_expr = []
                flag = False
                # print("matches", matches)
                for count, bool_value in enumerate(matches):
                    if bool_value:
                        if not flag:
                            eval_expr.extend(appl)
                        flag = True
                    else:
                        # eval_expr.append(expression[count])
                        eval_expr.append(expr[count])
                        flag = False

                # print(eval_expr)
                # eval_expr = [appl if t == var else t for t in expr]
                return self.eval(eval_expr)
        elif self.wffchecker(expression):
            return expression

        else:
            raise ValueError("Ill-formed lambda expression!", expression)

