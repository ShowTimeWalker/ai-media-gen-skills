# 阶段五：正文生成（串行逐章）

## 目标

根据章节蓝图按章节顺序生成正文，保证风格稳定、信息推进清晰、章节衔接自然。

## 输入

- `framework.md`
- `blueprint.md`
- `story/story.md`
- `story/arcs/arcXX_<卷名>.md`
- `chapters/outline/chXX.md`
- `state/timeline.md`
- `state/character_state.md`
- `state/relationship_graph.md`
- `state/plot_graph.md`
- `state/rule_log.md`
- `state/change_log.md`

## 输出

- `chapters/draft/chXX.md`

## 正文生成规则

- 必须严格遵守 `framework.md` 的视角和文风设定
- 章目标必须在正文内被完成或推进
- 章末必须保留明确钩子
- 避免重复叙事和无效回顾
- 仅允许串行生成：`ch01 -> ch02 -> ...`，禁止并行或跳章生成

## 上下文窗口规范（强制）

每一章正文生成前，必须加载以下上下文：

**固定种子上下文**（每章必读）：
- `framework.md`
- `blueprint.md`
- `story/story.md`
- 对应卷文件 `story/arcs/arcXX_<卷名>.md`
- 当前章蓝图 `chapters/outline/chXX.md`
- `state/timeline.md`
- `state/character_state.md`
- `state/relationship_graph.md`
- `state/plot_graph.md`
- `state/rule_log.md`

**滚动上下文**（每章必读）：
- 最近 10 章正文（`chapters/draft`）

**前 10 章未满时**：
- 采用“固定种子上下文 + 已有最近章节正文”
- 不强制凑满 10 章

**上下文过长时的兜底策略**：
- 固定种子上下文保持完整
- 最近 3 章保留逐段细节
- 更早章节用结构化摘要回填（角色状态/冲突状态/伏笔状态）

## 逐章推进策略

- 每完成 1 章立即做章后一致性检查
- 每完成 1 章必须回写状态文件：
  - `state/timeline.md`
  - `state/character_state.md`
  - `state/plot_graph.md`
  - `state/change_log.md`
- 章后输出：
  - 本章关键推进点
  - 与前章承接检查结果
  - 下一章接口状态

## 章节文件模板

```markdown
# Chapter XX 章名

（正文内容）

---

## 章后元信息
- 本章目标完成度：
- 新增伏笔：
- 已回收伏笔：
- 下章接口：
```

## 门禁规则

每章生成后都要给出固定选项：

1. 继续下一章
2. 重写某一章
3. 回到阶段四调整蓝图
4. 进入阶段六一致性校对

硬门禁补充：

- 若本章完成后未回写 `state/*`，不得进入下一章。
- 若 `state/*` 与正文冲突，必须先修正状态文件或重写本章后再继续。
