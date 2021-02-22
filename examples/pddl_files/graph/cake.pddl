;Header and description

(define (domain cake)

(:requirements :strips :negative-preconditions)

(:predicates
    (HAVE ?c)
    (EATEN ?c)
)

(:action Eat
    :parameters (?c)
    :precondition (and (HAVE ?c))
    :effect (and (not (HAVE ?c)) (EATEN ?c))
)
(:action Bake
    :parameters (?c)
    :precondition (and (not (HAVE ?c)))
    :effect (and (HAVE ?c))
)

)