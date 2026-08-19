# DRRL/ERL 多 Agent 评价实验

本目录保存使用统一 Agent 执行框架评价 DRRL 与 ERL 的候选实验协议。它规定
Agent 如何检索和核验证据、确定性程序如何计算指标和生成等级，
以及如何验证这套评价方法的准确性和重复性。

本目录不修改 DRRL 或 ERL 的构念和等级定义。规范性评价依据仍是：

- [`../DRRL/DRRL_EVALUATION_PROTOCOL.md`](../DRRL/DRRL_EVALUATION_PROTOCOL.md)
- [`../ERL/ERL_EVALUATION_PROTOCOL.md`](../ERL/ERL_EVALUATION_PROTOCOL.md)
- 两套协议各自的 Cluster A/B/C/D 字典

## 文档

- [`AI_AGENT_EVALUATION_PROTOCOL.md`](AI_AGENT_EVALUATION_PROTOCOL.md)：完整实验协议。
- [`STAGE_0_RUNBOOK.md`](STAGE_0_RUNBOOK.md)：8 家族阶段 0 试运行与执行框架可行性验证。
- [`PROMPT_AND_EVIDENCE_CONTRACT.md`](PROMPT_AND_EVIDENCE_CONTRACT.md)：角色提示词、盲核验和证据包契约。
- [`AUDIT_AND_ANALYSIS_PLAN.md`](AUDIT_AND_ANALYSIS_PLAN.md)：32 家族五模型审计、16 家族重复审计及统计计划。
- [`PREREGISTRATION_AND_COMPLETION.md`](PREREGISTRATION_AND_COMPLETION.md)：正式协议锁定、变更控制和完成判据。
- [`schemas/`](schemas/)：公开持久化文件的 JSON Schema。
- [`prompts/`](prompts/)：阶段 0 前的完整公共/角色提示词模板。
- [`scripts/select_audit_families.py`](scripts/select_audit_families.py)：确定性选择阶段 0、32 家族审计和 16 家族重复样本。

## 当前状态

当前文件是**阶段 0 前的候选实验规范**。阶段 0 可以校正歧义、schema、工具适配
和不可计算条目。正式实验只能在阶段 0 通过并生成公开 `protocol_lock` 后启动。
阶段 0 输出不进入正式评价结果或模型优劣比较。

## 确定性选择脚本

阶段 0 后建立正式协议锁定记录时执行：

```bash
python3 AGENT_EVALUATION/scripts/select_audit_families.py \
  --registry evidence_maps/2026-08-19-deepresearch-merge/CANONICAL_FAMILY_REGISTRY.csv \
  --alias-map evidence_maps/2026-08-19-deepresearch-merge/ALIAS_VERSION_MAP.csv \
  --output '<selection-manifest.json>'
```

抽样种子由注册表哈希、别名/版本表哈希和脚本内固定 domain 自动派生，不接受
研究者输入的随机种子或标签。相同输入文件和脚本版本必须产生完全相同的
8/32/16 清单与 98 家族主模型对分配。其中 32 家族正式审计集与 8 家族
阶段 0 试运行样本集严格不相交。

## 固定边界

1. Agent 只检索、抽取和核验证据，不直接决定最终 DRRL/ERL。
2. 可计算指标由预先固定的指标计算程序生成，等级由确定性判定程序生成。
3. DRRL 与 ERL 实行相互盲化，不继承对方的等级或判据状态。
4. 目标工程案例不参与 ERL 计算，只用于后续独立预测效度验证。
5. 服务故障、预算暂停和运行诊断记录不得改变数据集等级。
6. 正式结果、审计结果、敏感性分析结果和运行维护记录必须分别保存。
