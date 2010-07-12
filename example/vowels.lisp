;; -*- mode: clojure -*-
;; Copyright 2010 Curtis McEnroe <programble@gmail.com>
;; Licensed under the GNU GPLv3

;; Lispy example to count vowels in input

(def vowels '(\a \e \i \o \u))

(defn upper? (c)
  (and (>= c \A) (<= c \Z)))

(defn lower (c)
  (if (upper? c)
    (chr (+ (ord c) 32))
    c))

(defn str-lower (s)
  (apply str (map lower (str-to-list s))))

(defn vowel? (c)
  (contains? vowels c))

(defn count-vowels (s)
  (count (filter vowel? (str-to-list s))))

(print "Enter a phrase: ")
(let ((input (read-line))
      (vowel-count (count-vowels (str-lower input)))
      (unique-vowel-count (count-vowels (apply str (unique (str-to-list (str-lower input)))))))
  (println (str "The phrase contains " vowel-count " vowels."))
  (println (str "The phrase contains " unique-vowel-count " unique vowels.")))
