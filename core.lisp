;; Copyright 2010 Curtis McEnroe <programble@gmail.com>
;; Licensed under the GNU GPLv3

;; Def-related macros
(def defmacro (macro (n a & b) `(def ,n (macro ,a ,@b))))
(defmacro defun (n a & b) `(def ,n (lambda ,a ,@b)))

;; Logical operators
(defmacro and (x y) `(cond (,x (cond (,y t) (t nil))) (t nil)))
(defmacro not (x) `(cond (,x nil) (t t)))
(defmacro nand (x y) `(not (and ,x ,y)))
(defmacro or (x y) `(nand (nand ,x ,x) (nand ,y ,y)))
(defmacro xor (x y) `(or (and ,x (not ,y)) (and (not ,x) ,y)))

;; Comparison operators
(defmacro <= (x y) `(or (= ,x ,y) (< ,x ,y)))
(defmacro >= (x y) `(or (= ,x ,y) (> ,x ,y)))
(defmacro not= (x y) `(not (= ,x ,y)))

;; Common List Functions
(defmacro caar (x) `(car (car ,x)))
(defmacro cddr (x) `(cdr (cdr ,x)))
(defmacro cadr (x) `(car (cdr ,x)))
(defmacro caddr (x) `(car (cdr (cdr ,x))))
(defmacro cadar (x) `(car (cdr (car ,x))))
(defmacro caddar (x) `(car (cdr (cdr (car ,x)))))

;; Predicates
(defmacro nil? (x) `(cond (,x nil) (t)))

;; Flow control
(defmacro if (p x y) `(cond (,p ,x) (t ,y)))
(defmacro when (p & b) `(if ,p (do ,@b) nil))

;; Apply
(defmacro apply (f l) `(,f ,@(eval l)))

;; Identity (does nothing, woot woot)
(defun identity (x) x)

;; Reduce
(defun reduce (f xs ? x)
  (if (nil? x)
    (reduce f xs (car xs))
    (if (nil? xs)
      x
      (reduce f (cdr xs) (f x (car xs))))))

;; Association lists (maps)
(defun assoc (map key val)
  (cons (cons key val) map))

;; Stream functions
(defmacro printf (s & a) `(print (format ,s ,@a)))
(defmacro println (s) `(printf "%s\n" ,s))

;; Unit test
(defmacro test (t)
  `(do
     (def *test-count* (+ *test-count* 1))
     (if ,t
       (do
         (def *test-pass-count* (+ *test-pass-count* 1))
         (printf " [x] test %s passed\n" (repr (quote ,t))))
       (printf " [ ] test %s failed: %s\n" (repr (quote ,t)) (repr ,(cadr t))))))

(defmacro test-function (func & tests)
  `(do
     (printf "%s tests:\n" (quote ,func))
     (def *test-count* 0)
     (def *test-pass-count* 0)
     ,@tests
     (printf "%d/%d tests passed\n\n" *test-pass-count* *test-count*)))
