# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

import string

from lisp import *

class Reader:
    def __init__(self, source):
        self.source = source + '\n'
        self.index = -1

    def current(self):
        try:
            return self.source[self.index]
        except IndexError:
            raise SyntaxError("unexpected EOF")

    def next(self):
        self.index += 1
        return self.current()

    def prev(self):
        self.index -= 1
        return self.current()

    def read(self):
        exprs = []
        while self.index + 1 < len(self.source):
            self.next()
            if self.current() in string.whitespace:
                # Skip over whitespace
                continue
            elif self.current() == '(':
                exprs.append(self.read_list())
            elif self.current() == ')':
                raise SyntaxError("unexpected right paren")
            elif self.current() == '"':
                exprs.append(self.read_string())
            elif self.current() in string.digits:
                # Move back one
                self.prev()
                exprs.append(self.read_number())
            elif self.current() == "'":
                exprs.append(self.read_quote())
            else:
                # Move back one
                self.prev()
                exprs.append(self.read_symbol())
        return exprs

    def read_list(self):
        list = []
        while self.next() != ')':
            if self.current() in string.whitespace:
                # Skip over whitespace
                continue
            elif self.current() == '(':
                # Embedded list
                list.append(self.read_list())
            elif self.current() == '"':
                list.append(self.read_string())
            elif self.current() in string.digits:
                # Move back one
                self.prev()
                list.append(self.read_number())
            elif self.current() == "'":
                list.append(self.read_quote())
            else:
                # Move back one
                self.prev()
                list.append(self.read_symbol())
        return List(list)

    def read_string(self):
        string = ""
        while self.next() != '"':
            string += self.current()
        return String(string)

    def read_number(self):
        number = ""
        while self.next() not in string.whitespace + ")":
            number += self.current()
        if '.' in number:
            try:
                number = float(number)
            except ValueError:
                raise
        else:
            try:
                number = int(number)
            except ValueError:
                raise
        self.prev()
        return Atom(number)

    def read_symbol(self):
        symbol = ""
        while self.next() not in string.whitespace + ")":
            symbol += self.current()
        self.prev()
        return Symbol(symbol)

    def read_quote(self):
        expr = [Symbol("quote")]
        self.next()
        if self.current() == '(':
            expr.append(self.read_list())
        else:
            self.prev()
            expr.append(self.read_symbol())
        return List(expr)
