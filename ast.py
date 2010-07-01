# Copyright 2010 Curtis McEnroe <programble@gmail.com>
# Licensed under the GNU GPLv3

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

class Symbol:
    def __repr__(self):
        return self.data

    def evaluate(self, scope):
        # Resolve symbol
        return scope[self.data]
    
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
        if not len(self.data):
            return Symbol("nil")
        # Improper list
        elif self.data[-1] != []:
            # Call the car with cdr as argument
            return self.car().evaluate(scope)(scope, self.cdr())
        # Proper list
        else:
            # Call the car with cdr as arguments
            return self.car().evaluate(scope)(scope, *self.cdr().data)
