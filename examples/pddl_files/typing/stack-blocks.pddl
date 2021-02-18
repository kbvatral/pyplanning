(define (problem stack_blocks) (:domain blocksworld)
    (:objects 
        A B C - block
        T - table
    )

    (:init
        (On A T) (On B T) (On C A)
        (Clear B) (Clear C)
    )

    (:goal 
        (and (On A B) (On B C))
    )
)
