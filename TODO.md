TODO List
=========

Features
--------

 * Python interop
 * <del>Destructive set functions (`set!`, etc)</del>

Reader
------

 * Make quotes able to read more than just symbols and lists (allow
   quoting of anything using the quote reader macros)

AST
---

### Lambda

 * Do something to improve recursion
 * <del>Prevent new scopes being created on recursion</del>

Python Core
-----------

Lisp Core
---------

 * Fix `reduce` somehow (does not work for `t`/`nil` stuff)
 * Fix `reverse` (possibly a problem in `append`)

Scope
-----

