# Cluster B 计算字典：RGB–Thermal 配对多模态巡检

## 1. 适用范围

本字典适用于成对 RGB 与 Thermal 数据共同支持的工程缺陷、异常或目标分类、检测
与分割。每次评级必须声明具体目标语义和任务。

以下情况超出当前 Cluster B 范围：

- 只有 Thermal、没有对应 RGB；
- RGB 与 Thermal 不是同一资产/场景的可配对观测；
- 两种模态无法建立同一任务标签；
- 数据用于热环境统计但不用于配对工程识别。

超出范围时输出 `UNRATED_OUT_OF_SCOPE`，不得因缺少配对模态而判定为低 ERL。

## 2. 分析单位

| 单位 | 定义 |
|---|---|
| 配对样本 | 同一资产/场景在满足同步容差内的一组 RGB 与 Thermal 观测及标签 |
| 标签对象 | 缺陷、异常、资产或像素区域，按任务确定 |
| 独立采集单元 ICU-B | `资产/建筑/地点 × 采集时段 × 配对传感器系统` |
| 配对序列组 | 同一资产、同一设备在连续时间或连续视角下的观测序列 |
| 传感器系统 | 固定的 RGB 相机、热像仪、镜头、安装关系和采集配置组合 |

同一房屋、结构物或资产的多帧、多视角不能仅因文件不同而视为独立 ICU。

## 3. 必需输入

1. RGB 与 Thermal 原始文件及哈希；
2. 显式配对清单或可核验的配对键；
3. 标签及标签参考模态；
4. 时间戳、帧号或同步记录；
5. 内外参、配准矩阵或可复核配准结果；
6. 热数据类型说明（辐射温度、原始计数、伪彩色或归一化图）；
7. 传感器、资产/地点、时间与环境元数据；
8. 训练/验证分组和全部派生转换；
9. 标注质量与跨模态对齐审计结果。

本字典沿用总体协议的全部通用判据。C1.4 由数据清单、版本标识和内容哈希直接
裁决，不另造数值指标；热辐射测量、纯语义识别等不同任务下的条件判据须先按
应用范围标记为适用或 `NA`。

## 4. 通用计算规则

### 4.1 配对键

配对键应优先来自资产 ID、采集时间、帧号和传感器同步记录。仅按文件排序或相似
文件名猜测配对时，不得判为已确认配对。

### 4.2 坐标基准

所有空间误差必须声明参考坐标：RGB 像素、Thermal 像素或统一投影平面。若经过
裁剪、缩放或畸变校正，必须记录变换链和插值方法。

### 4.3 标签参考模态

必须声明标签是在 RGB、Thermal 还是融合图上制作。由一个模态直接复制到另一个
模态时，应审计错位，不得假定像素标签当然一致。

### 4.4 热数据

伪彩色 PNG/JPEG 不等于辐射温度数据。若应用范围包含温度测量，必须使用可追溯
辐射数据、发射率设置和环境补偿信息；若只做语义识别，热标定可以是风险指标而
非 ERL-1 必要性判据。

## 5. 指标定义

### B-S1 目标语义覆盖率

\[
TCR_B=\frac{|\mathcal{C}_{required}\cap\mathcal{C}_{mappable}|}{|\mathcal{C}_{required}|}
\]

输出逐类映射、合并/拆分关系和未覆盖语义。不同数据集的“异常”“渗漏”“立面
缺陷”等不得因均有前景掩膜而自动视为同一语义。判据：C1.1。

### B-P1 配对身份完备率

\[
PIC_B=\frac{N_{pairs\ with\ verified\ shared\ identity}}{N_{released\ pair\ records}}
\]

已确认身份要求同一资产/场景、合理时间关系及可核验配对键。输出未匹配、单模态、
重复匹配和一对多记录。判据：C1.2、C1.3。

### B-P2 配对身份冲突率

\[
PMR_B=\frac{N_{audited\ pairs\ judged\ mismatched}}{N_{audited\ pairs}}
\]

通过人工或几何证据确认的错配计入分子。审计应按 ICU、时间和传感器分层。判据：
C1.2。

### B-I1 双模态可读完整率

\[
MCR_B=\frac{N_{pairs\ with\ readable\ RGB,T,label}}{N_{expected\ pairs}}
\]

同时报告 RGB 缺失、Thermal 缺失、标签缺失、尺寸异常和文件损坏。合法空标签不算
缺失。判据：C1.2。

### B-R1 归一化配准误差

对审计对应点或几何边缘：

\[
NRE_B=\operatorname{median}_i\frac{\|x_i^{RGB}-T(x_i^{T})\|_2}{\sqrt{W_{RGB}^2+H_{RGB}^2}}
\]

