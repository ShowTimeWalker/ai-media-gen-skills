# 阶段七：定稿与发布包

## 目标

把阶段一至六产物整理为可发布版本与作者工作版本，便于连载发布和后续维护。

## 输入

- `framework.md`
- `blueprint.md`
- `story/story.md`
- `chapters/draft/chXX.md`
- `editing/consistency_report.md`
- `editing/retcon_tasks.md`（若已处理则同步状态）
- `state/timeline.md`
- `state/character_state.md`
- `state/relationship_graph.md`
- `state/plot_graph.md`
- `state/rule_log.md`
- `state/change_log.md`

## 输出

- `release/release_version.md`
- `release/author_working_version.md`
- `release/synopsis.md`
- `release/characters.md`
- `release/worldbook.md`
- `release/toc.md`

## 文件说明

- `release_version.md`：面向发布平台的整洁版（不含内部注释）
- `author_working_version.md`：含章节元信息与修订痕迹
- `synopsis.md`：长简介 + 短简介 + 卖点语
- `characters.md`：角色速查（身份、动机、关系、关键事件）
- `worldbook.md`：世界观与规则速查
- `toc.md`：卷-章目录及一句话摘要

发布包生成口径：

- `release/characters.md` 优先聚合 `state/character_state.md` 与 `state/relationship_graph.md`
- `release/worldbook.md` 优先聚合 `state/rule_log.md` 与 `state/timeline.md`
- `release/toc.md` 优先聚合 `state/plot_graph.md` 与章节摘要
- 对 `release/release_version.md`、`release/synopsis.md`、`release/toc.md` 在输出前执行轻度去AI味清洗
- 去AI味清洗规则遵循 `reference/de_ai_style_guard.md`，且不得改动设定与事实
- 清洗后必须做一次 state 与正文一致性复核，确保口径一致
- 若 `state/*` 与正文不一致，先回到阶段六修复后再生成发布包

## 收尾检查

1. 章节编号连续
2. 卷名与目录一致
3. 发布版不含内部标注
4. 关键伏笔在目录摘要中可追踪
5. 发布前建议执行 `reference/step8_multi_view_validation.md` 并查看 `editing/step8_validation_report.md`
6. 若 STEP8 存在 P0 问题，不建议直接发布

## 完成提示模板

```markdown
小说工作流已完成，发布包已生成。

你现在可以：
1. 直接用于发布（`release/release_version.md`）
2. 继续做精修（`release/author_working_version.md`）
3. 回到任意阶段局部重生成
```
