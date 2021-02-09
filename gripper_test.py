from logic import Predicate, GroundedPredicate, OR, NOT, AND
from knowledge import Domain, KnowledgeState
import numpy as np
import re

objects = [
    "rooma", "roomb",
    "ball1", "ball2", "ball3", "ball4",
    "left", "right"
]
predicates = [
    "ROOM ?x",          # true iff x is a room
    "BALL ?x",          # true iff x is a ball
    "GRIPPER ?x",       # true iff x is a gripper
    "at-robby ?x",      # true iff x is a room and the robot is in x
    "at-ball ?x ?y",    # true iff x is a ball, y is a room, and x is in y
    "free ?x",          # true iff x is a gripper and x does not hold a ball
    "carry ?x ?y"       # true iff x is a gripper, y is a ball, and x holds y
]
initial = [
    "ROOM rooma",
    "ROOM roomb",
    "BALL ball1",
    "BALL ball4",
    "GRIPPER left",
    "GRIPPER right",
    "free left",
    "free right",
    "at-robby rooma",
    "at-ball ball1 rooma",
    "at-ball ball2 rooma",
    "at-ball ball3 rooma",
    "at-ball ball4 rooma"
]

domain = Domain(objects, [Predicate.from_str(p) for p in predicates])
state = KnowledgeState(domain, [GroundedPredicate.from_str(domain, p) for p in initial])

p1 = GroundedPredicate.from_str(domain, "BALL ball1")
p2 = GroundedPredicate.from_str(domain, "ROOM rooma")
p3 = GroundedPredicate.from_str(domain, "ROOM roomb")
p4 = GroundedPredicate.from_str(domain, "at-ball ball1 rooma")
p5 = GroundedPredicate.from_str(domain, "at-ball ball1 roomb")

state2 = state.copy()
state2.teach(p5)
state2.teach(NOT(p4))

q1 = AND([p1, p2, p3, p4])
q2 = AND([p1, p2, p3, p5])

print(state.query(q1))
print(state.query(q2))
print(state2.query(q1))
print(state2.query(q2))