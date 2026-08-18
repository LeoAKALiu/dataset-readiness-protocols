# Cluster C 计算字典：三维城市/基础设施点云

## 1. 适用范围

本字典适用于三维城市或基础设施点云的语义分割、目标识别、变化检测或工程测量。
不同任务必须分别冻结应用范围，不能用场景语义分割 ERL 代表三维病害检测、变化
检测或几何测量成熟度。

当前优先操作化任务为室外点云语义分割，候选共同语义包括：

- `ground_impervious`；
- `vegetation`；
- `building_structure`；
- `vehicle`。

## 2. 分析单位

| 单位 | 定义 |
|---|---|
| 原始点 | 原始发布点云中的一个三维观测点，不作为独立统计样本 |
| 原始场景/条带 | 官方发布的连续场景、航带、扫描条带或测区文件 |
| 空间支持单元 SSU-C | 在统一物理坐标和冻结网格下形成的非重叠空间单元 |
| 独立采集单元 ICU-C | `测区/工程对象 × 测量批次 × 传感器系统` |
| 重叠组 | 同一区域由重复航带、重复扫描、重叠切块或派生采样产生的一组观测 |
| 传感器系统 | 扫描仪、平台、安装姿态、扫描模式和主要配置的组合 |

点数、随机裁块数和训练窗口数均不得作为独立数据集样本量。

## 3. 必需输入

1. 原始点云文件、格式和哈希；
2. 逐点/逐对象标签与映射；
3. 坐标参考系、长度单位和原点定义；
4. 测区、采集批次、传感器和平台记录；
5. 扫描轨迹、航带或站点信息（如适用）；
6. 配准、拼接、去噪、下采样和切块记录；
7. 强度、颜色、法向、时间戳等字段定义；
8. 官方或重建的训练/验证划分；
9. 标注质量与几何一致性审计结果。

本字典继承总体协议的全部通用判据。C1.4 由数据清单、版本标识和内容哈希直接
裁决，不另造数值指标；坐标、单位、配准和运动畸变判据按冻结的任务范围确定
适用性。

## 4. 通用计算规则

### 4.1 统一坐标与单位

所有几何指标在统一的物理长度单位下计算。无法确认单位、坐标顺序或参考系时，
依赖实际尺度的指标全部记为 `UNKNOWN`。不得仅凭坐标数值大小猜测米、厘米或毫米。

### 4.2 空间支持单元

SSU-C 的水平/三维尺寸根据任务和应用范围预注册。网格原点、坐标轴、单元尺寸和
边界处理固定后，对所有候选数据一致使用。重叠切块只计入其所属的唯一空间单元，
避免用切块数量虚增覆盖。

### 4.3 点密度

点密度至少同时报告：

- 每平方米或每立方米点数；
- 最近邻距离；
- 与传感器距离或扫描几何的关系；
- 逐 ICU 和逐语义类别分布。

只报告全局平均点密度不足以说明覆盖。

### 4.4 标注抽样

标注审计按类别、ICU、点密度层、距离层和场景位置分层。统计单位优先采用对象或
SSU-C，不以数十亿个点制造虚假精度。

## 5. 指标定义

### C-S1 目标语义覆盖率

\[
TCR_C=\frac{|\mathcal{C}_{required}\cap\mathcal{C}_{mappable}|}{|\mathcal{C}_{required}|}
\]

输出精确映射、合并、拆分、忽略类和未覆盖类。`building`、`structure`、`facade`
等标签不得在没有操作定义时视为等价。判据：C1.1。

### C-S2 语义映射损失率

以标签对象或 SSU-C 为单位：

\[
SML_C=\frac{N_{audited\ units\ losing\ required\ semantic\ distinction}}{N_{audited\ labelled\ units}}
\]

输出逐源类、目标类和 ICU 结果。判据：C1.1、C2.2。

### C-I1 点云—标签结构完整率

\[
PIR_C=\frac{N_{records\ with\ valid\ coordinates,fields,labels}}{N_{expected\ records}}
\]

检查非有限坐标、字段长度不一致、非法标签、标签遗漏、损坏文件和重复点 ID。合法
忽略标签单独记录，不计为缺失。判据：C1.2。

### C-I2 致命几何/标签错误 SSU 率

\[
FGER_C=\frac{N_{audited\ SSU\ with\ fatal\ geometry/label\ error}}{N_{audited\ SSU}}
\]

致命错误包括坐标轴交换、单位错误、标签整体错位、场景身份错配和不可恢复变换。
判据：C1.2、C1.3。

### C-P1 坐标与单位可追溯状态

分类输出：

- `crs_and_unit_verified`；
- `local_frame_and_unit_verified`；
- `unit_verified_frame_ambiguous`；
- `unit_inferred_not_verified`；
- `unknown`。

同时记录 EPSG/局部坐标定义、轴向、原点、长度单位和转换链。依赖实际尺度的任务
要求前两类之一。判据：C1.3。

### C-P2 尺度一致性误差

