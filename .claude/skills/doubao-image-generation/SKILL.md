---
name: doubao-image-generation
description: 使用豆包（火山引擎 Ark）生成或编辑图片，将结果保存到本地。当用户提到"豆包生图""豆包图片""Doubao""火山引擎图片"时引用；当工作流选择豆包作为图片生成供应商时引用；支持文生图和图生图两种场景。当用户同时提到"工作流""流水线""编排"时，不应直接引用此 skill，应优先让 content_generation_workflow 统一调度。
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
        - ARK_API_KEY
    primaryEnv: ARK_API_KEY
    pythonDeps:
      - "volcengine-python-sdk[ark]"
---

# 豆包生图

这个 skill 是纯图片生成能力，不负责对象存储上传，也不直接返回公网链接。

适用场景：

- 用户明确指定使用豆包生图
- 多媒体工作流需要一个图片生成供应商
- 需要文生图或图生图，但暂时只要本地结果

脚本位于 skill 目录内的 `scripts/`，运行时始终使用绝对路径。

设 `DOUBAO_SKILL_DIR` 为 `.claude/skills/doubao-image-generation` 的绝对路径：

- 文生图：`uv run --python python $DOUBAO_SKILL_DIR/scripts/text_to_image.py`
- 图生图：`uv run --python python $DOUBAO_SKILL_DIR/scripts/image_to_image.py`

## 快速调用

文生图：

```powershell
uv run --python python $DOUBAO_SKILL_DIR/scripts/text_to_image.py `
  --prompt "一张电影感写实人像海报，光影强烈，构图干净"
```

图生图：

```powershell
uv run --python python $DOUBAO_SKILL_DIR/scripts/image_to_image.py `
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

- 环境变量：`ARK_API_KEY`（必需，未设置时直接报错）

## 协作方式

- 如果用户只要求图片生成，本 skill 可直接完成任务
- 如果用户还需要公网链接或临时下载链接，应由后续的交付环节继续处理
- 当用户未指定供应商时，是否使用 Doubao 由多媒体内容生成 Agent 的预设策略决定
