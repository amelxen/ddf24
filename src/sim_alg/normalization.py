import pycode_similar
import ast
import tokenize
from io import BytesIO

class Normalizer(ast.NodeTransformer):

    def __init__(self, keep_prints=False):
        super(Normalizer, self).__init__()
        self.keep_prints = keep_prints
        self._node_count = 0

    @staticmethod
    def _mark_docstring_sub_nodes(node):

        def _mark_docstring_nodes(body):
            if body and isinstance(body, pycode_similar.collections.Sequence):
                for n in body:
                    if isinstance(n, ast.Expr) and isinstance(n.value, ast.Str):
                        n.is_docstring = True

        node_body = getattr(node, 'body', None)
        _mark_docstring_nodes(node_body)
        node_orelse = getattr(node, 'orelse', None)
        _mark_docstring_nodes(node_orelse)

    @staticmethod
    def _is_docstring(node):
        return getattr(node, 'is_docstring', False)

    def generic_visit(self, node):
        self._node_count = self._node_count + 1
        self._mark_docstring_sub_nodes(node)
        return super(Normalizer, self).generic_visit(node)

    def visit_Constant(self, node):
        node.value = "_VALUE_"
        return self.generic_visit(node)
        
    def visit_keyword(self, node):
        node.arg = "_KEYWORD_"
        return self.generic_visit(node)

    def visit_Expr(self, node):
        if not self._is_docstring(node):
            self.generic_visit(node)
            if hasattr(node, 'value'):
                return node

    def visit_arg(self, node):
        node.arg = "_ARG_"
        del node.annotation
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if not (node.id.startswith("_") and node.id.endswith("_")):
            node.id = "_NAME_"
        del node.ctx
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        node.attr = "_ATTR_"
        del node.ctx
        self.generic_visit(node)
        return node
    
    def visit_FunctionDef(self, node):
        node.name = "_FUN_"
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        node.name = "_CLASS_"
        self.generic_visit(node)
        return node

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            node.func.id = "_FUN_"
        self.generic_visit(node)
        return node

    def visit_Import(self, node):
        pass

    def visit_ImportFrom(self, node):
        pass


def remove_unused(code: str) -> str:
    pass


def str_normalization(code: str, 
                      normalizer: ast.NodeTransformer = ast.NodeTransformer()
                      ) -> str:
    root = ast.parse(code)
    normalizer.visit(root)
    res = ast.unparse(root)
    return res


def str_tokenize(code: str) -> list[str]:
    g = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
    res = []
    for token, val, _, _, _ in g:
        if token in [4, 5, 6, 63, 0]:
            continue
        res.append(val)
    return res
