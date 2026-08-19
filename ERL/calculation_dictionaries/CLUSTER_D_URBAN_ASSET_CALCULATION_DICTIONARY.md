# Cluster D 计算字典：城市场景与城市资产识别

## 1. 适用范围

Cluster D 面向二维城市场景与城市资产识别。至少拆分为两个独立应用范围：

- `D-Seg`：城市场景/城市资产语义或实例分割；
- `D-Det`：城市资产目标检测。

分类、分割和检测的标签单位、标注误差和性能终点不同，不得共用一个 ERL 等级：

\[
ERL(D\mid\Omega_{D-Seg})\neq ERL(D\mid\Omega_{D-Det})
\]

本字典不包含 RGB-T 多模态巡检；RGB-T 固定属于 Cluster B。

## 2. 分析单位

| 单位 | 定义 |
|---|---|
| 原始帧/影像 | 未经裁块增强的一张城市场景图像 |
| 资产实例 | 具有独立身份或可分离标注的城市资产对象 |
| 路线/序列组 | 同一采集路线、视频或连续街景序列 |
| 独立采集单元 ICU-D | `城市/区域 × 道路或建筑区段 × 采集批次 × 相机系统` |
| 重复组 | 精确重复、近重复、连续帧或同一资产多视角形成的组 |
| 环境层 | 城市、气候、道路类型、建筑风格、天气、昼夜、设备和视角等 |

同一路线连续帧、同一资产多视角和相邻街景不得作为独立 ICU。

## 3. 必需输入

1. 原始图像及哈希；
2. 分割掩膜、实例、检测框或图级标签；
3. 类别本体及应用范围映射；
4. 城市、地点、路线、时间、相机和平台元数据；
5. 视频、街景或多视角分组信息；
6. 官方或重建训练/验证划分；
7. 忽略区、遮挡、截断和拥挤密集区域（crowd）处理规则；
8. 全部裁块、缩放、重编码和标签转换记录；
9. 标注质量审计与裁决结果。

本字典沿用总体协议的全部通用判据。C1.4 由数据清单、版本标识和内容哈希直接
裁决，不另造数值指标。当前字典针对像素/图像级识别；若应用范围要求物理尺寸、
三维定位或测量，必须在评级前增设相机标定与物理尺度指标。常规 D-Seg/D-Det
不要求物理量时，C1.3 和 C4.4 中相应物理判据记为 `NA`，不得记为通过或失败。

## 4. 通用计算规则

### 4.1 任务隔离

- D-Seg 以像素/实例语义为标签输出，但标注质量统计优先以图像、对象或区域为
  单位；
- D-Det 以资产实例和检测框为标签单位；
- 不得将 D-Seg 的像素数和 D-Det 的框数合并；
- mIoU 与 mAP 不得混合构成预测效度终点。

### 4.2 城市与路线

“多个城市”必须由实际城市/区域身份支持；仅因图像外观不同不能推断跨城市。
路线、视频和相邻街景分组优先于随机图像划分。

### 4.3 小目标

目标尺度同时以像素面积占比、短边像素和可获得的物理距离描述。使用固定输入缩放
后再计算的尺度必须同时保留原始尺度，避免预处理掩盖源数据差异。

### 4.4 近重复

联合使用内容哈希、感知相似度、局部几何匹配和序列/位置元数据。算法及阈值在
评级前冻结，并以近重复图连通分量作为重复组。

## 5. 指标定义

### D-S1 目标语义覆盖率

\[
TCR_D=\frac{|\mathcal{C}_{required}\cap\mathcal{C}_{mappable}|}{|\mathcal{C}_{required}|}
\]

输出精确映射、合并、拆分、忽略类和范围外类。`traffic sign`、`road furniture`、
`urban asset` 等宽泛名称不得在没有操作定义时视为等价。判据：C1.1。

### D-S2 类别映射歧义率

\[
AMR_D=\frac{N_{audited\ objects/regions\ with\ ambiguous\ target\ mapping}}{N_{audited\ labelled\ objects/regions}}
\]

分别报告 D-Seg 和 D-Det。判据：C1.1、C2.2。

### D-I1 图像—标签配对完整率

\[
PIR_D=\frac{N_{valid\ image-label\ records}}{N_{expected\ images}}
\]

检查文件可读、尺寸匹配、标签值域、空标签合法性、框边界和图像身份。输出孤立
文件、损坏记录和错位数量。判据：C1.2。

### D-I2 致命结构错误率

\[
FER_D=\frac{N_{audited\ images\ with\ fatal\ structural\ error}}{N_{audited\ images}}
\]

包括标签整体错位、框坐标系错误、掩膜方向错误、图像—标签身份错配和不可恢复的
转换。判据：C1.2。

### D-A1 严重标注缺陷图像率

\[
CAER_D=\frac{N_{audited\ images\ with\ critical\ annotation\ defect}}{N_{audited\ images}}
\]

