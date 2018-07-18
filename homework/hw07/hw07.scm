(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s)))
  nil
)

(define (caddr s)
  (car (cdr (cdr s))))
  nil
)

(define (sign x)
  (cond
    ((> 0 x) -1)
    ((< 0 x) 1)
    ((= 0 x) 0)
      ))
  nil
)

(define (square x) (* x x))

(define (pow b n)
  (cond
    ((= n 0) 1)
    ((= n 1) b) 
    ((= n 2) (square b))
    ((even? n) (square (pow b (/ n 2))))
    ((odd? n) (* b (square (pow b (/ (- n 1) 2)))))))
  nil
)


(define (ordered? s)
  (cond
    ((null? s) #f)
    ((null? (cdr s)) #t)
    ((> (car s) (car (cdr s))) #f)
    ((= (car s) (car (cdr s))) (ordered? (cdr s)))
    ((<= (car s) (car (cdr s))) (ordered? (cdr s)))))
  nil
)


(define (nodots s)
  (cond 
    ((null? s) nil)
    ((number? s) (cons s nil))
    ((pair? (car s)) (cons (nodots (car s)) (nodots (cdr s))))
    (else (cons (car s) (nodots (cdr s))))

    ))


; Sets as sorted lists

(define (empty? s) (null? s))

(define (contains? s v)
    (cond ((empty? s) false)
          ((= (car s) v) #t) 
          (else (contains? (cdr s) v))
          ))

; Equivalent Python code, for your reference:
;
; def empty(s):
;     return s is Link.empty
;
; def contains(s, v):
;     if empty(s):
;         return False
;     elif s.first > v:
;         return False
;     elif s.first == v:
;         return True
;     else:
;         return contains(s.rest, v)

(define (add s v)
    (cond ((empty? s) (list v))
          ((contains? s v) s)
          ((empty? (cdr s)) (list (car s) v))
          ((> (car s) v) (cons v s))
          (else (cons (car s) (add (cdr s) v))) 
          ))

(define (intersect s t)
    (cond ((or (empty? s) (empty? t)) nil)
          ((= (car s) (car t)) (cons (car s) (intersect (cdr s) (cdr t))))
          ((< (car s) (car t)) (intersect (cdr s) t))
          ((> (car s) (car t)) (intersect s (cdr t)))
          ))

; Equivalent Python code, for your reference:
;
; def intersect(set1, set2):
;     if empty(set1) or empty(set2):
;         return Link.empty
;     else:
;         e1, e2 = set1.first, set2.first
;         if e1 == e2:
;             return Link(e1, intersect(set1.rest, set2.rest))
;         elif e1 < e2:
;             return intersect(set1.rest, set2)
;         elif e2 < e1:
;             return intersect(set1, set2.rest)

(define (union s t)
    (cond ((empty? s) t)
          ((empty? t) s)
          ((= (car s) (car t)) (cons (car s) (union (cdr s) (cdr t))))
          ((< (car s) (car t)) (cons (car s) (union (cdr s) t)))
          ((> (car s) (car t)) (cons (car t) (union (cdr t) s)))
          ))

; Q9 - Survey
(define (survey)
    ; Midsemester Survey: https://goo.gl/forms/DJozOAVLzfXARJGn2
    'parenthesis
)