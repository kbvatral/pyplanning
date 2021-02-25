;Header and description

(define (domain roboschool)

    (:requirements :strips :typing :negative-preconditions)

    (:types
        piece location bin shape color
    )

    (:predicates
        (trainerAt ?l - location)
        (pieceAt ?p - piece ?l - location)
        (binAt ?b - bin ?l - location)
        (CARRIES ?p - piece)
        (INSIDE ?p - piece ?b - bin)
        (ADJACENT ?l1 - location ?l2 - location)
        (BLOCKED ?l - location)
    )

    (:action Pickup
        :parameters (?p - piece ?l - location)
        :precondition (and (trainerAt ?l) (pieceAt ?p ?l) )
        :effect (and (CARRIES ?p) (not (pieceAt ?p ?l)) )
    )
    (:action Drop
        :parameters (?p - piece ?l - location ?b - bin)
        :precondition (and (trainerAt ?l) (CARRIES ?p) (binAt ?b ?l))
        :effect (and (INSIDE ?p ?b) (not (CARRIES ?p)) )
    )
    (:action Throw
        :parameters (?p - piece ?l1 - location ?l2 - location ?b - bin)
        :precondition (and (trainerAt ?l1) (CARRIES ?p) (binAt ?b ?l2) (ADJACENT ?l1 ?l2) )
        :effect (and (INSIDE ?p ?b) (not (CARRIES ?p)) )
    )
    (:action Move
        :parameters (?l1 - location ?l2 - location)
        :precondition (and (trainerAt ?l1) (ADJACENT ?l1 ?l2) (not (BLOCKED ?l2)) )
        :effect (and (trainerAt ?l2) (not (trainerAt ?l1)))
    )

)