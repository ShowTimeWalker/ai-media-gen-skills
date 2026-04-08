# 阶段四：章节蓝图（逐章卡片）

## 目标

把分卷故事拆解成逐章执行卡片，确保每章都有明确目标与钩子。

## 输入

- `framework.md`
- `blueprint.md`
- `story/story.md`
- `story/arcs/*.md`
- `state/timeline.md`
- `state/character_state.md`
- `state/relationship_graph.md`
- `state/plot_graph.md`
- `state/rule_log.md`
- `state/change_log.md`

## 输出

- `chapters/outline/chXX.md`

## 逐章卡片必须字段

- 章目标：本章必须完成什么推进
- 章冲突：本章最主要冲突点
- 信息增量：读者新增获得的信息
- 伏笔布置/回收：本章埋点与回收点
- 章结尾钩子：驱动读者进入下一章

## 章节文件模板

```markdown
# Chapter XX 章名

## 章目标
- ...

## 冲突设计
- 外部冲突：
- 内部冲突：

## 信息增量
- ...

## 伏笔管理
- 新埋伏笔：
- 回收伏笔：

## 结尾钩子
- ...
```

## 执行策略

1. 严格按章节顺序生成蓝图：`ch01 -> ch02 -> ch03 -> ...`
2. 生成当前章前，必须先读取 `state/*` 与上一章蓝图，确认时间线与人物状态不冲突
3. 每章蓝图完成后，必须同步回写 `state/plot_graph.md` 与 `state/change_log.md`
4. 每章蓝图完成后做一次章节接口检查（下章入口是否明确）
5. 保证章节编号连续，文件命名统一为 `ch01.md`、`ch02.md`

## 门禁规则

- 后一章蓝图不得先于前一章生成。
- 若上一章接口不清晰，必须先回修上一章再继续。
- 若本章蓝图未完成 state 回写，不得进入下一章蓝图。
- 全部章节蓝图串行完成后再进入阶段五正文生成。
