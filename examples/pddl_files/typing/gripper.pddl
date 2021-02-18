;;
;; PDDL file for a robot gripper toy domain.
;; Generally, we have n balls and a robot with two arms
;; with problems defined by moving the balls
;;

(define (domain gripper)
    (:requirements :strips :typing)

    (:types
        ball room gripper
    )

    (:predicates 
        (at-robby ?x - room)
        (at-ball ?x - ball ?y - room)
        (free ?x - gripper)
        (carry ?x - ball ?y - gripper)
    )

    (:action move 
        :parameters (?x - room ?y - room)
        :precondition (and (at-robby ?x))
        :effect (and (at-robby ?y) (not (at-robby ?x)))
    )
    (:action pickup 
        :parameters (?x - ball ?y - room ?z - gripper)
        :precondition (and (at-ball ?x ?y) (at-robby ?y) (free ?z))
        :effect (and (carry ?z ?x) (not (at-ball ?x ?y)) (not (free ?z)))
    )
    (:action drop 
        :parameters (?x - ball ?y - room ?z - gripper)
        :precondition (and (carry ?z ?x) (at-robby ?y))
        :effect (and (at-ball ?x ?y) (free ?z) (not (carry ?z ?x)))
    )
)