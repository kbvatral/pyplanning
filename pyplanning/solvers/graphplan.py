import itertools
from ..strips import KnowledgeState, Problem
from ..action import NopAction
from ..logic import NOT


def graph_plan(problem: Problem):
    graph = PlanningGraph(problem)
    graph.expand_graph()
    graph.expand_graph()
    return graph


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
        self.next_state = KnowledgeState(all_effects, True)
        
        self.action_mutex = set()
        self.get_mutex()

    def get_mutex(self):
        for actions in itertools.combinations(self.actions, 2):
            for e in actions[0].effects:
                # Inconsisent effects
                if (isinstance(e, NOT) and e.prop in actions[1].effects) or (NOT(e) in actions[1].effects):
                    self.action_mutex.add(frozenset(actions))
                # Interference (a1 effects -> a2 precondition)
                elif (isinstance(e, NOT) and e.prop in actions[1].precondition) or (NOT(e) in actions[1].precondition):
                    self.action_mutex.add(frozenset(actions))
            for p in actions[0].precondition:
                # Interference (a1 precondition -> a2 effects)
                if (isinstance(p, NOT) and p.prop in actions[1].effects) or (NOT(p) in actions[1].effects):
                    self.action_mutex.add(frozenset(actions))
                # Competing needs
                if (isinstance(p, NOT) and p.prop in actions[1].precondition) or (NOT(p) in actions[1].precondition):
                    self.action_mutex.add(frozenset(actions))

class PlanningGraph:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.levels = []
        self.grounded_actions = make_grounded_actions(problem)
        initial = make_grounded_preds(problem, problem.initial_state.knowledge)
        self.init_state = KnowledgeState(initial, explicit_delete=True)

    def get_current_state(self):
        if len(self.levels) == 0:
            return self.init_state
        curr_level = self.levels[-1]
        return curr_level.next_state

    def expand_graph(self):
        curr_state = self.get_current_state()
        valid_actions = []
        for ga in self.grounded_actions:
            if ga.action.check_preconditions(curr_state, ga.objects):
                valid_actions.append(ga)
        level = Level(curr_state, valid_actions)
        self.levels.append(level)

    def check_goal(self):
        return self.problem.check_goal(self.get_current_state())
