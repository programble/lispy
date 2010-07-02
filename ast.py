# Copyright 2010 Curtis McEnroe <programble@gmail.com>
# Licensed under the GNU GPLv3

from scope import Scope

class Base:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        # Must be of same type to compare
        if self.__class__ == other.__class__:
            return self.data == other.data
        else:
            return False

    def evaluate(self, scope):
        raise NotImplementedError("Abstract Function")

class Atom(Base):
    def __repr__(self):
        return repr(self.data)

    def evaluate(self, scope):
        return self

class Number(Atom):
    pass

class Character(Atom):
    def __repr__(self):
        return '\\' + self.data

class Symbol(Base):
    def __repr__(self):
        return self.data

    def evaluate(self, scope):
        # Resolve symbol
        return scope[self.data]

class Keyword(Atom):
    def __repr__(self):
        return ':' + self.data
    
class List(Base):
    def car(self):
        if len(self.data):
            return self.data[0]
        else:
            return List([])

    def cdr(self):
        # Empty list
        if not len(self.data):
            return List([])
        # Proper list
        elif self.data[-1] == []:
            return List(self.data[1:])
        # Improper list
        else:
            return self.data[1]
    
    def __repr__(self):
        # Empty list
        if self.data == []:
            return "()"
        # Proper list
        elif self.data[-1] == []:
            return '(' + ' '.join([repr(x) for x in self.data[:-1]]) + ')'
        # Improper list
        else:
            return '(' + repr(self.car()) + " . " + repr(self.cdr()) + ')'

    def evaluate(self, scope):
        # Empty list
        if not len(self.data) or self.data == [[]]:
            return Symbol("nil")
        # Improper list
        elif self.data[-1] != []:
            # Call the car with cdr as argument
            return self.car().evaluate(scope)(scope, self.cdr())
        # Proper list
        else:
            # Call the car with cdr as arguments
            return self.car().evaluate(scope)(scope, *self.cdr().data[:-1])

class String(List):
    def car(self):
        if len(self.data):
            return Character(self.data[0])
        else:
            return String("")

    def cdr(self):
        if len(self.data):
            return String("")
        else:
            return String(self.data[1:])

    def __repr__(self):
        return '"' + repr(self.data)[1:-1] + '"'

    def evaluate(self, scope):
        # A string evaluates to itself, as if a quoted list
        return self

class Lambda:
    def __init__(self, bindings, body):
        self.bindings = bindings
        self.body = body

    def evaluate(self, scope):
        return self

    def __call__(self, scope, *args):
        self.bindings.data = self.bindings.data[:-1] # HACK
        # Create a new function-local scope
        local = Scope(scope)
        # Bind each argument to a binding
        bi = ai = 0
        while bi != len(self.bindings.data) and ai != len(self.bindings.data):
            # Optional argument
            if self.bindings.data[bi] == Symbol('?'):
                if ai == len(args):
                    # Nothing supplied for this optional
                    local[self.bindings.data[bi+1].data] = Symbol("nil")
                    break
                else:
                    bi += 1
                    continue
            # Rest argument
            elif self.bindings.data[bi] == Symbol('&'):
                if ai == len(args):
                    raise TypeError("expected at least %d arguments, got %d" % (bi + 1, ai))
                local[self.bindings.data[bi+1].data] = List([x.evaluate(scope) for x in args[ai:]] + [[]])
                break
            # Normal argument
            else:
                # Too many or too few arguments
                if bi == len(self.bindings.data) or ai == len(args):
                    raise TypeError("expected %d arguments, got %d" % (len(self.bindings.data), len(args)))
                local[self.bindings.data[bi].data] = args[ai].evaluate(scope)
            ai += 1
            bi += 1
        self.bindings.data.append([]) # HACK
        # Evaluate each expression in the body (in local function scope)
        for expression in self.body[:-1]:
            expression.evaluate(local)
        # Return the evaluated last expression
        return self.body[-1].evaluate(local)

class Macro(Lambda):
    def __call__(self, scope, *args):
        self.bindings.data = self.bindings.data[:-1] # HACK
        # Create a new function-local scope
        local = Scope(scope)
        # Bind each argument to a binding
        bi = ai = 0
        while bi != len(self.bindings.data) and ai != len(self.bindings.data):
            # Optional argument
            if self.bindings.data[bi] == Symbol('?'):
                if ai == len(args):
                    # Nothing supplied for this optional
                    local[self.bindings.data[bi+1].data] = List([])
                    break
                else:
                    bi += 1
                    continue
            # Rest argument
            elif self.bindings.data[bi] == Symbol('&'):
                if ai == len(args):
                    raise TypeError("expected at least %d arguments, got %d" % (bi + 1, ai))
                local[self.bindings.data[bi+1].data] = List(args[ai:] + [[]])
                break
            # Normal argument
            else:
                # Too many or too few arguments
                if bi == len(self.bindings.data) or ai == len(args):
                    raise TypeError("expected %d arguments, got %d" % (len(self.bindings.data), len(args)))
                local[self.bindings.data[bi].data] = args[ai]
            ai += 1
            bi += 1
        self.bindings.data.append([]) # HACK
        # Evaluate each expression in the body (in local function scope)
        for expression in self.body[:-1]:
            expression.evaluate(local)
        # Return the evaluated last expression after evaluating it again in the outer scope
        return self.body[-1].evaluate(local).evaluate(scope)
