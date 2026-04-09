# 测试模式

## 概述

测试模式用于一次性跑通“从框架到发布包”的完整链路。触发后采用固定参数并全自动推进，直至全量产物生成完成。

> 边界说明：测试模式是固定规模回归测试模式；如需“前期正常构思 + 后续全自动推进且不限制篇幅”，请使用 `reference/full_auto_mode.md` 定义的全自动化模式。

## 触发方式

在阶段一输入「测试模式」「测试」或「test」。

## 固定参数

| 参数 | 固定值 |
|------|--------|
| 规格 | 中篇 |
| 章节数 | 30 章 |
| 单章目标字数 | 1500-2200 |
| 叙事视角 | 第三人称（默认） |
| 推进方式 | 阶段二到阶段七连续自动推进（阶段三到五严格串行） |

## 与正常流程的差异

| 环节 | 正常流程 | 测试模式 |
|------|---------|---------|
| 阶段一 | 完整 6 维确认并反复迭代 | 简化确认（题材 + 一句话灵感）后生成框架 |
| 阶段二 | 用户参与规格与结构设计 | 自动套用中篇模板 |
| 阶段三 | 逐卷确认 | 自动按卷串行生成主线与卷摘要 |
| 阶段四 | 章节蓝图串行推进 | 自动按章串行生成全书 30 章蓝图 |
| 阶段五 | 正文串行逐章生成 | 自动按章串行生成全书 30 章正文（含上下文窗口） |
| 阶段六 | 人工决定何时校对 | 自动生成一致性报告 |
| 阶段七 | 正常进入发布包 | 自动生成发布包（发布版 + 作者工作版） |

## 自动推进硬边界（强约束）

- 测试模式必须从阶段二开始连续执行到阶段七，禁止中途暂停为“待用户确认”状态。
- 执行过程中禁止输出“是否继续”“要不要继续”“如果你要我可以继续”类询问。
- 仅允许输出进度与当前缺失项，不允许将推进决策交还用户。

## 串行与上下文窗口规则

测试模式下，阶段三到阶段五同样遵循强制串行：

- 阶段三：`arc01 -> arc02 -> ...`
- 阶段四：`ch01 -> ch02 -> ...`
- 阶段五：`ch01 -> ch02 -> ...`

阶段五每章正文生成前，必须加载：

- 固定种子上下文：`framework.md` + `blueprint.md` + `story/story.md` + 对应 `story/arcs` + 当前章 `outline`
- 滚动上下文：最近 10 章正文
- 前 10 章未满时：固定种子 + 已有最近章节正文（不强制凑满 10 章）

## 自动产出范围

```
outputs/novels/<书名>_<yyyyMMdd_HHmm>/
  framework.md
  blueprint.md
  story/story.md
  story/arcs/arc*.md
  chapters/outline/ch01.md ~ ch30.md
  chapters/draft/ch01.md ~ ch30.md
  editing/consistency_report.md
  editing/retcon_tasks.md
  release/release_version.md
  release/author_working_version.md
  release/synopsis.md
  release/characters.md
  release/worldbook.md
  release/toc.md
```

## 完成判定门槛（硬条件）

仅当以下条件全部满足，才允许输出“测试模式已完成”：

1. `chapters/draft/ch01.md` 到 `chapters/draft/ch30.md` 全部存在
2. `chapters/outline/ch01.md` 到 `chapters/outline/ch30.md` 全部存在
3. `release/release_version.md`、`release/author_working_version.md`、`release/synopsis.md`、`release/characters.md`、`release/worldbook.md`、`release/toc.md` 全部存在
4. `editing/consistency_report.md` 与 `editing/retcon_tasks.md` 存在

任一文件缺失都不得宣告完成。

## 中断恢复规则（自动续跑）

- 若执行中断或落盘不完整，必须自动扫描缺失文件并从最小缺失项继续生成：
  - 缺章节蓝图：从最小缺失 `outline/chNN.md` 开始补齐至 `ch30.md`
  - 缺正文：从最小缺失 `draft/chNN.md` 开始补齐至 `ch30.md`
  - 缺发布包：补齐 `release/*` 全部关键文件
- 恢复过程只输出“当前缺失项 + 正在补齐进度”，不请求用户确认继续。

## 禁止话术（测试模式）

- “如果你要，我下一步可以继续……”
- “要不要我继续……”
- “你现在可以选择是否继续……”
- 任何将自动推进决策交回用户的表达

## 完成报告模板

```markdown
测试模式已完成，已完成全量一次性生成。

本次产出：
- 核心框架：framework.md
- 结构蓝图：blueprint.md
- 主线与卷摘要：story/
- 章节蓝图：全书 30 章
- 正文：全书 30 章
- 一致性报告：editing/consistency_report.md
- 发布包：release/

下一步建议：
1. 人工抽检关键章节连贯性和伏笔回收
2. 基于 retcon 清单做定向修订后再发布
```

## 冲突处理优先级

测试模式优先级高于常规流程：

- 章节规模固定为 30 章中篇
- 阶段二至七默认自动推进（阶段三至五仍保持串行）
- 若其他步骤文档与测试模式冲突，以本文件为准

## 与全自动化模式的关系

- 测试模式：固定 30 章中篇，目标是回归验证与稳定复现
- 全自动化模式：阶段一正常构思，阶段二至七自动推进，不限制篇幅
- 当用户明确要求“不限篇幅自动跑完”时，应优先切换全自动化模式
