# 模块与边界验证

所属领域 AI/ML，子方向 传统ML。

## 功能模块

| 序号 | 模块 | 职责 | 实现 | 测试 |
| --- | --- | --- | --- | --- |
| M1 | cabinet_telemetry | 单据接入与时点裁决 | `src/frostslot/cabinet_telemetry/service.py` | `tests/test_cabinet_telemetry.py` |
| M2 | coil_condition | 业务特征与时点档案 | `src/frostslot/coil_condition/service.py` | `tests/test_coil_condition.py` |
| M3 | recovery_neighbors | 训练、估计与基线 | `src/frostslot/recovery_neighbors/service.py` | `tests/test_recovery_neighbors.py` |
| M4 | fridge_replay | 时间回放与核验 | `src/frostslot/fridge_replay/service.py` | `tests/test_fridge_replay.py` |
| M5 | store_regimes | 群组偏移与可信分派 | `src/frostslot/store_regimes/service.py` | `tests/test_store_regimes.py` |
| M6 | trade_windows | 业务锁与资源分派 | `src/frostslot/trade_windows/service.py` | `tests/test_trade_windows.py` |
| M7 | defrost_ticket | 逐单证据与资源守恒 | `src/frostslot/defrost_ticket/service.py` | `tests/test_defrost_ticket.py` |
| M8 | service_plan | 版本登记与追溯 | `src/frostslot/service_plan/service.py` | `tests/test_service_plan.py` |

## 易错边界

| 用例 | 业务后果 | 处理位置 | 验证位置 |
| --- | --- | --- | --- |
| TRAP-14 | 同版本异值隔离，较旧修订不能复活 | `src/frostslot/cabinet_telemetry/service.py` | `tests/test_cabinet_telemetry.py::test_conflicting_revision_is_quarantined` |
| TRAP-19 | 业务锁优先，未获准的单据不消耗资源 | `src/frostslot/trade_windows/service.py` | `tests/test_trade_windows.py::test_prohibited_entries_never_spend` |
| TRAP-26 | 使用过期版本登记被拒，保留前次结果 | `src/frostslot/service_plan/service.py` | `tests/test_service_plan.py::test_stale_generation_keeps_prior` |
| TRAP-32 | 零方差业务特征仍有有界尺度 | `src/frostslot/coil_condition/service.py` | `tests/test_coil_condition.py::test_zero_variance_uses_unit_scale` |
| TRAP-42 | 训练冻结后到达的单据或回执不会回填 | `src/frostslot/coil_condition/service.py` | `tests/test_coil_condition.py::test_future_and_late_measurements_do_not_fit` |
| TRAP-43 | 训练与独立回放的单据按时段隔离 | `src/frostslot/fridge_replay/service.py` | `tests/test_fridge_replay.py::test_holdout_separates_ordered_periods` |
| TRAP-44 | 稀疏或常量参考出现越界值时拦住自动分派 | `src/frostslot/store_regimes/service.py` | `tests/test_store_regimes.py::test_constant_distribution_detects_outside` |
| TRAP-53 | 同批重排仍得到相同证据和决策 | `src/frostslot/defrost_ticket/service.py` | `tests/test_defrost_ticket.py::test_report_is_permutation_invariant` |
| TRAP-54 | 单笔推理与合并调用的结果一致 | `src/frostslot/recovery_neighbors/service.py` | `tests/test_recovery_neighbors.py::test_score_is_batch_invariant` |
