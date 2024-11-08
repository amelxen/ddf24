import pycode_similar
import ast
import tokenize
from io import BytesIO
import vulture
import sys, os


class Normalizer(ast.NodeTransformer):

    def __init__(self, unused_vars=dict()):
        super(Normalizer, self).__init__()
        self._node_count = 0
        self.unused_vars = unused_vars
        self._assign_ctx = False
        self._tuple_ctx = False

    @staticmethod
    def _mark_docstring_sub_nodes(node):

        def _mark_docstring_nodes(body):
            if body and isinstance(body, pycode_similar.collections.Sequence):
                for n in body:
                    if isinstance(n, ast.Expr) and isinstance(n.value, ast.Str):
                        n.is_docstring = True

        node_body = getattr(node, "body", None)
        _mark_docstring_nodes(node_body)
        node_orelse = getattr(node, "orelse", None)
        _mark_docstring_nodes(node_orelse)

    @staticmethod
    def _is_docstring(node):
        return getattr(node, "is_docstring", False)

    def visit_Constant(self, node):
        node.value = "_VALUE_"
        return self.generic_visit(node)

    def visit_keyword(self, node):
        node.arg = "_KEYWORD_"
        return self.generic_visit(node)

    def visit_Expr(self, node):
        if not self._is_docstring(node):
            self.generic_visit(node)
            if hasattr(node, "value"):
                return node

    def visit_arg(self, node):
        node.arg = "_ARG_"
        del node.annotation
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if node.id in self.unused_vars and node.lineno in self.unused_vars[node.id]:
            if self._assign_ctx and not self._tuple_ctx:
                return
            node.id = "_UNUSED_"
        elif not (node.id.startswith("_") and node.id.endswith("_")):
            node.id = "_NAME_"
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        node.attr = "_ATTR_"
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

    def visit_Assign(self, node):
        self._assign_ctx = True
        new_targets = []
        for target in node.targets:
            tmp = self.visit(target)
            if tmp is not None:
                new_targets.append(tmp)
        self._assign_ctx = False
        if len(new_targets) == 0:
            return
        self.generic_visit(node)
        return node

    def visit_AnnAssign(self, node):
        self._assign_ctx = True
        tmp = self.visit(node.target)
        self._assign_ctx = False
        if tmp is None:
            return
        self.generic_visit(node)
        return node

    def visit_AugAssign(self, node):
        self._assign_ctx = True
        tmp = self.visit(node.target)
        self._assign_ctx = False
        if tmp is None:
            return
        self.generic_visit(node)
        return node

    def visit_Tuple(self, node):
        if self._assign_ctx:
            self._tuple_ctx = True
        self.generic_visit(node)
        self._tuple_ctx = False
        for node in node.elts:
            if not isinstance(node, ast.Name) or node.id != "_UNUSED_":
                return node

    def visit_Import(self, node):
        pass

    def visit_ImportFrom(self, node):
        pass


def get_unused_vars(code: str) -> dict[str, set[int]]:
    try:
        vul = vulture.Vulture()
        sys.stdout = open(os.devnull, "w")
        vul.scan(code)
        unused = vul.get_unused_code()
        sys.stdout = sys.__stdout__
    except Exception as ex:
        sys.stdout = sys.__stdout__
        raise ex
    res = {}
    for item in unused:
        if item.typ == "variable":
            res.setdefault(item.name, set()).add(item.first_lineno)
    return res


def tree_normalization(
    code: str,
    normalizer: type[ast.NodeTransformer] = ast.NodeTransformer,
    remove_unused=False,
) -> ast.AST:
    if normalizer is Normalizer:
        if remove_unused:
            unused_vars = get_unused_vars(code)
            norm = normalizer(unused_vars)
            if len(unused_vars) > 0:
                pass
        else:
            norm = normalizer()
    else:
        norm = normalizer()

    root = ast.parse(code)
    norm.visit(root)
    return root


def str_normalization(
    code: str,
    normalizer: type[ast.NodeTransformer] = ast.NodeTransformer,
    remove_unused=False,
) -> str:
    return ast.unparse(tree_normalization(code, normalizer, remove_unused))


def str_tokenize(code: str) -> list[str]:
    g = tokenize.tokenize(BytesIO(code.encode("utf-8")).readline)
    res = []
    for token, val, _, _, _ in g:
        if token in [4, 5, 6, 63, 0]:
            continue
        res.append(val)
    return res
