# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

# TODO: Make this reader not suck

import string
from StringIO import StringIO

from lisp import *

class ReaderError(Exception):
    pass

class Reader:
    def __init__(self, source):
        self.stream = StringIO(source)

    def read(self):
        exprs = []
        token = self.get_token()

        while token != None:
            if token == '(':
                exprs.append(self.get_expr())
            elif token == ')':
                raise ReaderError("Unbalanced parens")
            elif token == "'":
                token = self.get_token()
                if token == None:
                    raise ReaderError("Unexpected EOF")
                elif token == '(':
                    exprs.append(List([Symbol("quote"), self.get_expr()]))
                else:
                    exprs.append(List([Symbol("quote"), token]))
            elif all([x in string.digits for x in token]):
                exprs.append(Atom(int(token)))
            else:
                exprs.append(Symbol(token))
            token = self.get_token()
        return exprs
        
    def get_expr(self):
        token = self.get_token()

        expr = []
        
        while token != ')':
            if token == None:
                raise ReaderError("Unexpected EOF")
            elif token == '(':
                expr.append(self.get_expr())
            elif token == "'":
                token = self.get_token()
                if token == None:
                    raise ReaderError("Unexpected EOF")
                elif token == '(':
                    expr.append(List([Symbol("quote"), self.get_expr()]))
                else:
                    expr.append(List([Symbol("quote"), token]))
            elif all([x in string.digits for x in token]):
                expr.append(Atom(int(token)))
            else:
                expr.append(Symbol(token))
            token = self.get_token()

        return List(expr)

    def get_token(self):
        token = self.stream.read(1)
        if token == '':
            # EOF
            return None
        elif token in string.whitespace:
            return self.get_token()
        elif token in "()'":
            return token
        else:
            while True:
                x = self.stream.read(1)
                if x == '':
                    break
                if x in string.whitespace or x == ")":
                    self.stream.seek(-1, 1)
                    break
                token += x
            return token

