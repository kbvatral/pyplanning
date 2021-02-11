from ..strips import KnowledgeState, Problem
import itertools
from ..utils import PriorityQueue
from .heuristics import null_heuristic


def search_plan(problem: Problem, heuristic=null_heuristic):
    return __asearch(problem, problem.initial_state, heuristic)

def __asearch(problem: Problem, start_state, heuristic=null_heuristic, delete_method="delete"):
    visited = set()
    fringe = PriorityQueue()
    fringe.push((start_state, []), heuristic(start_state))

    while len(fringe) > 0:
        s, plan = fringe.pop()
        if s in visited:
            continue
        visited.add(s)
        if problem.check_goal(s):
            return plan

        for a, next_ks in __generate_next_states(problem, s):
            if next_ks not in visited:
                new_plan = plan + [a]
                fringe.push((next_ks, new_plan), heuristic(next_ks))
    return None


def __generate_next_states(problem: Problem, state: KnowledgeState, delete_method="delete"):
    next_states = []
    for a_name, a in problem.domain.actions.items():
        for objs in itertools.permutations(problem.objects, a.num_params):
            res, next_ks = a.take_action(state, objs, delete_method)
            if res:
                next_states.append((a.ground(objs), next_ks))
    return next_states
