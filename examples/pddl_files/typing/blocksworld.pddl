(define (domain blocksworld)
  (:requirements :strips :typing)
  (:types
    block table - object
  )
  (:predicates
    (On ?b - block ?x - object)
    (Clear ?x - block)
  )
  (:action move
     :parameters (?b - block ?x - object ?y - block)
     :precondition (and (On ?b ?x) (Clear ?b) (Clear ?y))
     :effect (and (On ?b ?y) (Clear ?x) (not (On ?b ?x)) (not (Clear ?y)))
  )
  (:action moveToTable
      :parameters (?b - block ?x - block ?t - table)
      :precondition (and (On ?b ?x) (Clear ?b))
      :effect (and (On ?b ?t) (Clear ?x) (not (On ?b ?x)))
  )
  
)