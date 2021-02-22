import itertools
from ..strips import KnowledgeState, Problem
from ..action import NopAction

def graph_plan(problem: Problem):
    grounded_actions = make_grounded_actions(problem)

    state = problem.initial_state
    
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
