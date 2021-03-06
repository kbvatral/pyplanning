(define (problem store_triangles) (:domain roboschool)
(:objects
    p1 p2 p3 p4 p5 p6 p7 - piece
    bin1 bin2 bin3 - bin
    box sphere cone - shape
    red blue green - color

    A0 A1 A2 A3 A4
    B0 B1 B2 B3 B4
    C0 C1 C2 C3 C4
    D0 D1 D2 D3 D4
    E0 E1 E2 E3 E4 - location
)

(:init
    (pieceAt p1 B0) (pieceAt p2 A1) (pieceAt p3 A4) (pieceAt p4 C2) (pieceAt p5 E0) (pieceAt p6 D3) (pieceAt p7 E3)
    (binAt bin1 D2) (binAt bin2 A2) (binAt bin3 C4)
    (trainerAt B3)

    (BLOCKED A2) (BLOCKED A3) (BLOCKED C4) (BLOCKED D4) (BLOCKED D1) (BLOCKED E1)

    (ADJACENT A0 A1) (ADJACENT A1 A0) (ADJACENT A0 B0) (ADJACENT B0 A0)
    (ADJACENT A1 A2) (ADJACENT A2 A1) (ADJACENT A1 B1) (ADJACENT B1 A1)
    (ADJACENT A2 A3) (ADJACENT A3 A2) (ADJACENT A2 B2) (ADJACENT B2 A2)
    (ADJACENT A3 A4) (ADJACENT A4 A3) (ADJACENT A3 B3) (ADJACENT B3 A3)
    (ADJACENT A4 B4) (ADJACENT B4 A4)

    (ADJACENT B0 B1) (ADJACENT B1 B0) (ADJACENT B0 C0) (ADJACENT C0 B0)
    (ADJACENT B1 B2) (ADJACENT B2 B1) (ADJACENT B1 C1) (ADJACENT C1 B1)
    (ADJACENT B2 B3) (ADJACENT B3 B2) (ADJACENT B2 C2) (ADJACENT C2 B2)
    (ADJACENT B3 B4) (ADJACENT B4 B3) (ADJACENT B3 C3) (ADJACENT C3 B3)
    (ADJACENT B4 C4) (ADJACENT C4 B4)

    (ADJACENT C0 C1) (ADJACENT C1 C0) (ADJACENT C0 D0) (ADJACENT D0 C0)
    (ADJACENT C1 C2) (ADJACENT C2 C1) (ADJACENT C1 D1) (ADJACENT D1 C1)
    (ADJACENT C2 C3) (ADJACENT C3 C2) (ADJACENT C2 D2) (ADJACENT D2 C2)
    (ADJACENT C3 C4) (ADJACENT C4 C3) (ADJACENT C3 D3) (ADJACENT D3 C3)
    (ADJACENT C4 D4) (ADJACENT D4 C4)

    (ADJACENT D0 D1) (ADJACENT D1 D0) (ADJACENT D0 E0) (ADJACENT E0 D0)
    (ADJACENT D1 D2) (ADJACENT D2 D1) (ADJACENT D1 E1) (ADJACENT E1 D1)
    (ADJACENT D2 D3) (ADJACENT D3 D2) (ADJACENT D2 E2) (ADJACENT E2 D2)
    (ADJACENT D3 D4) (ADJACENT D4 D3) (ADJACENT D3 E3) (ADJACENT E3 D3)
    (ADJACENT D4 E4) (ADJACENT E4 D4)

    (ADJACENT E0 E1) (ADJACENT E1 E0) (ADJACENT E1 E2) (ADJACENT E2 E1)
    (ADJACENT E2 E3) (ADJACENT E3 E2) (ADJACENT E3 E4) (ADJACENT E4 E3)
)

(:goal (and
    (INSIDE p3 bin1) (INSIDE p4 bin1)
))

)
