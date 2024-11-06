from ast import parse

import ast

class AstHashVisitor(ast.NodeVisitor):
    def __init__(self, d, min_size = 15):
        self.mod = 1000000007
        self.d = d
        self.min_size = min_size

    def node_hash(self, l):
        return sum(l)

    def visit_or_default(self, node):
        res = self.visit(node)

        if res is None:
            return 1, 301122

        return res

    def visit_children(self, l):
        return [self.visit_or_default(el) for el in l]

    def save_hash(self, node, res):
        size = sum([e[0] for e in res])
        res_hash = self.node_hash([e[1] for e in res])

        if size >= self.min_size:
            self.d[(size, res_hash % self.mod)].append(node)

        return size, res_hash

    def visit_FunctionDef(self, node):
        return self.save_hash(node, [(1, 413)] + self.visit_children(node.body))

    def visit_Name(self, node):
        return 1, 4

    def visit_Call(self, node):
        return self.save_hash(node, [(1, 423123)] + self.visit_children(node.args))

    def visit_While(self, node):
        return self.save_hash(node, [(1, 4234)] + [self.visit_or_default(node.test)] + self.visit_children(node.body))

if __name__ == "__main__":
    with open('levenshtein.py', 'r') as file:
        code = file.read()
    d = dict()
    visitor = AstHashVisitor(d)
    res = visitor.visit(parse(code))

    t = 8