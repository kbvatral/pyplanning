import pyplanning as pp
from pyplanning.solvers.heuristics import ignore_delete_heuristic

#domain, problem = load_pddl("examples/blocksworld.pddl", "examples/stack-blocks.pddl")
domain, problem = pp.load_pddl("examples/gripper.pddl", "examples/gripper-four.pddl")

plan = pp.solvers.search_plan(problem, ignore_delete_heuristic(problem))
print(plan)