---
name: juzi_image_video_generation
description: Generate Juzi images or videos, query task status, and download results locally without delivery coupling.
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"],"env":["JUZI_API_KEY"]},"primaryEnv":"JUZI_API_KEY"}}
---

# 橘子图片视频生成

这个 skill 是纯内容生成能力，负责橘子的图片/视频任务创建、状态查询和本地下载，不负责对象存储上传或分享链接生成。

适用场景：

- 用户明确指定使用橘子生成图片或视频
- 多媒体工作流需要一个支持图片或视频的供应商
- 已有 `juzi_id`，只需要查询进度或下载本地结果

## 使用脚本

- 图片流程：`uv run --no-project --python python scripts/python/workflows/run_juzi_image_pipeline.py`
- 视频流程：`uv run --no-project --python python scripts/python/workflows/run_juzi_video_pipeline.py`
- 图片状态查询：`uv run --no-project --python python scripts/python/juzi/query_image_status.py --juzi-id <ID>`
- 视频状态查询：`uv run --no-project --python python scripts/python/juzi/query_video_status.py --juzi-id <ID>`

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

- OpenClaw 环境变量优先：`JUZI_API_KEY`
- 本地调试回退：`api_key/juzi.json`

## 协作方式

- 如果用户只要求生成并得到本地文件，本 skill 可直接完成
- 如果用户还需要可访问链接，应由 workflow 或 `qiniu_object_storage` 继续处理
- 当用户未指定供应商时，是否使用橘子由多媒体内容生成 Agent 的预设策略决定
