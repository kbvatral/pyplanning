from pddl import load_pddl

domain, problem = load_pddl("examples/blocksworld.pddl", "examples/stack-blocks.pddl")

solution = [
    (domain.actions['moveToTable'], ["C", "A", "T"]),
    (domain.actions['move'], ["B", "T", "C"]),
    (domain.actions['move'], ["A", "T", "B"])
]

current_state = problem.initial_state
print(problem.check_goal(current_state))
for a, o in solution:
    res, current_state = a.take_action(current_state, o)
    print(problem.check_goal(current_state))