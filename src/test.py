import sim_alg.ast
import sim_alg.lcs
import sim_alg.levenshtein
import tools
import normalization
import sim_alg
from index import asthash, top_k
from model import binary_classification
from model import aggregate
import time

import ast


def main():
    data_clear = tools.read_yandex_clear()
    data_plag = tools.read_yandex_plag()
    data = data_clear.copy()
    data.update(data_plag)

    # data = dict(list(data.items())[:20])
    data_tree = {}
    data_tokens = {}


    for key in data:
        try:
            tree = normalization.tree_normalization(
                data[key], normalization.Normalizer, True
            )
            toks = normalization.str_tokenize(ast.unparse(tree))
            data_tree[key] = tree
            data_tokens[key] = toks
        except Exception:
            pass

    # print(" ".join(data_tokens["plag_0"]))
    # print(ast.dump(data_tree["plag_0"], indent=2))

    indexer = top_k.AstIndexer(list(data_tree.items()))
    data_set = ["name,lev,lcs,ast_str,label"]
    loger = tools.PrintRunTime(1, len(data_tree)*4, 0)
    for target in data_tree.keys():

        potential_clones = indexer.get_top_k(target, 20)
        tree_samples, tok_samples = {}, {}
        for clone in potential_clones:
            tree_samples[clone] = ast.dump(data_tree[clone], indent=4)
            tok_samples[clone] = data_tokens[clone]
        loger.dump(f"index \"{target}\"")

        features = [f"\"{target}\""]

        mat = sim_alg.levenshtein.levenshtein_dist_ratio_array(tok_samples, {target: data_tokens[target]})
        feature = aggregate.agg_max(mat)
        features.append(f"{feature[target]:.3f}")
        loger.dump(f"lev \"{target}\"")

        mat = sim_alg.lcs.lcs_dist_ratio_array(tok_samples, {target: data_tokens[target]})
        feature = aggregate.agg_max(mat)
        features.append(f"{feature[target]:.3f}")
        loger.dump(f"lcs \"{target}\"")

        mat = sim_alg.ast.ast_str_diff_array(tree_samples, {target: ast.dump(data_tree[target])})
        feature = aggregate.agg_max(mat)
        features.append(f"{feature[target]:.3f}")
        loger.dump(f"ast \"{target}\"")

        # mat = sim_alg.ast.ast_tree_diff_array(tree_samples, {target: ast.dump(data_tree[target])}, True)
        # feature = aggregate.agg_max(mat)
        # features.append(feature[target])
        # print()

        if target.startswith("plag"):
            features.append(str(0))
        else:
            features.append(str(1))
        
        data_set.append(','.join(features))
        loger.dump(target)

    with open("test.csv", "w") as file:
        file.write('\n'.join(data_set))


if __name__ == "__main__":
    main()
