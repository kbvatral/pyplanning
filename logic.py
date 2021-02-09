from abc import ABC, abstractmethod
import re


class Proposition(ABC):
    @abstractmethod
    def check_grounded(self):
        ...


class Predicate(Proposition):
    def __init__(self, name, variables):
        if isinstance(variables, str):
            variables = [variables]
        if len(variables) < 0:
            raise TypeError("Predicates must contain at least one variable.")
        self.name = name
        self.variables = variables
    def __repr__(self) -> str:
        return "{} ?{}".format(self.name, " ?".join(self.variables))
    def __hash__(self) -> int:
        return hash(str(self))
    def __eq__(self, o) -> bool:
        # Variable names do not effect equality of predicates
        return self.name == o.name and len(self.variables) == len(o.variables)

    def check_grounded(self):
        return False
    def ground(self, objects):
        return GroundedPredicate(self, objects)

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

    def check_grounded(self):
        return True

    @staticmethod
    def from_str(p):
        comp = list(filter(None, p.split()))
        if len(comp) < 2:
            raise ValueError("Incorrect formatting for PDDL-style string.")

        predicate = Predicate(comp[0], ["x{}".format(i) for i in range(len(comp)-1)])
        return predicate.ground(comp[1:])


class AND(Proposition):
    def __init__(self, props):
        for p in props:
            if not isinstance(p, Proposition):
                raise TypeError("All arguments must be of type Proposition.")
        self.props = props

    def check_grounded(self):
        for p in self.props:
            if not p.check_grounded():
                return False
        return True


class OR(Proposition):
    def __init__(self, props):
        for p in props:
            if not isinstance(p, Proposition):
                raise TypeError("All arguments must be of type Proposition.")
        self.props = props

    def check_grounded(self):
        for p in self.props:
            if not p.check_grounded():
                return False
        return True


class NOT(Proposition):
    def __init__(self, prop):
        if not isinstance(prop, Proposition):
            raise TypeError("Argument must be of type Proposition.")
        self.prop = prop

    def check_grounded(self):
        return self.prop.check_grounded()
