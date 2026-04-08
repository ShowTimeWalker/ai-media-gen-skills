# 全自动化模式

## 概述

全自动化模式用于“保留完整前期构思，但后续自动跑完”的正式生产流程。阶段一按正常模式完成，阶段二至阶段七自动推进直至发布包输出。

## 触发方式

支持两种触发方式：

1. 阶段一开场关键词触发：
   - 「全自动模式」
   - 「自动跑完」
   - `full-auto`
2. 阶段一完成后的模式选项触发：
   - 选择“切换全自动推进（阶段二至阶段七自动完成）”

## 执行边界

- 阶段一：正常执行，完整构思与确认
- 阶段二至阶段七：全自动推进，不逐步等待用户确认
- 不限制篇幅：沿用用户在阶段一/二确定的规格（短/中/长篇或自定义）

## 规则继承

全自动化模式继承正常流程中的硬规则：

- 阶段三至阶段五严格串行，不允许并行
- 阶段五保持上下文窗口：固定种子 + 最近 10 章正文
- 状态中枢层 `state/*` 必读必回写
- 发现 `framework.md` 与新产出冲突时，按冲突规则记录并在最终报告中汇总

## 与测试模式差异

| 维度 | 全自动化模式 | 测试模式 |
|------|--------------|----------|
| 前期构思 | 阶段一正常完整执行 | 阶段一简化执行 |
| 篇幅 | 不限制，沿用已确认规格 | 固定 30 章中篇 |
| 用途 | 正式全流程自动生成 | 固定规模回归测试 |
| 产出深度 | 随规格变化，完整阶段二至七 | 固定模板化全量产出 |

## 输出清单（示例）

```
outputs/novels/<书名>_<yyyyMMdd_HHmm>/
  framework.md
  blueprint.md
  story/
    story.md
    arcs/arc*.md
  chapters/
    outline/ch*.md
    draft/ch*.md
  state/
    timeline.md
    character_state.md
    relationship_graph.md
    plot_graph.md
    rule_log.md
    change_log.md
  editing/
    consistency_report.md
    retcon_tasks.md
  release/
    release_version.md
    author_working_version.md
    synopsis.md
    characters.md
    worldbook.md
    toc.md
```

## 长篇保护建议

当规模较大（如 100 章以上）时，建议启用分卷检查点：

- 每卷结束后输出一次卷级风险摘要（时间线、人设、伏笔）
- 标注高风险章节列表和 `retcon` 优先任务

## 完成报告模板

```markdown
全自动化模式已完成，已按确认规格自动生成全流程产物。

本次模式：全自动化模式
确认规格：[短篇/中篇/长篇/自定义]
阶段执行：阶段一人工确认 + 阶段二至七自动推进

重点结果：
- 主线与分卷：已完成
- 章节蓝图与正文：已完成
- state 中枢：已回写并对账
- 一致性报告：已输出
- 发布包：已输出

高风险章节：
- [chXX] ...

retcon 优先任务：
1. [TaskXX]
2. [TaskXX]
```
