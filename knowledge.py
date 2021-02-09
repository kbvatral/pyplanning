from typing import Iterable
from logic import AND, NOT, OR, Predicate, GroundedPredicate, Proposition


class Domain:
    def __init__(self, objects, predicates):
        self.objects = set(objects)
        if len(self.objects) != len(objects):
            raise Warning("Objects with duplicate names were removed.")

        self.predicates = dict()
        for p in predicates:
            if not isinstance(p, Predicate):
                raise TypeError("All predicates must be of type Predicate.")
            self.predicates[p.name] = p
        if len(self.predicates) != len(predicates):
            raise Warning("Predicates with duplicate names were removed.")

        self.knowledge = set()

class KnowledgeState:
    def __init__(self, domain, initial):
        self.domain = domain
        self.knowledge = set()

        if initial is not None:
            for p in initial:
                self.teach(p)
    
    def copy(self):
        return KnowledgeState(self.domain, self.knowledge)

    def teach(self, p):
        if isinstance(p, GroundedPredicate):
            self.knowledge.add(p)
        elif isinstance(p, NOT) and isinstance(p.prop, GroundedPredicate):
            if p.prop in self.knowledge:
                self.knowledge.remove(p.prop)
        else:
            raise TypeError("p must be a GroundedPredicate.")

    def query(self, q):
        if isinstance(q, GroundedPredicate):
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
                "Query must be a combination of grounded propositional classes.")
