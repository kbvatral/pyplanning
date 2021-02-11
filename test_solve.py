import pyplanning as pp
from pyplanning.solvers.heuristics import ignore_delete_heuristic
import time
import math

#domain, problem = load_pddl("examples/blocksworld.pddl", "examples/stack-blocks.pddl")
domain, problem = pp.load_pddl("examples/gripper.pddl", "examples/gripper-four.pddl")

tic = time.time()
plan = pp.solvers.search_plan(problem)
print("Execution Time: %.2f" % (time.time() - tic))
print("Plan found:")
print(plan, "\n")

def custom_heuristic(state):
    num_total = len(problem.goal_state.props)
    num_complete = 0
    for prop in state.knowledge:
        if prop in problem.goal_state.props:
            num_complete += 1
    return math.ceil((num_total-num_complete)/2)

tic = time.time()
plan = pp.solvers.search_plan(problem, custom_heuristic)
print("Execution Time: %.2f" % (time.time() - tic))
print("Plan found:")
print(plan, "\n")