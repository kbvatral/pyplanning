(define (problem putOnSpare) (:domain sparetire)
(:objects 
    flat spare - tire
    trunk ground axle - location
)

(:init
    (AT spare trunk)
    (AT flat axle)
    (EMPTY ground)
)

(:goal (and
    (AT spare axle)
))

)