严重缺陷包括主要资产错标/漏标、大面积语义错误、框与对象无关、忽略区处理导致
系统性错误。输出逐类、逐城市、逐 ICU 和逐任务结果。判据：C2.1。

### D-A2 资产实例漏标率

需要独立裁决标注：

\[
OMR_D=\frac{N_{gold\ asset\ instances\ absent\ from\ released\ labels}}{N_{gold\ asset\ instances}}
\]

预先冻结最小可标注尺寸、crowd、遮挡和截断规则。D-Seg 若只有语义掩膜但无法
分离实例，可按连通区域或审核区域报告并注明代理性质。判据：C2.1。

### D-A3 检测框几何误差

仅适用于 D-Det。对匹配裁决框：

\[
BoxError_D=1-\operatorname{IoU}(B_{release},B_{adjudicated})
\]

报告对象宏平均、P50/P90、中心偏移和尺寸偏差。无法匹配的错标/漏标进入 D-A1、
D-A2，不以零 IoU 重复计算。判据：C2.1。

### D-A4 分割边界不一致度

仅适用于 D-Seg：

\[
BoundaryDisagreement_D=1-\operatorname{IoU}(M_{release},M_{adjudicated})
\]

同时报告边界 F-score 或物理/像素表面距离。先按对象或类别宏平均，不以全部像素
池化替代。判据：C2.1。

### D-A5 遮挡/截断状态完整率

若应用范围需要区分遮挡或截断：

\[
OTC_D=\frac{N_{applicable\ instances\ with\ valid\ occlusion/truncation\ state}}{N_{applicable\ instances}}
\]

任务不要求时标记 `NA`。判据：C2.1、C3.4。

### D-U1 ICU 可恢复率

\[
IRR_D=\frac{N_{images\ assigned\ to\ a\ defensible\ ICU-D}}{N_{images}}
\]

分别记录城市、区段、批次和相机字段来源。GPS 缺失并不当然导致失败，但无法恢复路线
或地点会限制独立性和覆盖判定。判据：C2.3。

### D-D1 精确重复样本率

\[
EDR_D=\frac{N_{images\ in\ exact\ duplicate\ groups\ of\ size>1}}{N_{images}}
\]

同时报告重新编码重复、标签冲突重复和跨数据版本重复。判据：C2.4b。

### D-D2 序列/近重复样本率

\[
NDR_D=\frac{N_{images\ in\ confirmed\ sequence/near-duplicate\ groups}}{N_{images}}
\]

输出连续视频、相邻街景、同资产多视角和普通视觉近重复的分解。判据：C2.4b。

### D-D3 跨划分城市/路线/身份泄漏数

\[
Leak_D=N_{duplicate,sequence,route,asset\ groups\ spanning\ train\ and\ validation/test}
\]

分别报告相同图像、同序列、同路线和同资产泄漏。确认精确重复和同序列泄漏属于
关键失败候选。判据：C2.4a。

### D-E1 重复折算有效影像数

\[
N_{eff,image}^{D}=G_{duplicate/sequence\ components},\qquad
ER_{image}^{D}=\frac{N_{eff,image}^{D}}{N_{images}}
\]

该指标是操作性代理，必须同时报告组大小和组类型。判据：C2.5。

### D-U2 有效 ICU 数与支配率

以各 ICU 的有效影像占比 \(p_u\) 计算：

\[
N_{eff,ICU}^{D}=\frac{1}{\sum_u p_u^2},\qquad Dom_D=\max_u p_u
\]

同时计算城市级、路线级和相机级集中度，不能只给一个总值。判据：C3.2、C3.3。

### D-CV1 工程变化轴覆盖率

逐轴计算城市/区域、道路类型、建筑风格、气候、天气、昼夜、相机系统和采集平台：

\[
Coverage_{D,k}=\frac{N_{required\ levels\ with\ minimum\ effective\ evidence}}{N_{required\ levels}}
\]

连续变量使用应用范围预定义分箱，不采用当前数据分位数。判据：C3.1。

### D-CV2 关键组合空洞率

\[
Hole_D=\frac{N_{required\ condition\ cells\ without\ minimum\ effective\ evidence}}{N_{required\ cells}}
\]

候选组合包括城市×类别、相机×类别、天气×类别和道路类型×资产。只使用预注册
的工程必要组合。判据：C3.5。

### D-T1 类别最小有效实例/区域覆盖

D-Det：

\[
TailMin_{D-det}=\min_c N_{eff,instance}(c)
\]

D-Seg：同时报告包含该类的有效图像组、独立 ICU、连通区域数和像素/面积占比，
不只使用像素数。判据：C3.4。

### D-T2 小目标覆盖

按原始图像尺度计算每个实例的面积占比和短边像素，报告预注册尺度层的：

