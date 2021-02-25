def null_heuristic(state):
    return 0

def plan_len(plan):
    if plan is None:
        return float('inf')
    else:
        return len(plan)

# def ignore_delete_heuristic(problem):
#     from .search import __asearch
#     def h(state):
#         plan = __asearch(problem, state, null_heuristic, "ignore")
#         return plan_len(plan)
#     return h