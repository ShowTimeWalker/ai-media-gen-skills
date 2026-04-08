# 阶段八：轻量多视角校验（发布前补充层）

## 目标

在不改变作者主流程的前提下，用最小成本做发布前风险检查，覆盖四类高频问题：结构、读者体验、平台适配、合规风险。

> 说明：本阶段是补充检查层，不替代阶段一至七，也不强制自动重写正文。

## 输入

- `framework.md`
- `blueprint.md`
- `chapters/draft/chXX.md`
- `state/timeline.md`
- `state/character_state.md`
- `state/relationship_graph.md`
- `state/plot_graph.md`
- `state/rule_log.md`
- `state/change_log.md`
- `release/release_version.md`
- `release/synopsis.md`
- `release/toc.md`

## 输出

- `editing/step8_validation_report.md`
- `editing/step8_quick_fixes.md`

## 校验范围（四视角）

### 1) 编辑视角

- 章节节奏是否失衡（连续低推进/高重复）
- 信息密度是否异常（有效信息过少）
- 章节钩子是否连续失效（驱动力不足）

### 2) 读者视角

- 潜在弃读点（拖沓、角色反应不可信、爽点不足）
- 情绪回报不足段落（铺垫长但兑现弱）
- 高风险章节列表（优先人工复核）

### 3) 平台视角

- 书名/简介/标签与正文匹配度
- 开篇抓力与品类预期一致性
- 目录与卖点表达清晰度

### 4) 合规视角

- 敏感内容风险点标注
- 价值观风险提示
- 平台发布前警示项

## 分级规则

- P0：必须修（影响发布安全或主线逻辑）
- P1：建议修（影响读者体验和留存）
- P2：可优化（不影响发布但可提升品质）

## 报告模板

`step8_validation_report.md` 建议结构：

1. 编辑视角问题
2. 读者视角问题
3. 平台视角问题
4. 合规视角问题
5. 总体风险结论（可发布/建议修订后发布）

每条问题包含：

- 问题描述
- 影响范围（章节/发布文档）
- 优先级（P0/P1/P2）
- 快速修订建议

`step8_quick_fixes.md` 建议结构：

- P0 必修
- P1 建议修
- P2 可优化

## 执行原则

- 仅输出问题与修订建议，不做复杂自动重写
- 若存在 P0 问题，不建议直接发布
- 修订后可重复执行本阶段做二次确认
