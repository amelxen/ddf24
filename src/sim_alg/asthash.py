from ast import parse
from ast import iter_child_nodes

def line_count(node):
    try:
        if node.end_lineno is None or node.end_col_offset is None:
            return 0
        return node.end_lineno - node.lineno + 1
    except AttributeError:
        return 0

class AstHashVisitor:
    def __init__(self, d, min_size = 20, min_lines = 5):
        self.mod = 1000000007
        self.d = d
        self.min_size = min_size
        self.min_lines = min_lines

    def node_hash(self, l):
        return sum(l) % self.mod #TODO maybe change to better hash

    def visit_children(self, l):
        return [self.visit(el) for el in l]

    def save_hash(self, node, res):
        res_hash = self.node_hash([e[1] for e in res])

        # # By subtree size
        size = sum([e[0] for e in res])
        lc = line_count(node)

        if size >= self.min_size and lc >= self.min_lines:
            if (size, res_hash % self.mod) not in self.d:
                self.d[(size, res_hash % self.mod)] = []
            self.d[(size, res_hash % self.mod)].append(node)

        return size, res_hash

    def visit(self, node):
        children = list(iter_child_nodes(node))
        node_hash = (1, hash(node.__class__.__name__))
        children_hash = self.visit_children(children)
        return self.save_hash(node, [node_hash] + children_hash)


if __name__ == "__main__":
    with open('levenshtein.py', 'r') as file:
        code = file.read()
    d = dict()
    visitor = AstHashVisitor(d)
    visitor.visit(parse(code))

    potential_clones = []
    for key, value in d.items():
        if len(value) < 2:
            continue
        potential_clones.append(value)
    print(potential_clones)