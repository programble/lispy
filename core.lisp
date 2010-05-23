;; Lisp Core definitions for Lispy

;; Define Macros
(def defmacro (macro (n a b) `(def ,n (macro ,a ,b))))
;(def defmacro (macro (n a & b) `(def ,n (macro ,a ,@b))))
(defmacro defun (n a b) `(def ,n (lambda ,a ,b)))
;(defmacro defun (n a & b) `(def ,n (lambda ,a ,@b)))
(def defn defun)

;; Logical operators
(defmacro and (x y) `(cond (,x (cond (,y t) (t nil))) (t nil)))
(defmacro not (x) `(cond (,x nil) (t t)))
(defmacro nand (x y) `(not (and ,x ,y)))
(defmacro or (x y) `(nand (nand ,x ,x) (nand ,y ,y)))
(defmacro xor (x y) `(or (and ,x (not ,y)) (and (not ,x) ,y)))

;; Comparison operators
(defmacro <= (x y) `(or (= ,x ,y) (< ,x ,y)))
(defmacro >= (x y) `(or (= ,x ,y) (> ,x ,y)))
(defmacro != (x y) `(not (= ,x ,y)))

;; Common List Functions
(defmacro caar (x) `(car (car ,x)))
(defmacro cadr (x) `(car (cdr ,x)))
(defmacro caddr (x) `(car (cdr (cdr ,x))))
(defmacro cadar (x) `(car (cdr (car ,x))))
(defmacro caddar (x) `(car (cdr (cdr (car ,x)))))

;; Predicates
(defun nil? (x)
  (or (= x '()) (= x nil)))

(defun even? (x)
  (= (% x 2) 0))

(defun odd? (x)
  (not (even? x)))

(defun zero? (x)
  (= x 0))

(defun pos? (x)
  (> x 0))

(defun neg? (x)
  (< x 0))

;; More normal flow control
(defmacro if (p x y) `(cond (,p ,x) (t ,y)))
;(defmacro when (p & b) `(if ,p (do ,@b) nil))

;; Append
(defun append (x y)
  (if (nil? x)
    (list y)
    (cons (car x) (append (cdr x) y))))

;; Reduce, one of the great FP functions
(defun reduce (f i xs)
  (if (nil? (cdr xs))
    (f i (car xs))
    (reduce f (f i (car xs)) (cdr xs))))

;; Filter
(defun filter (p xs)
  (if (nil? xs)
    xs
    (if (p (car xs))
      (cons (car xs) (filter p (cdr xs)))
      (filter p (cdr xs)))))

;; Apply
;(defmacro apply (f l) `(,f ,@l))

;; Range (Lisp implementation)
(defun range- (x)
  (if (zero? x)
    nil
    (append (range- (- x 1)) (- x 1))))