- 有效实例数；
- 有效图像组数；
- ICU 数；
- 遮挡/截断组成。

\[
SmallCoverage_D=\frac{N_{required\ small-object\ cells\ with\ minimum\ evidence}}{N_{required\ small-object\ cells}}
\]

判据：C3.4。

### D-T3 资产多视角集中度

若可识别资产身份，以每个资产的帧数占比 \(q_a\) 计算：

\[
AssetConcentration_D=\sum_a q_a^2
\]

同时报告原始实例数与独立资产数。无法识别资产身份时记为 `UNKNOWN`。判据：
C2.5、C3.3。

### D-SH1 城市/设备/背景—标签关联

计算城市、路线、相机、天气、建筑/道路背景与类别存在性的关联量，报告 Cramér's
V、NMI 或适合变量类型的指标及置换基线。高关联是风险信号，不自动构成失败。
判据：C4.1。

### D-SH2 背景捷径探针

对 D-Det 使用目标框外背景，对 D-Seg 使用目标区域掩蔽后的背景，冻结简单探针：

\[
ShortcutRatio_D=\frac{P_{background}}{P_{full}+\epsilon}
\]

报告逐类别、逐城市和跨相机结果。背景天然包含任务因果信息时，应在应用范围中说明，
不得机械解释。判据：C4.1、C4.5。

### D-SH3 低级图像/地理身份探针

仅使用颜色、压缩、分辨率、边框、水印、文件编码或位置身份预测标签。分别输出各
特征族结果，不合成为总分。若城市与类别完全混淆，标记
`UNIDENTIFIABLE_WITHIN_SOURCE`。判据：C4.1。

### D-RB1 留一城市/区域/路线保持率

\[
Retention_{D,u}=\frac{P_{heldout\ ICU/city=u}}{P_{source\ random\ reference}+\epsilon}
\]

优先留一城市；城市数不足时依次使用区域、路线或采集批次，但必须收窄证据外推
范围。输出最小值、中位数、IQR 和逐组结果。判据：C4.2。

### D-RB2 留一相机系统保持率

\[
SensorRetention_D=\min_s\frac{P_{heldout\ camera=s}}{P_{source\ random\ reference}+\epsilon}
\]

只有一个相机系统时不可估计，不得记为 1。判据：C4.2。

### D-RB3 最差已见子群差距

\[
WorstGap_D=P_{macro}-\min_g P_g
\]

子群来自预注册的城市、天气、昼夜、尺度、遮挡、相机和道路/建筑类型。报告每组
有效图像组、资产和 ICU 数。判据：C4.3。

## 6. 待校准阈值登记

| 符号 | 指标 | 方向 | 当前角色 |
|---|---|---|---|
| \(\tau_D^{map}\) | D-S1/D-S2 | 覆盖高、歧义低 | H/V |
| \(\tau_D^{integrity}\) | D-I1/D-I2 | 完整高、错误低 | H/V |
| \(\tau_D^{ann}\) | D-A1–D-A5 | 错误低、完备高 | V |
| \(\tau_D^{dup}\) | D-D1/D-D2 | 低 | V |
| \(\tau_D^{eff}\) | D-E1 | 高 | V |
| \(\tau_D^{unit}\) | D-U2 | 高 | V |
| \(\tau_D^{dominance}\) | D-U2/D-T3 | 低 | V |
| \(\tau_D^{axis}\) | D-CV1 | 高 | V |
| \(\tau_D^{hole}\) | D-CV2 | 低 | V |
| \(\tau_D^{tail}\) | D-T1 | 高 | V |
| \(\tau_D^{small}\) | D-T2 | 高 | V |
| \(\tau_D^{shortcut}\) | D-SH1–D-SH3 | 低 | V |
| \(\tau_D^{retention}\) | D-RB1/D-RB2 | 高 | V |
| \(\tau_D^{worst}\) | D-RB3 | 低 | V |

阈值必须分别为 D-Seg 与 D-Det 校准；不得直接复用。

## 7. 最低输出表结构

```text
dataset_id
dataset_version
application_envelope_id
task_subtype
metric_id
applicability
raw_value
unit
numerator
denominator
uncertainty_interval
grouping_level
evidence_quality
source_artifact
calculation_config_hash
criterion_state
threshold_id
notes
```

## 8. 禁止做法

- 将 D-Seg 与 D-Det 合并评级；
- 将像素、检测框或视频帧当作独立数据集样本；
- 随机拆分同一路线、连续序列或同一资产多视角；
- 用裁块或重采样数量提高有效样本量；
- 跨不同类别体系直接比较 in-domain mIoU 或 mAP；
- 将城市身份与类别关联直接解释为因果捷径；
- 使用目标工程案例选择类别映射、近重复阈值或探针；
- 将 Cityscapes 等单一数据集的受控降质版本当作独立数据集验证 ERL。
