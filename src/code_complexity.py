import radon

import radon.metrics


def hal_harvester(sample: str, v_max=200, d_max=4) -> tuple[float, float]:
    hal = radon.metrics.h_visit(sample)
    vol = hal.total.volume
    dif = hal.total.difficulty
    vol_norm = min(1.0, vol / v_max)
    dif_norm = min(1.0, dif / d_max)
    return vol_norm, dif_norm


def count_tokens(sample: list[str], max_count=400) -> float:
    return min(1.0, len(sample) / max_count)
