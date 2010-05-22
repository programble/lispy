# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

from scope import Scope
import lisp

global_scope = Scope()

# Core bindings
global_scope["t"] = lisp.Atom(True)
t = global_scope["t"]
global_scope["nil"] = lisp.List()
nil = global_scope["nil"]

# Core functions

def atom(scope, x):
    """atom(x) is True if x is an Atom"""
    return x.__class__ == lisp.Atom or x.__class___ == lisp.Symbol
global_scope["atom"] = atom

def eq(scope, x, y):
    """eq(x, y) is True is x and y are equal"""
    if x.__class__ != lisp.Atom:
        x = x.evaluate(scope)
    if y.__class__ != lisp.Atom:
        y = y.evaluate(scope)
    if x == y:
        return t
    else:
        return nil
global_scope["eq"] = eq

def car(scope, x):
    """car(x) is the first item of x if x is non-atomic"""
    return x.evaluate(scope).car()
global_scope["car"] = car

def cdr(scope, x):
    """cdr(x) is the rest of x if x is non-atomic"""
    return x.evaluate(scope).cdr()
global_scope["cdr"] = cdr

def cons(scope, x, y):
    """cons"""
    return y.evaluate(scope).cons(x.evaluate(scope))
global_scope["cons"] = cons

def cond(scope, *x):
    """cond"""
    for test in x:
        if test.car().evaluate(scope) == t:
            ret = test.cdr().car()
            if ret.__class__ != lisp.Atom:
                ret = ret.evaluate(scope)
            return ret
    return nil
global_scope["cond"] = cond

def quote(scope, x):
    """quote"""
    return x
global_scope["quote"] = quote

def _def(scope, symbol, x):
    if symbol.__class__ != lisp.Symbol:
        return nil
    scope[symbol.data] = x.evaluate(scope)
    return scope[symbol.data]
global_scope["def"] = _def

def _lambda(scope, names, *body):
    l = lisp.Lambda(names, body)
    return l
global_scope["lambda"] = _lambda

# Arithmetic functions

def add(scope, *x):
    ret = 0
    for i in x:
        if i.__class__ != lisp.Atom:
            i = i.evaluate(scope)
        ret += i.evaluate(scope)
    return lisp.Atom(ret)
global_scope["+"] = add

def sub(scope, *x):
    ret = 0
    for i in x:
        if i.__class__ != lisp.Atom:
            i = i.evaluate(scope)
        ret -= i.evaluate(scope)
    return lisp.Atom(ret)
global_scope["-"] = sub

def mul(scope, *x):
    ret = 1
    for i in x:
        if i.__class__ != lisp.Atom:
            i = i.evaluate(scope)
        ret *= i.evaluate(scope)
    return lisp.Atom(ret)
global_scope["*"] = mul

def div(scope, *x):
    if len(x) == 1:
        x = x[0]
        if x.__class__ != lisp.Atom:
            x = x.evaluate(scope)
        return 1 / x.evaluate(scope)
    if x[0].__class__ != lisp.Atom:
        x[0] = x[0].evaluate(scope)
    ret = x[0]
    for i in x[1:]:
        if i.__class__ != lisp.Atom:
            i = i.evaluate(scope)
        ret /= i.evaluate(scope)
    return lisp.Atom(ret)
global_scope["/"] = div


