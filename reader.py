# Copyright 2010 Curtis McEnroe <programble@gmail.com>
# Licensed under the GNU GPLv3

import string

from ast import *

class Reader:
    def __init__(self, source, filename=None):
        self.filename = filename
        self.lineno = 1
        self.source = source + '\n'
        self.index = -1

    def current(self):
        try:
            return self.source[self.index]
        except IndexError:
            raise EOFError("unexpected EOF")

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
                if self.current() == '\n':
                    self.lineno += 1
                # Ignore
                continue
            elif self.current() == ';':
                # Comment until EOL
                while self.next() != '\n':
                    pass
                self.lineno += 1
                continue
            elif self.current() == '(':
                exprs.append(self.read_list())
            elif self.current() == ')':
                raise SyntaxError("unexpected right parenthesis")
            elif self.current() == '"':
                exprs.append(self.read_string())
            elif self.current() in string.digits:
                self.prev()
                exprs.append(self.read_number())
            elif self.current() == '-':
                if self.next() in string.digits:
                    self.prev()
                    self.prev()
                    exprs.append(self.read_number())
                else:
                    self.prev()
                    self.prev()
                    exprs.append(self.read_symbol())
            elif self.current() in "'`,":
                exprs.append(self.read_quote())
            elif self.current() == ':':
                exprs.append(self.read_keyword())
            elif self.current() == '\\':
                exprs.append(self.read_character())
            else:
                self.prev()
                exprs.append(self.read_symbol())
            exprs[-1].meta["file"] = self.filename
            exprs[-1].meta["line"] = self.lineno
        return exprs

    def read_list(self):
        list = []
        proper = True
        while self.next() != ')':
            if self.current() in string.whitespace:
                if self.current() == '\n':
                    self.lineno += 1
                # Ignore
                continue
            elif self.current() == ';':
                # Comment until EOL
                while self.next() != '\n':
                    pass
                self.lineno += 1
                continue
            elif self.current() == '(':
                # List in a list in a list in a list
                list.append(self.read_list())
            elif self.current() == '.':
                # Improper list
                proper = False
            elif self.current() == '"':
                list.append(self.read_string())
            elif self.current() in string.digits:
                self.prev()
                list.append(self.read_number())
            elif self.current() == '-':
                if self.next() in string.digits:
                    self.prev()
                    self.prev()
                    list.append(self.read_number())
                else:
                    self.prev()
                    self.prev()
                    list.append(self.read_symbol())
            elif self.current() in "'`,":
                list.append(self.read_quote())
            elif self.current() == ':':
                list.append(self.read_keyword())
            elif self.current() == '\\':
                list.append(self.read_character())
            else:
                self.prev()
                list.append(self.read_symbol())
            list[-1].meta["file"] = self.filename
            list[-1].meta["line"] = self.lineno
        if proper and len(list):
            return List(list + [[]])
        else:
            return List(list)
        return l

    def read_string(self):
        string = ""
        while self.next() != '"':
            # Escape codes
            if self.current() == '\\':
                escape = self.next()
                if escape == 'n':
                    string += '\n'
                elif escape == 'r':
                    string += '\r'
                elif escape == '"':
                    string += '"'
                # TODO: Add more escape codes
                else:
                    string += '\\' + escape
            else:
                string += self.current()
        return String(string)

    def read_number(self):
        number = ""
        while self.next() not in string.whitespace + ')':
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
        return Number(number)

    def read_quote(self):
        if self.current() == "'":
            expr = [Symbol("quote")]
        elif self.current() == '`':
            expr = [Symbol("syntax-quote")]
        elif self.current() == ',':
            if self.next() == '@':
                expr = [Symbol("unquote-splice")]
            else:
                self.prev()
                expr = [Symbol("unquote")]
        self.next()
        if self.current() == '(':
            expr.append(self.read_list())
        else:
            self.prev()
            expr.append(self.read_symbol())
        return List(expr + [[]])

    def read_keyword(self):
        keyword = ""
        while self.next() not in string.whitespace + ')':
            keyword += self.current()
        self.prev()
        return Keyword(keyword)

    def read_character(self):
        return Character(self.next())

    def read_symbol(self):
        symbol = ""
        while self.next() not in string.whitespace + ')':
            if self.current() == '|':
                while self.next() != '|':
                    symbol += self.current()
            else:
                symbol += self.current()
        self.prev()
        return Symbol(symbol)

