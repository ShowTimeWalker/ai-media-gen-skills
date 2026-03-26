---
name: juzi_image_video_generation
description: Generate images or videos with Juzi APIs and optionally upload results to Qiniu to return a 10-minute share link. Use when this skill should run the workspace Juzi image/video generation workflows, poll task status, download outputs, and publish result links with OpenClaw-managed JUZI_API_KEY and QINIU_* env vars.
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"],"env":["JUZI_API_KEY","QINIU_ACCESS_KEY","QINIU_SECRET_KEY","QINIU_BUCKET","QINIU_PUBLIC_DOMAIN"]},"primaryEnv":"JUZI_API_KEY"}}
---

# 橘子图片视频生成

使用 `{baseDir}/scripts/run_image_pipeline.py` 执行图片一键流程，使用 `{baseDir}/scripts/run_video_pipeline.py` 执行视频一键流程。

如果用户已经有 `juzi_id`，使用 `{baseDir}/scripts/query_image_status.py` 或 `{baseDir}/scripts/query_video_status.py` 查询状态。

始终从项目根目录运行 `uv run --no-project --python python`，不要直接调用系统 `python`。

## 快速调用

图片一键流程：

```powershell
uv run --no-project --python python `
  {baseDir}\scripts\run_image_pipeline.py `
  --prompt "一只戴着飞行员护目镜的柴犬，3D卡通风格，背景简洁。"
```

视频一键流程：

```powershell
uv run --no-project --python python `
  {baseDir}\scripts\run_video_pipeline.py `
  --prompt "一辆红色跑车在夜晚城市街道中高速穿行，电影感镜头，光影反射明显。"
```

## 密钥与配置

- 在 OpenClaw 中优先使用 `skills.entries.juzi_image_video_generation.env` 注入这些变量：
  - `JUZI_API_KEY`
  - `QINIU_ACCESS_KEY`
  - `QINIU_SECRET_KEY`
  - `QINIU_BUCKET`
  - `QINIU_PUBLIC_DOMAIN`
- 该 skill 已声明 `metadata.openclaw.primaryEnv` 为 `JUZI_API_KEY`。
- 当前脚本仍保留项目内回退逻辑：
  - 橘子回退到 `api_key/juzi.json`
  - 七牛回退到 `api_key/qiniu.json`
  这些回退仅适合当前项目中的本地调试，不应作为 OpenClaw 的主要配置方式。

## 工作流程

1. 根据任务类型选择图片流程或视频流程脚本。
2. 调用橘子创建接口，获取 `juzi_id`。
3. 按默认轮询频率查询状态：
   - 图片：每 5 秒一次，默认超时 120 秒
   - 视频：每 15 秒一次，默认超时 900 秒
4. 任务成功后下载结果到 `outputs/juzi/images/` 或 `outputs/juzi/videos/`。
5. 上传到七牛 `QINIU_BUCKET`。
6. 生成默认 10 分钟有效的分享链接并输出 JSON 结果。

## 常用参数

图片流程：

- `--prompt`：提示词
- `--model`：模型，默认 `nano-banana-fast`
- `--ratio`：比例，默认 `1:1`
- `--quality`：质量，可选
- `--url`：参考图 URL，可传多次
- `--expires-in`：分享链接有效期秒数，默认 `600`

视频流程：

- `--prompt`：提示词
- `--model`：模型，默认 `VEO 3.1 Fast 多参考版`
- `--aspect-ratio`：比例，默认 `16:9`
- `--image-url`：参考图 URL，可传多次
- `--no-reference-images`：不使用默认参考图
- `--expires-in`：分享链接有效期秒数，默认 `600`

状态查询：

- `--juzi-id`：任务 ID

## 注意事项

- 当前视频生成接口存在偶发上游失败，脚本会直接报错并保留 `juzi_id`，方便后续重试或人工排查。
- 七牛分享链接默认是时效链接；如果空间是公开空间，裸链仍可能可访问，时效限制只有在私有空间下才真正强制生效。
- 如果 OpenClaw 配置或当前项目目录有变动，先阅读 [references/usage.md](./references/usage.md)。
