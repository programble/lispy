;; Copyright 2010 Curtis McEnroe <programble@gmail.com>
;; Licensed under the GNU GPLv3

(def *test* nil)

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
               (test (= (cons :foo (cons :bar nil)) '(:foo :bar))))

(test-function cond
               (test (= (cond (:foo :bar)) :bar))
               (test (= (cond (nil :foo)) nil))
               (test (= (cond (nil :foo) (:bar)) :bar))
               (test (= (cond (nil :foo) (:bar :baz)) :baz)))

(test-function syntax-quote
               (set! *test* :bar)
               (test (= `(foo ,*test*) '(foo :bar)))
               (set! *test* '(:bar :baz))
               (test (= `(foo ,@*test*) '(foo :bar :baz))))

(test-function list
               (set! *test* :foo)
               (test (= (list *test* :bar) '(:foo :bar))))

(test-function let
               (let ((foo :foo))
                 (test (= foo :foo)))
               (let ((foo :foo)
                     (bar (list foo :bar)))
                 (test (= bar '(:foo :bar))))
               (set! *test* :foo)
               (let ((*test* :bar))
                 (test (= *test* :bar))))

(test-function do
               (test (= (do :foo :bar :baz) :baz)))

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
               (test (= (/) 1))
               (test (= (/ 2.0) 0.5))
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
               (set! *test* (macro (x) `(+ ,x)))
               (test (= (macroexpand (*test* 1)) '(+ 1)))
               (set! *test* (macro (x) `(+ ,x ,x)))
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

(test-function str
               (test (= (str) ""))
               (test (= (str 1 2) "12")))

(test-function chr
               (test (= (chr 97) \a)))

(test-function ord
               (test (= (ord \a) 97)))

(test-function list?
               (test (list? '(1 2 3)))
               (test (list? nil))
               (test (not (list? 1))))

(test-function number?
               (test (number? 1))
               (test (number? 2.0))
               (test (not (number? \a))))

(test-function character?
               (test (character? \a))
               (test (not (character? 97))))

(test-function symbol?
               (test (symbol? 'foo))
               (test (not (symbol? nil))))

(test-function keyword?
               (test (keyword? :foo))
               (test (not (keyword? 'foo))))

(test-function string?
               (test (string? "foo"))
               (test (not (string? \f))))

(test-function fn?
               (test (fn? (fn () nil)))
               (test (not (fn? test))))

(test-function macro?
               (test (macro? test))
               (test (not (macro? (fn () nil)))))
