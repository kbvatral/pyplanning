from strips import KnowledgeState, Problem
import itertools

def bfs_solve(problem: Problem):
    visited = []
    queue = [(problem.initial_state, [])]

    while len(queue) > 0:
        s, plan = queue.pop(0)
        if s in visited:
            continue
        visited.append(s)
        if problem.check_goal(s):
            return True, plan

        for a, next_ks in generate_next_states(problem, s):
            if next_ks not in visited:
                new_plan = plan + [a]
                queue.append((next_ks, new_plan))
    return False, []

def generate_next_states(problem: Problem, state: KnowledgeState):
    next_states = []
    for a_name, a in problem.domain.actions.items():
        for objs in itertools.permutations(problem.objects, a.num_params):
            res, next_ks = a.take_action(state, objs)
            if res:
                next_states.append((a.ground(objs), next_ks))
    return next_states
