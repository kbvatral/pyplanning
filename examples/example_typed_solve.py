from pyplanning.solvers.heuristics import ignore_delete_heuristic
import pyplanning as pp
import time
import math

### Loading PDDL Files ###

domain, problem = pp.load_pddl(
    "pddl_files/typing/gripper.pddl", "pddl_files/typing/gripper-four.pddl")


### Solving using BFS ###

tic = time.time()
plan = pp.solvers.search_plan(problem)
print("Breadth-First Search")
print("Execution Time: %.2f" % (time.time() - tic))
print("Plan found:")
print(plan, "\n")


### Solving using A* with the Ignore Delete Lists Heuristic ###

tic = time.time()
plan = pp.solvers.search_plan(problem, heuristic=ignore_delete_heuristic(problem))
print("A* - Ignore Delete Lists Heuristic")
print("Execution Time: %.2f" % (time.time() - tic))
print("Plan found:")
print(plan, "\n")


### Solving using A* with a Custom Heuristic ###

def custom_heuristic(state):
    num_total = len(problem.goal_state.props)
    num_complete = 0
    for prop in state.knowledge:
        if prop in problem.goal_state.props:
            num_complete += 1
    return math.ceil((num_total-num_complete)/2)

tic = time.time()
plan = pp.solvers.search_plan(problem, custom_heuristic)
print("A* - Custom Heuristic")
print("Execution Time: %.2f" % (time.time() - tic))
print("Plan found:")
print(plan, "\n")
