from .logic import AND, NOT, OR, Predicate
from .action import Action
from .utils import TextTree
import re
from .strips import Domain, KnowledgeState, Problem

supported_requirements = {":strips"}


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
    objects = []
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
            objects = text_split[1:]
        elif text_split[0].lower() == ":init":
            initial = []
            for pred in child.children:
                i = Predicate.from_str(pred.text)
                if i.check_grounded():
                    initial.append(i)
                else:
                    raise SyntaxError(
                        "Initial state must be completely grounded.")
            initial_state = initial_state.teach(initial)
        elif text_split[0].lower() == ":goal":
            goal_state = process_proposition_nodes(child.children[0])
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
    for child in t.root.children:
        text_split = list(filter(None, child.text.split()))

        if text_split[0].lower() == "domain":
            domain_name = text_split[1]
        elif text_split[0].lower() == ":requirements":
            for req in text_split[1:]:
                if req.lower() not in supported_requirements:
                    raise NotImplementedError(
                        "The requirement '{}' is not yet supported.".format(req))
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
                    parameters = params
                elif item.lower() == ":precondition":
                    precondition = process_proposition_nodes(child.children[i])
                elif item.lower() == ":effect":
                    effect = process_proposition_nodes(child.children[i])
                else:
                    raise SyntaxError(
                        "Unrecognized keyword in action definition: {}".format(item))
            actions.append(
                Action(action_name, parameters, precondition, effect))
        else:
            raise SyntaxError("Unrecognized keyword: {}".format(text_split[0]))

    return Domain(domain_name, predicates, actions)


def process_proposition_nodes(t):
    txt = t.text.replace(" ", "").lower()
    if txt == "and":
        return AND([process_proposition_nodes(c) for c in t.children])
    elif txt == "or":
        return OR([process_proposition_nodes(c) for c in t.children])
    elif txt == "not":
        if len(t.children) != 1:
            raise SyntaxError(
                "Incorrect number of arguments for NOT statement.")
        return NOT(process_proposition_nodes(t.children[0]))
    else:
        return Predicate.from_str(t.text)
