from collections import defaultdict
from propositional import AND, OR, GroundedPredicate


class KnowledgeBase:
    def __init__(self, objects, predicates):
        self.objects = set(objects)
        if len(self.objects) != len(objects):
            raise Warning("Objects with duplicate names were removed.")

        self.predicates = dict()
        for p in predicates:
            self.predicates[p.name] = p
        if len(self.predicates) != len(predicates):
            raise Warning("Predicates with duplicate names were removed.")

        self.knowledge = defaultdict(bool)

    def teach(self, p):
        if not isinstance(p, GroundedPredicate):
            raise TypeError("p must be of type GroundedPredicate.")
        self.knowledge[p] = True

    def query(self, q):
        if isinstance(q, GroundedPredicate):
            res = self.knowledge[str(q)]
        elif isinstance(q, AND):
            res = True
            for prop in q.props:
                res = res and self.query(prop)
        elif isinstance(q, OR):
            res = False
            for prop in q.props:
                res = res or self.query(prop)
        else:
            raise TypeError(
                "Query must be a combination of propositional classes.")
        return res
