from predicate import Predicate
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

ws_pattern = re.compile(r'\s+')
pred = re.sub(ws_pattern, '', predicates[4]).split("?")

print(Predicate.from_str("ROOM ?x"))
