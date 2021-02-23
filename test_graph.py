import pyplanning as pp
import itertools

domain, problem = pp.load_pddl("examples/pddl_files/graph/cake.pddl", "examples/pddl_files/graph/haveandeat.pddl")
graph = pp.solvers.graph_plan(problem)
print(graph.check_goal())

# for a in itertools.product(*[["a1", "a2"]]):
#     print(a)