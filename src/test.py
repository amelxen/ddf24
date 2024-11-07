import tools
import normalization
from sim_alg import ast, lcs, levenshtein
from index import asthash, top_k
from model import binary_classification


def main():
    # data_clear = tools.read_yandex_clear()
    data_plag = tools.read_yandex_plag()
    data = data_plag.copy()
    # data.update(data_plag)
    data_copy = {}

    data = dict(list(data.items())[:100])

    for key in data:
        try:
            seq = normalization.str_normalization(
                data[key], normalization.Normalizer, False
            )
            seq = normalization.str_tokenize(seq)
            data_copy[key] = seq
        except Exception:
            pass

    print(" ".join(data_copy["plag_0"]))

    # matrics = levenshtein_dist_ratio_array(data_copy, data_copy, True)
    # threshold = 0.85
    # res = {}
    # for s_key, s_dists in matrics.items():
    #     res[s_key] = {}
    #     for t_key, ratio in s_dists.items():
    #         if s_key == t_key:
    #             continue
    #         if ratio >= threshold:
    #             res[s_key][t_key] = ratio
    # with open("result3.json", "w") as file:
    #     json.dump(res, file)


if __name__ == "__main__":
    main()
