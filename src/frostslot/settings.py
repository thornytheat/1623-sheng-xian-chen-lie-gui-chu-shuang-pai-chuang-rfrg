PROJECT_NAME = "生鲜陈列柜除霜排窗"
ROLE = "门店设备主管"
MODEL_LABEL = "近邻条件分位数"
TARGET = "continuous"
UNIT = "min"
ACTION_LABEL = "预约除霜与复温"
RESERVE_LABEL = "门店除霜工位"
DEFAULT_DAY = 144
DEFAULT_BUDGET = 14
REPORT_LAG = 1
GROUPS = ("商场负一层", "社区小站", "街边旗舰", "仓卖一体")
SIGNAL_NAMES = ("frost_load", "hygro_open", "power_margin", "stock_fill")
WATCH_FEATURE = "frost_load"
METRIC_LABEL = "平均绝对误差"
FIELD_LABELS = {
    "dew_point": "露点 ℃",
    "door_minutes": "开柜时长 min",
    "frost_mm": "霜层厚度 mm",
    "cabinet_kw": "额定功率 kW",
    "occupancy": "近一小时客流",
    "idle_window": "非销售窗口 min",
    "pallet": "冷藏存货占比 %",
}
FIELD_BOUNDS = {
    "dew_point": (3, 24),
    "door_minutes": (0, 54),
    "frost_mm": (0, 22),
    "cabinet_kw": (1, 9),
    "occupancy": (4, 95),
    "idle_window": (0, 115),
    "pallet": (10, 100),
}
CRITICAL_FIELDS = frozenset(("dew_point", "idle_window", "pallet"))
