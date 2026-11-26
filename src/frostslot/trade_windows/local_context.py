from statistics import median


def _exposure(evidence):
    if None in (evidence["occupancy"], evidence["pallet"], evidence["door_minutes"]):
        return None
    holding = evidence["pallet"] / 100
    return evidence["occupancy"] * (1 + holding) * (1 + evidence["door_minutes"] / 42)


def context(current, neighbors, old, score):
    fridge = current.record.reported
    exposure = _exposure(fridge)
    opening = [
        _exposure(row.record.reported)
        for row in old
        if row.record.clock // 12 == current.record.clock // 12
    ]
    opening = [value for value in opening if value is not None]
    store_ref = median(opening) if len(opening) >= 6 else None
    implied = score + 6 + max(0, (fridge["pallet"] or 0) - 55) * 0.19
    free = fridge["idle_window"]
    shortage = (
        free is not None
        and free < implied
        and exposure is not None
        and store_ref is not None
        and exposure > store_ref * 1.16
    )
    return {
        "decision": "销售负荷偏高，需先转运存货" if shortage else "",
        "support": len(opening),
        "planned_recovery_min": round(implied, 3),
        "trade_exposure": exposure,
        "prior_comparable_window": store_ref,
        "neighbor_cabinets": len(neighbors),
    }
