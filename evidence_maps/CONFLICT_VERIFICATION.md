# 四源冲突核验与裁决记录

日期：2026-08-19
范围：城市更新/城市体检公开数据集发现阶段；不执行 DRRL 或 ERL 评价。

## 裁决原则

1. 四个 DeepResearch 工具只是发现渠道，工具间共识不等于事实。
2. 身份、版本、许可和公开资产优先采用论文出版页、数据 DOI、机构数据门户和发布团队仓库。
3. 同一采集来源只计一个数据集家族；标签扩充、任务扩展和重新对齐作为版本节点保留。
4. `include` 表示当前证据足以进入正式评价池，不表示 DRRL 或 ERL 合格。
5. `provisional` 表示需要先解决身份、访问、许可或场景边界；不以“缺证据”替代“低分”。
6. 先前登录错误的 Google Doc 已全部排除，不是本次四源之一。

## 已解决的高影响冲突

| 对象 | 冲突 | 主来源核验 | 裁决 |
|---|---|---|---|
| SDNET2018 | Gemini 给出 `10.1016/j.autcon.2018.06.015` | Utah State University 页面给出数据 DOI `10.15142/T3TD19`，Data in Brief 论文 DOI 为 `10.1016/j.dib.2018.11.015` | 更正 DOI；保留一个家族 |
| MFNet | Gemini 给出 Information Fusion DOI，并把 LASNet 模型仓库当作数据仓库 | MFNet 论文 DOI 为 `10.1109/IROS.2017.8206396`；LASNet 是后续模型实现 | 更正论文身份；因语义主要是自动驾驶街景，降为 Cluster B 边界待审 |
| Rohbau3D | Gemini 给出不存在的 Zenodo 占位 DOI，并把语义版写成 2024 v2 | Scientific Data 论文 DOI 为 `10.1038/s41597-025-05827-7`；官方仓库说明当前发布加入语义/实例标签 | 一个家族、两个任务/发布节点；不采用伪 DOI |
| WHU-Railway3D | Gemini DOI 为 `10.1109/TITS.2024.IEEE` | IEEE/Crossref 为 `10.1109/TITS.2024.3469546`，官方仓库确认约 30 km、46 亿点 | 更正 DOI，正式纳入 C |
| GYU-DET | S2 根据商业转售文章排除；Gemini 根据 ResearchGate 纳入 | ScienceDB/DataCite 存在正式数据记录 `10.57760/sciencedb.19893`，许可 CC BY 4.0；论文描述 11,123 张、6 类病害 | 以原始 ScienceDB 发布覆盖转售线索，正式纳入 A |
| LCW | Gemini 把代码仓库当成主要数据资产，且未给出准确规模 | Virginia Tech 数据记录 `10.7294/16624672` 为 canonical asset，CC0，3,817 张精细标注图像 | 正式纳入 A；代码仓库只作实现来源 |
| BD3 | Gemini 称 GitHub 可直接取得 3,965 张全量数据且“Open Access” | GitHub 根目录只有代码和样例；新近 Kaggle 镜像存在但许可为 Unknown | 保留 `provisional`，待确认全量资产、发布者身份和许可 |
| OSV | Gemini 表中写“1,777 panoramic images” | WHU 官方页的 1,777 是 traffic lights 数量；官方页明确总标注对象为 5,636，但未在摘要中给出图像数 | 删除错误样本规模；正式纳入 D，规模待文件清单核验 |
| WHU Building | S2 写 8,188 图块/~22 万栋；Gemini 写 >1,400 km² | WHU 官方总页说明该家族含航空、两个卫星和变化检测子数据集，总覆盖 >1,400 km²；8,188 图块属于 Christchurch 航空子集 | 作为一个家族、多个子数据版本；禁止把家族总面积赋给单个版本 |
| WHU-Mix | Gemini 正文列出，15 行注册表和“D=2”统计却遗漏 | WHU 官方门户列出 raster 和 vector 两个版本；vector 版为 64k 图块、75.4 万建筑 | 新增独立 D 家族；不并入 WHU Building |
| CODEBRIM / SegCODEBRIM | 是新家族还是独立版本 | SegCODEBRIM Zenodo 明示图像取自 CODEBRIM，只新增裂缝掩膜 | 一个家族、两个发布/评价单元 |
| dacl1k / dacl10k | 扩展关系明确，但原图是否完全重叠不明 | 论文和发布说明支持同一家族演进；文件名不同，无法仅凭元数据确定重叠 | 一个家族、两个版本；以 pHash/内容哈希作为后续 Q3 任务 |
| METU 分类/分割 | 两个 Mendeley DOI 容易被当成两个家族 | 数据描述显示 40,000 个分类 patch 来源于 458 张原图；分割集为同一采集来源的独立发布 | 一个采集家族、两个发布/任务单元 |
| TTD | Gemini 写“3 tunnel image sets”，S2 写 1,298 张 512×512 切片 | 论文/Hugging Face 说明为三座隧道域，切片总数 1,298 | “3”记为独立采集域数量，不是样本量 |
| Sydney Urban Objects | Grok 放在 D | 数据是城市物体 3D 点云 | 调整到 Cluster C |

