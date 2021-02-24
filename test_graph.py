import pyplanning as pp
import itertools

domain, problem = pp.load_pddl("examples/pddl_files/graph/cake.pddl", "examples/pddl_files/graph/haveandeat.pddl")
plan = pp.solvers.graph_plan(problem)
print(plan)

# for a in itertools.product(*[["a1", "a2"]]):
#     print(a)