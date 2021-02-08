from collections import defaultdict
from typing import Iterable
from logic import AND, NOT, OR, Predicate, GroundedPredicate


class KnowledgeBase:
    def __init__(self, objects, predicates):
        self.objects = set(objects)
        if len(self.objects) != len(objects):
            raise Warning("Objects with duplicate names were removed.")

        self.predicates = dict()
        if isinstance(predicates, str) or not isinstance(predicates, Iterable):
            predicates = [predicates]
        for p in predicates:
            if isinstance(p, str):
                p_parse = Predicate.from_str(p)
                self.predicates[p_parse.name] = p_parse
            elif isinstance(p, Predicate):
                self.predicates[p.name] = p
            else:
                raise TypeError("All predicates must be of type Predicate or a PDDL parsable string")
        if len(self.predicates) != len(predicates):
            raise Warning("Predicates with duplicate names were removed.")

        self.knowledge = defaultdict(bool)

    def teach(self, p):
        if isinstance(p, GroundedPredicate):
            self.knowledge[p] = True
        elif isinstance(p, str):
            self.teach(GroundedPredicate.from_str(self, p))
        elif isinstance(p, Iterable):
            for p_sub in p:
                self.teach(p_sub)
        else:
            raise TypeError("p must be of type GroundedPredicate or a PDDL parsable string.")

    def query(self, q):
        if isinstance(q, GroundedPredicate):
            return self.knowledge[q]
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
