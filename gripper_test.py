from pddl import load_pddl

domain, problem = load_pddl("examples/gripper.pddl", "examples/gripper-four.pddl")

pickup_action = problem.domain.actions['pickup']
drop_action = problem.domain.actions['drop']
move_action = problem.domain.actions['move']

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