#!/usr/bin/env python
# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

import traceback
import readline

from reader import Reader
import core

# Load up and evaluate core.lisp
f = open("core.lisp")
reader = Reader(f.read())
f.close()
for expr in reader.read():
    expr.evaluate(core.global_scope)

# REPL Banner
print "Lispy 0.1.0"

source = ""
while True:
    # Get a new source line
    try:
        if source == "":
            source = raw_input("=> ") + '\n'
        else:
            source += raw_input() + '\n'
    except KeyboardInterrupt, EOFError:
        break
    # Read the source line
    reader = Reader(source)
    try:
        exprs = reader.read()
    except EOFError:
        # Need more input
        continue
    except Exception, e:
        print e
        source = ""
        continue
    # Evaluate the source line
    for expr in exprs:
        try:
            print expr.evaluate(core.global_scope)
        except Exception, e:
            traceback.print_exc()
    source = ""
