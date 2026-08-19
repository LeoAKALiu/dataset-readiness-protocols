# Cluster A 计算字典：二维基础设施表面/结构病害影像

## 1. 适用范围

本字典适用于二维 RGB 基础设施表面或结构病害的分类、检测与分割。每次评价仍
须冻结具体应用范围；分类、检测和分割不得默认共用等级。

当前优先操作化任务为多标签语义分割，候选共同语义包括：

- `crack`；
- `spalling`；
- `corrosion_related_damage`。

如果任务包含裂缝宽度、病害面积或物理尺寸测量，物理尺度成为必要性判据；仅做
语义识别时，物理尺度作为覆盖与风险指标。

## 2. 分析单位

| 单位 | 定义 |
|---|---|
| 原始样本 | 一张未经裁块增强的原始影像及其标签 |
| 标签对象 | 连通病害区域、检测框或图级标签，按任务确定 |
| 独立采集单元 ICU-A | `结构物/地点 × 检测批次 × 成像设备`；无法恢复全部字段时使用可证明的最小独立组合 |
| 重复组 | 由精确哈希或冻结的近重复图算法形成的连通分量 |
| 环境层 | 材料、结构类型、室内外、照明、湿润、距离、视角、设备等预定义层级 |

同一视频、连拍序列、同一结构物的相邻裁块和同一原图派生块不得作为独立 ICU。

## 3. 必需输入

1. 原始影像清单及哈希；
2. 标签文件及其与影像的映射；
3. 官方或重建后的训练/验证划分；
4. 类别定义与应用范围映射表；
5. 可获得的地点、结构物、设备、时间、材料和环境元数据；
6. 全部派生、裁块、方向修正和标签转换记录；
7. 标注质量审计样本及裁决结果。

任一关键输入缺失时，相应指标记为 `UNKNOWN`，不得自动记零。

本字典沿用总体协议的全部通用判据。C1.4 由数据清单、版本标识和内容哈希直接
裁决，不另造数值指标；C1.3 与 C4.4 按任务是否要求物理尺度决定适用性。

## 4. 通用计算规则

### 4.1 抽样

标注质量审计采用分层抽样，至少按以下可用层分配：

- 类别；
- ICU-A；
- 目标尺度；
- 正样本/负样本；
- 主要环境条件。

报告抽样框、抽样概率、实际样本数和未审计层。误差率同时报告点估计和二项比例
区间；等级门槛优先使用不利方向的区间端点，而不是仅使用点估计。

### 4.2 精确重复

- 对规范化解码后的像素计算内容哈希；
- 同时保留原始文件哈希以区分重新编码；
- 标签不同但影像相同的情况单独标记为 `same_image_conflicting_label`；
- 由同一原图裁出的块不以哈希不相同为由视为独立。

### 4.3 近重复

采用两阶段检测：

1. 感知哈希或局部特征召回候选对；
2. 冻结的视觉表征距离和几何重叠规则确认。

算法、模型、输入分辨率、距离、阈值和图连通规则必须在评级前冻结。近重复结果
以连通分量作为重复组，不以样本对数量作为主要分母。

## 5. 指标定义

### A-S1 目标语义覆盖率

**目的**：判断数据标签能否覆盖应用范围中的必需语义。

\[
TCR_A=\frac{|\mathcal{C}_{required}\cap\mathcal{C}_{mappable}|}{|\mathcal{C}_{required}|}
\]

- 分子：存在无致命歧义映射的必需类别数；
- 分母：应用范围中预先声明的必需类别数；
- 输出：比例、未覆盖类别清单、映射类型（精确/合并/拆分/近似）；
- 判据：C1.1；
- 注意：不同类别的工程重要性不通过加权补偿，任何必需类别缺失可成为硬阻塞。

### A-S2 语义映射歧义率

\[
AMR_A=\frac{N_{ambiguous\ labelled\ objects}}{N_{audited\ labelled\ objects}}
\]

歧义包括一个源标签无法唯一映射、同名标签含义跨 ICU 改变、合并后无法区分必需
工程语义。输出比例、区间和逐类结果。判据：C1.1、C2.2。

### A-I1 数据—标签配对完整率

\[
PIR_A=\frac{N_{valid\ image-label\ pairs}}{N_{expected\ images}}
\]

有效配对要求文件可解码、尺寸匹配、标签值域合法且影像身份一致。空标签若按任务
合法应保留，不得作为缺失。输出缺失、孤立、错位和损坏文件数量。判据：C1.2。

### A-I2 致命结构错误率

\[
FER_A=\frac{N_{samples\ with\ fatal\ structural\ error}}{N_{audited\ samples}}
\]

