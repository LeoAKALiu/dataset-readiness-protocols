# 预登记、变更控制与完成规范

## 1. 两次冻结

### 1.1 `stage0_candidate_lock`

阶段 0 开始前记录候选协议、代码、模型、工具和 8 家族样本。允许在阶段 0 中
修复装置，但所有变更必须留痕。

### 1.2 `protocol_lock`

阶段 0 通过后创建正式锁。至少包含：

- 家族、别名、版本和任务单元注册表哈希；
- DRRL/ERL 协议及八份 Cluster 字典哈希；
- Agent 主协议、提示词、schema 和状态机哈希；
- Pi Agent、adapter、工具和模型面板 manifest；
- 标准化器、指标程序和规则引擎哈希；
- 阶段 0、32 审计和 16 重复样本清单；
- sentinel 单元清单；
- 98 家族主有向对、32 家族偏移量和主流水线；
- 由注册表与别名/版本表内容自动派生、不可人工更换的选择种子；
- 检索轮次、停止、重试、软预警和安全暂停规则；
- 人工参考字段和描述字段抽样清单；
- 统计分析计划；
- 公开/私有持久化边界。

`protocol_lock` 使用规范化 JSON 生成总 SHA-256。任何子文件改变都会产生不同锁。
机器可读格式见
[`schemas/protocol-lock.schema.json`](schemas/protocol-lock.schema.json)，模型面板格式见
[`schemas/panel-manifest.schema.json`](schemas/panel-manifest.schema.json)。

## 2. GitHub 预登记

正式实验启动前，在公开仓库创建带日期的 Git tag 或 GitHub release。release 应
包含 `protocol_lock.json`、所有非敏感 manifest、选择清单和 commit。阶段 0 输出
标记 `EXCLUDED_FROM_FORMAL_ANALYSIS`。

当前 `AGENT_EVALUATION/` 文件只是候选执行包；在阶段 0 完成前不得创建暗示正式
锁已经生效的 tag。

## 3. 变更分类

| 类型 | 示例 | 正式运行处理 |
|---|---|---|
| 运行恢复 | 429、5xx、超时、进程中断 | 原 run/replicate 断点恢复，不改锁 |
| 非语义修复 | 不改变值的显示/导出修复 | 留日志并验证哈希语义等价 |
| 实质协议变更 | 字段、适用性、来源规则、阈值、提示义务变化 | 暂停，新锁，重跑全部受影响单元 |
| 模型/框架变化 | 模型替换、Pi/adapter/工具变化 | 新 `panel_id` 和 `run_id` |
| 数据发布变化 | 发布物、许可、入口、标注或版本变化 | 新发布节点或重新核验受影响节点 |

不得只对等级不理想的数据集应用修订。

## 4. 原子检查点

每个角色运行至少在下列边界原子写入：

1. 任务领取；
2. 每次工具调用完成；
3. 候选证据包通过 schema；
4. 盲核验独立抽取提交；
5. 比较器结果；
6. 第三复核终态；
7. 规则引擎输入冻结；
8. 等级输出及哈希。

恢复时先对账已提交的事件和内容哈希，禁止重复提交已完成证据或改变
`replicate_id`。运维日志单独写入，不得拼接进评分文件。

## 5. 组件完成门

| 组件 | 完成条件 |
|---|---|
| `DRRL_PRIMARY_COMPLETE` | 注册表内全部正式家族主流水线完成 |
| `ERL_ELIGIBILITY_COMPLETE` | 全部家族有可评/不可评及原因 |
| `ERL_PRIMARY_COMPLETE` | 全部可评任务单元的字典计算与规则输出完成 |
| `DRRL_AGENT_AUDIT_COMPLETE` | 32 家族 DRRL 五条双 Agent 流水线完成 |
| `ERL_AGENT_AUDIT_COMPLETE` | (N_{EA}) 个可评 ERL sentinel 的五条双 Agent 流水线完成 |
| `DRRL_REPEAT_AUDIT_COMPLETE` | 16 家族 DRRL 五条流水线第二次运行完成 |
| `ERL_REPEAT_AUDIT_COMPLETE` | (N_{ER}) 个可评 ERL sentinel 的五条流水线第二次运行完成 |
| `HUMAN_REFERENCE_COMPLETE` | 双人盲审、负责人裁决和参考锁完成 |
| `ANALYSIS_COMPLETE` | 统计输入、代码、环境和结果哈希一致 |

组件只有在所有必填字段为合法终态、没有 `RUN_INCOMPLETE`/待重试/待核验时才
完成。`UNRESOLVED_AFTER_REVIEW` 可作为证据终态，但必须进入完备度和弃答统计。

## 6. 总完成清单

机器可读格式见 [`schemas/completion-manifest.schema.json`](schemas/completion-manifest.schema.json)。
总清单至少记录：

- `protocol_lock_id`、`panel_id`、`run_id`；
- 每个组件预期、完成、合法终态和未完成数量；
- 输入、输出、代码和环境哈希；
- DRRL 和 ERL 各自的主/审计/重复/敏感性命名空间哈希；
- 未解决冲突数；
- `RUN_INCOMPLETE` 数；
- 总体状态与生成时间。

总体 `COMPLETE` 必须由程序根据组件门计算，不能由研究者手写覆盖。文件存在、
部分输出、HTTP 成功或单个模型完成均不等于整项实验完成。

JSON Schema 负责结构约束；跨字段计数、面板槽位排序和必需锁文件角色由
[`scripts/validate_manifests.py`](scripts/validate_manifests.py) 进行确定性复核。正式
发布必须同时通过 schema 和该语义校验器。

## 7. 公开复现包

公开包包含：

- 正式 release/tag 和 commit；
- 协议、字典、提示词、schema 与完整哈希；
- 注册表、选择清单、模型/角色分配；
- 脱敏可观察工具事件和结构化 Agent 输出；
- 来源 URL、定位、必要短摘录和响应哈希；
- 标准化、指标、规则与分析代码；
- 完成清单、变更日志和失败报告。

不公开 OAuth 凭据、账户身份、隐藏推理、受限完整缓存、私有数据和原始调试日志。
