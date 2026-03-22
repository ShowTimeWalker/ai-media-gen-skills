---
name: doubao-image-generation
description: Generate and edit images with Doubao Seedream via uv run --project. Use when this skill should call Ark image APIs with ARK_API_KEY.
metadata: {"openclaw":{"requires":{"bins":["uv"],"env":["ARK_API_KEY"]},"primaryEnv":"ARK_API_KEY"}}
---

# 豆包生图

使用 `{baseDir}/scripts/doubao_text_to_image.py` 执行文生图，使用 `{baseDir}/scripts/doubao_image_to_image.py` 执行图生图。

始终从项目根目录运行 `uv run --project`，不要直接调用系统 `python`。

## 快速调用

文生图：

```powershell
uv run --project C:\Users\Noah\Documents\vscode `
  {baseDir}\scripts\doubao_text_to_image.py `
  --prompt "一张电影感写实摄影风格的户外品牌海报"
```

图生图：

```powershell
uv run --project C:\Users\Noah\Documents\vscode `
  {baseDir}\scripts\doubao_image_to_image.py `
  --image C:\Users\Noah\Documents\vscode\resources\images\climb1.jpeg `
  --prompt "保留主体姿态，仅调整为日落暖光的电影感写实摄影风格"
```

## 密钥与配置

- 在 OpenClaw 中优先使用 `skills.entries.doubao-image-generation.env.ARK_API_KEY` 或 `skills.entries.doubao-image-generation.apiKey` 注入密钥。
- 该 skill 已声明 `metadata.openclaw.primaryEnv` 为 `ARK_API_KEY`，OpenClaw 会在 agent run 开始时把配置注入到进程环境。
- 当前脚本仍保留项目内回退逻辑：如果 `ARK_API_KEY` 不存在，会读取 `api_key/doubao.json`。这个回退仅适合当前项目里的直接脚本调试，不应作为 OpenClaw 的主要配置方式。
- 输出目录默认写入 `outputs/doubao/text_to_image/` 或 `outputs/doubao/image_to_image/`。

## 工作流程

1. 确认 `uv` 可用，且当前项目依赖已安装。
2. 根据任务类型选择文生图或图生图脚本。
3. 传入提示词、尺寸和可选输出路径。
4. 需要图生图时，优先传本地图片路径；如果用户给的是 URL，也可以直接传入。
5. 如果首选模型额度不足，脚本会按 `5.0 -> 4.5 -> 4.0` 自动降级。

## 常用参数

文生图：

- `--prompt`：提示词
- `--model`：首选模型 ID，默认 `doubao-seedream-5-0-260128`
- `--size`：输出尺寸，默认 `2K`
- `--output`：输出文件路径

图生图：

- `--image`：本地图片路径或图片 URL
- `--prompt`：编辑提示词
- `--model`：首选模型 ID，默认 `doubao-seedream-5-0-260128`
- `--size`：输出尺寸，默认 `2K`
- `--output`：输出文件路径

## 注意事项

- 图生图脚本会先把本地图片编码成 `data:` URL，再提交给接口。
- 当前脚本固定传 `watermark=False`，这只控制生成结果不额外添加 AI 水印，不能去除输入原图自带的水印。
- 如果接口返回额度不足错误，会自动尝试降级模型；如果是敏感内容或参数错误，需要调整提示词或输入图。
- 如果目录结构或 OpenClaw 配置有变动，先阅读 [references/usage.md](./references/usage.md)。
