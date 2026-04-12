# 阶段六：一致性校对与修订建议

## 目标

在不破坏主线节奏的前提下，系统识别正文中的逻辑和设定问题，产出可执行修订清单。

## 输入

- `framework.md`
- `blueprint.md`
- `story/story.md`
- `chapters/draft/卷X_序号_ch起始-ch结束.md`
- `state/timeline.md`
- `state/character_state.md`
- `state/relationship_graph.md`
- `state/plot_graph.md`
- `state/rule_log.md`
- `state/change_log.md`

## 输出

- `editing/consistency_report.md`
- `editing/retcon_tasks.md`

## 校验维度

1. 人设一致性（动机、行为、语言习惯）
2. 时间线一致性（事件顺序、时间跨度）
3. 规则一致性（力量体系、社会规则、禁忌代价）
4. 伏笔闭环（埋点与回收对应关系）
5. 叙事视角稳定性（视角漂移、叙述口径冲突）
6. 文风偏移（句式密度、情绪颗粒度、节奏失衡）

## 报告模板

`consistency_report.md` 建议按严重级别分组：

- P0：必须修（影响主线逻辑）
- P1：建议修（影响阅读体验）
- P2：可选优化（风格层面）

每条问题包含：问题描述、定位章节、影响范围、修复建议、关联状态条目 ID（如 `CHAR_*`/`EVT_*`/`ARC_*`/`FORESHADOW_*`/`RULE_*`）。

`retcon_tasks.md` 按任务清单输出：

- [ ] Task01：修复内容
- [ ] Task02：修复内容

建议任务格式：

- [ ] TaskXX：修复内容（章节：chXX，状态条目：`ID`，优先级：P0/P1/P2）

## 门禁规则

- 阶段六完成后，先让用户决定是否执行修订，再进入阶段七。
