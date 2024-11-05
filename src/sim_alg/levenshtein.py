import Levenshtein
import time
import json

import tools
import preproc


def levenshtein_dist_ratio(str1: bytes, str2: bytes) -> float:
    return Levenshtein.ratio(str1, str2)


def levenshtein_dist_ratio_array(samples: dict[str, bytes], targets: dict[str, bytes], debug = False) -> dict[str, dict[str, float]]:
    res = {}
    if debug:
        start_time = time.time()
        count = 0
    for s_key, s_value in samples.items():
        for t_key, t_value in targets.items():
            res.setdefault(s_key, {})[t_key] = levenshtein_dist_ratio(s_value, t_value)
        if debug:
            count += len(targets)
            print(f"\"{s_key}\":\t {(time.time() - start_time):.2f}s.\t {(count / (0.01+ (time.time() - start_time))):.2f}/s.")
    return res


def levenshtein_max_dist_ratio_array(samples: dict[str, bytes], targets: dict[str, bytes], debug = False) -> dict[str, list[str, float]]:
    matrix = levenshtein_dist_ratio_array(samples, targets, debug)
    res = {}
    for s_key, s_dists in matrix.items():
        for t_key, ratio in s_dists.items():
            if s_key == t_key:
                continue
            if res.setdefault(t_key, ["", 0.0])[1] < ratio:
                res[t_key] = [s_key, ratio]
    return res



if __name__ == "__main__":
    data_clear = tools.read_yandex_clear()
    data_plag = tools.read_yandex_plag()
    data = data_clear.copy()
    data.update(data_plag)

    for key in data:
        data[key] = preproc.prep(data[key])

    matrics = levenshtein_dist_ratio_array(data, data, True)
    threshold = 0.9
    res = {}
    for s_key, s_dists in matrics.items():
        res[s_key] = {}
        for t_key, ratio in s_dists.items():
            if s_key == t_key:
                continue
            if ratio >= threshold:
                res[s_key][t_key] = ratio
    with open("result.json", "w") as file:
        json.dump(res, file)
