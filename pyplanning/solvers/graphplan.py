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
    def __init__(self, prev_layer, actions):
        self.prev_layer = prev_layer
        for prop in self.prev_layer.state.knowledge:
            actions.append(NopAction(prop))
        self.actions = frozenset(actions)

        all_effects = set()
        for ga in actions:
            all_effects.update(ga.effects)
        self.state = KnowledgeState(all_effects, True)

        self.action_mutex = set()
        self.get_action_mutex()
        self.literal_mutex = set()
        self.get_literal_mutex()

    def get_action_mutex(self):
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
                for p2 in actions[1].precondition:
                    if frozenset([p, p2]) in self.prev_layer.literal_mutex:
                        self.action_mutex.add(frozenset(actions))
                        break

    def get_literal_mutex(self):
        # Direct mutex (e.g. literal and ~literal)
        for literal in self.state.knowledge:
            if isinstance(literal, NOT) and literal.prop in self.state.knowledge:
                self.literal_mutex.add(frozenset([literal.prop, literal]))
            elif NOT(literal) in self.state.knowledge:
                self.literal_mutex.add(frozenset([literal, NOT(literal)]))
        # Inconsistent support
        for literals in itertools.combinations(self.state.knowledge, 2):
            l1_a = self.get_producing_actions(literals[0])
            l2_a = self.get_producing_actions(literals[1])
            found = False
            for action_pair in itertools.product(l1_a, l2_a):
                if frozenset(action_pair) not in self.action_mutex:
                    found = True  # non-mutex action pair means literals can be produced
                    break
            if not found:
                self.literal_mutex.add(frozenset(literals))

    def get_producing_actions(self, literal):
        producing = []
        for a in self.actions:
            if literal in a.effects:
                producing.append(a)
        return producing


class InitialLevel(Level):
    def __init__(self, state):
        self.prev_layer = None
        self.actions = frozenset()
        self.state = state
        self.action_mutex = set()
        self.literal_mutex = set()


class PlanningGraph:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.grounded_actions = make_grounded_actions(problem)
        self.init_state = KnowledgeState(make_grounded_preds(
            problem, problem.initial_state.knowledge), explicit_delete=True)
        self.levels = [InitialLevel(self.init_state)]

    def get_current_state(self):
        return self.levels[-1].state

    def expand_graph(self):
        curr_state = self.get_current_state()
        valid_actions = []
        for ga in self.grounded_actions:
            if ga.action.check_preconditions(curr_state, ga.objects):
                valid_actions.append(ga)
        level = Level(self.levels[-1], valid_actions)
        self.levels.append(level)

    def check_goal(self):
        return self.problem.check_goal(self.get_current_state())
