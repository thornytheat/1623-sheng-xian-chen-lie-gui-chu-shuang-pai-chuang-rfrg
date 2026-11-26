from math import ceil

from ..settings import ACTION_LABEL, FIELD_BOUNDS
from .contracts import Request


def project_request(card, gate, calendar_day=None) -> Request:
    record = card.signal.record
    values = {
        key: record.reported[key]
        if record.reported.get(key) is not None
        else (lo + hi) / 2
        for key, (lo, hi) in FIELD_BOUNDS.items()
    }
    frost_mm = values["frost_mm"]
    occupancy = values["occupancy"]
    idle_window = values["idle_window"]
    score = card.estimate if gate.allowed else card.prior
    blocked = idle_window < 18 or occupancy > 78
    priority = max(
        0, (score - 8) * (1 + frost_mm / 22) - max(0, score - idle_window) * 2
    )
    units = max(1, min(5, ceil(score / 18)))
    status = "candidate"
    reason = "RULE_ELIGIBLE"
    details = ()
    if blocked and all(
        record.reported.get(k) is not None for k in ("occupancy", "idle_window")
    ):
        status, reason, details = "held", "BUSINESS_LOCK", ("销售窗口或存货保护期",)
    elif not gate.allowed:
        status, reason, details = "manual", "TRUST_REVIEW", gate.reasons
    elif priority <= 0:
        status, reason, details = "monitor", "BELOW_ACTION", ("预计收益未达到处置阈值",)
    if status == "candidate" and units * 15 > idle_window:
        status, reason, details = (
            "held",
            "WINDOW_TOO_SHORT",
            ("完整作业时长超过许可窗口",),
        )
    if status == "candidate" and record.clock + units > 96:
        status, reason, details = "held", "CROSS_SHIFT", ("作业跨过本班日边界",)
    return Request(
        record.case_id,
        record.group,
        record.day if calendar_day is None else calendar_day,
        record.clock,
        record.group,
        units,
        round(score, 7),
        card.lower if gate.allowed else None,
        card.upper if gate.allowed else None,
        round(priority, 7),
        gate.source,
        status,
        reason,
        details,
        ACTION_LABEL,
    )


def resource_limit(day_budget: int) -> int:
    return max(1, day_budget // 2)
