from abc import ABC
import re


class Proposition(ABC):
    pass


class Predicate(Proposition):
    def __init__(self, name, variables):
        if isinstance(variables, str):
            variables = [variables]
        if len(variables) < 0:
            raise TypeError("Predicates must contain at least one variable.")
        self.name = name
        self.variables = variables

    def ground(self, objects):
        return GroundedPredicate(self, objects)

    def __repr__(self) -> str:
        return "{} ?{}".format(self.name, " ?".join(self.variables))

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, o) -> bool:
        # Variable names do not effect equality of predicates
        return self.name == o.name and len(self.variables) == len(o.variables)

    @staticmethod
    def from_str(str):
        # remove whitespace with re and potential empty variable names with filter none
        ws_pattern = re.compile(r'\s+')
        pred = list(filter(None, re.sub(ws_pattern, '', str).split("?")))

        if len(pred) < 2:
            raise ValueError(
                "Incorrect formatting for PDDL-style predicate string.")
        return Predicate(pred[0], pred[1:])


class GroundedPredicate(Proposition):
    def __init__(self, predicate, objects):
        if len(objects) != len(predicate.variables):
            raise TypeError("Incorrect number of variables: expected {}, got {}".format(
                len(predicate.variables), len(objects)))

        self.predicate = predicate
        self.objects = objects

    def __repr__(self) -> str:
        return "{}({})".format(self.predicate.name, ", ".join(self.objects))

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, o) -> bool:
        return self.predicate == o.predicate and self.objects == o.objects

    @staticmethod
    def from_str(domain, p):
        comp = list(filter(None, p.split()))
        if len(comp) < 2:
            raise ValueError("Incorrect formatting for PDDL-style string.")
        if comp[0] not in domain.predicates:
            raise ValueError(
                "Unable to find a matching predicate in the domain for parsed string: {}".format(comp[0]))
        for v in comp[1:]:
            if v not in domain.objects:
                raise ValueError(
                    "Unable to find a matching object in the domain for parsed string: {}".format(v))

        predicate = domain.predicates[comp[0]]
        return predicate.ground(comp[1:])


class AND(Proposition):
    def __init__(self, props):
        for p in props:
            if not isinstance(p, Proposition):
                raise TypeError("All arguments must be of type Proposition.")
        self.props = props
        self.count = -1

    def __iter__(self):
        self.count = -1
        return self

    def __next__(self):
        self.count += 1
        if self.count < len(self.props):
            return self.props[self.count]
        raise StopIteration


class OR(Proposition):
    def __init__(self, props):
        for p in props:
            if not isinstance(p, Proposition):
                raise TypeError("All arguments must be of type Proposition.")
        self.props = props
        self.count = -1

    def __iter__(self):
        self.count = -1
        return self

    def __next__(self):
        self.count += 1
        if self.count < len(self.props):
            return self.props[self.count]
        raise StopIteration


class NOT(Proposition):
    def __init__(self, prop):
        if not isinstance(prop, Proposition):
            raise TypeError("Argument must be of type Proposition.")
        self.prop = prop