同时报告像素误差的 P50/P90/P95、不同图像区域和不同 ICU 的误差。若有目标掩膜，
补充跨模态投影 IoU。仅报告一张示例图不能构成 Q3。判据：C1.3、C4.4。

### B-R2 配准失效样本率

\[
RFR_B=\frac{N_{audited\ pairs\ exceeding\ frozen\ registration\ tolerance}}{N_{audited\ pairs}}
\]

容差必须与目标尺寸和工程用途关联。小缺陷任务不应直接沿用大目标检测容差。
判据：C4.4。

### B-T1 同步时间差

\[
Jitter_{B,i}=|t_i^{RGB}-t_i^{T}|
\]

报告 P50/P90/P95/最大值和超过容差的比例。没有原始时间戳或同步记录时记为
`UNKNOWN`，不能用文件修改时间代替。静态固定场景可声明同步不敏感，但必须在
应用范围中预先说明。判据：C1.3、C4.4。

### B-C1 热数据可追溯类型

分类输出：

- `radiometric_temperature`；
- `calibrated_sensor_counts`；
- `uncalibrated_sensor_counts`；
- `normalized_grayscale`；
- `pseudocolor_only`；
- `unknown`。

同时记录位深、单位、发射率、大气/反射温度补偿和动态范围。该项本身不形成连续
分数。判据：C1.3、C4.4。

### B-C2 辐射元数据完备率

仅当应用范围要求温度解释时计算：

\[
RMC_B=\frac{N_{applicable\ pairs\ with\ required\ radiometric\ metadata}}{N_{applicable\ pairs}}
\]

缺少发射率或环境补偿但任务不要求绝对温度时标记 `NA`，而不是失败。判据：
C1.3、C4.4。

### B-A1 跨模态严重标注缺陷率

\[
CMAE_B=\frac{N_{audited\ pairs\ with\ critical\ semantic\ or\ alignment\ defect}}{N_{audited\ pairs}}
\]

缺陷包括语义错标、主要目标漏标、标签参考模态不明、物理上不可能的模态关系以及
投影后明显错位。报告逐类、逐 ICU 和逐标签参考模态结果。判据：C2.1、C2.2。

### B-A2 模态边界不一致度

对可在两种模态中确定的审核对象，分别形成裁决掩膜：

\[
MBD_B=1-\operatorname{IoU}(T(M_T),M_{RGB})
\]

该指标结合了配准与观察差异，必须与 B-R1 分开解释。只在两模态都可见的对象上
使用；其他对象记 `NA`。判据：C2.1、C4.4。

### B-U1 ICU 可恢复率

\[
IRR_B=\frac{N_{pairs\ assigned\ to\ a\ defensible\ ICU-B}}{N_{pairs}}
\]

输出资产、时间、传感器字段的来源。仅靠连续文件编号不能证明资产独立。判据：
C2.3。

### B-D1 配对序列重复率

在 RGB 和 Thermal 联合确认近重复：

\[
PSDR_B=\frac{N_{pairs\ in\ repeated\ sequence/view\ groups}}{N_{pairs}}
\]

同一资产的连续帧和多视角组同时报告组大小、时间跨度和 ICU 内/跨 ICU 分解。
判据：C2.4b。

### B-D2 跨划分身份泄漏数

\[
Leak_B=N_{asset/sequence/duplicate\ groups\ spanning\ train\ and\ validation/test}
\]

资产身份、配对序列或精确重复跨划分均单独报告。确认的精确或同资产泄漏属于候选
关键阻塞。判据：C2.4a。

### B-E1 重复折算有效配对数

以联合 RGB-T 近重复图连通分量计数：

\[
N_{eff,pair}^{B}=G_{joint\ duplicate\ components},\qquad
ER_{pair}^{B}=\frac{N_{eff,pair}^{B}}{N_{pairs}}
\]

不得分别计算两种模态后取较大值。判据：C2.5。

### B-U2 有效 ICU 数与支配率

以 ICU 的有效配对占比 \(p_u\) 计算：

\[
N_{eff,ICU}^{B}=\frac{1}{\sum_u p_u^2},\qquad Dom_B=\max_u p_u
\]

输出原始 ICU 数、有效 ICU 数和最大 ICU 身份。判据：C3.2、C3.3。

### B-CV1 环境单轴覆盖率

逐轴计算环境温度、昼夜、季节、天气、材料、资产类型、拍摄距离和传感器系统的
覆盖：

\[
Coverage_{B,k}=\frac{N_{required\ levels\ with\ minimum\ effective\ pairs}}{N_{required\ levels}}
\]

