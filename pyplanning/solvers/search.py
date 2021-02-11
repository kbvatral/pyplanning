from ..strips import KnowledgeState, Problem
import itertools
from ..utils import PriorityQueue
from .heuristics import null_heuristic


def search_solve(problem: Problem, heuristic=null_heuristic):
    visited = set()
    fringe = PriorityQueue()
    fringe.push((problem.initial_state, []), heuristic(problem.initial_state))

    while len(fringe) > 0:
        s, plan = fringe.pop()
        if s in visited:
            continue
        visited.add(s)
        if problem.check_goal(s):
            return plan

        for a, next_ks in generate_next_states(problem, s):
            if next_ks not in visited:
                new_plan = plan + [a]
                fringe.push((next_ks, new_plan), heuristic(next_ks))
    return None


def generate_next_states(problem: Problem, state: KnowledgeState):
    next_states = []
    for a_name, a in problem.domain.actions.items():
        for objs in itertools.permutations(problem.objects, a.num_params):
            res, next_ks = a.take_action(state, objs)
            if res:
                next_states.append((a.ground(objs), next_ks))
    return next_states
