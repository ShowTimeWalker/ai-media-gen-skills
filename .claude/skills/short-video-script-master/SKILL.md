---
name: short-video-script-master
description: 剧本创作大师。通过结构化对话引导用户从创意出发，完成核心框架定调和故事创作。当用户提到"点子王""编剧""点子""灵感""召唤点子王""编剧出来干活""剧本大师"以及含义相近的词汇时引用。
metadata:
  openclaw:
    requires: {}
---

# 剧本创作大师

通过结构化对话，帮助用户从模糊的创意想法出发，逐步完成整部短剧的核心框架定调和故事创作。目标投放平台以红果短剧为主。

本 Skill 不调用任何外部 API，纯粹通过对话引导完成。

## 知识库索引

| 阶段 | 参考文件 | 用途 |
|------|---------|------|
| 阶段一 | `reference/step1_ideation.md` | 创意收集的对话引导策略和退出条件 |
| 阶段一 | `reference/hongguo_genre_map.md` | 红果爆款类型图谱，用户提到类型时查阅展示 |
| 阶段二 | `reference/step2_core_framework.md` | 核心框架定调：剧集规格、主要剧情、核心人物、主要场景、画风风格、整剧基调 |
| 阶段三 | `reference/step3_story.md` | 故事线设计：3A 大纲确认 + 3B 篇章创作 |
| 阶段四 | `reference/step4_screenplay.md` | 剧本创作：按篇章批量生成逐集剧本 |
| 阶段五 | `reference/step5_production_script.md` | 生产脚本：将片段拆分转化为 AI 生成指令（中文首帧图 prompt + 视频 motion prompt） |
| 阶段六 | `reference/step6_keyframe_prompts.md` | 关键帧图片提示词：预生成角色/场景参考图 prompt，再基于参考图为每个片段生成首帧和末帧图片 prompt |

## 工作流程

### 阶段一：创意收集

通过自由对话收集创作素材。查阅 `reference/step1_ideation.md` 获取完整的对话引导策略。当用户提到具体类型时，查阅 `reference/hongguo_genre_map.md` 向用户展示类型特征和爆款公式。当类型方向、核心情绪、一句话灵感三个维度明确后，进入阶段二。

### 阶段二：核心框架定调

与用户确认剧集规格（单集时长、总时长、集数），然后生成整部剧的核心框架，包括：主要剧情概述、核心人物（年龄、具体形象）、主要场景、画风风格、整剧基调。查阅 `reference/step2_core_framework.md` 获取完整的规格选项、输出格式和关键规则。**必须等待用户二次确认**才能进入阶段三。

### 阶段三：故事线设计

分两步完成。查阅 `reference/step3_story.md` 获取完整规范。

**3A — 大纲确认**：生成主线概述 + 所有篇章标题和一句话概览（含集数分配），**必须等待用户确认**才能进入 3B。

**3B — 篇章创作**：基于确认后的大纲，逐个创作每个篇章的完整故事，输出到 `stories/` 目录。全部完成后生成主线总文件 `story.md`。

### 阶段四：剧本创作与片段拆分

按篇章逐步推进，前一个篇章确认后再进行下一个。查阅 `reference/step4_screenplay.md` 获取完整规范。

**4A — 剧本生成**：读取篇章故事文件，为该篇章所有集数生成剧本（场景列表、画面、旁白对白、声音设计、结尾钩子）。用户确认后进入 4B。

**4B — 片段拆分**：将每集剧本拆分为 6-8 秒的 AI 视频片段，用朴实平白的语言描述画面内容（禁止比喻、华丽辞藻、抽象概念）。用户确认后进入下一个篇章的 4A。

### 阶段五：生产脚本

将片段拆分转化为可直接用于 AI 视频生成的结构化生产指令。查阅 `reference/step5_production_script.md` 获取完整规范。

**5A — 全局参数提取**：从 framework.md 提取 Style Lock（风格前缀）和 Character Reference（角色外观关键词），与用户确认后进入 5B。

**5B — 片段指令生成**：为该篇章所有集数的每个片段生成首帧图 prompt（中文，描述静态起始画面）和视频 motion prompt（中文，描述 6-8s 内的运动变化）。按篇章批量生成，用户确认后写入 `production_scripts/` 目录。

### 阶段六：关键帧图片提示词

为 AI 图片生成准备结构化 prompt，通过预定义的角色和场景参考图提升跨片段一致性。查阅 `reference/step6_keyframe_prompts.md` 获取完整规范。本阶段只输出 prompt，不调用外部 API。

**6A — 角色参考图 Prompt（项目级）**：从 framework.md 提取角色外观，为每个核心角色生成参考图 prompt（基础姿态 + 关键表情，灰色纯色背景）。用户确认后进入 6B。

**6B — 场景参考图 Prompt（项目级）**：从 framework.md 提取场景描述，为每个场景生成参考图 prompt（区分光线条件，无人物）。与 6A 一起向用户确认后进入 6C。

**6C — 关键帧 Prompt（篇章级）**：基于 STEP 5 的首帧图 Prompt 和末帧描述，为该篇章所有集数的每个片段生成首帧和末帧的完整图片 prompt，标注参考图引用。按篇章批量生成，用户确认后写入 `reference_images/` 目录。
