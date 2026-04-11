---
name: fanqie-best-practices
description: 番茄小说平台向写作与自检：首秀与读完率、书名简介封面、章节节奏与合规要点、可编辑的个人写作习惯；维护模式下同步公开页面快照并审慎合并回本 Skill 的 reference。当用户提到「番茄小说」「番茄首秀」「读完率」「书名简介」「番茄审核」「番茄规则」「同步番茄官网」「更新番茄写作 skill」及含义相近表述时引用。
---

# 番茄小说写作与维护（本 Skill）

本 Skill 自包含：日常写作参考与「维护同步」流程均在下列文件中，不依赖其他 Skill。

## 使用模式

| 模式 | 何时使用 | 先读文件 |
|------|----------|----------|
| A 日常写作 | 构思、连载、改稿、自查合规与格式 | 下表「日常索引」按主题打开 |
| B 维护同步 | 用户明确要求从官网等公开页拉取信息并更新本 Skill | `reference/maintenance_sync_workflow.md` |

**模式 B 闸门**：合并进本 Skill 前必须先向用户展示拟修改要点或 diff，经确认后再写入；易变数据（榜单、活动列表）优先写入 `reference/sourced_snapshots_index.md` 并标注抓取时间与来源链接。

**模式 B 执行快照（工作区根目录）**：设置环境变量 `OUTPUT_ROOT` 后运行：

```text
uv run python .claude/skills/fanqie-best-practices/scripts/fanqie_official_sync.py
```

完整步骤、可选环境变量与**脚本全文附录**见 `reference/maintenance_sync_workflow.md`（§3、§7）；可执行副本为 `scripts/fanqie_official_sync.py`。

## 日常索引（渐进式披露）

| 主题 | 文件 | 用途 |
|------|------|------|
| 平台向写作与运营习惯 | `reference/platform_writing_guide.md` | 首秀、更新、简介、标签、节奏与互动等可执行建议 |
| 内容安全与格式 | `reference/compliance_and_format.md` | 审核红线与常见驳回类型、正文与标题格式自检 |
| 题材与风向（归纳） | `reference/topic_inspiration_baseline.md` | 可选灵感方向，非实时榜单 |
| 个人写作习惯 | `reference/user_writing_habits.md` | 用户可编辑：字数、时段、章末习惯、复盘问题 |
| 已摘录的快照索引 | `reference/sourced_snapshots_index.md` | 带时间与链接的摘录，避免把易腐数据写进长期正文 |
| 维护同步流程与脚本附录 | `reference/maintenance_sync_workflow.md` | 含执行指令与 `fanqie_official_sync.py` 全文；可执行文件在 `scripts/fanqie_official_sync.py` |

执行指导：根据用户问题只加载必要文件，避免一次展开全部 reference。
