;; Copyright 2010 Curtis McEnroe <programble@gmail.com>
;; Licensed under the GNU GPLv3

;; Def-related macros
(def defmacro (macro (n a & b) `(def ,n (macro ,a ,@b))))
(defmacro defn (n a & b) `(def ,n (fn ,a ,@b)))

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
(defn nil? (x)
  (cond (x nil) (t)))

;; Flow control
(defmacro if (p x y) `(cond (,p ,x) (t ,y)))
(defmacro when (p & b) `(if ,p (do ,@b) nil))

;; Apply
(defmacro apply (f l) `(,f ,@(eval l)))

;; Identity (does nothing, woot woot)
(defn identity (x) x)

;; Reduce
(defn reduce (f xs ? x)
  (if (nil? x)
    (reduce f (cdr xs) (car xs))
    (if (nil? xs)
      x
      (reduce f (cdr xs) (f x (car xs))))))

;; Filter
(defn filter (p xs)
  (if (nil? xs)
    xs
    (if (p (car xs))
      (cons (car xs) (filter p (cdr xs)))
      (filter p (cdr xs)))))

;; Map
(defn map (f xs)
  (if (nil? xs)
    xs
    (cons (f (car xs)) (map f (cdr xs)))))

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
       (printf " [ ] test %s failed: %s %s\n" (repr (quote ,t)) (repr ,(cadr t)) (repr ,(car (cdr (cdr t))))))))

(defmacro test-function (func & tests)
  `(do
     (printf "%s tests:\n" (quote ,func))
     (def *test-count* 0)
     (def *test-pass-count* 0)
     ,@tests
     (printf "%d/%d tests passed\n\n" *test-pass-count* *test-count*)))

;; Number-related functions
(defmacro inc (x) `(+ ,x 1))
(defmacro dec (x) `(- ,x 1))

(defn max (& xs)
  (reduce (fn (x y) (if (> y x) y x)) xs))

(defn min (& xs)
  (reduce (fn (x y) (if (< y x) y x)) xs))

;; Number-related predicates
(defn even? (x)
  (= (% x 2) 0))

(defn odd? (x)
  (not (even? x)))

(defn zero? (x)
  (= x 0))

(defn pos? (x)
  (> x 0))

(defn neg? (x)
  (< x 0))

;; List-related functions
(defn contains? (xs key)
  (if (nil? xs)
    nil
    (if (= (car xs) key)
      t
      (contains? (cdr xs) key))))

(defn count (xs)
  (reduce (fn (acc _) (inc acc)) xs 0))

(defn nth (xs i)
  (if (zero? i)
    (car xs)
    (nth (cdr xs) (dec i))))

(defn last (xs)
  (if (nil? (cdr xs))
    (car xs)
    (last (cdr xs))))

(defn append (xs y)
  (if (nil? xs)
    (cons y nil)
    (cons (car xs) (append (cdr xs) y))))

(defn concat (xs ys)
  (if (nil? xs)
    ys
    (cons (car xs) (concat (cdr xs) ys))))

(defn take (n xs)
  (if (zero? n)
    nil
    (cons (car xs) (take (dec n) (cdr xs)))))

(defn take-while (p xs)
  (when (p (car xs))
    (cons (car xs) (take-while p (cdr xs)))))

(defn drop (n xs)
  (if (zero? n)
    xs
    (drop (dec n) (cdr xs))))

(defn repeat (n x)
  (if (zero? n)
    nil
    (cons x (repeat (dec n) x))))

(defn reverse (xs)
  (if (nil? xs)
    xs
    (append (reverse (cdr xs)) (car xs))))

(defn zip (xs ys)
  (if (or (nil? xs) (nil? ys))
    nil
    (cons (cons (car xs) (car ys)) (zip (cdr xs) (cdr ys)))))

;; Association list related functions
(defn keys (alist)
  (map car alist))

(defn vals (alist)
  (map cdr alist))

(defn get (alist key)
  (if (nil? alist)
    nil
    (if (= (caar alist) key)
      (cdr (car alist))
      (get (cdr alist) key))))

(defn assoc (alist key val)
    (cons (cons key val) (dissoc alist key)))

(defn dissoc (alist key)
  (filter (fn (x) (not= (car x) key)) alist))
