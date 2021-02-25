import itertools
from ..strips import KnowledgeState, Problem
from ..action import NopAction
from ..logic import AND, NOT
from ..utils import PriorityQueue
import copy


def graph_plan(problem: Problem, max_depth=1000):
    graph = PlanningGraph(problem)
    if graph.check_goal():
        return {}

    for i in range(max_depth):
        print("Level {}".format(i+1))
        graph.expand_graph()
        if graph.check_goal():
            res, plan = graph.extract_solution()
            if res:
                return remove_plan_nops(plan)
        if graph.check_graph_levelOff() and graph.check_noGood_levelOff():
            return None # Full planning failure

    raise RuntimeError("Max depth reached in search for a plan.")


def remove_plan_nops(plan):
    new_plan = {}
    for level, actions in plan.items():
        new_actions = set()
        for a in actions:
            if not isinstance(a, NopAction):
                new_actions.add(a)
        if len(new_actions) > 0:
            new_plan[level] = new_actions
    return new_plan


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
        self.goals = frozenset(self.problem.goal_state.props)
        self.grounded_actions = make_grounded_actions(problem)
        self.init_state = KnowledgeState(make_grounded_preds(
            problem, problem.initial_state.knowledge), explicit_delete=True)
        self.levels = [InitialLevel(self.init_state)]
        self.no_goods = set()
        self.no_goods_history = []

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
        base_check = self.problem.check_goal(self.get_current_state())
        if base_check:
            for a_pair in itertools.combinations(self.problem.goal_state.props, 2):
                if frozenset(a_pair) in self.levels[-1].literal_mutex:
                    return False
            return True
        return False

    def check_graph_levelOff(self):
        if len(self.levels) < 2:
            return False

        curr_level = self.levels[-1]
        prev_level = self.levels[-2]
        
        actions_bool = (curr_level.actions == prev_level.actions)
        state_bool = (curr_level.state == prev_level.state)
        action_mutex_bool = (curr_level.action_mutex == prev_level.action_mutex)
        literal_mutex_bool = (curr_level.literal_mutex == prev_level.literal_mutex)

        if actions_bool and state_bool and action_mutex_bool and literal_mutex_bool:
            return True
        return False

    def check_noGood_levelOff(self):
        if len(self.no_goods_history) < 2:
            return False
        return (self.no_goods == self.no_goods_history[-1])

    def extract_solution(self):
        last_level = len(self.levels) - 1
        self.no_goods_history.append(self.no_goods.copy())
        return self.backward_search(last_level, self.goals)

    def backward_search(self, level, goals):
        if (level, goals) in self.no_goods:
            return False, None
        if level == 0:
            if self.levels[level].state.query(AND(goals)):
                return True, {0: {}}
            else:
                self.no_goods.add((level, goals))
                return False, None

        current_level = self.levels[level]
        fringe = PriorityQueue()
        visited = set()
        for a in get_relevant_actions(current_level.actions, goals):
            fringe.push(frozenset([a]))

        while len(fringe) > 0:
            action_set = fringe.pop()
            if action_set in visited:
                continue
            visited.add(action_set)
            all_effects = get_all_effects(action_set)

            if goals.issubset(all_effects):
                # Found a set of actions that achieves the goals,
                # now check if the preconditions for those actions are reachable
                precons = get_all_preconditions(action_set)
                res, subplan = self.backward_search(
                    level-1, frozenset(precons))
                if res:
                    plan = copy.deepcopy(subplan)
                    plan[level] = action_set
                    return True, plan
            else:
                goals_remaining = goals.difference(all_effects)
                for ra in get_relevant_actions(current_level.actions, goals_remaining):
                    if not check_mutex(current_level, action_set, ra):
                        new_set = frozenset(list(action_set) + [ra])
                        if new_set not in visited:
                            fringe.push(new_set)

        self.no_goods.add((level, goals))
        return False, None


def check_mutex(level: Level, action_set, action):
    for a in action_set:
        if frozenset([action, a]) in level.action_mutex:
            return True
    return False


def get_all_effects(action_set):
    all_effects = set()
    for a in action_set:
        all_effects.update(a.effects)
    return all_effects


def get_all_preconditions(action_set):
    all_precons = set()
    for a in action_set:
        all_precons.update(a.precondition)
    return all_precons


def get_relevant_actions(all_actions, goals):
    relevant = []
    for a in all_actions:
        if len(a.effects.intersection(goals)) > 0:
            relevant.append(a)
    return relevant
