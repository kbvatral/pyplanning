import pyplanning as pp


# domain, problem = pp.load_pddl("examples/pddl_files/typing/gripper.pddl", "examples/pddl_files/typing/gripper-four.pddl")
# domain, problem = pp.load_pddl("examples/pddl_files/typing/blocksworld.pddl", "examples/pddl_files/typing/stack-blocks.pddl")
# domain, problem = pp.load_pddl("examples/pddl_files/graph/sparetire.pddl", "examples/pddl_files/graph/putOnSpare.pddl")
domain, problem = pp.load_pddl("examples/pddl_files/roboschool/roboschool.pddl", "examples/pddl_files/roboschool/store_triangles.pddl")

plan = pp.solvers.ff.ff_plan(problem)
print(plan)