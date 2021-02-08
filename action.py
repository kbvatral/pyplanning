from typing import Iterable
from logic import GroundedPredicate, NOT, Proposition, AND, Predicate, OR
from kb import KnowledgeBase


class Action:
    def __init__(self, name: str, parameters: Iterable, precondition: Proposition, effect: AND) -> None:
        self.name = name
        self.parameters = parameters

        if not isinstance(precondition, Proposition):
            raise TypeError("Precondition must be of type Proposition")
        self.precondition = precondition

        if not isinstance(effect, AND):
            raise TypeError("Effect must be of type AND")
        for e in effect.props:
            if not isinstance(e, GroundedPredicate) and not isinstance(e, Predicate):
                raise TypeError("Effect must be a conjunction of only objects of type Predicate or GroundedPredicate")
        self.effect = effect
    
    def check_preconditions(self, kb: KnowledgeBase, objects):
        if len(objects) != len(self.parameters):
            raise ValueError("Incorrect number of paramters: expected {}, got {}".format(len(self.parameters), len(objects)))
        mapping = {}
        for param, obj in zip(self.parameters, objects):
            mapping[param] = obj
        return kb.query(ground_proposition_by_map(self.precondition, mapping))

    def process_effects(self, kb: KnowledgeBase, objects):
        if len(objects) != len(self.parameters):
            raise ValueError("Incorrect number of paramters: expected {}, got {}".format(len(self.parameters), len(objects)))
        mapping = {}
        for param, obj in zip(self.parameters, objects):
            mapping[param] = obj
        kb.teach(ground_proposition_by_map(self.effect, mapping))
        return kb
    
    def take_action(self, kb: KnowledgeBase, objects):
        if len(objects) != len(self.parameters):
            raise ValueError("Incorrect number of paramters: expected {}, got {}".format(len(self.parameters), len(objects)))
        if self.check_preconditions(kb, objects):
            return True, self.process_effects(kb, objects)
        return False, kb

def ground_proposition_by_map(prop, variable_map):
    if isinstance(prop, Predicate):
        objs = []
        for var in prop.variables:
            if var in variable_map:
                objs.append(variable_map[var])
            else:
                raise ValueError("Unable to find object for variable {} in the provided mapping.".format(var))
        return prop.ground(objs)
    elif isinstance(prop, GroundedPredicate):
        return prop
    elif isinstance(prop, AND):
        return AND([ground_proposition_by_map(p) for p in prop.props])
    elif isinstance(prop, OR):
        return OR([ground_proposition_by_map(p) for p in prop.props])
    elif isinstance(prop, NOT):
        return NOT(ground_proposition_by_map(prop.prop))
    else:
        raise TypeError("Input must be of type Proposition.")