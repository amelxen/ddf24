import pycode_similar

import src.tools as tools


def ast_diff_array(
    samples: dict[str, str],
    targets: dict[str, str],
    diff_method=pycode_similar.UnifiedDiff,
    debug=False,
) -> dict[str, dict[str, float]]:
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
            dumper.dump(f'"{s_key}"')
    return res


def ast_str_diff_array(
    samples: dict[str, str], targets: dict[str, str], debug=False
) -> dict[str, dict[str, float]]:
    return ast_diff_array(samples, targets, pycode_similar.UnifiedDiff, debug)


def ast_str_diff_array(
    samples: dict[str, str], targets: dict[str, str], debug=False
) -> dict[str, dict[str, float]]:
    return ast_diff_array(samples, targets, pycode_similar.TreeDiff, debug)
