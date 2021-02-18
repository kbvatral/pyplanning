from .logic import NOT, Proposition, AND, Predicate, OR


class Action:
    def __init__(self, name, parameters, precondition, effect):
        self.name = name
        self.parameters = []
        self.types = []
        if parameters is not None:
            for p, t in parameters:
                self.parameters.append(p)
                self.types.append(t)
        self.num_params = len(self.parameters)

        if not isinstance(precondition, Proposition) and precondition is not None:
            raise TypeError("Precondition must be of type Proposition")
        self.precondition = precondition

        if effect is not None:
            if not isinstance(effect, AND):
                raise TypeError("Effect must be of type AND")
            for e in effect.props:
                if not is_teachable(e):
                    raise TypeError(
                        "Effect must be a conjunction of only teachable predicates.")
        self.effect = effect

    def check_preconditions(self, state, objects):
        if self.precondition is None:
            return True

        if len(objects) != len(self.parameters):
            raise ValueError("Incorrect number of paramters: expected {}, got {}".format(
                len(self.parameters), len(objects)))
        mapping = {}
        for param, obj in zip(self.parameters, objects):
            mapping[param] = obj
        ground_pre = ground_proposition_by_map(self.precondition, mapping)
        return state.query(ground_pre)

    def process_effects(self, state, objects, delete_method="delete"):
        if self.effect is None:
            return state.teach([])

        if len(objects) != len(self.parameters):
            raise ValueError("Incorrect number of paramters: expected {}, got {}".format(
                len(self.parameters), len(objects)))
        mapping = {}
        for param, obj in zip(self.parameters, objects):
            mapping[param] = obj
        ground_effect = ground_proposition_by_map(self.effect, mapping)
        return state.teach(ground_effect.props, delete_method)

    def take_action(self, state, objects, delete_method="delete"):
        if len(objects) != len(self.parameters):
            raise ValueError("Incorrect number of paramters: expected {}, got {}".format(
                len(self.parameters), len(objects)))
        if self.check_preconditions(state, objects):
            return True, self.process_effects(state, objects, delete_method)
        return False, state

    def ground(self, objects):
        return GroundedAction(self, objects)


class GroundedAction:
    def __init__(self, action, objects):
        if len(objects) != action.num_params:
            raise TypeError("Incorrect number of variables: expected {}, got {}".format(
                action.num_params, len(objects)))

        self.action = action
        self.objects = objects

    def __repr__(self) -> str:
        return "{}({})".format(self.action.name, ", ".join(self.objects))


def ground_proposition_by_map(prop, variable_map):
    if isinstance(prop, Predicate):
        return prop.ground(variable_map)
    elif isinstance(prop, AND):
        return AND([ground_proposition_by_map(p, variable_map) for p in prop.props])
    elif isinstance(prop, OR):
        return OR([ground_proposition_by_map(p, variable_map) for p in prop.props])
    elif isinstance(prop, NOT):
        return NOT(ground_proposition_by_map(prop.prop, variable_map))
    else:
        raise TypeError("Input must be of type Proposition.")


def is_teachable(prop):
    if isinstance(prop, NOT) and isinstance(prop.prop, Predicate):
        return True
    elif isinstance(prop, Predicate):
        return True
    else:
        return False
