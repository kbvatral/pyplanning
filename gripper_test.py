from logic import Predicate, GroundedPredicate, OR, NOT, AND
from kb import KnowledgeBase
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


kb = KnowledgeBase(objects, predicates)
kb.teach(initial)

p1 = GroundedPredicate.from_str(kb, "BALL ball1")
p2 = GroundedPredicate.from_str(kb, "ROOM rooma")
p3 = GroundedPredicate.from_str(kb, "at-ball ball1 rooma")
print(kb.query(AND([p1,p2,p3])))