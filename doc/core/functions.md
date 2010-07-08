Core Functions
==============

Python Core
-----------

Documentation on core functions implemented in Python

### quote

    (quote x)

Prevents its argument from being evaluated. The reader macro `'`
expands to this function.

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
