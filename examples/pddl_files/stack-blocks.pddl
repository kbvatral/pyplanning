(define (problem stack_blocks) (:domain blocksworld)
    (:objects 
        A B C T
    )

    (:init
        (On A T) (On B T) (On C A)
        (Block A) (Block B) (Block C)
        (Table T)
        (Clear B) (Clear C)
    )

    (:goal 
        (and (On A B) (On B C))
    )
)
