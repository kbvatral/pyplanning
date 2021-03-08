from pyplanning.logic import AND


def null_heuristic(state):
    return 0

def plan_len(plan):
    if plan is None:
        return float('inf')
    else:
        return len(plan)

def goals_remaining(problem):
    if not isinstance(problem.goal_state, AND):
        raise TypeError("Goal state must be of type AND to use the goals remaining heuristic.")
    def h(state):
        cost = 0
        for g in problem.goal_state.props:
            if not state.query(g):
                cost += 1
        return cost
    return h

# def ignore_delete_heuristic(problem):
#     from .search import __asearch
#     def h(state):
#         plan = __asearch(problem, state, null_heuristic, "ignore")
#         return plan_len(plan)
#     return h