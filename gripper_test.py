from logic import Predicate, GroundedPredicate, OR, NOT, AND
from action import Action
from knowledge import Domain, KnowledgeState, Problem
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
    "BALL ball2",
    "BALL ball3",
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
goal = [
    "at-ball ball1 roomb",
    "at-ball ball2 roomb",
    "at-ball ball3 roomb",
    "at-ball ball4 roomb"
]

move_action = Action(
    "move", 
    ["x","y"], 
    AND([Predicate.from_str("ROOM ?x"), Predicate.from_str("ROOM ?y"), Predicate.from_str("at-robby ?x")]),
    AND([Predicate.from_str("at-robby ?y"), NOT(Predicate.from_str("at-robby ?x"))])
)
pickup_action = Action(
    "pickup",
    ["x", "y", "z"],
    AND([Predicate.from_str("BALL ?x"), Predicate.from_str("ROOM ?y"), Predicate.from_str("GRIPPER ?z"), Predicate.from_str("at-ball ?x ?y"), Predicate.from_str("at-robby ?y"), Predicate.from_str("free ?z")]),
    AND([Predicate.from_str("carry ?z ?x"), NOT(Predicate.from_str("at-ball ?x ?y")), NOT(Predicate.from_str("free ?z"))])
)
drop_action = Action(
    "drop",
    ["x", "y", "z"],
    AND([Predicate.from_str("BALL ?x"), Predicate.from_str("ROOM ?y"), Predicate.from_str("GRIPPER ?z"), Predicate.from_str("carry ?z ?x"), Predicate.from_str("at-robby ?y")]),
    AND([Predicate.from_str("at-ball ?x ?y"), Predicate.from_str("free ?z"), NOT(Predicate.from_str("carry ?z ?x"))])
)

action_set = [move_action, pickup_action, drop_action]
domain = Domain([Predicate.from_str(p) for p in predicates], action_set)
initial_state = KnowledgeState()
for p in initial:
    initial_state.teach(GroundedPredicate.from_str(p))
goal_state = AND([GroundedPredicate.from_str(p) for p in goal])
problem = Problem(domain, objects, initial_state, goal_state)

actions = [
    (pickup_action, ["ball1", "rooma", "left"]),
    (pickup_action, ["ball2", "rooma", "right"]),
    (move_action, ["rooma", "roomb"]),
    (drop_action, ["ball1", "roomb", "left"]),
    (drop_action, ["ball2", "roomb", "right"]),
    (move_action, ["roomb", "rooma"]),
    (pickup_action, ["ball3", "rooma", "left"]),
    (pickup_action, ["ball4", "rooma", "right"]),
    (move_action, ["rooma", "roomb"]),
    (drop_action, ["ball3", "roomb", "left"]),
    (drop_action, ["ball4", "roomb", "right"]),
]

current_state = problem.initial_state
print(problem.check_goal(current_state))
for a, o in actions:
    res, current_state = a.take_action(current_state, o)
    print(problem.check_goal(current_state))
