(define (domain blocksworld)
  (:requirements :strips)
  (:predicates
    (On ?b ?x)
    (Clear ?x)
    (Block ?b)
    (Table ?t)
  )
  (:action move
     :parameters (?b ?x ?y)
     :precondition (and (On ?b ?x) (Clear ?b) (Clear ?y) (Block ?b) (Block ?y))
     :effect (and (On ?b ?y) (Clear ?x) (not (On ?b ?x)) (not (Clear ?y)))
  )
  (:action moveToTable
      :parameters (?b ?x ?t)
      :precondition (and (On ?b ?x) (Clear ?b) (Block ?b) (Table ?t))
      :effect (and (On ?b ?t) (Clear ?x) (not (On ?b ?x)))
  )
  
)