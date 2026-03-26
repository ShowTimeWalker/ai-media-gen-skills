---
name: juzi_image_video_generation
description: Generate Juzi images or videos, poll task status, and download results locally without storage coupling.
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"],"env":["JUZI_API_KEY"]},"primaryEnv":"JUZI_API_KEY"}}
---

# 橘子图片视频生成

这个 skill 只负责橘子侧的生成、轮询和本地下载，不负责对象存储上传。

## 使用脚本

- 图片一键流程：`uv run --no-project --python python scripts/python/workflows/run_juzi_image_pipeline.py`
- 视频一键流程：`uv run --no-project --python python scripts/python/workflows/run_juzi_video_pipeline.py`
- 图片状态查询：`uv run --no-project --python python scripts/python/juzi/query_image_status.py --juzi-id <ID>`
- 视频状态查询：`uv run --no-project --python python scripts/python/juzi/query_video_status.py --juzi-id <ID>`

## 快速调用

图片：

```powershell
uv run --no-project --python python scripts/python/workflows/run_juzi_image_pipeline.py `
  --prompt "一只卡通风格的橙色猫咪坐在木桌上，背景简洁，光线自然"
```

视频：

```powershell
uv run --no-project --python python scripts/python/workflows/run_juzi_video_pipeline.py `
  --prompt "一辆红色跑车在夜晚城市街道中高速穿行，电影感镜头，光影反射明显"
```

## 输入与输出

- 本地输出目录：
  - `outputs/juzi/images/`
  - `outputs/juzi/videos/`
- 脚本最终输出 JSON，包含：
  - `juzi_id`
  - `local_path`
  - `source_url`
  - `final_response`

## 配置

- OpenClaw 环境变量优先：`JUZI_API_KEY`
- 本地调试回退：`api_key/juzi.json`

## 协作方式

- 如果用户还需要把结果发布到公网或生成临时下载链接，再调用 `qiniu_object_storage`。
- 如果用户只想查进度，不要重复创建任务，直接使用状态查询脚本。