连续温度分箱必须基于工程范围预定义，不能依据当前数据分位数事后划分。判据：
C3.1。

### B-CV2 环境—资产组合空洞率

\[
Hole_B=\frac{N_{required\ asset\times condition\ cells\ without\ evidence}}{N_{required\ cells}}
\]

只展开工程上必要的交互组合。输出空洞清单。判据：C3.5。

### B-TL1 类别最小有效配对覆盖

\[
TailMin_B=\min_{c\in\mathcal{C}_{required}}N_{eff,pair}^{B}(c)
\]

同时报告类别覆盖的 ICU 数、资产数和传感器系统数。判据：C3.4。

### B-SH1 元数据—标签关联强度

分别计算资产 ID、传感器系统、环境温度分箱、日期和地点与标签的关联量。连续变量
使用适当的非线性关联或分箱敏感性分析；分类变量报告 Cramér's V/NMI。高关联只是
风险信号。判据：C4.1。

### B-SH2 单模态支配画像

冻结相同训练协议，计算 RGB、Thermal 和融合探针表现：

\[
Dominance_B=\frac{\max(P_{RGB},P_T)}{P_{RGBT}+\epsilon}
\]

同时报告融合相对最佳单模态差值：

\[
FusionGain_B=P_{RGBT}-\max(P_{RGB},P_T)
\]

该指标描述模态利用，不等于跨域泛化；不得仅因融合收益小而降低 ERL。当前角色：
诊断；判据：C4.1、C4.5。

### B-SH3 传感器伪影捷径探针

仅使用固定模式噪声、边框、伪彩色映射、位深和设备特征预测标签。报告宏指标、
置换基线和跨 ICU 稳定性。若传感器与类别在采集设计上完全混淆，标记
`UNIDENTIFIABLE_WITHIN_SOURCE`。判据：C4.1。

### B-RB1 留一资产/地点/传感器保持率

分别按可用层执行：

\[
Retention_{B,u}=\frac{P_{heldout\ ICU=u}}{P_{source\ random\ reference}+\epsilon}
\]

至少输出留一资产、留一地点和留一传感器系统中可执行的层；不得将同一资产不同
帧分到训练和留一测试。报告最小值、中位数和 IQR。判据：C4.2。

### B-RB2 最差环境子群差距

\[
WorstGap_B=P_{macro}-\min_g P_g
\]

子群来自预注册的昼夜、温度、天气、资产类型、距离和传感器系统。样本或 ICU 数
不足时记为不可估计。判据：C4.3。

## 6. 待校准阈值登记

| 符号 | 指标 | 方向 | 当前角色 |
|---|---|---|---|
| \(\tau_B^{pair}\) | B-P1/B-P2 | 完备高、冲突低 | H/V |
| \(\tau_B^{reg}\) | B-R1/B-R2 | 低 | 条件 V/H |
| \(\tau_B^{sync}\) | B-T1 | 低 | 条件 V/H |
| \(\tau_B^{radiometric}\) | B-C1/B-C2 | 任务依赖 | 条件 V/H |
| \(\tau_B^{ann}\) | B-A1/B-A2 | 低 | V |
| \(\tau_B^{dup}\) | B-D1 | 低 | V |
| \(\tau_B^{eff}\) | B-E1 | 高 | V |
| \(\tau_B^{unit}\) | B-U2 | 高 | V |
| \(\tau_B^{dominance}\) | B-U2 | 低 | V |
| \(\tau_B^{axis}\) | B-CV1 | 高 | V |
| \(\tau_B^{hole}\) | B-CV2 | 低 | V |
| \(\tau_B^{tail}\) | B-TL1 | 高 | V |
| \(\tau_B^{shortcut}\) | B-SH1/B-SH3 | 低 | V |
| \(\tau_B^{retention}\) | B-RB1 | 高 | V |
| \(\tau_B^{worst}\) | B-RB2 | 低 | V |

## 7. 最低输出表结构

```text
dataset_id
dataset_version
application_envelope_id
metric_id
applicability
raw_value
unit
numerator
denominator
uncertainty_interval
pairing_key_source
reference_modality
evidence_quality
source_artifact
calculation_config_hash
criterion_state
threshold_id
notes
```

## 8. 禁止做法

- 将文件名相似直接视为已确认配对；
- 将伪彩色热图称为温度真值；
- 将空间配准和时间同步混成一个分数；
- 将同一资产多帧视为独立工程样本；
- 用目标案例调节配准容差或融合探针；
- 将融合收益当作 ERL 本身；
- 把语义不同的数据集通过“前景/背景”强行组成共同验证任务；
- 将纯热或非配对数据判为低 ERL，而不是范围外。
