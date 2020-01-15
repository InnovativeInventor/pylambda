import sys
from collections import OrderedDict

class UntypedLambda():
    """
    A simple untyped lambda calculus interpreter. More documentation in the README.
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
                self.expression = self.tokenize(expression)

        if hasattr(self, 'expression'):
            self.context = [self.expression]
        else:
            self.context = []

        self.functions = {} 

    def __repr__(self):
        return str(self.expression)

    def __str__(self):
        return "".join(self.expression)

    def is_beta(self):
        """
        Determines if the lambda expression can be beta-reducible 
        (this just applies eval() once and compares, no guarantees!) 
        """
        if ("λ" or "\\") and self.expression[-1] in ["]", ")"]:
            before_expr = self.expression

            if len(self.eval(self.expression)) < len(before_expr):
                self.expression = before_expr
                return True
            else:
                self.expression = before_expr
                return False

    def check(self):
        return self.wffchecker(self.expression)

    def read(self):
        with open(self.filename, "r") as f:
            expression = self.tokenize(f.readline())
        
        # Clean up lambda expression (may not be necessary)
        self.expression = list(filter(None, expression))
        # print(self.expression) # debug

    def wffchecker(self, expression: list):
        """
        This should eventually be made redundant by self.eval
        """
        # parens, parens_list = self.find_parens(expression)
        try:
            if len(expression) == 1:
                return expression[0].isalpha()
            elif expression[-1] == ")":
                index = len(expression) - list(reversed(expression)).index("(")
                expr_1 = expression[:index]
                expr_2 = expression[index:-1]
                return self.wffchecker(expr_1) and self.wffchecker(expr_2)
            elif (expression[0] == "λ" or expression[0] == "\\") and expression[2] == "." and expression[3] == "[":
                # index = expression.index("]")
                var = expression[1]
                # expr = expression[3:index] # not checking rn
                return self.wffchecker(var)
        except:
            pass

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
        if not expression:
            expression = self.expression

        if isinstance(expression, str):
            expression = self.tokenize(expression)

        if len(expression) == 1 and expression[0].isalpha():
            self.expression = expression[0]
            self.context.append(self.expression)
            return self.expression

        parens, parens_list = self.find_parens(expression)

        if (expression[0] == "λ" or expression[0] == "\\") and expression[2] == "." and expression[-1] == ")":
            index_appl = parens[parens_list[-1]]
            index_expr = parens[parens_list[0]]
            appl = expression[parens_list[-1]+1:index_appl]
            var = expression[1]
            expr = expression[parens_list[0]+1:index_expr]
            if self.wffchecker(var):
                # print("appl", appl)

                # replaces and *actually* evaluates lambda expression
                matches = [x in expr for x in var] # verify
                eval_expr = []
                flag = False
                for count, bool_value in enumerate(matches):
                    if bool_value and expr[count] not in self.functions.keys(): # *some* scoping
                        if not flag:
                            eval_expr.extend(appl)
                        flag = True
                    else:
                        # If it doesn't match
                        eval_expr.append(expr[count])
                        flag = False

                # print(eval_expr)
                # eval_expr = [appl if t == var else t for t in expr]
                return self.eval(eval_expr)

        elif self.wffchecker(expression):
            self.expression = expression
            self.context.append(self.expression)
            return self.expression

        elif self.expression[0] == "fn":
            # fn name x . expr
            self.functions[self.expression[1]] = ["λ"].extend(self.expression[2:])
            # ["λ"].extend(self.expression[2:] should look like ["λ", "x", ".", <expr>]

        elif self.expression[0] in self.functions.keys():
            # named func application
            index_appl = parens[parens_list[0]]
            self.eval(self.functions[self.expression[0]].extend(["(", self.expression[parens_list[0]:index_appl]]))

        else:
            raise ValueError("Ill-formed lambda expression!", expression)

    def tokenize(self, expression = None):
        special_tokens = [")", "(", "]", "[", "λ", ".", "\\"]
        if not expression:
            expression = self.expression

        if isinstance(expression, list):
            return expression

        for each_token in special_tokens:
            expression = expression.replace(each_token, " " + each_token + " ")

        return expression.rstrip().split()

    def repl(self):
        try:
            while True:
                # TODO: add more parsing to functions append and eval
                command = input("lbda > ")
                self.eval(self.tokenize(command))
                print(self)
        except KeyError:
            print("Exiting . . .!")


