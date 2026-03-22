---
name: doubao-image-generation
description: 使用豆包模型执行文生图和图生图。适用于需要在当前项目中调用豆包 Seedream 模型生成图片、基于本地图片或图片 URL 做图像编辑、需要无水印输出、或在额度不足时自动降级模型的场景。用户提到豆包、文生图、图生图、本地图片生成、Seedream、图片编辑、图片生成脚本时使用此 skill。
---

# 豆包生图

## 快速入口

根据任务类型选择脚本：

- 文生图：运行 [scripts/doubao_text_to_image.py](./scripts/doubao_text_to_image.py)
- 图生图：运行 [scripts/doubao_image_to_image.py](./scripts/doubao_image_to_image.py)

始终从项目根目录使用 `uv run --project` 执行，不要直接调用系统 `python`。

PowerShell 示例：

```powershell
uv run --project C:\Users\Noah\Documents\vscode `
  C:\Users\Noah\Documents\vscode\skills\doubao-image-generation\scripts\doubao_text_to_image.py `
  --prompt "一张写实风格的户外登山海报"
```

```powershell
uv run --project C:\Users\Noah\Documents\vscode `
  C:\Users\Noah\Documents\vscode\skills\doubao-image-generation\scripts\doubao_image_to_image.py `
  --image C:\Users\Noah\Documents\vscode\resources\images\climb1.jpeg `
  --prompt "保持主体姿态不变，调整为日落暖光的写实摄影风格"
```

## 工作流程

1. 先确认项目依赖已通过 `uv` 安装。
2. 优先使用项目内现成资源：`api_key/doubao.json`、`resources/images/`、`outputs/doubao/`。
3. 文生图时只传提示词、尺寸、可选模型和输出路径。
4. 图生图时优先传本地图片路径；如果用户给的是 URL，也可以直接传。
5. 如果接口提示额度不足，脚本会按 `5.0 -> 4.5 -> 4.0` 自动降级。
6. 默认关闭水印，不需要额外传参。

## 配置约定

- API Key 优先读取环境变量 `ARK_API_KEY`
- 如果环境变量未设置，则读取当前项目的 `api_key/doubao.json`
- 输出目录默认写入当前项目的 `outputs/doubao/text_to_image/` 或 `outputs/doubao/image_to_image/`
- 图生图默认输入图片为当前项目的 `resources/images/climb1.jpeg`

如果项目目录结构变了，先阅读 [references/usage.md](./references/usage.md)，再调整脚本中的路径定位逻辑。

## 参数说明

### 文生图

常用参数：

- `--prompt`：提示词
- `--model`：首选模型 ID，默认 `doubao-seedream-5-0-260128`
- `--size`：输出尺寸，默认 `2K`
- `--output`：输出文件路径

### 图生图

常用参数：

- `--image`：本地图片路径或图片 URL
- `--prompt`：编辑提示词
- `--model`：首选模型 ID，默认 `doubao-seedream-5-0-260128`
- `--size`：输出尺寸，默认 `2K`
- `--output`：输出文件路径

## 注意事项

- 图生图脚本会把本地图片自动转成 `data:` URL 后再提交给接口。
- 如果接口返回敏感内容错误，优先改提示词或换输入图，不要误判成脚本故障。
- 当前脚本固定 `watermark=False`，只控制生成结果是否加 AI 水印，不能移除输入原图自带的水印。
- 该 skill 面向当前项目目录结构设计，不是通用多项目模板。

## 参考资料

- 使用细节与目录假设：查看 [references/usage.md](./references/usage.md)
