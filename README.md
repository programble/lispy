Lispy
=====

Lispy is a Lisp implementation in Python. It is influenced by John
McCarthy's paper "Recursive Functions of Symbolic Expressions and
Their Computation by Machine, Part I", which can be found
[here](http://www-formal.stanford.edu/jmc/recursive/); Common Lisp;
Emacs Lisp and Clojure.

Some code is based on [fogus](http://github.com/fogus/)'s
[lithp](http://github.com/fogus/lithp).

Features
--------

Full Feature list coming soon.

Usage
-----

    Usage: lispy [options] file
           lispy [options] -r
           lispy [options] -e expr
    Options:
      -r, --repl        Start an REPL
      -e, --evaluate    Evaluate a single expression
      -n, --no-core     Do not load lisp core
      --version         Print version information and exit

### REPL

To run a Lispy REPL, either run Lispy without a filename, or run
Lispy with the `-r` or `--repl` option.

    lispy
    lispy -r
    lispy --repl

Once the REPL is started, you can enter expressions at the `=>`
prompt. Lispy will evaluate them and show the result.

### Evaluating a File

To evaluate a Lispy source code file, run lispy with the filename as
an argument.

    lispy foobar.lisp

### Evaluating a Single Expression

To evaluate a single expression, run Lispy with the `-e` or
`--evaluate` option and supply the expression as an argument.

    lispy -e "(+ 6 4)"

The expression will be evaluated and its result shown.

### Running with no core

Using the `-n` or `--no-core` option prevents Lispy from loading and
evaluating the Lisp core (`core.lisp`). This can be used in
conjunction with any other option.

Using the core-less mode is not recommended because many standard
definitions are included in `core.lisp`, and without it, Lispy may be
very difficult to use.
