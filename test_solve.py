import pyplanning as pp

#domain, problem = load_pddl("examples/blocksworld.pddl", "examples/stack-blocks.pddl")
domain, problem = pp.load_pddl("examples/gripper.pddl", "examples/gripper-four.pddl")

plan = pp.solvers.search_solve(problem)
print(plan)