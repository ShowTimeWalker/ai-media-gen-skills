---
name: juzi_image_video_generation
description: 使用橘子 AI 生成图片或视频，将结果保存到本地。当用户需要生成图片或视频时引用；当用户提到"橘子""Juzi""juzi"时引用；当用户已有 juzi_id 需要查询任务进度或下载结果时引用。当用户同时提到"工作流""流水线""编排"时，不应直接引用此 skill，应优先让 content_generation_workflow 统一调度。
metadata:
  openclaw:
    requires:
      bins:
        - uv
      anyBins:
        - python
        - python3
        - py
      env:
        - JUZI_API_KEY
    primaryEnv: JUZI_API_KEY
---

# 橘子图片视频生成

这个 skill 是纯内容生成能力，负责橘子的图片/视频任务创建、状态查询和本地下载，不负责对象存储上传或分享链接生成。

适用场景：

- 用户明确指定使用橘子生成图片或视频
- 多媒体工作流需要一个支持图片或视频的供应商
- 已有 `juzi_id`，只需要查询进度或下载本地结果

## 使用脚本

脚本位于 skill 目录内的 `scripts/`，运行时始终使用绝对路径。

设 `JUZI_SKILL_DIR` 为 `.claude/skills/juzi_image_video_generation` 的绝对路径：

- 图片流程：`uv run --no-project --python python $JUZI_SKILL_DIR/scripts/run_juzi_image_pipeline.py`
- 视频流程：`uv run --no-project --python python $JUZI_SKILL_DIR/scripts/run_juzi_video_pipeline.py`
- 图片状态查询：`uv run --no-project --python python $JUZI_SKILL_DIR/scripts/query_image_status.py --juzi-id <ID>`
- 视频状态查询：`uv run --no-project --python python $JUZI_SKILL_DIR/scripts/query_video_status.py --juzi-id <ID>`

## 输出约定

- 本地输出目录：
  - `outputs/juzi/images/`
  - `outputs/juzi/videos/`
- 输出 JSON 至少包含：
  - `type`
  - `provider`
  - `juzi_id`
  - `local_path`
  - `source_url`

## 配置

- 环境变量：`JUZI_API_KEY`（必需，未设置时直接报错）

## 协作方式

- 如果用户只要求生成并得到本地文件，本 skill 可直接完成
- 如果用户还需要可访问链接，应由后续的交付环节继续处理
- 当用户未指定供应商时，是否使用橘子由多媒体内容生成 Agent 的预设策略决定
