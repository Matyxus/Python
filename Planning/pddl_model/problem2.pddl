(define (problem problem1) (:domain bridge)
 
(:objects
    l r - islands
    a b c d e f - guys
    t1 t2 - torch
)
 
(:init
    (= (total-cost) 0)
    ; connections between islands
    (connected l r)
    (connected r l)
    ; initial positions of guys
    (at a l)
    (at b l)
    (at c l)
    (at d l)
    (at e l)
    (at f l)
    ; crossing speed of each guy
    (= (crossing-speed a) 1)
    (= (crossing-speed b) 2)
    (= (crossing-speed c) 3)
    (= (crossing-speed d) 4)
    (= (crossing-speed e) 5)
    (= (crossing-speed f) 6)
    ; crossing speed of each guy comparisons
    (greater f a)
    (greater f b)
    (greater f c)
    (greater f d)
    (greater f e)
    (greater e a)
    (greater e b)
    (greater e c)
    (greater e d)
    (greater d a)
    (greater d b)
    (greater d c)
    (greater c a)
    (greater c b)
    (greater b a)
    ; predicates for who holds torch (and which torch)
    (has a t1)
    (has b none)
    (has c none)
    (has d none)
    (has e none)
    (has f t2)
)   
; destinations of guys
(:goal
    (and 
        (at a r)
        (at b r)
        (at c r)
        (at d r)
        (at e r)
        (at f r)
    )
)
 
(:metric minimize (total-cost))
)
