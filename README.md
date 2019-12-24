## Pylambda

Pylambda is an effort to create an untyped lambda calculus interpreter in Python. It recursively evaluates and checks if a statement is well formed.

## Grammar (in [BNF](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form) form)
```
<alpha>      := a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z 
<var>        := <alpha><var>
<expression> := <var> | <expression> ( <expression> ) | λ <var> . [ <expression> }
```

NB: Spaces are important.

