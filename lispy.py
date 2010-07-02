#!/usr/bin/env python
# Copyright 2010 Curtis McEnroe <programble@gmail.com>
# Licensed under the GNU GPLv3

import sys
import getopt
import traceback
import readline

from reader import Reader
import core

__version__ = "0.2.0"

def load_lisp_core(filename="core.lisp"):
    # Load up and evaluate core.lisp
    f = open(filename)
    reader = Reader(f.read())
    f.close()
    for expr in reader.read():
        expr.evaluate(core.scope)

def repl():
    global EOFError
    # REPL Banner
    version()
    
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
                print expr.evaluate(core.scope)
            except Exception, e:
                traceback.print_exc()
        source = ""

def evaluate(expr):
    reader = Reader(expr)
    try:
        exprs = reader.read()
    except Exception, e:
        print e
        return
    for expr in exprs:
        try:
            print expr.evaluate(core.scope)
        except Exception, e:
            print e
            return

def evaluate_file(filename):
    try:
        f = open(filename)
    except IOError:
        print "Cannot open file %s" % repr(filename)
        return
    reader = Reader(f.read())
    f.close()
    try:
        exprs = reader.read()
    except Exception, e:
        print e
        return
    for expr in exprs:
        try:
            expr.evaluate(core.scope)
        except Exception, e:
            traceback.print_exc()
            return

def version():
    print "Lispy", __version__
        
def help():
    print "Usage: %s [options] file" % sys.argv[0]
    print "       %s [options] -r" % sys.argv[0]
    print "       %s [options] -e expr" % sys.argv[0]
    print "Options:"
    print "  -r, --repl                  Start an REPL"
    print "  -e EXPR, --evaluate=EXPR    Evaluate a single expression"
    print "  -n, --no-core               Do not load Lisp core"
    print "  -c FILE, --core=FILE        Load the core from a different file"
    print "  --version                   Print version information and exit"
    print
        
def main(argv):
    # Parse command line arguments
    try:
        opts, args = getopt.getopt(argv, "e:rnc:h", ["evaluate=", "repl", "no-core", "core=", "help", "version"])
    except getopt.GetoptError, err:
        print '%s\n' % err
        help()
        sys.exit(1)

    load_core = True
    core_filename = "core.lisp"
        
    for opt, arg in opts:
        if opt in ("-n", "--no-core"):
            load_core = False
        elif opt in ("-c", "--core"):
            core_filename = arg
        elif opt in ("-e", "--evaluate"):
            if load_core:
                load_lisp_core(core_filename)
            evaluate(arg)
            sys.exit()
        elif opt in ("-r", "--repl"):
            if load_core:
                load_lisp_core(core_filename)
            repl()
            sys.exit()
        elif opt == "--version":
            version()
            sys.exit()
        elif opt in ("-h", "--help"):
            help()
            sys.exit()

    if load_core:
        load_lisp_core(core_filename)
    
    # If not given a file to evaluate, start an REPL
    if len(args) == 0:
        repl()
    else:
        evaluate_file(args[0])

if __name__ == "__main__":
    main(sys.argv[1:])
