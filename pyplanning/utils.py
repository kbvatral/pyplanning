import heapq

class TextTree:
    def __init__(self, text):
        self.raw_text = text
        self.root = TextTreeNode(None)
        start_idx = text.find("(")
        self.process(self.root, text[start_idx+1:])

    def process(self, node, text):
        for i, c in enumerate(text):
            if c == "(":
                new_node = TextTreeNode(node)
                node.add_child(new_node)
                return self.process(new_node, text[i+1:])
            elif c == ")":
                if node.parent is not None:
                    return self.process(node.parent, text[i+1:])
            else:
                node.append(c)

    def print(self):
        self.__print_tree(self.root, 0)
    def __print_tree(self, node, level):
        print("{}{}".format(''.join(["\t" for i in range(level)]), node.text))
        for child in node.children:
            self.__print_tree(child, level+1)


class TextTreeNode:
    def __init__(self, parent):
        self.parent = parent
        self.text = ""
        self.children = []
    def append(self, c):
        self.text += c
    def add_child(self, child):
        self.children.append(child)

class PriorityQueue:
    def __init__(self):
        self.fringe = []
        heapq.heapify(self.fringe)
        self.fringe_count = 0

    def push(self, item, priority):
        item_tuple = (priority, self.fringe_count, item)
        heapq.heappush(self.fringe, item_tuple)
        self.fringe_count += 1

    def pop(self):
        _, _, item = heapq.heappop(self.fringe)
        return item