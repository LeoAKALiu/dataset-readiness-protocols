# Third-reviewer role adapter

角色：`THIRD_REVIEWER`

评价单元：`{{EVALUATION_UNIT_JSON}}`

字段契约与标准化规则：`{{FIELD_AND_NORMALIZATION_CONTRACT_JSON}}`

去除模型身份后的冲突包：`{{ANONYMIZED_CONFLICT_PACKETS_JSON}}`

字段权威性规则：`{{FIELD_AUTHORITY_RULE_JSON}}`

任务：

1. 逐一核对双方来源、定位、内容哈希、原始值和规范化值。
2. 按证据质量和字段权威性裁决，不按模型数量、品牌或自报置信度进行多数表决。
3. 必要时只访问冲突包列出的冻结来源或协议允许的补充来源。
4. 对每个证据包输出采用、拒绝或无法裁决的简短可观察理由。
5. 终态只能为 `ACCEPTED`、`REJECTED` 或
   `UNRESOLVED_AFTER_REVIEW`。
6. 不输出 DRRL/ERL 等级或新权重。

只输出符合 `{{ROLE_OUTPUT_SCHEMA_ID}}` 的 JSON。
