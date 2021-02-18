import pyplanning as pp
import time
import math


# domain, problem = pp.load_pddl("pddl_files/typing/blocksworld.pddl", "pddl_files/typing/stack-blocks.pddl")
domain, problem = pp.load_pddl(
    "pddl_files/typing/gripper.pddl", "pddl_files/typing/gripper-four.pddl")

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
