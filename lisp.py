# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

from scope import Scope

class Atom:
    def __init__(self, data):
        self.data = data
        
    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return self.data == other.data
        else:
            return False

    def cons(self, other):
        return List([other, self])
    
    def evaluate(self, scope):
        # An atom evaluates to itself
        return self
        
    def __repr__(self):
        return repr(self.data)

class Symbol(Atom):
    def __init__(self, data):
        Atom.__init__(self, data)

    def evaluate(self, scope):
        # A symbol evaluates to its binding
        return scope[self.data]

    def __repr__(self):
        return self.data

class List(Atom):
    def __init__(self, data=[]):
        Atom.__init__(self, data)

    def car(self):
        if len(self.data) == 0:
            return List()
        x = self.data[0]
        return x

    def cdr(self):
        return List(self.data[1:])

    def cons(self, other):
        return List([other] + self.data)
    
    def evaluate(self, scope):
        # A list is evaluated by calling the car as a function with the cdr as arguments
        fn = self.car()
        fn = fn.evaluate(scope)
        return fn(scope, *self.cdr().data)

    def __repr__(self):
        return "(%s)" % ' '.join([repr(x) for x in self.data])

class String(List):
    def __init__(self, data=""):
        List.__init__(self, data)

    def car(self):
        return Atom(self.data[0])

    def cdr(self):
        return String(self.data[1:])

    def cons(self, other):
        return String(other.data + self.data)

    def evaluate(self, scope):
        # A String evaluates to itself (as if quoted)
        return self

    def __repr__(self):
        return repr(self.data)
    
class Lambda:
    def __init__(self, names, body):
        self.names = names
        self.body = body

    def __call__(self, scope, *args):
        # Make sure we have the right amount of args for the amount of names
        if len(args) != len(self.names.data):
            raise TypeError("expected %d arguments, got %d" % (len(self.names.data), len(args)))
        # Create a new local function scope
        fn_scope = Scope(scope)
        # Bind each arg to a name in the function scope
        for name, value in zip([x.data for x in self.names.data], args):
            # Evaluate each arg before binding
            if value.__class__ != Atom:
                value = value.evaluate(scope)
            fn_scope[name] = value
        # Evaluate each expression in lambda body
        for expression in self.body[:-1]:
            expression.evaluate(fn_scope)
        # Evaluate last expression and return its result
        return self.body[-1].evaluate(fn_scope)

    def evaluate(self, scope):
        # A lambda evaluates to itself
        return self

class Macro(Lambda):
    def __call__(self, scope, *args):
        # Make sure we have the right amount of args for the amount of names
        if len(args) != len(self.names.data):
            raise TypeError("expected %d arguments, got %d" % (len(self.names.data), len(args)))
        # Create a new local function scope
        fn_scope = Scope(scope)
        # Bind each arg to a name in the function scope
        for name, value in zip([x.data for x in self.names.data], args):
            # Do not evaluate each arg before binding
            fn_scope[name] = value
        # Evaluate each expression in lambda body
        for expression in self.body[:-1]:
            expression.evaluate(fn_scope)
        # Evaluate last expression, then evaluate it again in the outer scope
        return self.body[-1].evaluate(fn_scope).evaluate(scope)
