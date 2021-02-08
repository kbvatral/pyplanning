class Proposition:
    pass


class GroundedPredicate(Proposition):
    def __init__(self, predicate, *args):
        if len(args) != len(predicate.variables):
            raise TypeError("Incorrect number of variables: expected {}, got {}".format(
                len(predicate.variables), len(args)))

        self.predicate = predicate
        self.args = args

    def __repr__(self) -> str:
        return "{}({})".format(self.predicate.name, ", ".join(self.args))
    def __hash__(self) -> int:
        return hash(str(self))
    def __eq__(self, o: object) -> bool:
        return self.predicate == o.predicate and self.args == o.args

    @staticmethod
    def from_str(kb, p):
        comp = list(filter(None, p.split()))
        if len(comp) < 2:
            raise ValueError("Incorrect formatting for PDDL-style string.")
        if comp[0] not in kb.predicates:
            raise ValueError("Unable to find a matching predicate in the knowledge base for parsed string: {}".format(comp[0]))
        for v in comp[1:]:
            if v not in kb.objects:
                raise ValueError("Unable to find a matching object in the knowledge base for parsed string: {}".format(v))
        
        predicate = kb.predicates[comp[0]]
        return predicate.ground(*comp[1:])


class AND(Proposition):
    def __init__(self, *args):
        for p in args:
            if not isinstance(p, Proposition):
                raise TypeError("All arguments must be of type Proposition.")
        self.props = args


class OR(Proposition):
    def __init__(self, *args):
        for p in args:
            if not isinstance(p, Proposition):
                raise TypeError("All arguments must be of type Proposition.")
        self.props = args


class NOT(Proposition):
    def __init__(self, prop):
        if not isinstance(prop, Proposition):
            raise TypeError("Argument must be of type Proposition.")
        self.prop = prop
