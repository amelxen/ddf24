import ast
import pathlib

import index.top_k
import sim_alg.ast
import sim_alg.lcs
import sim_alg.levenshtein
import tools
import normalization
import index
from model import binary_classification, aggregate
import sim_alg
import code_complexity


def predict(
    sources: dict[str, str],
    targets: list[str],
    weights_path: pathlib.Path,
    top_k: int = 20,
) -> dict[str, tuple[bool, list[str]]]:

    data_tree = {}
    data_tokens = {}

    for key in sources:
        try:
            tree = normalization.tree_normalization(
                sources[key], normalization.Normalizer, True
            )
            toks = normalization.str_tokenize(ast.unparse(tree))
            data_tree[key] = tree
            data_tokens[key] = toks
        except Exception:
            pass

    indexer = index.top_k.AstIndexer(list(data_tree.items()))
    model = binary_classification.BinClassifier()
    model.load_model(weights_path)
    loger = tools.PrintRunTime(1, len(targets), 1)
    res = {}

    for target in targets:
        potential_clones = indexer.get_top_k(target, top_k)
        tree_samples, tok_samples = {}, {}
        for clone in potential_clones:
            tree_samples[clone] = ast.dump(data_tree[clone], indent=4)
            tok_samples[clone] = data_tokens[clone]

        features = []

        mat = sim_alg.levenshtein.levenshtein_dist_ratio_array(
            tok_samples, {target: data_tokens[target]}
        )
        feature = aggregate.agg_max(mat)
        features.append(feature[target])

        mat = sim_alg.lcs.lcs_dist_ratio_array(
            tok_samples, {target: data_tokens[target]}
        )
        feature = aggregate.agg_max(mat)
        features.append(feature[target])

        mat = sim_alg.ast.ast_str_diff_array(
            tree_samples, {target: ast.dump(data_tree[target])}
        )
        feature = aggregate.agg_max(mat)
        features.append(feature[target])

        vol, dif = code_complexity.hal_harvester(data_tree[target])
        count = code_complexity.count_tokens(data_tokens[target])
        features.append(vol)
        features.append(dif)
        features.append(count)

        loger.dump(f'"{target}"')
        pred = model.predict([features])[0]
        if pred == 0:
            res[target] = (True, potential_clones)
        else:
            res[target] = (False, potential_clones)

    return res
