## Pylambda
[![Build
Status](https://travis-ci.com/InnovativeInventor/pylambda.svg?branch=master)](https://travis-ci.com/InnovativeInventor/pylambda) [![codecov](https://codecov.io/gh/InnovativeInventor/pylambda/branch/master/graph/badge.svg)](https://codecov.io/gh/InnovativeInventor/pylambda)

Pylambda is an effort to create an untyped lambda calculus interpreter in Python. It recursively evaluates and checks if a statement is well formed.

Features:
- [x] Turing complete
- [x] Evaluates untyped lambda calculus 
- [x] Validates grammar for untyped lambda calculus (doesn't fully validate that a statement is well-formed)
- [ ] Easy to read `__repr__`
- [ ] Special encodings ([Church](https://en.wikipedia.org/wiki/Church_encoding))
- [ ] Simple types

## Grammar (in [BNF](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form) form)
```
<alpha>      := a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z 
<var>        := <alpha><var>
<expression> := <var> | <expression> ( <expression> ) | λ <var> . [ <expression> }
```

NB: Spaces are important. No variable reuse is allowed.

## Example usage
Evaluating a lambda expression:
```python
expression = "λ x . [ x ]  ( λ y . [ λ z. [ z ] ] )"
interpreter = pylambda.UntypedLambda()
interpreter.eval(expression = expression)
```
