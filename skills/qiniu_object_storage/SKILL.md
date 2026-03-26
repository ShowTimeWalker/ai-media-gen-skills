---
name: qiniu_object_storage
description: Upload local files to Qiniu object storage and return public or signed download URLs.
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"],"env":["QINIU_ACCESS_KEY","QINIU_SECRET_KEY","QINIU_BUCKET","QINIU_PUBLIC_DOMAIN"]},"primaryEnv":"QINIU_ACCESS_KEY"}}
---

# 七牛对象存储

这个 skill 只负责文件分发，不负责图片或视频生成。

## 使用脚本

- 上传文件并返回公网 URL：`uv run --no-project --python python scripts/python/qiniu/upload_file.py --file <本地文件>`
- 生成临时私有下载链接：`uv run --no-project --python python scripts/python/qiniu/generate_private_download_url.py --key <对象key> --expires-in 600`

## 快速调用

上传图片：

```powershell
uv run --no-project --python python scripts/python/qiniu/upload_file.py `
  --file outputs/doubao/images/text_to_image/example.png
```

上传视频并返回私有链接：

```powershell
uv run --no-project --python python scripts/python/qiniu/upload_file.py `
  --file outputs/juzi/videos/example.mp4 `
  --private-url `
  --expires-in 600
```

## 输入与输出

- 如果上传文件位于 `outputs/` 目录下，对象 key 会优先复用相对路径，例如：
  - `doubao/images/...`
  - `juzi/images/...`
  - `juzi/videos/...`
- 如果文件不在 `outputs/` 目录下，则使用 `--prefix` 生成对象 key。
- 脚本最终输出 JSON，包含：
  - `bucket`
  - `object_key`
  - `public_url`
  - `private_url`（当传入 `--private-url` 时）

## 配置

- OpenClaw 环境变量优先：
  - `QINIU_ACCESS_KEY`
  - `QINIU_SECRET_KEY`
  - `QINIU_BUCKET`
  - `QINIU_PUBLIC_DOMAIN`
- 本地调试回退：`api_key/qiniu.json`

## 协作方式

- 这个 skill 可以和 `juzi_image_video_generation` 或 `doubao-image-generation` 组合使用。
- 如果用户已经有本地文件路径，优先直接上传，不要重复生成。
