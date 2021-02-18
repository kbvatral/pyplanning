;;
;; PDDL file for a robot gripper toy domain.
;; Generally, we have n balls and a robot with two arms
;; with problems defined by moving the balls
;;

(define (domain gripper)
    (:requirements :strips)

    (:predicates 
        (ROOM ?x)
        (BALL ?x)
        (GRIPPER ?x)
        (at-robby ?x)
        (at-ball ?x ?y)
        (free ?x)
        (carry ?x ?y)
    )

    (:action move 
        :parameters (?x ?y)
        :precondition (and (ROOM ?x) (ROOM ?y) (at-robby ?x))
        :effect (and (at-robby ?y) (not (at-robby ?x)))
    )
    (:action pickup 
        :parameters (?x ?y ?z)
        :precondition (and (BALL ?x) (ROOM ?y) (GRIPPER ?z) (at-ball ?x ?y) (at-robby ?y) (free ?z))
        :effect (and (carry ?z ?x) (not (at-ball ?x ?y)) (not (free ?z)))
    )
    (:action drop 
        :parameters (?x ?y ?z)
        :precondition (and (BALL ?x) (ROOM ?y) (GRIPPER ?z)(carry ?z ?x) (at-robby ?y))
        :effect (and (at-ball ?x ?y) (free ?z)(not (carry ?z ?x)))
    )
)