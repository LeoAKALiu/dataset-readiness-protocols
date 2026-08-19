# Dataset Readiness Protocols

Public working archive for two complementary dataset assessment protocols:

- **DRRL — Dataset Reuse Readiness Level:** whether an independent third party can acquire, understand, verify, and integrate a specified dataset release with controlled avoidable friction.
- **ERL — Engineering Readiness Level:** the prospective engineering-domain transfer potential of a source dataset within a predefined application envelope, assessed before target engineering cases are used.

DRRL and ERL are independent axes. DRRL does not predict zero-shot engineering performance, and ERL does not measure licensing, download, documentation, or third-party integration effort.

## Repository structure

```text
DRRL/
├── DRRL_EVALUATION_PROTOCOL.md
└── reuse_verification_dictionaries/
    ├── CLUSTER_A_2D_DEFECT_REUSE_VERIFICATION_DICTIONARY.md
    ├── CLUSTER_B_RGBT_REUSE_VERIFICATION_DICTIONARY.md
    ├── CLUSTER_C_3D_POINT_CLOUD_REUSE_VERIFICATION_DICTIONARY.md
    └── CLUSTER_D_URBAN_ASSET_REUSE_VERIFICATION_DICTIONARY.md

ERL/
├── README.md
├── ERL_EVALUATION_PROTOCOL.md
├── TARGET_ENGINEERING_CASE_ANNOTATION_REQUIREMENTS.md
└── calculation_dictionaries/
    ├── CLUSTER_A_2D_DEFECT_CALCULATION_DICTIONARY.md
    ├── CLUSTER_B_RGBT_CALCULATION_DICTIONARY.md
    ├── CLUSTER_C_3D_POINT_CLOUD_CALCULATION_DICTIONARY.md
    └── CLUSTER_D_URBAN_ASSET_CALCULATION_DICTIONARY.md

evidence_maps/
└── 2026-08-19-deepresearch-merge/
    ├── MERGE_REPORT.md
    ├── CANONICAL_FAMILY_REGISTRY.csv
    ├── ALIAS_VERSION_MAP.csv
    ├── CONFLICT_VERIFICATION.md
    └── build_registry.py
```

## Protocols

### DRRL

- [DRRL evaluation protocol](DRRL/DRRL_EVALUATION_PROTOCOL.md)
- [Cluster A: 2D infrastructure defect imagery](DRRL/reuse_verification_dictionaries/CLUSTER_A_2D_DEFECT_REUSE_VERIFICATION_DICTIONARY.md)
- [Cluster B: paired RGB–Thermal data](DRRL/reuse_verification_dictionaries/CLUSTER_B_RGBT_REUSE_VERIFICATION_DICTIONARY.md)
- [Cluster C: 3D urban and infrastructure point clouds](DRRL/reuse_verification_dictionaries/CLUSTER_C_3D_POINT_CLOUD_REUSE_VERIFICATION_DICTIONARY.md)
- [Cluster D: urban assets and urban-scene data](DRRL/reuse_verification_dictionaries/CLUSTER_D_URBAN_ASSET_REUSE_VERIFICATION_DICTIONARY.md)

### ERL

- [ERL archive guide](ERL/README.md)
- [ERL evaluation protocol](ERL/ERL_EVALUATION_PROTOCOL.md)
- [ERL target engineering case annotation requirements](ERL/TARGET_ENGINEERING_CASE_ANNOTATION_REQUIREMENTS.md)
- [Cluster A calculation dictionary](ERL/calculation_dictionaries/CLUSTER_A_2D_DEFECT_CALCULATION_DICTIONARY.md)
- [Cluster B calculation dictionary](ERL/calculation_dictionaries/CLUSTER_B_RGBT_CALCULATION_DICTIONARY.md)
- [Cluster C calculation dictionary](ERL/calculation_dictionaries/CLUSTER_C_3D_POINT_CLOUD_CALCULATION_DICTIONARY.md)
- [Cluster D calculation dictionary](ERL/calculation_dictionaries/CLUSTER_D_URBAN_ASSET_CALCULATION_DICTIONARY.md)

### Dataset evidence maps

- [2026-08-19 four-source DeepResearch merge](evidence_maps/2026-08-19-deepresearch-merge/MERGE_REPORT.md)
- [Canonical dataset-family registry](evidence_maps/2026-08-19-deepresearch-merge/CANONICAL_FAMILY_REGISTRY.csv)
- [Alias and version map](evidence_maps/2026-08-19-deepresearch-merge/ALIAS_VERSION_MAP.csv)
- [Conflict verification record](evidence_maps/2026-08-19-deepresearch-merge/CONFLICT_VERIFICATION.md)

## Cluster definitions

| Cluster | Scope |
|---|---|
| A | 2D infrastructure surface or structural defect imagery |
| B | Paired RGB–Thermal multimodal inspection data |
| C | 3D urban or infrastructure point clouds |
| D | Urban-scene and urban-asset recognition data |

## Current status

These documents define the current constructs, boundaries, cumulative level logic, evidence states, and Cluster-specific operational dictionaries. They are not a claim that absolute thresholds or predictive validity have already been established.

- ERL empirical thresholds remain to be calibrated on development datasets and tested on independent validation datasets.
- DRRL friction thresholds and independent reuse-validity criteria remain to be calibrated.
- No dataset should be described as formally re-rated solely because the protocol documents exist.

The Chinese Markdown documents are the normative working texts in this repository. The English content in this README is an orientation summary.

## Construct separation

| DRRL | ERL | Interpretation |
|---|---|---|
| High | High | Reusable by third parties and promising for the declared engineering application |
| High | Low | Easy to reuse but weakly suited to the declared engineering application |
| Low | High | Potentially valuable for engineering use but difficult to acquire, interpret, verify, or integrate |
| Low | Low | Neither reuse-ready nor promising for the declared engineering application |

## Contributing

Issues and pull requests should identify the affected protocol, criterion or dictionary check, the proposed change, and the supporting evidence. Changes to thresholds or level gates should distinguish development evidence from independent validation evidence.

## Citation

Until a formal archival release is published, cite the repository URL together with the exact commit hash used for an assessment.

## License

The protocol documentation in this repository is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE).

---

# 数据集就绪度评价协议

本仓库公开维护两套相互独立、可组合使用的数据集评价协议：

- **DRRL（数据集复用就绪等级）**：评价独立第三方能否在指定复用范围内，以受控的可避免摩擦完成数据集获取、理解、核验和接入。
- **ERL（面向工程域迁移的数据集工程成熟度等级）**：在不使用目标工程案例计算等级的前提下，评价源数据集在预定义工程应用范围内的迁移潜力。

DRRL 不预测 zero-shot 工程表现；ERL 不评价许可、下载、文档和第三方接入成本。当前协议中的待校准参数不能在缺乏开发集和独立验证集证据时被任意设定。
