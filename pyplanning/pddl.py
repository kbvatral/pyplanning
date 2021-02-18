from .logic import AND, NOT, OR, Predicate
from .action import Action
from .utils import TextTree, TypeTree
import re
from .strips import Domain, KnowledgeState, Problem

supported_requirements = {":strips", ":typing", ":disjunctive-preconditions"}


def load_pddl(domain_file, problem_file):
    domain = load_domain(domain_file)
    problem = load_problem(domain, problem_file)
    return domain, problem


def strip_comments(lines):
    strip_comments = []
    for l in lines:
        idx = l.find(";")
        if idx == -1:
            strip_comments.append(l)
        else:
            strip_comments.append(l[:idx])
    return strip_comments


def load_textTree(text_file):
    all_text = ""
    with open(text_file, "r") as df:
        lines = df.readlines()
        lines = strip_comments(lines)
        all_text = ''.join(lines)
    all_text = all_text.replace('\r', '').replace('\n', '')
    return TextTree(all_text)


def load_problem(domain, problem_file):
    t = load_textTree(problem_file)
    if t.root.text.replace(" ", "").lower() != "define":
        raise SyntaxError("Incorrectly formatted PDDL file.")

    problem_name = ""
    objects = {}
    initial_state = KnowledgeState()
    goal_state = None

    for child in t.root.children:
        text_split = list(filter(None, child.text.split()))

        if text_split[0].lower() == "problem":
            problem_name = text_split[1]
        elif text_split[0].lower() == ":domain":
            domain_name = text_split[1]
            if domain_name != domain.name:
                raise SyntaxError(
                    "Domain supplied in problem file does not match the domain supplied in the domain file.")
        elif text_split[0].lower() == ":objects":
            objs = []
            skip_next = True
            for i, o in enumerate(text_split):
                if skip_next:
                    skip_next = False
                elif o == "-":
                    objects[text_split[i+1]] = objs
                    objs = []
                    skip_next = True
                else:
                    objs.append(o)
            if len(objs) != 0:
                objects["object"] = objs
        elif text_split[0].lower() == ":init":
            initial = []
            for pred in child.children:
                i = grounded_pred_from_str(pred.text, domain.predicates.values())
                if i.check_grounded():
                    initial.append(i)
                else:
                    raise SyntaxError(
                        "Initial state must be completely grounded.")
            initial_state = initial_state.teach(initial)
        elif text_split[0].lower() == ":goal":
            goal_state = process_proposition_nodes(child.children[0], domain.predicates.values())
            if not goal_state.check_grounded():
                raise SyntaxError("Goal state must be completely grounded.")
        else:
            raise SyntaxError("Unrecognized keyword: {}".format(text_split[0]))

    return Problem(problem_name, domain, objects, initial_state, goal_state)


def load_domain(domain_file):
    t = load_textTree(domain_file)
    if t.root.text.replace(" ", "").lower() != "define":
        raise SyntaxError("Incorrectly formatted PDDL file.")

    domain_name = ""
    predicates = []
    actions = []
    types = TypeTree()

    for child in t.root.children:
        text_split = list(filter(None, child.text.split()))

        if text_split[0].lower() == "domain":
            domain_name = text_split[1]
        elif text_split[0].lower() == ":requirements":
            for req in text_split[1:]:
                if req.lower() not in supported_requirements:
                    raise NotImplementedError(
                        "The requirement '{}' is not yet supported.".format(req))
        elif text_split[0].lower() == ":types":
            tps = []
            skip_next = True
            for i, t in enumerate(text_split):
                if skip_next:
                    skip_next = False
                elif t == "-":
                    types.add_types(tps, text_split[i+1])
                    tps = []
                    skip_next = True
                else:
                    tps.append(t)
            if len(tps) != 0:
                types.add_types(tps)
        elif text_split[0].lower() == ":predicates":
            for pred in child.children:
                predicates.append(Predicate.from_str(pred.text))
        elif text_split[0].lower() == ":action":
            action_name = text_split[1]
            parameters = None
            precondition = None
            effect = None
            for i, item in enumerate(text_split[2:]):
                if item.lower() == ":parameters":
                    ws_pattern = re.compile(r'\s+')
                    params = list(
                        filter(None, re.sub(ws_pattern, '', child.children[i].text).split("?")))
                    parameters = []
                    for p in params:
                        splits = p.split("-")
                        pname = splits[0]
                        ptype = splits[1] if len(splits) == 2 else None
                        parameters.append((pname, ptype))
                elif item.lower() == ":precondition":
                    precondition = process_proposition_nodes(child.children[i], predicates)
                elif item.lower() == ":effect":
                    effect = process_proposition_nodes(child.children[i], predicates)
                else:
                    raise SyntaxError(
                        "Unrecognized keyword in action definition: {}".format(item))
            actions.append(
                Action(action_name, parameters, precondition, effect))
        else:
            raise SyntaxError("Unrecognized keyword: {}".format(text_split[0]))

    return Domain(domain_name, types, predicates, actions)


def process_proposition_nodes(t, predicates):
    txt = t.text.replace(" ", "").lower()
    if txt == "and":
        return AND([process_proposition_nodes(c, predicates) for c in t.children])
    elif txt == "or":
        return OR([process_proposition_nodes(c, predicates) for c in t.children])
    elif txt == "not":
        if len(t.children) != 1:
            raise SyntaxError(
                "Incorrect number of arguments for NOT statement.")
        return NOT(process_proposition_nodes(t.children[0], predicates))
    else:
        return grounded_pred_from_str(t.text, predicates)

def grounded_pred_from_str(s, predicates):
    s = s.replace('\r', '').replace('\n', '')
    pred = list(filter(None, s.split()))
    if len(pred) < 2:
        raise ValueError(
            "Incorrect formatting for PDDL-style predicate string.")

    name = pred[0]
    pred_match = None
    for p in predicates:
        if p.name == name:
            pred_match = p
            break
    if pred_match is None:
        raise SyntaxError("Predicate not yet defined: {}".format(name))
    
    if len(pred[1:]) != len(pred_match.variables):
        raise SyntaxError("Incorrect number of arguments for the predicate with name {}".format(pred.name))
    var_names = []
    grounding = {}
    for i, p in enumerate(pred[1:]):
        if p[0] == "?":
            if len(p) < 2:
                raise ValueError(
                    "Incorrect formatting for PDDL-style predicate string.")
            if (p[1:], pred_match.types[i]) in var_names:
                raise ValueError("Duplicate variable name found: {}".format(p[1:]))
            var_names.append((p[1:], pred_match.types[i]))
        else:
            vn = "x{}".format(i)
            if (vn, pred_match.types[i]) in var_names:
                raise ValueError("Duplicate variable name found: {}".format(vn))
            var_names.append((vn, pred_match.types[i]))
            grounding[vn] = p
    return Predicate(name, var_names, grounding)
    