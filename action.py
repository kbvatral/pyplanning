from logic import GroundedPredicate, NOT, Proposition, AND, Predicate, OR


class Action:
    def __init__(self, name, parameters, precondition, effect):
        self.name = name
        self.parameters = parameters

        if not isinstance(precondition, Proposition):
            raise TypeError("Precondition must be of type Proposition")
        self.precondition = precondition

        if not isinstance(effect, AND):
            raise TypeError("Effect must be of type AND")
        for e in effect.props:
            if not is_teachable(e):
                raise TypeError("Effect must be a conjunction of only objects of teachable predicates.")
        self.effect = effect
    
    def check_preconditions(self, state, objects):
        if len(objects) != len(self.parameters):
            raise ValueError("Incorrect number of paramters: expected {}, got {}".format(len(self.parameters), len(objects)))
        mapping = {}
        for param, obj in zip(self.parameters, objects):
            mapping[param] = obj
        ground_pre = ground_proposition_by_map(self.precondition, mapping)
        return state.query(ground_pre)

    def process_effects(self, state, objects):
        if len(objects) != len(self.parameters):
            raise ValueError("Incorrect number of paramters: expected {}, got {}".format(len(self.parameters), len(objects)))
        mapping = {}
        for param, obj in zip(self.parameters, objects):
            mapping[param] = obj
        ground_effect = ground_proposition_by_map(self.effect, mapping)
        state_new = state.copy()
        for e in ground_effect.props:
            state_new.teach(e)
        return state_new
    
    def take_action(self, state, objects):
        if len(objects) != len(self.parameters):
            raise ValueError("Incorrect number of paramters: expected {}, got {}".format(len(self.parameters), len(objects)))
        if self.check_preconditions(state, objects):
            return True, self.process_effects(state, objects)
        return False, state

def ground_proposition_by_map(prop, variable_map):
    if isinstance(prop, Predicate):
        objs = []
        for var in prop.variables:
            if var in variable_map:
                objs.append(variable_map[var])
            else:
                raise ValueError("Unable to find object for variable {} in the provided mapping.".format(var))
        return prop.ground(objs)
    elif isinstance(prop, GroundedPredicate):
        return prop
    elif isinstance(prop, AND):
        return AND([ground_proposition_by_map(p, variable_map) for p in prop.props])
    elif isinstance(prop, OR):
        return OR([ground_proposition_by_map(p, variable_map) for p in prop.props])
    elif isinstance(prop, NOT):
        return NOT(ground_proposition_by_map(prop.prop, variable_map))
    else:
        raise TypeError("Input must be of type Proposition.")

def is_teachable(prop):
    if isinstance(prop, NOT) and is_predicate(prop.prop):
        return True
    elif is_predicate(prop):
        return True
    else:
        return False
        
def is_predicate(prop):
    if isinstance(prop, Predicate) or isinstance(prop, GroundedPredicate):
        return True
    return False