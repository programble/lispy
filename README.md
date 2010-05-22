Lispy
=====

Lispy is a Lisp implementation in Python based on John McCarthy's
paper "Recursive Functions of Symbolic Expressions and Their
Computation by Machine, Part I", which can be found
[here](http://www-formal.stanford.edu/jmc/recursive/).

Some code is based on [fogus](http://github.com/fogus/)'s
[lithp](http://github.com/fogus/lithp).

Features
--------

Lispy implements all seven core functions discussed in McCarthy's
paper:

1. `atom`
2. `eq`
3. `car`
4. `cdr`
5. `cons`
6. `cond`
7. `quote`

Lispy also implements the two special forms:

1. `def`
2. `lambda`

As of now, Lispy also includes the basic arithmetic operators:

 * `+`
 * `-`
 * `*`
 * `/`

Lispy also binds two extra symbols in the global scope:

 * `t`
 * `nil`

Usage
-----

As of yet, there is no complete REPL for Lispy. To run a makeshift
REPL, run

    python lispy.py

In order to evaluate code, enter an expression at the `=>` prompt and
press enter. The expression will be evaluated and its result
displayed.

