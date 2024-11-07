from typing import Sequence
import Levenshtein
import json

import tools
import normalization


def levenshtein_dist_ratio(str1: Sequence, str2: Sequence) -> float:
    return Levenshtein.ratio(str1, str2)


def levenshtein_dist_ratio_array(samples: dict[str, Sequence], targets: dict[str, Sequence], debug = False) -> dict[str, dict[str, float]]:
    res = {}
    if debug:
        dumper = tools.PrintRunTime(len(targets), len(targets) * len(samples))
    for s_key, s_value in samples.items():
        for t_key, t_value in targets.items():
            res.setdefault(s_key, {})[t_key] = levenshtein_dist_ratio(s_value, t_value)
        if debug:
            dumper.dump(f"\"{s_key}\"")
    return res


if __name__ == "__main__":
    data_clear = tools.read_yandex_clear()
    data_plag = tools.read_yandex_plag()
    data = data_clear.copy()
    data.update(data_plag)
    data_copy = {}

    for key in data:
        try:
            seq = normalization.str_normalization(data[key], normalization.Normalizer, False)
            seq = normalization.str_tokenize(seq)
            data_copy[key] = seq
        except Exception:
            pass

    # print(' '.join(data_copy["plag_0"]))
    # data_copy = dict(list(data_copy.items())[:100])

    matrics = levenshtein_dist_ratio_array(data_copy, data_copy, True)
    threshold = 0.85
    res = {}
    for s_key, s_dists in matrics.items():
        res[s_key] = {}
        for t_key, ratio in s_dists.items():
            if s_key == t_key:
                continue
            if ratio >= threshold:
                res[s_key][t_key] = ratio
    with open("result3.json", "w") as file:
        json.dump(res, file)
