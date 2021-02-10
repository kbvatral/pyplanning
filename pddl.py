from logic import AND, NOT, OR, Predicate, Proposition
from action import Action
from utils import TextTree
import re
from strips import Domain

def load_pddl(domain_file, problem_file):
    pass

def load_domain(domain_file):
    all_text = ""
    with open(domain_file, "r") as df:
        lines = df.readlines()
        all_text = ''.join(lines)

    all_text = all_text.replace('\r', '').replace('\n', '')
    t = TextTree(all_text)

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
            pass
        
        elif text_split[0].lower() == ":predicates":
            for pred in child.children:
                predicates.append(Predicate.from_str(pred.text))
        
        elif text_split[0].lower() == ":action":
            action_name = text_split[1]
            parameters =  None
            precondition = None
            effect = None
            for i, item in enumerate(text_split[2:]):
                if item.lower() == ":parameters":
                    ws_pattern = re.compile(r'\s+')
                    params = list(filter(None, re.sub(ws_pattern, '', child.children[i].text).split("?")))
                    parameters = params
                elif item.lower() == ":precondition":
                    precondition = process_proposition_nodes(child.children[i])
                elif item.lower() == ":effect":
                    effect = process_proposition_nodes(child.children[i])
                else:
                    raise SyntaxError("Unrecognized keyword in action definition: {}".format(item))
            actions.append(Action(action_name, parameters, precondition, effect))

    return Domain(domain_name, predicates, actions)

def process_proposition_nodes(t):
    txt = t.text.replace(" ", "").lower()
    if txt == "and":
        if len(t.children) < 2:
            raise SyntaxError("AND statement must contain at least 2 arguments.")
        return AND([process_proposition_nodes(c) for c in t.children])
    elif txt == "or":
        if len(t.children) < 2:
            raise SyntaxError("OR statement must contain at least 2 arguments.")
        return OR([process_proposition_nodes(c) for c in t.children])
    elif txt == "not":
        if len(t.children) != 1:
            raise SyntaxError("Incorrect number of arguments for NOT statement.")
        return NOT(process_proposition_nodes(t.children[0]))
    else:
        return Predicate.from_str(t.text)