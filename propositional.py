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
