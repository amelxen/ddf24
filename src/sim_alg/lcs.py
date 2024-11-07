from typing import Sequence
import json

import tools
import normalization


def lcs(a: Sequence, b: Sequence) -> int:
    a_h = [elem.__hash__() for elem in a]
    b_h = [elem.__hash__() for elem in b]
    if len(a_h) > len(b_h):
        a_h, b_h = b_h, a_h
    arr1, arr2 = [0 for _ in range(len(b_h) + 1)], [0 for _ in range(len(b_h) + 1)]
    for idx_a in range(len(a_h)):
        for idx_b in range(len(b_h)):
            arr2[idx_b + 1] = arr1[idx_b] + 1 if a_h[idx_a] == b_h[idx_b] else max(arr1[idx_b + 1], arr2[idx_b])
        arr1, arr2 = arr2, arr1
    return arr1[len(b_h)]


def lcs_dist_ratio(str1: Sequence, str2: Sequence) -> float:
    ratio = lcs(str1, str2) / max(len(str1), len(str2))
    return ratio


def lcs_dist_ratio_array(samples: dict[str, Sequence], targets: dict[str, Sequence], debug = False) -> dict[str, dict[str, float]]:
    res = {}
    if debug:
        dumper = tools.PrintRunTime(len(targets), len(targets) * len(samples))
    for s_key, s_value in samples.items():
        for t_key, t_value in targets.items():
            res.setdefault(s_key, {})[t_key] = lcs_dist_ratio(s_value, t_value)
        if debug:
            dumper.dump(f"\"{s_key}\"")
    return res


if __name__ == "__main__":
    data_clear = tools.read_yandex_clear()
    data_plag = tools.read_yandex_plag()
    data = data_clear.copy()
    data.update(data_plag)
    data_copy = {}

    data = dict(list(data.items())[:10])

    for key in data:
        try:
            seq = normalization.str_normalization(data[key], normalization.Normalizer, False)
            seq = normalization.str_tokenize(seq)
            data_copy[key] = seq
        except Exception:
            pass

    matrics = lcs_dist_ratio_array(data_copy, data_copy, True)
    threshold = 0.85
    res = {}
    for s_key, s_dists in matrics.items():
        res[s_key] = {}
        for t_key, ratio in s_dists.items():
            if s_key == t_key:
                continue
            if ratio >= threshold:
                res[s_key][t_key] = ratio
    with open("result4.json", "w") as file:
        json.dump(res, file)
