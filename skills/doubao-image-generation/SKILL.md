---
name: doubao-image-generation
description: Generate or edit images with Doubao and save the result locally for later workflow delivery.
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"],"env":["ARK_API_KEY"]},"primaryEnv":"ARK_API_KEY"}}
---

# 豆包生图

这个 skill 是纯图片生成能力，不负责对象存储上传，也不直接返回公网链接。

适用场景：

- 用户明确指定使用豆包生图
- 多媒体工作流需要一个图片生成供应商
- 需要文生图或图生图，但暂时只要本地结果

从项目根目录运行以下脚本：

- 文生图：`uv run --no-project --python python scripts/python/doubao/text_to_image.py`
- 图生图：`uv run --no-project --python python scripts/python/doubao/image_to_image.py`

## 快速调用

文生图：

```powershell
uv run --no-project --python python scripts/python/doubao/text_to_image.py `
  --prompt "一张电影感写实人像海报，光影强烈，构图干净"
```

图生图：

```powershell
uv run --no-project --python python scripts/python/doubao/image_to_image.py `
  --image resources/images/climb1.jpeg `
  --prompt "保留主体动作，改为日落暖光的写实摄影风格"
```

## 输入与输出

- 输入：提示词；图生图时可附带本地图片路径或图片 URL
- 本地输出目录：
  - `outputs/doubao/images/text_to_image/`
  - `outputs/doubao/images/image_to_image/`
- 脚本最终输出 JSON，包含：
  - `type`
  - `scene`
  - `provider`
  - `used_model`
  - `local_path`

## 配置

- OpenClaw 环境变量优先：`ARK_API_KEY`
- 本地调试回退：`api_key/doubao.json`

## 协作方式

- 如果用户只要求图片生成，本 skill 可直接完成任务
- 如果用户还需要公网链接或临时下载链接，应由 workflow 或 `qiniu_object_storage` 继续处理
- 当用户未指定供应商时，是否使用 Doubao 由多媒体内容生成 Agent 的预设策略决定
