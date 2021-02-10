from pddl import load_pddl
from bfs_solver import bfs_solve

#domain, problem = load_pddl("examples/blocksworld.pddl", "examples/stack-blocks.pddl")
domain, problem = load_pddl("examples/gripper.pddl", "examples/gripper-four.pddl")

res, plan = bfs_solve(problem)
print(plan)