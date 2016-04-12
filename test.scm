; almost-fibonacci is a non recursive function
; The actual fibonacci function is the fixpoint of almost-fibonacci
(define almost-fibonacci 
  (lambda (f) 
	(lambda (n) 
	  (if (= n 0) 0 
		(if (= n 1) 1 
		  (+ (f (- n 1)) (f (- n 2)))))))) 


; almost-factorial is also non-recursive
(define almost-factorial 
  (lambda (f) 
	(lambda (n) 
	  (if (= n 0) 1 
		(* n (f (- n 1)))))))

(define a (quote 1 2 3 4))
(define b (quote 5 6 7 8))

; Y combinator or fixpoint combinator 
; finds the fixed point of functions.
; takes a non recursive function and returns a version of the function which is 
; recursive.
(define Y (lambda (f) (f (lambda (x) ((Y f) x)))))

(define factorial (Y almost-factorial))
(define fibonacci (Y almost-fibonacci))



(define double (lambda (x) (+ x x)))
(define add (lambda (x y) (+ x y)))

; map takes a function f and a list l
; returns a new list whose elements are obtained by applying f to the elemtes 
; in l
(define map 
  (lambda (f l) 
	(if (null? l) l 
	  (cons (f (car l)) (map f (cdr l))))))

; reduce takes a binary function f, a list l and an initial value i
; recursively apply f to the elements in l, recombine the values and returns it.
(define foldr 
  (lambda (f l i) 
	(if (null? l) i 
	  (f (car l) (foldr f (cdr l) i)))))
(define reduce foldr)


; defun macro allows us to write (defun fn (args) body) instead of
; (define fn (lambda (args) body)
(define defun 
  (macro (name arg-list body)
		 (list (quote define) name (list (quote lambda) arg-list body))))
(defun triple (x) (+ x x x))

; defmacro - similar to defun but for macros
(define defmacro
  (macro (name arg-list body)
		 (list (quote define) name (list (quote macro) arg-list body))))
(defmacro when (condition body)
  (list (quote if) condition body #f))


; An implementation of objects like structures using closure.
(define accumulator 
  (lambda (n)
	(list 
	  (lambda () (set! n (+ n 1))) 
	  (lambda () n))))

