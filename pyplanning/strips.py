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

    def get_typed_objs(self, t):
        all_types = self.domain.types.get_all_children(t)
        all_objs = []
        for c in all_types:
            if c in self.objects:
                all_objs += self.objects[c]
        return all_objs


class KnowledgeState:
    def __init__(self, knowledge=[], explicit_delete=False):
        self.knowledge = frozenset(knowledge)
        self.explicit_delete = explicit_delete

    def __eq__(self, o):
        return self.knowledge == o.knowledge

    def __hash__(self) -> int:
        return hash(self.knowledge)

    def teach(self, p):
        if not isinstance(p, Iterable):
            p = [p]
        new_knowledge = set(self.knowledge)

        for prop in p:
            if isinstance(prop, Predicate) and prop.check_grounded():
                new_knowledge.add(prop)
            elif isinstance(prop, NOT) and isinstance(prop.prop, Predicate) and prop.check_grounded():
                if self.explicit_delete:
                    new_knowledge.add(prop)
                else:
                    if prop.prop in self.knowledge:
                        new_knowledge.remove(prop.prop)
            else:
                raise TypeError("p must be a list of fully grounded Predicates.")
        return KnowledgeState(new_knowledge, self.explicit_delete)

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
            if self.explicit_delete:
                return (q in self.knowledge)
            else:
                return not self.query(q.prop)
        else:
            raise TypeError(
                "Query must be a combination of fully grounded propositional classes.")

    def __repr__(self):
        return str(self.knowledge)
