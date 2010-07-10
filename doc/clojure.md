Lispy for Clojure Developers
============================

Vectors don't exist
-------------------

Vectors don't exist in Lispy. Lispy uses straight lists in most places
where Clojure would use vectors:

Clojure:
    (defn foo [x] x)
Lispy:
    (defn foo (x) x)
Clojure:
    (let [x 2 y 3] (+ x y))
Lispy:
    (let ((x 2) (y 3)) (+ x y))
Clojure:
    (dolist [x (range 5)] (println x))
Lispy:
    (dolist (x (range 6)) (println x))

Any other use of vectors as data must be replaced by quoted lists.

Clojure:
    (def foo [1 2 3])
Lispy:
    (def foo '(1 2 3))

car and cdr
-----------

Lispy takes `car` and `cdr` from Common Lisp. These functions are
`first` and `next`, respectively, in Clojure.

Clojure:
    (first [1 2 3])
Lispy:
    (car '(1 2 3))
Clojure:
    (next [1 2 3])
Lispy:
    (cdr '(1 2 3))
