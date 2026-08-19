# ERL 工程域迁移评价协议档案

本目录保存面向工程域迁移的数据集工程成熟度等级（Engineering Readiness
Level, ERL）新协议。它与本仓库既有 ERL、DRRL、可靠性评分实验和历史论文
材料相互独立，不继承旧协议的名称、权重、切点、等级或数据集评分。

## 当前状态

- 总体构念、评价边界、等级结构和开发/验证程序已经形成。
- Cluster A/B/C/D 的候选计算字典已经建立。
- 所有经验阈值仍以符号表示，尚未通过开发集校准。
- 在阈值、判据角色和独立验证方案冻结前，不得据此正式重评现有数据集。

## 文件

- [`ERL_EVALUATION_PROTOCOL.md`](ERL_EVALUATION_PROTOCOL.md)：完整评价协议。
- [`TARGET_ENGINEERING_CASE_ANNOTATION_REQUIREMENTS.md`](TARGET_ENGINEERING_CASE_ANNOTATION_REQUIREMENTS.md)：
  用于 ERL 阈值开发和独立预测效度验证的目标工程案例标注要求。
- [`calculation_dictionaries/CLUSTER_A_2D_DEFECT_CALCULATION_DICTIONARY.md`](calculation_dictionaries/CLUSTER_A_2D_DEFECT_CALCULATION_DICTIONARY.md)：
  二维基础设施病害影像。
- [`calculation_dictionaries/CLUSTER_B_RGBT_CALCULATION_DICTIONARY.md`](calculation_dictionaries/CLUSTER_B_RGBT_CALCULATION_DICTIONARY.md)：
  RGB–Thermal 配对多模态巡检。
- [`calculation_dictionaries/CLUSTER_C_3D_POINT_CLOUD_CALCULATION_DICTIONARY.md`](calculation_dictionaries/CLUSTER_C_3D_POINT_CLOUD_CALCULATION_DICTIONARY.md)：
  三维城市/基础设施点云。
- [`calculation_dictionaries/CLUSTER_D_URBAN_ASSET_CALCULATION_DICTIONARY.md`](calculation_dictionaries/CLUSTER_D_URBAN_ASSET_CALCULATION_DICTIONARY.md)：
  城市场景与城市资产识别。

## 固定 Cluster 口径

| Cluster | 含义 |
|---|---|
| A | 二维基础设施表面/结构病害影像 |
| B | RGB–Thermal 配对多模态巡检 |
| C | 三维城市/基础设施点云 |
| D | 城市场景与城市资产识别 |

历史文件中的 Cluster 字母仅按其原始语境解释，不用于推导本目录的新协议。
