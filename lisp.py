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
        # 
        return List([other, self])
    
    def evaluate(self, scope):
        return self.data
        
    def __repr__(self):
        return repr(self.data)

class Symbol(Atom):
    def __init__(self, data):
        Atom.__init__(self, data)

    def evaluate(self, scope):
        return scope[self.data]

    def __repr__(self):
        return self.data

class List(Atom):
    def __init__(self, data=[]):
        Atom.__init__(self, data)

    def car(self):
        return self.data[0]

    def cdr(self):
        return List(self.data[1:])

    def cons(self, other):
        return List([other] + self.data)
    
    def evaluate(self, scope):
        # A list is evaluated by calling the car as a function with the cdr as arguments
        #return self.car().evaluate(scope)(*[x.evaluate(scope) for x in self.cdr().data])
        fn = self.car()
        while not callable(fn):
            fn = fn.evaluate(scope)
        return fn(scope, *self.cdr().data)

    def __repr__(self):
        return "(%s)" % ' '.join([repr(x) for x in self.data])

class Lambda:
    def __init__(self, names, body):
        self.names = names
        self.body = body

    def fn(self, scope, *args):
        if len(args) != len(self.names.data):
            raise TypeError("expected %d arguments, got %d" % (len(self.names.data), len(args)))
        fn_scope = Scope(scope)
        for name, value in zip([x.data for x in self.names.data], args):
            if value.__class__ != Atom:
                value = value.evaluate(scope)
            fn_scope[name] = value
        for expression in self.body[:-1]:
            expression.evaluate(fn_scope)
        return self.body[-1].evaluate(fn_scope)

    def evaluate(self, scope):
        return self.fn
