# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

import sys

from scope import Scope
import lisp

# Global scope (This is where the entire core goes)
global_scope = Scope()

# Standard core bindings
t = lisp.Symbol("t")
global_scope["t"] = t
nil = lisp.Symbol("nil")
global_scope["nil"] = nil

# Lispy Information
global_scope["*lispy-version*"] = lisp.List([lisp.Atom(0), lisp.Atom(1), lisp.Atom(0)])
global_scope["*lispy-platform*"] = lisp.String(sys.platform)

# Core functions (from McCarthy's paper)

def atom(scope, x):
    """Returns t if x is atomic"""
    x = x.evaluate(scope)
    
    if x.__class__ == lisp.Atom:
        return t
    else:
        return nil
global_scope["atom"] = atom

def eq(scope, x, y):
    """Returns t if x and y are equal"""
    # First evaluate arguments
    x = x.evaluate(scope)
    y = y.evaluate(scope)
    
    if x == y:
        return t
    else:
        return nil
global_scope["eq"] = eq
global_scope["="] = eq

def car(scope, x):
    """Returns the first item (car) of list x"""
    return x.evaluate(scope).car()
global_scope["car"] = car

def cdr(scope, x):
    """Returns the tail (cdr) of list x"""
    return x.evaluate(scope).cdr()
global_scope["cdr"] = cdr

def cons(scope, x, y):
    """Joins y and x"""
    # First evaluate arguments
    x = x.evaluate(scope)
    y = y.evaluate(scope)
    
    return y.cons(x)
global_scope["cons"] = cons

def cond(scope, *x):
    """For each expression, if the car evaluates to t, the cdr is evaluated and its result returned"""
    for test in x:
        if test.car().evaluate(scope) == t:
            return test.cdr().car().evaluate(scope)
    return nil
global_scope["cond"] = cond

def quote(scope, x):
    """Returns its argument"""
    return x
global_scope["quote"] = quote

# Special Forms (from McCarthy's paper)

def def_(scope, symbol, x):
    # Can only bind to a symbol
    if symbol.__class__ != lisp.Symbol:
        return nil
    # Evaluate value
    x = x.evaluate(scope)
    # Bind in global scope
    global_scope[symbol.data] = x
    return scope[symbol.data]
global_scope["def"] = def_

def lambda_(scope, names, *body):
    """Returns a new lambda"""
    l = lisp.Lambda(names, body)
    return l
global_scope["lambda"] = lambda_
global_scope["fn"] = lambda_

# Macro Functions

def backquote(scope, expr):
    """Returns a new list with only the unquoted items evaluated"""
    # Cannot backquote a non-list
    if expr.__class__ != lisp.List:
        return expr
    new = []
    for x in expr.data:
        if x.__class__ == lisp.List:
            # Evaluate only unquoted items
            if x.car() == lisp.Symbol("unquote"):
                new.append(x.cdr().car().evaluate(scope))
            elif x.car() == lisp.Symbol("unquote-list"):
                l = x.cdr().car().evaluate(scope)
                for i in l.data:
                    new.append(i)
            else:
                new.append(backquote(scope, x))
        else:
            new.append(x)
    return lisp.List(new)
global_scope["backquote"] = backquote

def macro(scope, names, *body):
    """Returns a new macro"""
    m = lisp.Macro(names, body)
    return m
global_scope["macro"] = macro

def macroexpand(scope, expr):
    m = expr.car().evaluate(scope)
    l = lisp.Lambda(m.names, m.body)
    return l(scope, *[lisp.List([lisp.Symbol("quote"), x]) for x in expr.cdr().data])
global_scope["macroexpand"] = macroexpand

# Other core functions

def list_(scope, *x):
    """Evaluates all arguments then returns a List of them"""
    return lisp.List([i.evaluate(scope) for i in x])
global_scope["list"] = list_

def let(scope, bindings, *exprs):
    """Creates a new scope with bindings and evaluates expressions in that scope, returning the result of the last expression"""
    # Create a new scope
    local_scope = Scope(scope)
    # Bind each pair in bindings
    for pair in bindings.data:
        local_scope[pair.car().data] = pair.cdr().car().evaluate(local_scope)
    # Evaluate each expr in local scope
    for expr in exprs[:-1]:
        expr.evaluate(local_scope)
    # Return the result of the last expr
    return exprs[-1].evaluate(local_scope)
global_scope["let"] = let

def do(scope, *exprs):
    """Evaluates each expression and returns the result of the last"""
    for expr in exprs[:-1]:
        expr.evaluate(scope)
    return exprs[-1].evaluate(scope)
global_scope["do"] = do

def dolist(scope, nl, *exprs):
    """Evaluates each expression for each item in the list"""
    ret = nil
    # Create new local scope
    local_scope = Scope(scope)
    # Evaluate the list
    l = nl.cdr().car().evaluate(scope)
    for i in l.data:
        # Bind this item to the name
        local_scope[nl.car().data] = i.evaluate(scope)
        for expr in exprs:
            ret = expr.evaluate(local_scope)
    return ret
global_scope["dolist"] = dolist

# Arithmetic functions

def add(scope, *x):
    if len(x) == 0:
        return 0
    if len(x) == 1:
        return x[0]
    else:
        return add(scope, lisp.Atom(x[0].evaluate(scope).data + x[1].evaluate(scope).data), *x[2:])
global_scope["+"] = add

def sub(scope, *x):
    if len(x) == 0:
        return 0
    if len(x) == 1:
        return x[0]
    else:
        return sub(scope, lisp.Atom(x[0].evaluate(scope).data - x[1].evaluate(scope).data), *x[2:])
global_scope["-"] = sub

def mul(scope, *x):
    if len(x) == 0:
        return 1
    if len(x) == 1:
        return x[0]
    else:
        return mul(scope, lisp.Atom(x[0].evaluate(scope).data * x[1].evaluate(scope).data), *x[2:])
global_scope["*"] = mul

def div(scope, *x):
    if len(x) == 0:
        return 0
    if len(x) == 1:
        return x[0]
    else:
        return div(scope, lisp.Atom(x[0].evaluate(scope).data / x[1].evaluate(scope).data), *x[2:])
global_scope["/"] = div

def mod(scope, x, y):
    x = x.evaluate(scope)
    y = y.evaluate(scope)
    return lisp.Atom(x.data % y.data)
global_scope["%"] = mod

# Comparison Operators

def lt(scope, x, y):
    x = x.evaluate(scope)
    y = y.evaluate(scope)
    if x.data < y.data:
        return t
    else:
        return nil
global_scope["<"] = lt

def gt(scope, x, y):
    x = x.evaluate(scope)
    y = y.evaluate(scope)
    if x.data > y.data:
        return t
    else:
        return nil
global_scope[">"] = gt

# Other functions

def range_(scope, x):
    """Returns a list of numbers from 0 to x - 1"""
    return lisp.List([lisp.Atom(i) for i in range(x.evaluate(scope).data)])
global_scope["range"] = range_

# Stdio functions

def format(scope, fs, *a):
    fs = fs.evaluate(scope).data
    args = []
    for i in a:
        args.append(i.evaluate(scope).data)
    return lisp.String(fs % tuple(args))
global_scope["format"] = format

def print_(scope, s):
    sys.stdout.write(s.evaluate(scope).data)
    return nil
global_scope["print"] = print_

# Misc. Functions
def time_(scope, x):
    import time
    s = time.time()
    x.evaluate(scope)
    s = time.time() - s
    return lisp.Atom(s)
global_scope["time"] = time_

