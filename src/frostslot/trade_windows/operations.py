from collections import defaultdict
from math import isfinite

REVIEW_NAME = "除霜周期和销售窗口"
IMPACT_NAME = "霜层潜热代理量"
HEADROOM_NAME = "复温后剩余窗口/min"
OVERRIDE_NOTE = "高存货陈列柜需要额外复温缓冲"


def operational_check(readings, estimate):
    """高货量柜的时窗包含复温与商品保护缓冲。"""
    dew_point = readings["dew_point"]
    door_minutes = readings["door_minutes"]
    frost_mm = readings["frost_mm"]
    idle_window = readings["idle_window"]
    pallet = readings["pallet"]
    impact = frost_mm * (1 + dew_point / 25) * (1 + door_minutes / 100)
    headroom = idle_window - max(15.0, estimate)
    override = bool(pallet > 72 and idle_window < estimate + 12)
    if not isfinite(impact) or not isfinite(headroom):
        raise ValueError("业务复核的观测量超出计算范围")
    return {
        "name": REVIEW_NAME,
        "impact_label": IMPACT_NAME,
        "headroom_label": HEADROOM_NAME,
        "impact": round(impact, 6),
        "headroom": round(headroom, 6),
        "requires_operator": override,
        "reason": OVERRIDE_NOTE if override else "",
    }


def summarize_workload(actions, evidence):
    distribution = defaultdict(
        lambda: {
            "selected_impact": 0.0,
            "selected": 0,
            "tight_window": 0,
            "needs_operator": 0,
        }
    )
    for action in actions:
        branch = distribution[action.cohort]
        current = evidence[action.case_id]["operational_check"]
        if action.status == "allocated":
            branch["selected"] += 1
            branch["selected_impact"] += current["impact"]
            if current["headroom"] < 0:
                branch["tight_window"] += 1
        if current["requires_operator"]:
            branch["needs_operator"] += 1
    return {
        name: {**data, "selected_impact": round(data["selected_impact"], 4)}
        for name, data in sorted(distribution.items())
    }
