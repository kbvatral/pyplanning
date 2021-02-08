import re
from propositional import GroundedPredicate


class Predicate:
    def __init__(self, name, *args):
        if len(args) < 0:
            raise TypeError("Predicates must contain at least one variable.")
        self.name = name
        self.variables = args

    def ground(self, *args):
        return GroundedPredicate(self, *args)

    def __repr__(self) -> str:
        return "{} ?{}".format(self.name, " ?".join(self.variables))
    def __eq__(self, o: object) -> bool:
        return self.name == o.name and len(self.variables) == len(o.variables)

    @staticmethod
    def from_str(str):
        # remove whitespace with re and potential empty variable names with filter none
        ws_pattern = re.compile(r'\s+')
        pred = list(filter(None, re.sub(ws_pattern, '', str).split("?")))

        if len(pred) < 2:
            raise ValueError(
                "Incorrect formatting for PDDL-style predicate string.")
        return Predicate(pred[0], *pred[1:])
