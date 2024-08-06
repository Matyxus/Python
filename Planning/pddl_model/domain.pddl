(define (domain bridge)  ; name of the domain
 
    (:requirements
        :typing            ; we will use types of objects
        :action-costs      ; actions have associated costs
        :disjunctive-preconditions ; or predicate
    )

    (:types islands guys torch - object)

    (:constants
        none - torch ; invalid torch
    )

    (:predicates
        (connected ?i1 ?i2 - islands); connection between islands
        (at ?g - guys ?i - islands); current guy location (one of the islands)
        (has ?g - guys ?t - torch); current guy has torch "t" ("none" for not having torch)
        (greater ?g1 ?g2 - guys); true if crossing speed of "g1" is >= "g2"
    )

    (:functions
      (crossing-speed ?g - guys) - number ; crossing speed of each guy over bridge (time)
      (total-cost) - number ; sum of total time spent on going over bridges
    )

	; --------------------- Actions ---------------------

	(:action pass-torch
        :parameters (?g1 ?g2 - guys ?t - torch ?i - islands)
        :precondition (and 
        	; Are guys on the same island?
        	(at ?g1 ?i)
        	(at ?g2 ?i)
        	; Does one have torch and other does not ?
        	(has ?g1 ?t)
        	(not (has ?g1 none))
        	(has ?g2 none)

        )
        ; Change ownership of torch, set other to not have torch
        :effect  (and 
        	(not (has ?g1 ?t))
        	(has ?g1 none)
        	(not (has ?g2 none))
        	(has ?g2 ?t)
        )
    )

    (:action cross-alone
        :parameters (?g - guys ?i1 ?i2 - islands)
        :precondition (and 
        	(at ?g ?i1) ; Is guy on the island?
        	(connected ?i1 ?i2) ; Are islands connected?
        	; Does he have a torch?
        	(not (has ?g none))

        )
        ; Change positions, increase cost
        :effect  (and 
        	(not (at ?g ?i1))
        	(at ?g ?i2)
        	(increase (total-cost) (crossing-speed ?g))
        )
    )


    (:action cross-together
        :parameters (?g1 ?g2 - guys ?i1 ?i2 - islands)
        :precondition (and 
        	; Are guys on the same island?
        	(at ?g1 ?i1)
        	(at ?g2 ?i1)
        	(connected ?i1 ?i2) ; Are islands connected?
        	(or (not (has ?g1 none)) (not (has ?g2 none))) ; Does atleast one have torch ?
        	(greater ?g1 ?g2); Is the crossing speed of "g1" >= "g2" ?

        )
        ; Change positions, increase cost
        :effect  (and 
        	(not (at ?g1 ?i1))
        	(at ?g1 ?i2)
        	(not (at ?g2 ?i1))
        	(at ?g2 ?i2)
        	(increase (total-cost) (crossing-speed ?g1))
        )
    ) 
)
