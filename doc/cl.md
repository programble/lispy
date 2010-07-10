Lispy for Common Lispers
========================

Functions / Lambdas
-------------------

In Lispy, CL's `lambda` is known as `fn`.

CL:
    (lambda (x) (+ x 2))
Lispy:
    (fn (x) (+ x 2))

In Lispy, CL's `defun` is known as `defn`.

CL:
    (defun foo (x) (+ x 2))
Lispy:
    (defn foo (x) (+ x 2))

Predicates
----------

Predicates in Lispy end in `?`, not CL's `p`.

CL:
    (zerop x)
Lispy:
    (zero? x)

Other functions
---------------

Here is a CL to Lispy function names map.

 * `length` -> `count`
 * `progn` -> `do`

Binding Stuff
-------------

Lispy tries to be immutable. Any functions that break this rule and
that are destructive end in `!` and usually return the previous value.

### def

`def` binds something in the global scope. Once it is bound, it cannot
be rebound without first calling `undef!` on it. `undef!` unbinds the
symbol and returns its value.

### set!

`set!` changes the bound value of a symbol and returns its previous
value. `unset!` unbinds a symbol and returns its value.

Argument Syntax
---------------

The `&rest` equivalent in Lispy is `&`.

CL:
    (defun foo (x &rest y) y)
Lispy:
    (defn foo (x & y) y)

The `&optional` equivalent in Lispy is `?`.

CL:
    (defun foo (x &optional y) y)
Lispy:
    (defn foo (x ? y) y)

Notes
-----

Lispy doesn't yell all the time like CL does.
