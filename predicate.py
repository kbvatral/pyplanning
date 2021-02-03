import re

class Predicate:
    def __init__(self, name, *args):
        self.name = name

        if len(args) < 0:
            raise TypeError("Predicates must contain at least one variable.")
        self.variables = args
    
    def ground(self, *args):
        if len(args) != len(self.variables):
            raise TypeError("Incorrect number of variables: expected {}, got {}".format(len(self.variables), len(args)))
        return "{}({})".format(self.name, ", ".join(args))

    def __repr__(self) -> str:
        return "{} ?{}".format(self.name, " ?".join(self.variables))

    @staticmethod
    def from_str(str):
        # remove whitespace with re and potential empty variable names with filter none
        ws_pattern = re.compile(r'\s+')
        pred = list(filter(None, re.sub(ws_pattern, '', str).split("?")))
        
        if len(pred) < 2:
            raise ValueError("Incorrect formatting for PDDL-style predicate string.")
        return Predicate(pred[0], *pred[1:])