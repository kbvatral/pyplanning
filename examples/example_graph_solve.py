import pyplanning as pp
import time

# domain, problem = pp.load_pddl("examples/pddl_files/graph/sparetire.pddl", "examples/pddl_files/graph/putOnSpare.pddl")
# domain, problem = pp.load_pddl("examples/pddl_files/typing/blocksworld.pddl", "examples/pddl_files/typing/stack-blocks.pddl")
# domain, problem = pp.load_pddl("examples/pddl_files/typing/gripper.pddl", "examples/pddl_files/typing/gripper-four.pddl")
domain, problem = pp.load_pddl("pddl_files/roboschool/roboschool.pddl", "pddl_files/roboschool/store_triangles.pddl")


### Solve using GraphPlan ###

tic = time.time()
plan = pp.solvers.graph_plan(problem)
print("GraphPlan")
print("Execution Time: %.2f" % (time.time() - tic))
print("Plan found:")
print(plan, "\n")


### Solve using A* with Goals Remaining Heuristic ###

tic = time.time()
plan = pp.solvers.search_plan(problem, pp.solvers.heuristics.goals_remaining(problem))
print("A* with Goals Remaining Heuristic")
print("Execution Time: %.2f" % (time.time() - tic))
print("Plan found:")
print(plan, "\n")


### Solving using BFS ###

tic = time.time()
plan = pp.solvers.search_plan(problem)
print("Breadth-First Search")
print("Execution Time: %.2f" % (time.time() - tic))
print("Plan found:")
print(plan, "\n")


