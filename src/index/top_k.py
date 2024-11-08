import itertools
from _ast import AST

from index.asthash import AstHashVisitor, line_count


class AstIndexer:
    def __init__(self, samples_ast: list[tuple[str, AST]]):
        self.samples_hash = dict()
        for sample, ast in samples_ast:
            d = dict()
            visitor = AstHashVisitor(d)
            visitor.visit(ast)
            self.samples_hash[sample] = d

    def get_top_k(self, sample: str, top_k: int) -> list[str]:
        sample_hash = self.samples_hash[sample]
        samples_similarity = []

        for cmp, cmp_hashs in self.samples_hash.items():
            if cmp == sample:
                continue

            all_keys = set(list(sample_hash.keys()) + list(cmp_hashs.keys()))

            similarity = 0

            for key in all_keys:
                if key not in sample_hash or key not in cmp_hashs:
                    continue

                potential_clones = itertools.product(sample_hash[key], cmp_hashs[key])
                for sample_ast, cmp_ast in potential_clones:
                    sample_lines = line_count(sample_ast)
                    cmp_lines = line_count(cmp_ast)

                    similarity += (sample_lines + cmp_lines) / 2

            samples_similarity.append((cmp, similarity))

        sorted_samples = sorted(samples_similarity, key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], sorted_samples))[:top_k]
