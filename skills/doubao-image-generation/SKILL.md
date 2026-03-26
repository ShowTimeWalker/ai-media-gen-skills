---
name: doubao-image-generation
description: Generate or edit images with Doubao, upload the result to Qiniu, and return the image URL.
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"],"env":["ARK_API_KEY","QINIU_ACCESS_KEY","QINIU_SECRET_KEY","QINIU_BUCKET","QINIU_PUBLIC_DOMAIN"]},"primaryEnv":"ARK_API_KEY"}}
---

# 豆包生图

这个 skill 负责豆包图片生成与编辑，并在成功后自动上传到七牛，最终返回图片 URL。

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

- 输入：提示词，必要时附带本地图片路径或图片 URL。
- 本地输出目录：
  - `outputs/doubao/images/text_to_image/`
  - `outputs/doubao/images/image_to_image/`
- 七牛对象 key 默认复用 `outputs/` 下的相对路径，因此返回 URL 会按 `doubao/images/...` 分层。
- 脚本最终输出 JSON，包含：
  - `used_model`
  - `local_path`
  - `bucket`
  - `object_key`
  - `url`

## 配置

- OpenClaw 环境变量优先：
  - `ARK_API_KEY`
  - `QINIU_ACCESS_KEY`
  - `QINIU_SECRET_KEY`
  - `QINIU_BUCKET`
  - `QINIU_PUBLIC_DOMAIN`
- 本地调试仍保留文件回退：
  - `api_key/doubao.json`
  - `api_key/qiniu.json`

## 注意事项

- 脚本固定传 `watermark=False`，只表示生成结果不额外加 AI 水印，不能去掉输入图本身已有的水印。
- 如果首选模型额度不足，会按 `5.0 -> 4.5 -> 4.0` 自动降级。
- 如果需要只做存储分发，不要复用这个 skill，直接使用 `qiniu_object_storage`。
