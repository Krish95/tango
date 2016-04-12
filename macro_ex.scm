(define adder (macro (x) (+ x 1)))
(define when (macro (test branch) (list (quote if) test (list (quote begin) branch) (quote ()))))
(define t-becomes-nil (macro (var) (list (quote if) (list (quote =) var (quote #t)) (list (quote set!) var (quote ())) (quote ()))))
(define inc (macro (var) (list (quote set!) var (list (quote +) var (quote 1)))))

(define cond (macro (expr stmt) ()))

(cond ((> 3 2) (quote greater))
      ((< 3 2) (quote less)))   