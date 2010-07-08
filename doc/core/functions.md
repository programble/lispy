Core Functions
==============

Python Core
-----------

Documentation on core functions implemented in Python

### quote

    (quote x)

Prevents its argument from being evaluated.

The reader macro `'` expands to this function.

    => (quote x)
    x
    => 'x
    x

### eval

    (eval x)

Evaluates its argument (twice). Can be used to evaluate quoted data.

    => (eval (quote eval))
    <function eval at 0x87a34c4>

### ==

    (== x y)

Tests its two arguments for equality. Evaluates to `t` on equality and
`nil` otherwise.

    => (== 1 2)
    nil
    => (== 1 1)
    t

### car

    (car xs)

Evaluates to the `car` of the list `xs`. The `car` is the first item
of the list. If the list is empty, evaluates to `nil`.

    => (car '(1 2 3))
    1
    => (car '())
    nil

### cdr

    (cdr xs)

Evaluates to the `cdr` (rest) of the list `xs`. If the list is empty
or contains only one item, evaluates to `nil`. For proper lists,
always evaluates to another list. For improper lists, evaluates to one
value.

    => (cdr '(1 2 3))
    (2 3)
    => (cdr '(1))
    nil
    => (cdr '())
    nil
    => (cdr '(1 . 2))
    2

### cons

    (cons x y)

Evaluates to a new cons list in which `x` is the car and `y` is the
cdr.

    => (cons 1 2)
    (1 . 2)
    => (cons 1 (cons 2 nil))
    (1 2)

### cond

    (cond & clauses)

For each clause supplied, the car of the clause is evaluated, and if
non-nil, the cdr is returned, or if the clause has only one item, the
car is returned. Clauses are evaluated in order, and evaluation stops
after the first clause evaluates non-nil. If no clauses evaluate to
non-nil, `nil` is returned.

    => (cond (nil 1) (nil 2) (t 3))
    3
    => (cond (nil 1) (nil 2) (nil 3))
    nil

### def

    (def name value)

Binds `name` to `value` in the global scope. Evaluates to `name` if
the binding succeeds, otherwise evaluates to `nil`. Binding will fail
if `name` is not a symbol, or `name` has already been bound in the
global scope.

    => (def x 1)
    x
    => x
    1
    => (def x 2)
    nil

### undef!

    (undef! name)

Unbinds `name` in the global scope. Evaluates to the value of `name`,
or `nil` if `name` was not bound.

    => (def x 1)
    x
    => (undef! x)
    1
    => (undef! y)
    nil

### set!

    (set! name value)

Rebinds `name` in the scope it is bound in to `value`. Evaluates to
the previous value of `name`, or `nil` if `name` is not bound.

    => (def x 1)
    x
    => (set! x 2)
    1
    => x
    2
    => (set! y 3)
    nil

### unset!

    (unset! name)

Unbinds `name` in the scope it is bound in. Evaluates to the value of
`name` or `nil` if `name` is not bound.

    => (def x 1)
    x
    => (unset! x)
    1
    => (unset! y)
    nil

### fn

    (fn args & body)

Creates a new Lambda function that takes the list `args` as arguments
and evaluates `body` in order and returns the value of the last
expression.

    => (fn (x) (eval x))
    <ast.Lambda instance at 0x873066c>

### syntax-quote

    (syntax-quote expression)

Similar to `quote`, except that any unquoted (see `unquote`) parts of
`expression` are evaluated.

The reader macro <code>`</code> expands to this function.

    => (def x 1)
    x
    => `(foo (unquote x))
    (foo 1)

#### unquote

    (unquote expression)

Note: only bound inside `syntax-quote`

Evaluates `expression` and replaces with its result inside
`syntax-quote`.

The reader macro `,` expands to this function.

    => (def x 1)
    x
    => `(foo ,x)
    (foo 1)

#### unquote-splice

    (unquote-splice expression)

Note: only bound inside `syntax-quote`

Evaluates `expression` and splices the resulting list into a
`syntax-quote` expression.

The reader macro `,@` expands to this function.

    => (def x '(1 2 3))
    x
    => `(foo ,@x)
    (foo 1 2 3)

### macro

    (macro args & body)

Creates a new macro that takes the list `args` as arguments and
evaluates the expressions in `body` in order, and evaluates the last
expression twice, returning its result.

    => (macro (x) `(foo ,x))
    <ast.Macro instance at 0x87305ec>

### list

    (list & items)

Creates a new list by evaluating each argument it receives.

    => (def x 1)
    x
    => (list x 2 3)
    (1 2 3)

### let

    (let bindings & body)

Creates a new scope in which is binding in `bindings` is bound and
evaluates each expression in `body` sequentially, returning the result
of the last expression.

`bindings` is a list of `(name value)` pairs.

    => (let ((x 1) (y 2)) (list x y))
    (1 2)

### do

    (do & body)

Evaluates each expression in `body` and returns the result of the last
expression.

    => (def x 1)
    x
    => (do (set! x 2) x)
    2

### +

    (+ & values)

If given no arguments, evaluates to 0. If given one or more arguments,
evaluates to the sum of all arguments.

    => (+)
    0
    => (+ 1 2 3)
    6

### -

    (- & values)

If given no arguments, evaluates to 0. If given one argument,
evaluates to the negation of that value. If given two or more
arguments, evaluates to the difference of all arguments.

    => (-)
    0
    => (- 1)
    -1
    => (- 1 2 3)
    -4

### *

    (* & values)

If given no arguments, evaluates to 1. If given one argument,
evaluates to its value. If given two or more arguments, evaluates to
the product of all arguments.

    => (*)
    1
    => (* 2)
    2
    => (* 2 2 3)
    12

### /

    (/ & values)

If given no arguments, evaluates to 1. If given one arguments,
evaluates to the reciprocal of the value. If given two or more
arguments, evaluates to the quotient of all arguments.

    => (/)
    1
    => (/ 2.0)
    0.5
    => (/ 6.0 2.0 2.0)
    1.5

### %

    (% x y)

Evaluates to the remainder of the division of `x` by `y`.

    => (% 4 2)
    0
    => (% 5 2)
    1

### <

    (< x y)

Evaluates to `t` if `x` is less then `y`, otherwise, evaluates to
`nil`.

    => (< 1 2)
    t
    => (< 2 1)
    nil

### >

    (> x y)

Evaluates to `t` if `x` is greater than `y`, otherwise, evaluates to
`nil`.

    => (> 2 1)
    t
    => (> 1 2)
    nil

### macroexpand

    (macroexpand expression)

Expands the expression until the car is not a macro.

    => (def m (macro (x) `(foo ,x)))
    m
    => (macroexpand (m 1))
    (foo 1)

### format

    (format string & args)

Formats the string `string` with `args` in the style of C's `printf`.

    => (format "foo%d" 2)
    "foo2"

### repr

    (repr expression)

Evaluates to the string representation of `expression`.

    => (repr 1)
    "1"
    => (repr '(1 2 3))
    "(1 2 3)"

### print

    (print string)

Writes `string` to the stream `*out*` is bound to. Always evaluates to
`nil`.

    => (print "foobar\n")
    foobar
    nil
