#!/usr/bin/env python
# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

from reader import Reader
import core

import traceback

# Load up and evaluate core.lisp
f = open("core.lisp")
reader = Reader(f.read())
f.close()
for expr in reader.read():
    expr.evaluate(core.global_scope)

while True:
    source = raw_input("=> ")
    reader = Reader(source)
    try:
        exprs = reader.read()
    except Exception, e:
        print e
    for expr in exprs:
        try:
            x = expr.evaluate(core.global_scope)
            print x
        except Exception, e:
            traceback.print_exc()
