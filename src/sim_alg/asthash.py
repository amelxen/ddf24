from ast import parse
from ast import iter_child_nodes


class AstHashVisitor:
    def __init__(self, d, min_size = 15):
        self.mod = 1000000007
        self.d = d
        self.min_size = min_size

    def node_hash(self, l):
        return sum(l) % self.mod

    def visit_children(self, l):
        return [self.visit(el) for el in l]

    def save_hash(self, node, res):
        size = sum([e[0] for e in res])
        res_hash = self.node_hash([e[1] for e in res])

        if size >= self.min_size:
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
    res = visitor.visit(parse(code))