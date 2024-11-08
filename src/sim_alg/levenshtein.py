from typing import Sequence
import Levenshtein

import tools as tools


def levenshtein_dist_ratio(str1: Sequence, str2: Sequence) -> float:
    return Levenshtein.ratio(str1, str2)


def levenshtein_dist_ratio_array(
    samples: dict[str, Sequence], targets: dict[str, Sequence], debug=False
) -> dict[str, dict[str, float]]:
    res = {}
    if debug:
        dumper = tools.PrintRunTime(len(targets), len(targets) * len(samples))
    for s_key, s_value in samples.items():
        for t_key, t_value in targets.items():
            res.setdefault(s_key, {})[t_key] = levenshtein_dist_ratio(s_value, t_value)
        if debug:
            dumper.dump(f'"{s_key}"')
    return res
