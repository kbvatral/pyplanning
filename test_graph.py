import pyplanning as pp

# domain, problem = pp.load_pddl("examples/pddl_files/graph/sparetire.pddl", "examples/pddl_files/graph/putOnSpare.pddl")
# domain, problem = pp.load_pddl("examples/pddl_files/typing/blocksworld.pddl", "examples/pddl_files/typing/stack-blocks.pddl")
domain, problem = pp.load_pddl("examples/pddl_files/typing/gripper.pddl", "examples/pddl_files/typing/gripper-four.pddl")

plan = pp.solvers.graph_plan(problem)
print(plan)