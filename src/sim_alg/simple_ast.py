import pycode_similar
import json

import tools

def ast_diff_array(samples: dict[str, str], targets: dict[str, str], diff_method = pycode_similar.UnifiedDiff, debug = False) -> dict[str, dict[str, float]]:
    res = {}
    if debug:
        dumper = tools.PrintRunTime(len(targets), len(targets) * len(samples))
    for s_key, s_value in samples.items():
        tmp = [s_value]
        tmp.extend(list(targets.values()))
        t_diffs = pycode_similar.detect(tmp, diff_method, True, True)
        for idx in range(len(t_diffs)):
            t_diffs[idx] = pycode_similar.summarize(t_diffs[idx][1])[0]
        for t_key, t_diff in zip(targets.keys(), t_diffs):
            res.setdefault(s_key, {})[t_key] = t_diff
        if debug:
            dumper.dump(f"\"{s_key}\"")
    return res


if __name__ == "__main__":
    data_clear = tools.read_yandex_clear()
    data_plag = tools.read_yandex_plag()
    data = data_clear.copy()
    data.update(data_plag)

    matrics = ast_diff_array(data, data, debug=True)
    threshold = 0.9
    res = {}
    for s_key, s_dists in matrics.items():
        res[s_key] = {}
        for t_key, ratio in s_dists.items():
            if s_key == t_key:
                continue
            if ratio >= threshold:
                res[s_key][t_key] = ratio
    with open("ast_result.json", "w") as file:
        json.dump(res, file)

