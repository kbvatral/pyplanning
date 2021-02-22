import pyplanning as pp
import itertools

domain, problem = pp.load_pddl("examples/pddl_files/graph/cake.pddl", "examples/pddl_files/graph/haveandeat.pddl")
level = pp.solvers.graph_plan(problem)
print(level)

# for a in itertools.product(*[["a1", "a2"]]):
#     print(a)