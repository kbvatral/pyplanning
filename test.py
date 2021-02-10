from pddl import TextTree, load_domain, load_problem

# a = "(Hello (Name) (Date) (Location))"
# t = TextTree(a)
# t.print()

d = load_domain("examples/gripper.pddl")
p = load_problem(d, "examples/gripper-four.pddl")
print(p)