对具有已知参考尺寸、控制点或重叠测量的对象：

\[
ScaleError_C=\operatorname{median}_i\frac{|d_i^{cloud}-d_i^{reference}|}{d_i^{reference}}
\]

报告 P50/P90/P95、参考来源和测量不确定性。没有参考时记为 `UNKNOWN`，不得用
模型预测尺寸替代。判据：C4.4。

### C-A1 严重标注缺陷 SSU 率

\[
CAER_C=\frac{N_{audited\ SSU\ with\ critical\ annotation\ defect}}{N_{audited\ SSU}}
\]

严重缺陷包括主要类别错标、对象系统性漏标、标签漂移到相邻结构和场景错配。
报告逐类、逐 ICU 和逐密度层结果。判据：C2.1。

### C-A2 对象/区域漏标率

需要独立裁决标注：

\[
OMR_C=\frac{N_{gold\ objects/regions\ absent\ from\ released\ labels}}{N_{gold\ objects/regions}}
\]

对象形成规则和最小可审计尺寸预先冻结。仅比较点级多数标签不足以发现整对象漏标。
判据：C2.1。

### C-A3 边界混淆率

在对象边界缓冲区内：

\[
BCR_C=\frac{N_{audited\ boundary\ points\ disagreed\ with\ adjudication}}{N_{audited\ boundary\ points}}
\]

缓冲宽度使用物理单位并按任务冻结。同步报告对象级 IoU，避免高密度区域支配结果。
判据：C2.1。

### C-U1 ICU 可恢复率

\[
IRR_C=\frac{N_{points\ or\ SSU\ assigned\ to\ defensible\ ICU-C}}{N_{points\ or\ SSU}}
\]

主要输出采用 SSU 加权，同时附点加权结果。仅有文件名但无法识别测区、批次或
传感器时，相应字段记未知。判据：C2.3。

### C-D1 精确重复点/记录率

在统一坐标和字段规则下识别完全重复记录：

\[
EDR_C=\frac{N_{duplicated\ point\ records}}{N_{point\ records}}
\]

该指标仅描述文件冗余，不代表空间覆盖重复。输出坐标重复、全字段重复和冲突标签
重复。判据：C2.4b。

### C-D2 空间重叠冗余率

基于 SSU 与扫描来源：

\[
SOR_C=\frac{N_{SSU\ observed\ by\ multiple\ released\ tiles/strips\ without\ independent\ use}}{N_{observed\ SSU}}
\]

具有独立时间或视角价值的重复扫描单独标记，不自动视为冗余；必须说明其是否提供
新的工程变化。判据：C2.4b。

### C-D3 跨划分空间/测区泄漏数

\[
Leak_C=N_{spatial\ overlap,scene,survey\ groups\ spanning\ train\ and\ validation/test}
\]

分别报告相同点、重叠 SSU、同一连续测区和同一测量批次泄漏。确认的相同点或重叠
区域泄漏属于硬失败候选。判据：C2.4a。

### C-E1 非重叠空间有效覆盖

\[
N_{eff,SSU}^{C}=N_{unique\ non-overlapping\ occupied\ SSU}
\]

同时报告有效水平面积、有效三维体积或有效线路长度：

\[
A_{eff}^{C}=N_{eff,SSU}^{C}\times A_{SSU}
\]

选择面积、体积或线路长度取决于任务。不得用点数替代。判据：C2.5。

### C-U2 有效 ICU 数与支配率

以各 ICU 的有效 SSU 占比 \(p_u\) 计算：

\[
N_{eff,ICU}^{C}=\frac{1}{\sum_u p_u^2},\qquad Dom_C=\max_u p_u
\]

输出原始 ICU 数、有效 ICU 数、最大 ICU 及其语义组成。判据：C3.2、C3.3。

### C-DEN1 点密度分布

在每个 SSU 中计算点数/物理面积或体积以及最近邻距离，输出逐 ICU、逐类别的
P05/P25/P50/P75/P95。不得只保留平均值。判据：C3.1、C3.4。

### C-DEN2 距离—密度覆盖率

对应用范围预先定义的传感器距离和密度分箱：

\[
Coverage_{density,range}^{C}=\frac{N_{required\ range\times density\ cells\ with\ minimum\ SSU}}{N_{required\ cells}}
\]

没有传感器距离时，可使用可靠代理，但必须标明推断方法和不确定性。判据：C3.1、
C3.5。

### C-CV1 工程变化轴覆盖率

逐轴计算地点、地形、场景类型、扫描平台、传感器、扫描高度、视角、季节和时间的
覆盖：

\[
Coverage_{C,k}=\frac{N_{required\ levels\ with\ minimum\ effective\ SSU}}{N_{required\ levels}}
\]

输出每轴结果和未覆盖层，不以宏平均替代。判据：C3.1。

### C-CV2 关键组合空洞率

\[
Hole_C=\frac{N_{required\ condition\ cells\ without\ minimum\ effective\ SSU}}{N_{required\ cells}}
\]

