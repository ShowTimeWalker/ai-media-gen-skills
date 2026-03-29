---
name: doubao-video-generation
description: 使用豆包 Seedance（火山引擎 Ark）生成视频，将结果保存到本地。当用户提到"豆包生视频""豆包视频""Doubao 视频""Seedance""火山引擎视频"时引用；当工作流选择豆包作为视频生成供应商时引用；支持文生视频、首帧图生视频、首尾帧图生视频、基于参考图生视频。当用户同时提到"工作流""流水线""编排"时，不应直接引用此 skill，应优先让 content_generation_workflow 统一调度。
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

# 豆包视频生成

这个 skill 是纯视频生成能力，不负责对象存储上传，也不直接返回公网链接。

适用场景：

- 用户明确指定使用豆包（Seedance）生成视频
- 多媒体工作流需要一个视频生成供应商
- 需要文生视频、首帧图生视频、首尾帧图生视频或参考图生视频

脚本位于 skill 目录内的 `scripts/`，运行时始终使用绝对路径。

设 `DOUBAO_VIDEO_SKILL_DIR` 为 `.claude/skills/doubao-video-generation` 的绝对路径：

- 创建视频任务：`uv run --python python $DOUBAO_VIDEO_SKILL_DIR/scripts/create_video_task.py`
- 查询视频任务：`uv run --python python $DOUBAO_VIDEO_SKILL_DIR/scripts/query_video_task.py`
- 下载视频：`uv run --python python $DOUBAO_VIDEO_SKILL_DIR/scripts/download_video.py`

## 快速调用

文生视频（创建 + 轮询 + 下载一步完成）：

```powershell
uv run --python python $DOUBAO_VIDEO_SKILL_DIR/scripts/create_video_task.py `
  --prompt "写实风格，晴朗的蓝天之下，一大片白色的雏菊花田，镜头逐渐拉近，最终定格在一朵雏菊花的特写上，花瓣上有几颗晶莹的露珠" `
  --ratio 16:9 --duration 5 --poll
```

首帧图生视频：

```powershell
uv run --python python $DOUBAO_VIDEO_SKILL_DIR/scripts/create_video_task.py `
  --prompt "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头" `
  --image-url "https://example.com/first_frame.png" `
  --role first_frame --ratio adaptive --duration 5 --poll
```

仅创建任务（异步工作流场景）：

```powershell
uv run --python python $DOUBAO_VIDEO_SKILL_DIR/scripts/create_video_task.py `
  --prompt "小猫对着镜头打哈欠" --ratio 16:9 --duration 5
```

## 输入与输出

### 输入

| 参数 | 说明 | 必需 |
|------|------|------|
| `--prompt` | 提示词 | 是 |
| `--model` | 模型 ID，默认 `doubao-seedance-1-5-pro-251215` | 否 |
| `--image-url` | 图片 URL（可多次传），配合 `--role` 使用 | 否 |
| `--role` | 图片角色：`first_frame` / `last_frame` / `reference_image` | 否 |
| `--ratio` | 宽高比：16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive | 否，默认 16:9 |
| `--duration` | 视频时长（秒）：2~12 | 否，默认 5 |
| `--resolution` | 分辨率：480p, 720p, 1080p | 否，默认 480p |
| `--seed` | 随机种子 | 否 |
| `--generate-audio` | 是否生成有声视频（仅 1.5 pro 支持） | 否 |
| `--watermark` | 是否添加水印 | 否 |
| `--draft` | 是否生成样片（仅 1.5 pro） | 否 |
| `--service-tier` | 推理模式：default（在线）/ flex（离线，50% 价格） | 否 |
| `--poll` | 创建后自动轮询直到完成并下载 | 否 |
| `--poll-interval` | 轮询间隔秒数，默认 10 | 否 |
| `--timeout` | 轮询超时秒数，默认 900 | 否 |

### 本地输出目录

- `outputs/doubao/videos/text_to_video/`
- `outputs/doubao/videos/image_to_video/`

### 脚本输出 JSON

创建任务返回：
```json
{
  "type": "video",
  "scene": "text_to_video",
  "provider": "doubao",
  "task_id": "cgt-2025xxxx",
  "status": "queued"
}
```

轮询完成并下载后返回：
```json
{
  "type": "video",
  "scene": "text_to_video",
  "provider": "doubao",
  "task_id": "cgt-2025xxxx",
  "used_model": "doubao-seedance-1-5-pro-251215",
  "local_path": "outputs/doubao/videos/text_to_video/20260330_120000_cgt-xxx.mp4",
  "source_url": "https://...",
  "resolution": "1080p",
  "ratio": "16:9",
  "duration": 5
}
```

查询任务返回：
```json
{
  "task_id": "cgt-2025xxxx",
  "status": "succeeded",
  "video_url": "https://...",
  "model": "doubao-seedance-1-5-pro-251215",
  "duration": 5,
  "ratio": "16:9"
}
```

## 模型选择

| 模型 | Model ID | 特点 |
|------|----------|------|
| Seedance 1.5 Pro | `doubao-seedance-1-5-pro-251215` | 最高质量，支持有声视频、样片模式、返回尾帧、4~12秒（默认） |

## 提示词最佳实践（强制）

调用脚本生成视频前，**必须**先读取 `references/seedance_1_5_pro_prompt_guide.md`，并对照其中的**提示词质量检查清单**审核用户的提示词。

### 执行规则

1. **必须读取参考文档**：每次生成视频前，先读取 `references/seedance_1_5_pro_prompt_guide.md`
2. **提示词公式**：主体 + 运动 + 环境（非必须）+ 运镜/切镜（非必须）+ 美学描述（非必须）+ 声音（非必须）
3. **必须通过质量检查**：对照检查清单逐项审核，全部通过后方可执行
4. **不通过则拒绝并返回理由，然后自行优化重试**：如果提示词不满足检查清单，**必须拒绝执行**，返回 JSON 格式的拒绝信息，包含具体的不合规项和建议：
   ```json
   {
     "status": "rejected",
     "reasons": [
       "主体不明确：缺少主体的外貌、穿着、姿态等描述",
       "缺少运动描述：未描述主体的动作和运动方式",
       "缺少环境描述：提示词公式中环境为必须项"
     ],
     "suggestions": [
       "补充主体的具体外貌和穿着描述",
       "描述主体的动作、运动方式及节奏（如'缓缓走'、'快速奔跑'）",
       "补充环境信息，如光线、天气、场景氛围"
     ]
   }
   ```
   返回拒绝信息后，**自行根据参考文档中的最佳实践优化提示词**，向用户展示优化后的提示词并确认，用户同意后再执行
5. **允许图生视频场景适当简化**：有首帧图片时，主体外观描述可简化，但仍需描述运动、环境和声音

### 常见不合规情况（应拒绝）

- 只有一句话且无具体动作描述（如"一只猫"）
- 主体不明确（如"一个人在走"）
- 多人场景角色特征不可区分
- 包含切镜但未区分镜头编号或景别
- 包含对话但未指定语言类型或音色特征

## 配置

- 环境变量：`ARK_API_KEY`（必需，未设置时直接报错）

## 协作方式

- 如果用户只要求视频生成，本 skill 可直接完成任务（使用 `--poll` 模式）
- 如果使用异步工作流模式，先调用 `create_video_task.py` 创建任务，再定时调用 `query_video_task.py` 轮询，最后用 `download_video.py` 下载
- 如果用户还需要公网链接或临时下载链接，应由后续的交付环节（qiniu skill）继续处理
- 当用户未指定供应商时，是否使用 Doubao 由多媒体内容生成工作流的预设策略决定
