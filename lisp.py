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
        x = repr(self.data)
        return '"' + x[1:-1] + '"'
    
class Lambda:
    def __init__(self, names, body):
        self.names = names
        self.body = body

    def __call__(self, scope, *args):
        # Make sure we have the right amount of args for the amount of names
        if Symbol('&') in self.names.data:
            if len(args) < len(self.names.data) - 1:
                raise TypeError("expected %d arguments, got %d" % (len(self.names.data) - 1, len(args)))
        else:
            if len(args) != len(self.names.data):
                raise TypeError("expected %d arguments, got %d" % (len(self.names.data), len(args)))
        # Create a new local function scope
        if scope.bindings.has_key("*current-lambda*") and scope["*current-lambda*"] == self:
            fn_scope = scope
        else:
            fn_scope = Scope(scope)
        # Marker
        fn_scope["*current-lambda*"] = self
        # Bind each arg to a name in the function scope
        for i in range(len(args)):
            name = self.names.data[i].data
            # Arity
            if name == '&':
                fn_scope[self.names.data[i+1].data] = List([a.evaluate(scope) for a in args[i:]])
                break
            fn_scope[name] = args[i].evaluate(scope)
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
        if Symbol('&') in self.names.data:
            if len(args) < len(self.names.data) - 1:
                raise TypeError("expected %d arguments, got %d" % (len(self.names.data) - 1, len(args)))
        else:
            if len(args) != len(self.names.data):
                raise TypeError("expected %d arguments, got %d" % (len(self.names.data), len(args)))
        # Create a new local function scope
        fn_scope = Scope(scope)
        # Bind each arg to a name in the function scope
        for i in range(len(args)):
            name = self.names.data[i].data
            # Arity
            if name == '&':
                fn_scope[self.names.data[i+1].data] = List(args[i:])
                break
            fn_scope[name] = args[i]
        # Evaluate each expression in lambda body
        for expression in self.body[:-1]:
            expression.evaluate(fn_scope)
        # Evaluate last expression, then evaluate it again in the outer scope
        return self.body[-1].evaluate(fn_scope).evaluate(scope)
