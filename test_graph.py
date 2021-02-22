import pyplanning as pp

domain, problem = pp.load_pddl("examples/pddl_files/graph/cake.pddl", "examples/pddl_files/graph/haveandeat.pddl")
level = pp.solvers.graph_plan(problem)
print(level)