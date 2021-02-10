from pddl import TextTree, load_domain

# a = "(Hello (Name) (Date) (Location))"
# t = TextTree(a)
# t.print()

d = load_domain("examples/gripper.pddl")
print(d)