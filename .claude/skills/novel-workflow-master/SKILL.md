---
name: novel-workflow-master
description: 小说工作流大师。通过结构化对话从创意到定稿，完成可发布的小说工程文件。当用户提到"写小说""网文工作流""小说大纲到正文""连载创作""小说工程化"以及含义相近的词汇时引用。
metadata:
  openclaw:
    requires: {}
---

# 小说工作流大师

通过阶段化对话，帮助用户从模糊想法出发，完成小说的框架、结构、章节蓝图、正文、一致性修订与发布包整理。

本 Skill 不调用任何外部 API，也不依赖其他 Skill。

## 知识库索引

| 阶段 | 参考文件 | 用途 |
|------|---------|------|
| 阶段一 | `reference/step1_ideation_and_framework.md` | 创意入口与核心框架：确认类型、读者、叙事方式、核心冲突，生成 `framework.md` |
| 阶段二 | `reference/step2_scale_and_blueprint.md` | 规格与结构骨架：确定短/中/长篇方案，生成 `blueprint.md` |
| 阶段三 | `reference/step3_story_and_arcs.md` | 主线与篇章故事：生成主线文件和各卷/篇章剧情文件 |
| 阶段四 | `reference/step4_chapter_outlines.md` | 章节蓝图：逐章卡片（章目标、冲突、信息增量、伏笔、章钩子） |
| 阶段五 | `reference/step5_draft_writing.md` | 正文生成：按批次生成章节正文并提供续写/重写闸门 |
| 阶段六 | `reference/step6_consistency_editing.md` | 一致性校对：人物、时间线、规则、伏笔、视角、文风偏移检查 |
| 阶段七 | `reference/step7_release_package.md` | 定稿与发布包：卷汇总、简介、角色表、世界观速查、目录 |
| 测试模式 | `reference/test_mode.md` | 测试模式规范：固定参数、自动推进范围、输出边界和优先级 |

## 全局锚定规则

阶段一产出的 `framework.md` 是整部作品的宪法文件。阶段二至阶段七必须始终读取并遵循：

- 核心人物：外观、性格、动机、人物弧线
- 核心关系：关系类型、冲突来源、关系演化边界
- 世界规则：力量体系、社会秩序、禁忌与代价
- 叙事设定：视角（第一/第三人称）、时态、文风约束
- 商业节奏：前若干章钩子、转折节点、付费前后节奏

如后续阶段发现与 `framework.md` 冲突，必须暂停当前步骤，先与用户确认是修改框架还是调整新产出内容。

## 交互闸门（统一）

每阶段结束后都提供固定选项：

1. 继续下一阶段
2. 回到上一阶段修改
3. 当前阶段局部重生成
4. 查看当前工程文件索引

## 测试模式

用户在创意入口输入「测试模式」「测试」或「test」时触发。测试模式固定参数（中篇，30 章，单章目标 1500-2200 字），从阶段三开始全程自动生成直至完成，不与用户逐步互动。默认输出：完整主线 + 前 3 章正文 + 一份一致性报告。

测试模式设定优先级高于正常流程，遇到冲突以 `reference/test_mode.md` 为准。

## 工作流程

### 阶段一：创意入口与核心框架

通过开放式提问收集创意，确认 6 个关键维度（题材、目标读者、叙事视角、文风、核心情绪、一句话灵感），输出 `framework.md`。必须等待用户确认后进入阶段二。

### 阶段二：规格与结构骨架

基于框架选择小说规格（短篇/中篇/长篇），确认总章数、总字数、卷结构和节奏曲线，输出 `blueprint.md`。必须等待用户确认后进入阶段三。

### 阶段三：主线与篇章故事

先输出全局主线，再按卷（或篇）生成剧情文件，输出 `story/story.md` 与 `story/arcs/*.md`。支持按卷批量推进。

### 阶段四：章节蓝图

基于阶段三内容生成逐章卡片，输出 `chapters/outline/chXX.md`。先生成样章蓝图，确认后再批量扩展。

### 阶段五：正文生成

按批次（建议每批 3-5 章）生成 `chapters/draft/chXX.md`，每批结束给出继续/回改/重写闸门。

### 阶段六：一致性校对与修订建议

对已生成正文做一致性检查，输出 `editing/consistency_report.md` 与 `editing/retcon_tasks.md`，标注高优先级修订项。

### 阶段七：定稿与发布包

整合发布材料，输出 `release/` 目录（卷汇总、作品简介、角色表、世界观速查、章节目录），并区分发布版与作者工作版。

## 输出目录约定

```
outputs/novels/<书名>_<yyyyMMdd_HHmm>/
  framework.md
  blueprint.md
  story/
    story.md
    arcs/
      arc01_<卷名>.md
  chapters/
    outline/
      ch01.md
    draft/
      ch01.md
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