致命错误包括影像—标签错配、标签方向错误、尺寸系统性错位、错误类别编码以及不可
恢复的派生变换。输出总体和错误类型分层结果。判据：C1.2。

### A-A1 严重标注缺陷图像率

\[
CAER_A=\frac{N_{audited\ images\ with\ at\ least\ one\ critical\ annotation\ defect}}{N_{audited\ images}}
\]

严重缺陷包括必需类别错标、明显漏掉主要病害、将非病害大面积标为病害、标签与
影像不对应。输出点估计、区间、逐类和逐 ICU 结果。判据：C2.1。

### A-A2 病害对象漏标率

需要独立金标准或重复标注：

\[
OMR_A=\frac{N_{gold\ objects\ absent\ from\ released\ annotation}}{N_{gold\ objects}}
\]

对象连接规则、最小可审计尺寸和争议区处理必须预先声明。输出逐类结果。无法建立
金标准时记为 `UNKNOWN`，可由其他等价证据路径替代。判据：C2.1。

### A-A3 边界不一致度

对分割任务，在审核对象上计算：

\[
BD_A=1-\operatorname{IoU}(M_{release},M_{adjudicated})
\]

同时报告边界 F-score 或表面距离，以避免小目标 IoU 的尺度效应。先按对象计算再
宏平均，不以所有像素池化替代。检测任务使用框 IoU；分类任务记为 `NA`。
判据：C2.1。

### A-A4 逻辑/物理矛盾标签率

\[
LCR_A=\frac{N_{audited\ labels\ violating\ frozen\ rules}}{N_{audited\ labels}}
\]

规则示例：类别互斥冲突、掩膜超出影像、明显非结构表面被标为结构病害、物理尺寸
超出应用范围且未标记。规则必须在获得计算结果前冻结。判据：C2.2。

### A-U1 ICU 可恢复率

\[
IRR_A=\frac{N_{samples\ assigned\ to\ a\ defensible\ ICU-A}}{N_{samples}}
\]

记录 ICU 来源字段和推断规则。只能由文件名猜测且无法核验的分组不计为可恢复。
判据：C2.3。

### A-D1 精确重复样本率

\[
EDR_A=\frac{N_{samples\ in\ exact\ duplicate\ groups\ of\ size>1}}{N_{samples}}
\]

同时输出重复组数、最大组大小、同标签重复和冲突标签重复。判据：C2.4b。

### A-D2 近重复样本率

\[
NDR_A=\frac{N_{samples\ in\ confirmed\ near\ duplicate\ groups\ of\ size>1}}{N_{samples}}
\]

精确重复包含在单独结果中，解释时不与近重复再次相加。输出按 ICU 内/跨 ICU
分解。判据：C2.4b。

### A-D3 跨划分泄漏数

\[
Leak_A=N_{duplicate\ groups\ spanning\ train\ and\ validation/test}
\]

分别报告精确泄漏、近重复泄漏和同一采集序列泄漏。确认的精确泄漏属于关键失败；
近重复与同序列泄漏的门槛待校准。判据：C2.4a、C2.4b。

### A-E1 重复折算有效样本数

将冻结近重复图的每个连通分量视为一个信息组：

\[
N_{eff,dup}^{A}=G_{duplicate\ components}
\]

\[
ER_{dup}^{A}=\frac{N_{eff,dup}^{A}}{N_{samples}}
\]

这是操作性代理，不是统计学无偏有效样本量。必须同时报告原始样本数、组数和组
大小分布。判据：C2.5；当前角色：诊断候选。

### A-U2 有效 ICU 数

以各 ICU 的重复折算有效样本占比 \(p_u\) 计算逆集中度：

\[
N_{eff,ICU}^{A}=\frac{1}{\sum_u p_u^2}
\]

同时报告原始 ICU 数。该指标区分“很多 ICU 但几乎全部样本来自一个 ICU”的情况。
判据：C3.2。

### A-U3 最大 ICU 支配率

\[
Dom_A=\max_u p_u
\]

输出最大 ICU 身份、占比及其类别组成。判据：C3.3。

### A-C1 单轴覆盖率

对应用范围预先指定的离散层或连续分箱：

\[
Coverage_{A,k}=\frac{N_{required\ levels\ observed\ with\ minimum\ evidence}}{N_{required\ levels}}
\]

逐轴报告材料、结构类型、照明、湿润、距离、视角、设备等覆盖；不得仅报告宏平均
而掩盖关键轴缺失。判据：C3.1。

### A-C2 关键组合空洞率

\[
Hole_A=\frac{N_{required\ condition\ cells\ without\ minimum\ effective\ evidence}}{N_{required\ condition\ cells}}
\]

组合矩阵只包含工程上预先指定的关键交互，不盲目展开全部笛卡尔积。输出空洞单元
清单。判据：C3.5。