常见组合包括传感器×距离、类别×密度、场景×平台。只使用预注册的工程必要组合。
判据：C3.5。

### C-T1 类别最小空间覆盖

\[
TailMin_C=\min_{c\in\mathcal{C}_{required}}N_{eff,SSU}^{C}(c)
\]

同时报告各类独立对象数、ICU 数、有效面积/线路长度。点数只作辅助。判据：C3.4。

### C-RG1 配准残差

对多站、多条带、多时相或多传感器数据，在控制点/重叠稳定区域计算：

\[
RegResidual_C=\operatorname{median}_i\|x_i^{source}-T(x_i^{reference})\|_2
\]

报告 P50/P90/P95、最大值、逐 ICU 和逐轴残差。若数据本身不涉及拼接或跨时相
对齐，标记 `NA`。判据：C4.4。

### C-RG2 配准缝受影响 SSU 率

\[
SeamRate_C=\frac{N_{SSU\ intersecting\ confirmed\ harmful\ seam}}{N_{SSU}}
\]

“有重叠”不等于“有害配准缝”，须依据冻结的几何异常规则确认。判据：C4.4。

### C-M1 运动畸变风险率

对移动扫描或动态平台：

\[
MotionRisk_C=\frac{N_{audited\ SSU\ exceeding\ motion\ distortion\ tolerance}}{N_{audited\ SSU}}
\]

静态扫描可标记 `NA`。判据：C4.4。

### C-SH1 采集属性—标签关联强度

计算传感器、条带、扫描高度、距离层、点密度层、强度分布与标签的关联量，并通过
置换基线评估。高关联只表示潜在捷径。判据：C4.1。

### C-SH2 简化几何/密度捷径探针

仅使用点密度、强度统计、扫描线结构、局部高度和文件/条带身份预测标签，报告宏
指标及相对完整几何探针比率：

\[
ShortcutRatio_C=\frac{P_{simple\ acquisition\ features}}{P_{full\ geometry}+\epsilon}
\]

探针、采样和预算预先冻结。判据：C4.1、C4.5。

### C-RB1 留一测区/批次/传感器保留率

\[
Retention_{C,u}=\frac{P_{heldout\ ICU=u}}{P_{source\ random\ reference}+\epsilon}
\]

分别在可执行的留一测区、留一批次和留一传感器层报告最小值、中位数和 IQR。
同一连续测区的相邻块不得分到训练与留一测试。判据：C4.2。

### C-RB2 最差已见子群差距

\[
WorstGap_C=P_{macro}-\min_g P_g
\]

子群来自预注册的点密度、距离、传感器、场景类型和类别。报告每组 SSU、ICU 和
对象数。判据：C4.3。

## 6. 待校准阈值登记

| 符号 | 指标 | 方向 | 当前角色 |
|---|---|---|---|
| \(\tau_C^{map}\) | C-S1/C-S2 | 覆盖高、损失低 | H/V |
| \(\tau_C^{integrity}\) | C-I1/C-I2 | 完整高、错误低 | H/V |
| \(\tau_C^{coord}\) | C-P1/C-P2 | 可追溯、误差低 | 条件 H/V |
| \(\tau_C^{ann}\) | C-A1/C-A2/C-A3 | 低 | V |
| \(\tau_C^{dup}\) | C-D1/C-D2 | 低 | V |
| \(\tau_C^{eff}\) | C-E1 | 高 | V |
| \(\tau_C^{unit}\) | C-U2 | 高 | V |
| \(\tau_C^{dominance}\) | C-U2 | 低 | V |
| \(\tau_C^{density}\) | C-DEN1/C-DEN2 | 覆盖充分 | V |
| \(\tau_C^{axis}\) | C-CV1 | 高 | V |
| \(\tau_C^{hole}\) | C-CV2 | 低 | V |
| \(\tau_C^{tail}\) | C-T1 | 高 | V |
| \(\tau_C^{reg}\) | C-RG1/C-RG2 | 低 | 条件 V/H |
| \(\tau_C^{motion}\) | C-M1 | 低 | 条件 V |
| \(\tau_C^{shortcut}\) | C-SH1/C-SH2 | 低 | V |
| \(\tau_C^{retention}\) | C-RB1 | 高 | V |
| \(\tau_C^{worst}\) | C-RB2 | 低 | V |

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
spatial_support_unit_definition
coordinate_reference
length_unit
evidence_quality
source_artifact
calculation_config_hash
criterion_state
threshold_id
notes
```

## 8. 禁止做法

- 把点数、窗口数或裁块数当作独立样本量；
- 用全局平均点密度替代距离和空间分布；
- 在单位不明时计算物理尺度指标；
- 把重叠扫描一律算作多样性或一律算作重复；
- 将相邻空间块随机拆分制造跨域测试；
- 用目标案例调整体素、SSU 或配准容差；
- 将四类城市语义分割结果外推到病害检测、变化检测或工程测量；
- 将受控下采样变体视为新的独立数据集。
