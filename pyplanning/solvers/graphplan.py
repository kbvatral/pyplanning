import itertools
from ..strips import KnowledgeState, Problem
from ..action import NopAction
from ..logic import AND, NOT, Predicate
from ..utils import PriorityQueue
import copy
import time


def graph_plan(problem: Problem, max_depth=1000, print_debug=False):
    graph = PlanningGraph(problem)
    if graph.check_goal():
        return {}

    for i in range(max_depth):
        if print_debug:
            print("Level {}".format(i+1))

        tic = time.time()
        graph.expand_graph()
        toc = time.time()
        if print_debug:
            print("\t Expansion Time: %.3f" % (toc - tic))

        if graph.check_goal():
            tic = time.time()
            res, plan = graph.extract_solution()
            toc = time.time()
            if print_debug:
                print("\t Extraction Time: %.3f" % (toc - tic))
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


def make_grounded_actions(problem, constant_predicates):
    """
    Make a set of actions grounded in every possible set of literals
    and NopActions for every possible predicate
    """
    grounded = []
    for a_name, a in problem.domain.actions.items():
        for objs in itertools.product(*[problem.get_typed_objs(t) for t in a.types]):
            if len(set(objs)) != len(objs):
                continue
            grounded.append(a.ground(objs))

    for p_name, p in problem.domain.predicates.items():
        if p in constant_predicates:
            continue
        for objs in itertools.product(*[problem.get_typed_objs(t) for t in p.types]):
            if len(set(objs)) != len(objs):
                continue
            gp = p.ground(objs)
            gpn = NOT(gp)
            grounded.append(NopAction(gp))
            grounded.append(NopAction(gpn))

    return frozenset(grounded)


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


def find_constant_predicates(problem: Problem):
    constant_predicates = set(problem.domain.predicates.values())
    for p in problem.domain.predicates.values():
        constant_predicates.add(NOT(p))

    for a in problem.domain.actions.values():
        for prop in a.effect.props:
            constant_predicates.discard(prop)
            if isinstance(prop, NOT):
                constant_predicates.discard(prop.prop)
            else:
                constant_predicates.discard(NOT(prop))
    return constant_predicates


def find_constant_knowledge(knowledge: KnowledgeState, constant_predicates):
    constant_knowledge = set()
    for k in knowledge.knowledge:
        if isinstance(k, NOT):
            raw_pred = NOT(k.prop.unground())
        else:
            raw_pred = k.unground()
        if raw_pred in constant_predicates:
            constant_knowledge.add(k)
    return constant_knowledge


class Level:
    def __init__(self, prev_layer, actions):
        self.prev_layer = prev_layer
        self.actions = frozenset(actions)
        all_effects = get_all_effects(actions)
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
        producing_actions = {}
        # Direct mutex (e.g. literal and ~literal)
        for literal in self.state.knowledge:
            if isinstance(literal, NOT) and literal.prop in self.state.knowledge:
                self.literal_mutex.add(frozenset([literal.prop, literal]))
            elif NOT(literal) in self.state.knowledge:
                self.literal_mutex.add(frozenset([literal, NOT(literal)]))
            # Cache producing actions for use below
            producing_actions[literal] = self.get_producing_actions(literal)
        
        # Inconsistent support
        for literals in itertools.combinations(self.state.knowledge, 2):
            l1_a = producing_actions[literals[0]]
            l2_a = producing_actions[literals[1]]
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
        self.init_state = KnowledgeState(make_grounded_preds(
            problem, problem.initial_state.knowledge), explicit_delete=True)
        self.levels = [InitialLevel(self.init_state)]
        self.constant_predicates = find_constant_predicates(problem)
        self.constant_knowledge = find_constant_knowledge(self.init_state, self.constant_predicates)
        self.grounded_actions = make_grounded_actions(problem, self.constant_predicates)
        self.no_goods = set()
        self.no_goods_history = []

    def get_current_state(self):
        full_knowledge = self.levels[-1].state.knowledge.union(self.constant_knowledge)
        return KnowledgeState(full_knowledge, True)

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

    def remove_constant_knowledge(self, k):
        mutable = k.copy()
        for pred in k:
            if pred in self.constant_knowledge:
                mutable.discard(pred)
        return mutable

    def extract_solution(self):
        last_level = len(self.levels) - 1
        self.no_goods_history.append(self.no_goods.copy())
        g = self.remove_constant_knowledge(self.goals)
        return self.backward_search(last_level, g)

    def backward_search(self, level, goals):
        if (level, goals) in self.no_goods:
            return False, None
        if level == 0:
            if self.levels[level].state.query(AND(goals)):
                return True, {0: {}}
            else:
                self.no_goods.add((level, goals))
                return False, None

        # Use BFS to find a set of actions that achieves the goals
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
                precons = self.remove_constant_knowledge(precons)
                res, subplan = self.backward_search(
                    level-1, frozenset(precons))
                if res:
                    plan = copy.deepcopy(subplan)
                    plan[level] = action_set
                    return True, plan
            else:
                # Expand the current action set with any relevant actions
                # which are not in mutex with the current set
                goals_remaining = goals.difference(all_effects)
                for ra in get_relevant_actions(current_level.actions, goals_remaining):
                    if not check_mutex(current_level, action_set, ra):
                        new_set = frozenset(list(action_set) + [ra])
                        if new_set not in visited:
                            fringe.push(new_set)

        # If the fringe is empty without returning,
        # then we have a no good
        self.no_goods.add((level, goals))
        return False, None


def check_mutex(level: Level, action_set, action):
    """
    Determines whether an action is mutex with any of the actions
    in the given set of actions at the given level
    """
    for a in action_set:
        if frozenset([action, a]) in level.action_mutex:
            return True
    return False


def get_all_effects(action_set):
    """
    Returns a set of all effects for the actions in the given set
    """
    all_effects = set()
    for a in action_set:
        all_effects.update(a.effects)
    return all_effects


def get_all_preconditions(action_set):
    """
    Returns a set of all preconditions for the actions in the given set
    """
    all_precons = set()
    for a in action_set:
        all_precons.update(a.precondition)
    return all_precons


def get_relevant_actions(all_actions, goals):
    """
    Returns a subset of actions which have at least one of the goals
    in their effects
    """
    relevant = []
    for a in all_actions:
        if len(a.effects.intersection(goals)) > 0:
            relevant.append(a)
    return relevant
