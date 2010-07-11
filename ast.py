# Copyright 2010 Curtis McEnroe <programble@gmail.com>
# Licensed under the GNU GPLv3

from scope import Scope

class Base:
    def __init__(self, data):
        self.data = data
        self.meta = {"name": None}

    def __eq__(self, other):
        # Must be of same type to compare
        if self.__class__ == other.__class__:
            return self.data == other.data
        else:
            return False

    def __str__(self):
        return str(self.data)

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
        if ' ' in self.data or ')' in self.data:
            return '|' + self.data + '|'
        else:
            return self.data

    def evaluate(self, scope):
        # Resolve symbol
        return scope[self.data]

class Keyword(Atom):
    def __repr__(self):
        return ':' + self.data
    
class List(Base):
    def car(self):
        if len(self.data) and self.data != [[]]:
            return self.data[0]
        else:
            return List([])

    def cdr(self):
        # Empty list
        if not len(self.data) or self.data == [[]]:
            return List([])
        # Proper list
        elif self.data[-1] == [] and len(self.data) > 2:
            return List(self.data[1:])
        elif self.data[1] == []:
            return List([])
        # Improper list
        else:
            return self.data[1]
    
    def __repr__(self):
        # Empty list
        if self.data == []:
            return "nil"
        # Proper list
        elif self.data[-1] == []:
            return '(' + ' '.join([repr(x) for x in self.data[:-1]]) + ')'
        # Improper list
        else:
            return '(' + repr(self.car()) + " . " + repr(self.cdr()) + ')'

    def __str__(self):
        return repr(self)

    def evaluate(self, scope):
        # Empty list
        if not len(self.data) or self.data == [[]]:
            return self
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
        if not len(self.data):
            return String("")
        else:
            return String(self.data[1:])

    def __repr__(self):
        return '"' + repr(self.data)[1:-1] + '"'

    def __str__(self):
        return str(self.data)

    def evaluate(self, scope):
        # A string evaluates to itself, as if a quoted list
        return self

class Lambda:
    def __init__(self, scope, bindings, body):
        self.bindings = bindings
        self.body = body
        self.scope = scope
        self.meta = {"name": None}

    def evaluate(self, scope):
        return self

    def __call__(self, scope, *args):
        if scope.has_key("recur") and scope["recur"] == self:
            # This is recursion, don't create a new scope
            local = scope
        else:
            # Calling scope -> creating scope -> local scope
            # Clone creation scope so its parent can be set to calling scope
            creation = Scope()
            creation.bindings = self.scope.bindings
            creation.parent = scope
            # Create a new scope
            local = Scope(creation)
        # Bind `recur` to self (to alow for recursion from anonymous functions)
        local["recur"] = self
        # Bind each argument to a binding
        bi = ai = 0
        bindings = self.bindings.data[:-1]
        while bi != len(bindings) and ai != len(bindings):
            # Optional argument
            if bindings[bi] == Symbol('?'):
                if ai >= len(args):
                    if bindings[bi+1].__class__ == List:
                        # A default value is supplied
                        local[bindings[bi+1].car().data] = bindings[bi+1].cdr().car().evaluate(local)
                    else:
                        # Nothing supplied for this optional and no default value
                        local[bindings[bi+1].data] = List([])
                    ai -= 1
                    bi += 1
                else:
                    if bindings[bi+1].__class__ == List:
                        # A default value is supplied, replace with just the symbol
                        local[bindings[bi+1].car().data] = args[ai].evaluate(scope)
                    else:
                        local[bindings[bi+1].data] = args[ai].evaluate(scope)
                    bi += 1
                    #continue
            # Rest argument
            elif bindings[bi] == Symbol('&'):
                if ai == len(args):
                    #raise TypeError("expected at least %d arguments, got %d" % (bi + 1, ai))
                    local[bindings[bi+1].data] = List([])
                else:
                    local[bindings[bi+1].data] = List([x.evaluate(scope) for x in args[ai:]] + [[]])
                break
            # Normal argument
            else:
                # Too many or too few arguments
                if bi >= len(bindings) or ai >= len(args):
                    raise TypeError("expected %d arguments, got %d" % (len(bindings), len(args)))
                local[bindings[bi].data] = args[ai].evaluate(scope)
            ai += 1
            bi += 1
        # Evaluate each expression in the body (in local function scope)
        for expression in self.body[:-1]:
            expression.evaluate(local)
        # Return the evaluated last expression
        return self.body[-1].evaluate(local)

class Macro(Lambda):
    def __call__(self, scope, *args):
        # Create a new function-local scope
        local = Scope(scope)
        # Bind each argument to a binding
        bindings = self.bindings.data[:-1]
        bi = ai = 0
        while bi != len(bindings) and ai != len(bindings):
            # Optional argument
            if bindings[bi] == Symbol('?'):
                if ai >= len(args):
                    if bindings[bi+1].__class__ == List:
                        # A default value is supplied
                        local[bindings[bi+1].car().data] = bindings[bi+1].cdr().car()
                    else:
                        # Nothing supplied for this optional and no default value
                        local[bindings[bi+1].data] = List([])
                    ai -= 1
                    bi += 1
                else:
                    if bindings[bi+1].__class__ == List:
                        # A default value is supplied, replace with just the symbol
                        local[bindings[bi+1].car().data] = args[ai]
                    else:
                        local[bindings[bi+1].data] = args[ai]
                    bi += 1
                    #continue
            # Rest argument
            elif bindings[bi] == Symbol('&'):
                if ai == len(args):
                    #raise TypeError("expected at least %d arguments, got %d" % (bi + 1, ai))
                    local[bindings[bi+1].data] = List([])
                else:
                    local[bindings[bi+1].data] = List(list(args[ai:]) + [[]])
                break
            # Normal argument
            else:
                # Too many or too few arguments
                if bi == len(bindings) or ai == len(args):
                    raise TypeError("expected %d arguments, got %d" % (len(bindings), len(args)))
                local[bindings[bi].data] = args[ai]
            ai += 1
            bi += 1
        # Evaluate each expression in the body (in local function scope)
        for expression in self.body[:-1]:
            expression.evaluate(local)
        # Return the evaluated last expression after evaluating it again in the outer scope
        return self.body[-1].evaluate(local).evaluate(scope)
