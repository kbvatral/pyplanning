;Header and description

(define (domain sparetire)

(:requirements :strips :typing :negative-preconditions)

(:types 
    tire location
)
(:predicates 
    (AT ?t - tire ?l - location)
    (EMPTY ?l - location)
)
(:action Move
    :parameters (?t - tire ?l1 - location ?l2 - location)
    :precondition (and (AT ?t ?l1) (EMPTY ?l2))
    :effect (and (AT ?t ?l2) (EMPTY ?l1) (not (AT ?t ?l1)) (not (EMPTY ?l2)))
)

)