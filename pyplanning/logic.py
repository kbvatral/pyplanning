from abc import ABC, abstractmethod
import re
from typing import Iterable


class Proposition(ABC):
    @abstractmethod
    def check_grounded(self):
        ...


class Predicate(Proposition):
    def __init__(self, name, variables, grounding={}):
        if len(variables) < 0:
            raise TypeError("Predicates must contain at least one variable.")
        self.name = name
        self.variables = []
        self.types = []
        for v, t in variables:
            self.variables.append(v)
            self.types.append(t)
        self.grounding = grounding

    def __repr__(self) -> str:
        str_rep = "{} ".format(self.name)
        for v in self.variables:
            if v in self.grounding:
                str_rep += "{} ".format(self.grounding[v])
            else:
                str_rep += "?{} ".format(v)
        return str_rep[:-1]
    
    def hash_str(self) -> str:
        str_rep = "{} ".format(self.name)
        for i, v in enumerate(self.variables):
            if v in self.grounding:
                str_rep += "{} ".format(self.grounding[v])
            else:
                str_rep += "?x{} ".format(i)
        return str_rep[:-1]

    def __hash__(self) -> int:
        return hash(self.hash_str())

    def __eq__(self, o) -> bool:
        # TODO This method of equality is very hacky and should be updated
        if type(o) != type(self):
            return False
        return self.hash_str() == o.hash_str()

    def check_grounded(self):
        for n in self.variables:
            if n not in self.grounding:
                return False
        return True

    def ground(self, objects):
        new_grounding = self.grounding.copy()
        if isinstance(objects, dict):
            for k, v in objects.items():
                if k in self.variables:
                    new_grounding[k] = v
        elif isinstance(objects, Iterable):
            for i, o in enumerate(objects):
                new_grounding[self.variables[i]] = o
        else:
            raise TypeError(
                "Expected argument `objects` to be an Interable type.")
        return Predicate(self.name, list(zip(self.variables, self.types)), new_grounding)
    
    def unground(self):
        return Predicate(self.name, list(zip(self.variables, self.types)))

    @staticmethod
    def from_str(s):
        # remove whitespace with re and potential empty variable names with filter none
        ws_pattern = re.compile(r'\s+')
        pred = list(filter(None, re.sub(ws_pattern, '', s).split("?")))
        if len(pred) < 2:
            raise ValueError(
                "Incorrect formatting for PDDL-style predicate string.")

        name = pred[0]
        variables = []
        for p in pred[1:]:
            splits = p.split("-")
            var_name = splits[0]
            obj_type = splits[1] if len(splits) == 2 else None
            variables.append((var_name, obj_type))
        return Predicate(name, variables)


class AND(Proposition):
    def __init__(self, props):
        for p in props:
            if not isinstance(p, Proposition):
                raise TypeError("All arguments must be of type Proposition.")
        self.props = props

    def __repr__(self):
        return "AND{}".format(tuple(self.props))

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

    def __repr__(self):
        return "OR{}".format(tuple(self.props))

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

    def __repr__(self):
        return "NOT({})".format(self.prop)

    def __eq__(self, o):
        return isinstance(o, NOT) and o.prop == self.prop

    def __hash__(self):
        if isinstance(self.prop, Predicate):
            rep = "NOT({})".format(self.prop.hash_str())
            return hash(rep)
        else:
            return hash(str(self))

    def check_grounded(self):
        return self.prop.check_grounded()
