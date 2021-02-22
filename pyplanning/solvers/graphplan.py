import itertools
from ..strips import KnowledgeState, Problem
from ..action import NopAction
from ..logic import NOT

def graph_plan(problem: Problem):
    grounded_actions = make_grounded_actions(problem)
    initial = make_grounded_preds(problem, problem.initial_state.knowledge)
    state = KnowledgeState(initial, explicit_delete=True)
    
    valid_actions = []
    for ga in grounded_actions:
        if ga.action.check_preconditions(state, ga.objects):
            valid_actions.append(ga)
    level = Level(state, valid_actions)
    return level

def make_grounded_actions(problem):
    grounded = []
    for a_name, a in problem.domain.actions.items():
        for objs in itertools.product(*[problem.get_typed_objs(t) for t in a.types]):
            if len(set(objs)) != len(objs):
                continue
            grounded.append(a.ground(objs))
    return grounded
    
def make_grounded_preds(problem, initial):
    grounded = set(initial)
    for p_name, p in problem.domain.predicates.items():
        for objs in itertools.product(*[problem.get_typed_objs(t) for t in p.types]):
            if len(set(objs)) != len(objs):
                continue
            gp = p.ground(objs)
            if gp not in grounded:
                grounded.add(NOT(gp))
    return grounded

class Level:
    def __init__(self, state, actions):
        self.prev_state = state
        for prop in self.prev_state.knowledge:
            actions.append(NopAction(prop))
        self.actions = frozenset(actions)
        
        all_effects = set()
        for ga in actions:
            all_effects.update(ga.effects)
        self.next_state = KnowledgeState(all_effects)
