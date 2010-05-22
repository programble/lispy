#!/usr/bin/env python
# Copyright 2010 Curtis (Programble) <programble@gmail.com>
# Licensed under the GNU GPLv3

from reader import Reader
import core

while True:
    source = raw_input("=> ")
    reader = Reader(source)
    try:
        exprs = reader.read()
    except Exception, e:
        print e
    for expr in exprs:
        try:
            print expr.evaluate(core.global_scope)
        except Exception, e:
            print e
