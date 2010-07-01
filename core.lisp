;; Lisp Core definitions for Lispy

;; Define Macros
(def defmacro (macro (n a & b) `(def ,n (macro ,a ,@b))))
(defmacro defun (n a & b) `(def ,n (lambda ,a ,@b)))
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
(defmacro cddr (x) `(cdr (cdr ,x)))
(defmacro cadr (x) `(car (cdr ,x)))
(defmacro caddr (x) `(car (cdr (cdr ,x))))
(defmacro cadar (x) `(car (cdr (car ,x))))
(defmacro caddar (x) `(car (cdr (cdr (car ,x)))))

;; Common number functions
(defmacro inc (x) `(+ ,x 1))
(defmacro dec (x) `(- ,x 1))

(defun max (& xs)
  (reduce (lambda (x y) (if (> y x) y x)) (car xs) xs))

(defun min (& xs)
  (reduce (lambda (x y) (if (< y x) y x)) (car xs) xs))

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
(defmacro if-not (p x y) `(if (not ,p) ,x ,y))
(defmacro when (p & b) `(if ,p (do ,@b) nil))
(defmacro when-not (p & b) `(when (not ,p) ,@b))
(def unless when-not)

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

(defun identity (x) x)

(defun contains? (ele coll)
  (reduce (lambda (acc x) (or acc (= x ele))) nil coll))

(defun map (fun coll)
  (reduce (lambda (acc x) (cons (fun x) acc)) '() coll))

(defun reverse (coll) (reduce (lambda (acc x) (cons x acc)) '() coll))

;; Association list functions.
(defun keys (coll) (map car coll))

(defun vals (coll) (map cadr coll))

(defun get (key coll) 
  (reduce (lambda (acc x) (if (= key (car x)) (cadr x) nil)) nil coll))

(defun remove (key coll)
  (filter (lambda (x) (!= key (car x))) coll))

(defun insert (key val coll) (cons '(key val) coll))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Apply
(defmacro apply (f l) `(,f ,@l))

;; Range
(defun range- (x)
  (if (zero? x)
    nil
    (cons x (range- (dec x)))))

;; Stdio macros
(defmacro printf (fs & a) `(print (format ,fs ,@a)))
(defmacro println (x) `(printf "%s\n" ,x))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defmacro constantly (x) `(lambda (& args) ,x))

(defun count (coll) (reduce (lambda (acc x) (inc acc)) 0 coll))

(defun distinct (coll) (reduce (lambda (acc x) (if (contains? x acc) acc (cons x acc))) '() coll))

(defmacro dotimes (name bound & body) `(dolist (,name (range ,bound)) ,@body))

(defmacro every? (pred coll) `(reduce (lambda (acc x) (and acc (,pred x))) t ,coll))

(defun keep (fun coll) (reduce (lambda (acc x) (if (nil? (fun x)) acc (cons (fun x) acc)))))

(defun last (coll)
  (if (nil? (cdr coll))
    (car coll)
    (last (cdr coll))))

(defun repeat (n x)
  (if (zero? n)
    '()
    (cons x (repeat (dec n) x))))

(defun repeatedly (n f)
  (unless (zero? n)
    (cons (f) (repeatedly (dec n) f))))

(defun some (pred coll)
  (reduce (lambda (acc x) (or acc (pred x))) nil coll))

(defun last (list)
  (if (cdr list)
    (last (cdr list))
    list))
