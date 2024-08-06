(define (problem problem1) (:domain bridge) 
	(:objects
	    l r - islands
	    a b c d - guys
	    t0 - torch
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
	    ; crossing speed of each guy
	    (= (crossing-speed a) 1)
	    (= (crossing-speed b) 2)
	    (= (crossing-speed c) 5)
	    (= (crossing-speed d) 8)
	    ; crossing speed of each guy comparisons
	    (greater d a)
	    (greater d b)
	    (greater d c)
	    (greater c b)
	    (greater c a)
	    (greater b a)
	    ; predicates for who holds torch (and which torch)
	    (has a t0)
	    (has b none)
	    (has c none)
	    (has d none)
	)   
	(:goal ; destinations of guys
	    (and 
	        (at a r)
	        (at b r)
	        (at c r)
	        (at d r)
	    )
	)
	(:metric minimize (total-cost))
)


