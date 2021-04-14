import itertools
from ..logic import NOT
from ..strips import KnowledgeState, Problem
from .search import __generate_next_states
from ..utils import PriorityQueue


def ff_heuristic(state, problem):
    graph = FFGraph(problem, state)
    return graph.plan_length

def ff_plan(problem: Problem):
    return __enforced_hil_climb(problem, problem.initial_state, heuristic=ff_heuristic)

def __enforced_hil_climb(problem: Problem, start_state: KnowledgeState, heuristic=ff_heuristic):
    current_state = start_state
    plan = []
    h_current = heuristic(start_state, problem)

    while not problem.check_goal(current_state):
        best_h = h_current
        best_a = None
        new_state = None
        for a, next_ks in __generate_next_states(problem, current_state):
            h = heuristic(next_ks, problem)
            if h < best_h:
                best_h = h
                best_a = a
                new_state = next_ks
        
        if best_a is not None:
            h_current = best_h
            plan.append(best_a)
            current_state = new_state
        else:
            current_state, h_current, actions = __bfs_next(problem, current_state, h_current, heuristic)
            if current_state is None:
                raise RuntimeError("Unable to find a plan after exhaustively searching.")
            plan += actions
    
    return plan
        

def __bfs_next(problem, start_state, h_start, heuristic):
    visited = set()
    fringe = PriorityQueue()
    fringe.push((start_state, []), 0)

    while len(fringe) > 0:
        s, plan = fringe.pop()
        if s in visited:
            continue
        h_new = heuristic(s, problem)
        visited.add(s)
        if h_new < h_start:
            return s, h_new, plan

        for a, next_ks in __generate_next_states(problem, s):
            if next_ks not in visited:
                new_plan = plan + [a]
                fringe.push((next_ks, new_plan), 0)
    
    return None, None, None

class FFGraph:
    def __init__(self, problem: Problem, initial_state=None, max_depth=1000) -> None:
        self.problem = problem
        self.goals = frozenset(self.problem.goal_state.props)
        if initial_state is None:
            self.initial_state = KnowledgeState(problem.initial_state.knowledge, False)
        else:
            self.initial_state = initial_state
        self.levels = [FFInitialLevel(self.initial_state)]
        self.__make_grounded_actions()
        
        i=0
        while not self.check_goal():
            i+=1
            self.__expand_graph()
            if i==max_depth:
                raise TimeoutError("Reached max depth before graph completed.")
        self.__extract_plan()
        
    def check_goal(self) -> bool:
        return self.problem.check_goal(self.get_current_state())

    def get_current_state(self) -> KnowledgeState:
        return self.levels[-1].state

    def __make_grounded_actions(self) -> None:
        grounded = []
        for a_name, a in self.problem.domain.actions.items():
            for objs in itertools.product(*[self.problem.get_typed_objs(t) for t in a.types]):
                if len(set(objs)) != len(objs):
                    continue
                grounded.append(a.ground(objs))
        self.grounded_actions = grounded

    def __expand_graph(self) -> None:
        curr_state = self.get_current_state()
        valid_actions = []
        for ga in self.grounded_actions:
            if ga.action.check_preconditions(curr_state, ga.objects):
                valid_actions.append(ga)
        level = FFLevel(self.levels[-1], valid_actions)
        self.levels.append(level)
    
    def __extract_plan(self):
        self.plan = []
        self.plan_length = 0
        deferred_goals = set()
        local_goals = set(self.goals)
        for level in reversed(self.levels):
            level_plan = set()
            achieved_goals = set()
            prev_state = None
            if level.prev_layer is not None:
                prev_state = level.prev_layer.state

            # If goal exists in the previous level, then
            # we defer to the previous level for action.
            # Otherwise, find an action that achieves the goal
            # and put it in the plan
            for g in local_goals:
                if prev_state is not None and prev_state.query(g):
                    deferred_goals.add(g)
                elif g in achieved_goals:
                    continue # goal already achieved by another action
                else:
                    for action in level.actions:
                        if g in action.effects:
                            level_plan.add(action)
                            self.plan_length += 1
                            achieved_goals.update(remove_negatives(action.effects))
                            deferred_goals.update(remove_negatives(action.precondition))
                            break
                    
            self.plan.insert(0, level_plan)
            local_goals = deferred_goals
            deferred_goals = set()


class FFLevel:
    def __init__(self, prev_layer, actions):
        self.prev_layer = prev_layer
        self.actions = frozenset(actions)
        self.__compute_add_effects()
        self.state = KnowledgeState(self.prev_layer.state.knowledge.union(self.add_effects), False)

    def __compute_add_effects(self):
        all_effects = set()
        for a in self.actions:
            all_effects.update(remove_negatives(a.effects))
        self.add_effects = frozenset(all_effects)


class FFInitialLevel(FFLevel):
    def __init__(self, state):
        self.prev_layer = None
        self.actions = frozenset()
        self.state = state

def remove_negatives(props):
    new_props = set()
    for prop in props:
        if not isinstance(prop, NOT):
            new_props.add(prop)
    return new_props