## 未完全解决、必须保持 provisional 的冲突

| 类型 | 对象 | 尚缺证据 | 下一步 |
|---|---|---|---|
| 公开资产 | BD3、InfraCrackNet、CUBIT-Det、BCL、WHU-Infra3D 等 | 全量包、稳定入口或许可未同时成立 | 逐一执行官方入口解析、文件清单和许可核验 |
| 场景边界 | MFNet、KAIST、FLIR、M3FD、LLVIP | 具备 RGB-T 配对，但标签以人/车为主，不是工程资产或病害 | 在冻结 Cluster B 语义边界前不得进入正式 B 评价 |
| 数据形态 | SUM Helsinki | 主要发布物是带语义的 mesh，不是原始点云 | 若协议只接受点云则排除；若接受可逆采样 mesh，需单列子型 |
| 城市体检相关性 | SemanticKITTI | 是城市驾驶点云，但不以城市资产盘点/工程诊断为目标 | 保持 provisional，避免用模态相同替代构念相同 |
| 派生聚合集 | CrackSeg9k、StructDamage | 大量源数据重复；训练/测试之间可能继承泄漏 | 下载后建立成员清单和跨家族 pHash 图，不新增采集家族 |
| 遥感边界 | Inria、SpaceNet、WHU Building、WHU-Mix | 是城市建筑资产，但与近景城市体检的成像机制不同 | 当前放 D；论文分析必须按街景/遥感子型分层，不混成单一效度结论 |
| 标识消歧 | ESTATE、UNS Geo、CMAB、UrbanLF | 缩写冲突或 canonical 入口不足 | 找到标题、作者、稳定 URL/DOI 后再解除 provisional |

## 四份报告自身的计数问题

- S1 报告的表格、`include/provisional` 小计和“23 个家族”叙述不能相互推出，且把 `bikit` 聚合工具计入数据集候选。
- S2 报告按 Cluster 行数合计为 63 个 A–D 条目，却宣称“50 个唯一家族”；报告没有提供足够的跨 Cluster 归并表来复现该数字。
- Grok 报告的 A/B/C/D 行数合计与“约 34 个唯一家族”、`include/provisional` 小计不一致，并把 Sydney Urban Objects 归入二维 D。
- Gemini 报告正文提到 S2DS、S2DS 之外的 WHU-Mix 等对象，但 15 行注册表没有完整收录；其“15 家族/19 版本/28 单元”无法从报告内表格稳定复算。

因此，本轮不继承任何工具给出的总数。最终数字完全由 `CANONICAL_FAMILY_REGISTRY.csv` 的逐行家族记录计算。

## 已使用的关键主来源

- [SDNET2018 官方论文/数据入口](https://digitalcommons.usu.edu/cee_facpub/3613/)
- [SegCODEBRIM Zenodo](https://zenodo.org/records/10071534)
- [GYU-DET ScienceDB](https://www.scidb.cn/detail?dataSetId=68827df9f367442c8be0c283e60ed3b7)
- [LCW Virginia Tech Data](https://data.lib.vt.edu/articles/dataset/Labeled_Cracks_in_the_Wild_LCW_Dataset/16624672)
- [Rohbau3D 官方仓库](https://github.com/RauchLukas/Rohbau3D)
- [WHU-Urban3D 官方站点](https://whu3d.com/dataset/)
- [WHU-Railway3D 官方仓库](https://github.com/WHU-USI3DV/WHU-Railway3D)
- [WHU 数据集总门户](https://gpcv.whu.edu.cn/data/)
- [OSV 官方页](https://gpcv.whu.edu.cn/data/osv_page.html)
