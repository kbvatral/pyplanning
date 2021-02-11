from ..strips import KnowledgeState, Problem
import itertools
import heapq

def null_heuristic(state):
    return 0

def search_solve(problem: Problem, heuristic=null_heuristic):
    visited = set()
    fringe = [(heuristic(problem.initial_state), 0, problem.initial_state, [])]
    heapq.heapify(fringe)
    fringe_count = 1 # used to tie-break costs based on add order

    while len(fringe) > 0:
        _, _, s, plan = heapq.heappop(fringe)
        if s in visited:
            continue
        visited.add(s)
        if problem.check_goal(s):
            return plan

        for a, next_ks in generate_next_states(problem, s):
            if next_ks not in visited:
                new_plan = plan + [a]
                heapq.heappush(fringe, (heuristic(next_ks), fringe_count, next_ks, new_plan))
                fringe_count += 1
    return None

def generate_next_states(problem: Problem, state: KnowledgeState):
    next_states = []
    for a_name, a in problem.domain.actions.items():
        for objs in itertools.permutations(problem.objects, a.num_params):
            res, next_ks = a.take_action(state, objs)
            if res:
                next_states.append((a.ground(objs), next_ks))
    return next_states
