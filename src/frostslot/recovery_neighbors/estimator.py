from collections import defaultdict
from math import fsum, sqrt
from statistics import median


def weighted_percentile(pairs, quantile):
    ranked = sorted(pairs)
    threshold = fsum(weight for _, weight in ranked) * quantile
    running_mass = 0.0
    for value, weight in ranked:
        running_mass += weight
        if running_mass >= threshold:
            return value
    return ranked[-1][0]


def train(rows):
    by_store = defaultdict(list)
    points = []
    for row in rows:
        reference = (row.x, row.y, row.signal.record.case_id)
        points.append(reference)
        by_store[row.signal.record.group].append(reference)
    return {
        "cold_load": list(points),
        "stores": dict(by_store),
        "neighborhood": 11,
        "guard_fraction": 0.67,
        "median_recovery": median(row.y for row in rows),
    }


def _rank(reference, current):
    profile, outcome, case_id = reference
    weights = (2.25, 1.5, 0.55, 1.0)
    change = sqrt(
        fsum(weight * (a - b) ** 2 for weight, a, b in zip(weights, profile, current))
    )
    return change, case_id, outcome


def infer(state, signal):
    local = state["stores"].get(signal.record.group, [])
    rank_set = local if len(local) >= 18 else state["cold_load"]
    nearby = sorted(_rank(row, signal.normalized) for row in rank_set)[
        : state["neighborhood"]
    ]
    if nearby[0][0] > 5.5:
        return float(state["median_recovery"])
    weights = [(time, 1 / max(0.16, distance) ** 1.3) for distance, _, time in nearby]
    return weighted_percentile(weights, state["guard_fraction"])


def explain(state):
    return {
        "k": state["neighborhood"],
        "quantile": state["guard_fraction"],
        "median_minutes": state["median_recovery"],
        "reference_cases": {
            store: len(readings) for store, readings in state["stores"].items()
        },
    }
