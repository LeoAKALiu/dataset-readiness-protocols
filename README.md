# Dataset Readiness Protocols

Public working archive for two independent and composable dataset assessment protocols:

- **DRRL — Dataset Reuse Readiness Level:** whether an independent third party can reuse a specified dataset release with low barriers and verifiable outcomes within a declared reuse scope.
- **ERL — Engineering Readiness Level:** a pre-target-case assessment of a source dataset's zero-shot engineering-domain transfer potential within a predefined application envelope, based solely on observable source-dataset evidence.

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
├── MERGE_REPORT.md
├── CANONICAL_FAMILY_REGISTRY.csv
├── ALIAS_VERSION_MAP.csv
├── CONFLICT_VERIFICATION.md
└── build_registry.py

AGENT_EVALUATION/
├── AI_AGENT_EVALUATION_PROTOCOL.md
├── STAGE_0_RUNBOOK.md
├── PROMPT_AND_EVIDENCE_CONTRACT.md
├── AUDIT_AND_ANALYSIS_PLAN.md
├── PREREGISTRATION_AND_COMPLETION.md
├── schemas/
└── scripts/

EXPERIMENT_PROTOCOL/
└── INTEGRATED_STUDY_PROTOCOL.md
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

- [2026-08-19 four-source DeepResearch merge](evidence_maps/MERGE_REPORT.md)
- [Canonical dataset-family registry](evidence_maps/CANONICAL_FAMILY_REGISTRY.csv)
- [Alias and version map](evidence_maps/ALIAS_VERSION_MAP.csv)
- [Conflict verification record](evidence_maps/CONFLICT_VERIFICATION.md)

### Multi-agent evaluation experiment

- [Agent experiment archive guide](AGENT_EVALUATION/README.md)
- [Complete AI Agent evaluation protocol](AGENT_EVALUATION/AI_AGENT_EVALUATION_PROTOCOL.md)
- [Stage 0 runbook](AGENT_EVALUATION/STAGE_0_RUNBOOK.md)
- [Prompt and evidence contract](AGENT_EVALUATION/PROMPT_AND_EVIDENCE_CONTRACT.md)
- [Audit and analysis plan](AGENT_EVALUATION/AUDIT_AND_ANALYSIS_PLAN.md)
- [Preregistration and completion specification](AGENT_EVALUATION/PREREGISTRATION_AND_COMPLETION.md)

### Integrated study protocol

- [Integrated DRRL/ERL study protocol](EXPERIMENT_PROTOCOL/INTEGRATED_STUDY_PROTOCOL.md)

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
- The Agent experiment package is a pre-Stage-0 candidate. It is not the formal preregistration lock until the Stage 0 feasibility run is complete and a dated GitHub tag/release is published.

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

- **DRRL（数据集复用就绪等级）**：对于指定的数据集发布版本和复用范围，评价独立第三方能否低障碍、可核验地完成数据复用。
- **ERL（面向工程域迁移的数据集工程成熟度等级）**：在目标工程案例出现前，仅依据源数据集自身的可观察证据，评价其在预定义工程应用范围内的 zero-shot 工程域迁移潜力；目标工程案例仅用于后续预测效度验证，不参与等级计算。

DRRL 不预测 zero-shot 工程表现；ERL 不评价许可、下载、文档和第三方接入成本。当前协议中的待校准参数不能在缺乏开发集和独立验证集证据时被任意设定。
