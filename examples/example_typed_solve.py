import pyplanning as pp
from pyplanning.solvers.heuristics import ignore_delete_heuristic
import time
import math


domain, problem = pp.load_pddl("examples/pddl_files/typing/blocksworld.pddl", "examples/pddl_files/typing/stack-blocks.pddl")

tic = time.time()
plan = pp.solvers.search_plan(problem)

print("Execution Time: %.2f" % (time.time() - tic))
print("Plan found:")
print(plan, "\n")