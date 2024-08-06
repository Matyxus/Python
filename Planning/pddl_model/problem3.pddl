(define (problem problem1) (:domain bridge)
 
(:objects
    i1 i2 i3 i4 - islands
    a b c d e f - guys
    t1 t2 - torch
)
 
(:init
    (= (total-cost) 0)
    ; connections between islands
    (connected i1 i2)
    (connected i2 i1)
    (connected i2 i3)
    (connected i2 i4)
    (connected i3 i2)
    (connected i4 i2)
    ; initial positions of guys
    (at a i1)
    (at b i1)
    (at c i1)
    (at d i1)
    (at e i1)
    (at f i1)
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
        (at a i3)
        (at b i3)
        (at c i3)
        (at d i4)
        (at e i4)
        (at f i4)
    )
)
 
(:metric minimize (total-cost))
)
