;; Copyright 2010 Curtis McEnroe <programble@gmail.com>
;; Licensed under the GNU GPLv3

(test-function =
               (test (= 1 1))
               (test (= :foo :foo))
               (test (= 'foo 'foo))
               (test (= '(1 2) '(1 2)))
               (test (= '(1 . 2) '(1 . 2)))
               (test (= '() ()))
               (test (= '() nil)))

(test-function car
               (test (= (car '(:foo :bar :baz)) :foo))
               (test (= (car '(:foo . :bar)) :foo))
               (test (= (car '(:foo)) :foo))
               (test (= (car '()) nil)))

(test-function cdr
               (test (= (cdr '(:foo . :bar)) :bar))
               (test (= (cdr '(:foo :bar)) '(:bar)))
               (test (= (cdr '(:foo :bar :baz)) '(:bar :baz)))
               (test (= (cdr '(:foo)) nil))
               (test (= (cdr '()) nil)))

(test-function cons
               (test (= (cons :foo :bar) '(:foo . :bar)))
               (test (= (cons :foo nil) '(:foo)))
               (test (= (cons nil nil) '(nil)))
               (test (= (cons :foo (cons :bar nil)) '(:foo :bar))))

(test-function cond
               (test (= (cond (:foo :bar)) :bar))
               (test (= (cond (nil :foo)) nil))
               (test (= (cond (nil :foo) (:bar)) :bar))
               (test (= (cond (nil :foo) (:bar :baz)) :baz)))

(test-function def
               (def *test* :foo)
               (test (= *test* :foo))
               (def *test* :bar)
               (test (= *test* :bar)))

(test-function syntax-quote
               (test (= `(foo ,*test*) '(foo :bar)))
               (def *test* '(:bar :baz))
               (test (= `(foo ,@*test*) '(foo :bar :baz))))

(test-function list
               (def *test* :foo)
               (test (= (list *test* :bar) '(:foo :bar))))

(test-function let
               (let ((foo :foo))
                 (test (= foo :foo)))
               (let ((foo :foo)
                     (bar (list foo :bar)))
                 (test (= bar '(:foo :bar))))
               (def *test* :foo)
               (let ((*test* :bar))
                 (test (= *test* :bar))))

(test-function do
               (test (= (do :foo :bar :baz) :baz)))

(test-function dolist
               (test (= (dolist (x '(:foo :bar :baz)) x) :baz)))

(test-function +
               (test (= (+) 0))
               (test (= (+ 1) 1))
               (test (= (+ 1 2) 3))
               (test (= (+ 1 2 3) 6)))

(test-function -
               (test (= (-) 0))
               (test (= (- 1) -1))
               (test (= (- 4 3) 1))
               (test (= (- 1 2 3) -4)))

(test-function *
               (test (= (*) 1))
               (test (= (* 2) 2))
               (test (= (* 2 3) 6))
               (test (= (* 2 3 4) 24)))

(test-function /
               (test (= (/) 0))
               (test (= (/ 2) 2))
               (test (= (/ 1.0 2.0) 0.5))
               (test (= (/ 1.0 2.0 2.0) 0.25)))

(test-function %
               (test (= (% 4 2) 0))
               (test (= (% 5 2) 1)))

(test-function <
               (test (< 1 2))
               (test (= (< 2 1) nil)))

(test-function >
               (test (> 2 1))
               (test (= (> 1 2) nil)))

(test-function macroexpand
               (def *test* (macro (x) `(+ ,x)))
               (test (= (macroexpand (*test* 1)) '(+ 1)))
               (def *test* (macro (x) `(+ ,x ,x)))
               (def *test-test* (macro (x) `(*test* ,x)))
               (test (= (macroexpand (*test-test* 1)) '(+ 1 1))))

(test-function format
               (test (= (format "%s" "foo") "foo"))
               (test (= (format "%s" :foo) "foo"))
               (test (= (format "%d" 2) "2"))
               (test (= (format "%s" 'foo) "foo")))

(test-function repr
               (test (= (repr 1) "1"))
               (test (= (repr "foo") "\"foo\""))
               (test (= (repr :foo) ":foo"))
               (test (= (repr '(1 . 2)) "(1 . 2)"))
               (test (= (repr '(1 2)) "(1 2)")))
