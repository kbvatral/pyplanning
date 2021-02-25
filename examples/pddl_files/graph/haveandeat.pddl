(define (problem haveandeat) (:domain cake)
(:objects 
    Cake
)

(:init
    (HAVE Cake)
)

(:goal (and
    (HAVE Cake) (EATEN Cake)
))

)
