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
| 阶段一 | `reference/tomato_hot_themes.md` | 番茄热门题材灵感参考：按男女频与关键词给出高潜主题与开篇钩子 |
| 阶段二 | `reference/step2_scale_and_blueprint.md` | 规格与结构骨架：确定短/中/长篇方案，生成 `blueprint.md` |
| 阶段三 | `reference/step3_story_and_arcs.md` | 主线与篇章故事：生成主线文件和各卷/篇章剧情文件 |
| 阶段四 | `reference/step4_chapter_outlines.md` | 章节蓝图：逐章卡片（章目标、冲突、信息增量、伏笔、章钩子） |
| 阶段五 | `reference/step5_draft_writing.md` | 正文生成：按批次生成章节正文并提供续写/重写闸门 |
| 阶段六 | `reference/step6_consistency_editing.md` | 一致性校对：人物、时间线、规则、伏笔、视角、文风偏移检查 |
| 阶段七 | `reference/step7_release_package.md` | 定稿与发布包：卷汇总、简介、角色表、世界观速查、目录 |
| 阶段八 | `reference/step8_multi_view_validation.md` | 轻量多视角校验：编辑/读者/平台/合规四视角发布前检查 |
| 全自动化模式 | `reference/full_auto_mode.md` | 全自动化模式规范：阶段一正常构思后，阶段二至七自动推进，不限制篇幅 |
| 去AI味规则 | `reference/de_ai_style_guard.md` | 去AI味轻度修订规范：正文与发布包的自动清洗边界、禁改项与验收项 |
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

## 数字优先交互规范

为减少用户输入成本，所有关键决策点默认采用“数字优先”：

- 必须提供编号选项（如 `1`、`2`、`3`）
- 支持单数字回复推进流程
- `0` 表示使用系统默认推荐
- `9` 表示进入自定义输入（仅在需要时）

如用户输入自然语言，仍应兼容解析；但提示优先给出数字选项。

## 串行执行总则（阶段三至阶段五）

- 阶段三、阶段四、阶段五必须严格串行执行，禁止并行生成或并行子任务。
- 阶段三按卷顺序推进：`arc01 -> arc02 -> ...`，上一卷主线一致性检查通过后才能进入下一卷。
- 阶段四按章顺序推进：`ch01 -> ch02 -> ...`，后一章蓝图必须参考前一章蓝图与最新主线状态。
- 阶段五按章顺序推进：`ch01 -> ch02 -> ...`，正文生成时必须加载固定种子上下文与最近章节上下文窗口（详见 `reference/step5_draft_writing.md`）。

## 状态中枢层（drafting 期间）

从阶段四开始启用 `state/` 目录，作为创作过程中的活文档中枢。阶段四、五、六、七都要读取 `state/*`，阶段五每章写作后必须回写 `state/*` 再进入下一章。

标准状态文件：

- `state/timeline.md`
- `state/character_state.md`
- `state/relationship_graph.md`
- `state/plot_graph.md`
- `state/rule_log.md`
- `state/change_log.md`

统一 ID 规范：

- 角色：`CHAR_*`
- 事件：`EVT_*`
- 主线/支线：`ARC_*`
- 伏笔：`FORESHADOW_*`
- 规则：`RULE_*`

## 全自动化模式

用户可通过两种方式启用全自动化模式：

- 在阶段一输入触发词：「全自动模式」「自动跑完」「full-auto」
- 阶段一完成后在模式选项中选择“切换全自动推进”

全自动化模式规则：

- 阶段一与正常模式完全一致，保留完整构思与确认流程
- 从阶段二开始自动推进至阶段七，不逐步等待用户确认
- 不限制篇幅，沿用用户在阶段一/二确定的规格（短/中/长篇或自定义）
- 串行、上下文窗口、state 回写等规则与正常模式一致
- 具体执行规范以 `reference/full_auto_mode.md` 为准

## 去AI味轻度钩子

适用阶段：阶段五正文、阶段七发布包。

执行目标：在不改变剧情和关键信息点的前提下，降低模板腔和机械表达，让文本更自然。

硬边界：

- 禁止改动剧情事件、事实信息、角色动机、时间线和因果链
- 允许替换模板连接词、拆分机械长句、减少重复句式、清理总结腔
- 关键设定、术语、伏笔锚点必须保持不变

具体执行规范以 `reference/de_ai_style_guard.md` 为准。

## 测试模式

用户在创意入口输入「测试模式」「测试」或「test」时触发。测试模式固定参数（中篇，30 章，单章目标 1500-2200 字），从阶段三开始全程自动生成直至完成，不与用户逐步互动。默认输出：完整主线 + 30 章章节蓝图 + 30 章正文 + 一致性报告 + 发布包。

测试模式设定优先级高于正常流程，遇到冲突以 `reference/test_mode.md` 为准。

## 工作流程

### 阶段一：创意入口与核心框架

通过开放式提问收集创意，确认 6 个关键维度（题材、目标读者、叙事视角、文风、核心情绪、一句话灵感），输出 `framework.md`。必须等待用户确认后进入阶段二。

### 阶段二：规格与结构骨架

基于框架选择小说规格（短篇/中篇/长篇/超长篇），确认总章数、总字数、卷结构和节奏曲线，输出 `blueprint.md`。规格模板最高支持约 100 万字规模。必须等待用户确认后进入阶段三。

### 阶段三：主线与篇章故事

先输出全局主线，再按卷顺序生成剧情文件，输出 `story/story.md` 与 `story/arcs/*.md`。仅在上一卷校验通过后进入下一卷。

### 阶段四：章节蓝图

基于阶段三内容按章节顺序生成逐章卡片，输出 `chapters/outline/chXX.md`。必须严格按 `ch01 -> ch02 -> ...` 推进。

### 阶段五：正文生成

按章节顺序生成 `chapters/draft/chXX.md`，每章生成前都要读取固定种子上下文与最近 10 章正文（不足 10 章时读取已有章节）。

### 阶段六：一致性校对与修订建议

对已生成正文做一致性检查，输出 `editing/consistency_report.md` 与 `editing/retcon_tasks.md`，标注高优先级修订项。

### 阶段七：定稿与发布包

整合发布材料，输出 `release/` 目录（卷汇总、作品简介、角色表、世界观速查、章节目录），并区分发布版与作者工作版。

### 阶段八：轻量多视角校验（补充层）

阶段八是作者主流程后的补充检查层，不替代阶段一至七。用于在发布前快速做四视角风险扫描（编辑/读者/平台/合规），输出校验报告与快速修订清单，不强制自动改文。

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
