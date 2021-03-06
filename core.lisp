;; -*- mode: clojure -*-
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

;; Version as string
(defn lispy-version ()
  (if *lispy-version-head*
    (format "Lispy %d.%d.%d-HEAD" (car *lispy-version*) (cadr *lispy-version*) (caddr *lispy-version*))
    (format "Lispy %d.%d.%d" (car *lispy-version*) (cadr *lispy-version*) (caddr *lispy-version*))))

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
(defn reduce (f xs ? (x :not-supplied))
  (if (= x :not-supplied)
    (reduce f (cdr xs) (car xs))
    (if (nil? (cdr xs))
      (f x (car xs))
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

;; Alter!
(defmacro alter! (name func & args)
  `(set! ,name (,func ,name ,@args)))

;; Letfn
(defmacro letfn (bindings & body)
  `(let ,(for (binding bindings) `(,(car binding) (fn ,(cadr binding) ,@(cddr binding))))
     ,@body))

;; Condp
(defmacro condp (pred expr & clauses)
  `(cond
    ,@(for (clause clauses)
        `((,pred ,expr ,(car clause)) ,(cadr clause)))))

;; Stream functions
(defmacro printf (s & a) `(print (format ,s ,@a)))
(defmacro println (s) `(printf "%s\n" ,s))

;; Unit test
(defmacro test (t)
  `(do
     (alter! *test-count* + 1)
     (if ,t
       (do
         (alter! *test-pass-count* + 1)
         (printf " [x] test %s passed\n" (repr (quote ,t))))
       (printf " [ ] test %s failed: %s %s\n" (repr (quote ,t)) (repr ,(cadr t)) (repr ,(car (cdr (cdr t))))))))

(defmacro test-function (func & tests)
  `(do
     (printf "%s tests:\n" (quote ,func))
     (let ((*test-count* 0)
           (*test-pass-count* 0))
       ,@tests
       (printf "%d/%d tests passed\n\n" *test-pass-count* *test-count*))))

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

(defn list (& args)
  args)

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

(defn drop-while (p xs)
  (if (p (car xs))
    (drop-while p (cdr xs))
    xs))

(defn repeat (n x)
  (if (zero? n)
    nil
    (cons x (repeat (dec n) x))))

(defn reverse (xs)
  (reduce (fn (acc x) (cons x acc)) xs nil))

(defn zip (xs ys)
  (if (or (nil? xs) (nil? ys))
    nil
    (cons (cons (car xs) (car ys)) (zip (cdr xs) (cdr ys)))))

(defmacro dolist (bind & body)
  (let ((name (car bind))
        (list (cadr bind)))
    `((fn (xs)
        (if (nil? xs)
          xs
          (do
            (let ((,name (car xs)))
              ,@body)
            (recur (cdr xs)))))
      ,list)))

(defmacro for (binding body) 
  `(map (fn (,(car binding)) ,body) ,(cadr binding)))

(defn interpose (x xs)
  (if (nil? (cdr xs))
    xs
    (cons (car xs) (cons x (interpose x (cdr xs))))))

(defn unique (xs)
  (reduce (fn (acc x) (if (contains? acc x) acc (cons x acc))) xs nil))

(defn proper? (xs)
  (list? (cdr xs)))

(defn improper? (xs)
  (not (proper? xs)))

(defn range (min ? max)
  (if (nil? max)
    (range 0 min)
    (if (= min max)
      nil
      (cons min (range (inc min) max)))))

;; Association list related functions
(defn keys (alist)
  (map car alist))

(defn vals (alist)
  (map cdr alist))

(defn get (alist key ? not-found)
  (if (nil? alist)
    not-found
    (if (= (caar alist) key)
      (cdr (car alist))
      (get (cdr alist) key not-found))))

(defn assoc (alist key val)
    (cons (cons key val) (dissoc alist key)))

(defn dissoc (alist key)
  (filter (fn (x) (not= (car x) key)) alist))

;; String related functions

(defn str-to-list (str)
  (if (= str "")
    nil
    (cons (car str) (str-to-list (cdr str)))))

;; Functions that make functions

(defn constantly (x)
  (fn (& _) x))

;; Repl start-up
(when *repl*
  (println (lispy-version)))
