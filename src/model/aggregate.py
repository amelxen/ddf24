
def agg_max(mat: dict[str, dict[str, float]]) -> dict[str, float]:
    res = {}
    for s_key, s_dists in mat.items():
        for t_key, ratio in s_dists.items():
            if s_key == t_key:
                continue
            if res.setdefault(t_key, 0.0) < ratio:
                res[t_key] = ratio
    return res