### A-T1 类别最小有效覆盖

\[
TailMin_A=\min_{c\in\mathcal{C}_{required}}N_{eff,dup}^{A}(c)
\]

同时报告每类覆盖的 ICU 数和每 ICU 有效对象数。图像级多标签任务按含该类的有效
样本组计数；检测/分割同时报告对象数。判据：C3.4。

### A-T2 目标尺度覆盖

对分割/检测对象计算面积占比或等效直径分布，报告：

- 第 5/25/50/75/95 分位数；
- 应用范围要求的尺度分箱覆盖率；
- 每个尺度层的有效对象数和 ICU 数。

有物理标尺时同时报告毫米/厘米尺度；无标尺时只能声明像素尺度覆盖。判据：C3.4、
C4.4。

### A-SH1 元数据—标签关联强度

对类别存在性与地点、设备、日期、材料等变量计算 Cramér's V、归一化互信息或
适合变量类型的关联量。输出逐变量、逐类别值以及置换区间。不得将高关联自动解释
为伪相关；它只是风险信号。判据：C4.1；当前角色：诊断候选。

### A-SH2 背景捷径探针

冻结前景掩蔽规则，仅使用背景训练简单探针。报告背景探针宏指标
\(P_{bg}\)、完整影像探针指标 \(P_{full}\) 及：

\[
ShortcutRatio_A=\frac{P_{bg}}{P_{full}+\epsilon}
\]

探针架构、训练预算、划分和种子预先冻结；目标数据不得参与。判据：C4.1、C4.5。

### A-SH3 低级视觉捷径探针

仅使用颜色直方图、频域、纹理或压缩统计量预测标签，报告宏指标及相对完整输入
探针的比率。不同低级特征族分开输出，不合成为总分。判据：C4.1、C4.5。

### A-R1 留一 ICU 保持率

对每个可评 ICU 进行源内留一测试：

\[
Retention_{A,u}=\frac{P_{heldout\ ICU=u}}{P_{source\ random\ reference}+\epsilon}
\]

输出最小值、中位数、IQR 和逐 ICU 结果。不得把 ICU 当作模型随机种子。探针集合
必须冻结。判据：C4.2。

### A-R2 最差已见子群差距

\[
WorstGap_A=P_{macro}-\min_g P_g
\]

子群仅来自预先声明的材料、光照、湿润、尺度、设备等。报告子群样本与 ICU 数；
样本不足的子群记为不可估计。判据：C4.3。

### A-P1 物理尺度完备率

仅当应用范围要求物理尺寸时作为必要条件：

\[
PSC_A=\frac{N_{samples\ with\ traceable\ physical\ scale}}{N_{applicable\ samples}}
\]

可追溯尺度来自标定、测距、已知参照或可靠成像几何；仅凭经验猜测不计入。输出
尺度来源类型和误差。判据：C1.3、C4.4。

## 6. 待校准阈值登记

| 符号 | 对应指标 | 方向 | 当前角色 |
|---|---|---|---|
| \(\tau_A^{map}\) | A-S1/A-S2 | 覆盖高、歧义低 | ERL-1 规则待细化 |
| \(\tau_A^{ann}\) | A-A1/A-A2/A-A3 | 低 | V |
| \(\tau_A^{logic}\) | A-A4 | 低 | V |
| \(\tau_A^{dup}\) | A-D1/A-D2 | 低 | V |
| \(\tau_A^{eff}\) | A-E1 | 高 | V |
| \(\tau_A^{unit}\) | A-U2 | 高 | V |
| \(\tau_A^{dominance}\) | A-U3 | 低 | V |
| \(\tau_A^{axis}\) | A-C1 | 高 | V |
| \(\tau_A^{hole}\) | A-C2 | 低 | V |
| \(\tau_A^{tail}\) | A-T1/A-T2 | 高 | V |
| \(\tau_A^{shortcut}\) | A-SH1/A-SH2/A-SH3 | 低 | V |
| \(\tau_A^{retention}\) | A-R1 | 高 | V |
| \(\tau_A^{worst}\) | A-R2 | 低 | V |
| \(\tau_A^{scale}\) | A-P1 | 高 | 条件 V/H |

## 7. 最低输出表结构

每个指标至少输出：

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
evidence_quality
source_artifact
calculation_config_hash
criterion_state
threshold_id
notes
```

## 8. 禁止做法

- 用原始图像数量直接提高等级；
- 把裁块数量当作独立样本量；
- 用全体像素数制造标注质量的虚假精度；
- 用候选池分位数确定切点；
- 将背景与标签关联直接断言为因果捷径；
- 使用目标工程案例选择近重复阈值或探针；
- 将受控降质变体作为新的独立数据集样本。
