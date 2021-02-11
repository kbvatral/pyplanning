from pddl import load_pddl
from search_solver import search_solve

#domain, problem = load_pddl("examples/blocksworld.pddl", "examples/stack-blocks.pddl")
domain, problem = load_pddl("examples/gripper.pddl", "examples/gripper-four.pddl")

plan = search_solve(problem)
print(plan)