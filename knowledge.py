from logic import AND, NOT, OR, Predicate, GroundedPredicate, Proposition
from action import Action


class Domain:
    def __init__(self, predicates, actions):
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
    def __init__(self, domain, objects, initial_state, goal_state):
        if not isinstance(domain, Domain):
            raise TypeError("Supplied domain must be of type Domain.")
        if not isinstance(initial_state, KnowledgeState):
            raise TypeError("Initial State must be of type KnowledgeState.")
        if not isinstance(goal_state, Proposition):
            raise TypeError("Goal state must be of type Proposition.")
        if not goal_state.check_grounded():
            raise TypeError("Goal state must be completely grounded.")

        self.domain = domain
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.objects = set(objects)
        if len(self.objects) != len(objects):
            raise Warning("Objects with duplicate names were removed.")
    
    def check_goal(self, state):
        return state.query(self.goal_state)

class KnowledgeState:
    def __init__(self):
        self.knowledge = set()
    
    def copy(self):
        k = KnowledgeState()
        for p in self.knowledge:
            k.teach(p)
        return k

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

    def __repr__(self):
        return str(self.knowledge)
