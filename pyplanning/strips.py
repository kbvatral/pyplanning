from typing import Iterable
from .logic import AND, NOT, OR, Predicate, Proposition
from .action import Action


class Domain:
    def __init__(self, name, types, predicates, actions):
        self.name = name
        self.types = types
        self.predicates = dict()
        for p in predicates:
            if not isinstance(p, Predicate):
                raise TypeError("All predicates must be of type Predicate.")
            self.predicates[p.name] = p
        if len(self.predicates) != len(predicates):
            raise Warning("Predicates with duplicate names were removed.")

        self.actions = dict()
        for a in actions:
            if not isinstance(a, Action):
                raise TypeError("All actions must be of type Action.")
            self.actions[a.name] = a
        if len(self.actions) != len(actions):
            raise Warning("Actions with duplicate names were removed.")


class Problem:
    def __init__(self, name, domain, objects, initial_state, goal_state):
        if not isinstance(domain, Domain):
            raise TypeError("Supplied domain must be of type Domain.")
        if not isinstance(initial_state, KnowledgeState):
            raise TypeError("Initial State must be of type KnowledgeState.")
        if not isinstance(goal_state, Proposition):
            raise TypeError("Goal state must be of type Proposition.")
        if not goal_state.check_grounded():
            raise TypeError("Goal state must be completely grounded.")

        self.name = name
        self.domain = domain
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.objects = objects

    def check_goal(self, state):
        return state.query(self.goal_state)


class KnowledgeState:
    def __init__(self, knowledge=[]):
        self.knowledge = frozenset(knowledge)

    def __eq__(self, o):
        return self.knowledge == o.knowledge

    def __hash__(self) -> int:
        return hash(self.knowledge)

    def teach(self, p, delete_method="delete"):
        if not isinstance(p, Iterable):
            p = [p]
        new_knowledge = set(self.knowledge)

        for prop in p:
            if isinstance(prop, Predicate) and prop.check_grounded():
                new_knowledge.add(prop)
            elif isinstance(prop, NOT) and isinstance(prop.prop, Predicate) and prop.check_grounded():
                if delete_method.lower() == "delete":
                    if prop.prop in self.knowledge:
                        new_knowledge.remove(prop.prop)
                elif delete_method.lower() == "add":
                    new_knowledge.add(prop)
                elif delete_method.lower() == "ignore":
                    pass
                else:
                    raise ValueError(
                        "Unrecognized delete method. Method must be one of 'delete', 'add', or 'ignore'.")
            else:
                raise TypeError("p must be a list of fully grounded Predicates.")
        return KnowledgeState(new_knowledge)

    def query(self, q):
        if isinstance(q, Predicate) and q.check_grounded():
            return (q in self.knowledge)
        elif isinstance(q, AND):
            for prop in q.props:
                if not self.query(prop):
                    return False
            return True
        elif isinstance(q, OR):
            for prop in q.props:
                if self.query(prop):
                    return True
            return False
        elif isinstance(q, NOT):
            return not self.query(q.prop)
        else:
            raise TypeError(
                "Query must be a combination of fully grounded propositional classes.")

    def __repr__(self):
        return str(self.knowledge)
