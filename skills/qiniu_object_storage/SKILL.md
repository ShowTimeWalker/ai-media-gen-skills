---
name: qiniu_object_storage
description: Upload local files to Qiniu object storage and return public or signed delivery links.
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"],"env":["QINIU_ACCESS_KEY","QINIU_SECRET_KEY","QINIU_BUCKET","QINIU_PUBLIC_DOMAIN"]},"primaryEnv":"QINIU_ACCESS_KEY"}}
---

# 七牛对象存储

这个 skill 是纯存储与分发能力，不负责图片或视频生成。

适用场景：

- 已有本地文件，需要上传到对象存储
- 需要返回公网 URL
- 需要生成带时效的私有下载链接

## 使用脚本

- 上传文件并返回公网 URL：`uv run --no-project --python python scripts/python/qiniu/upload_file.py --file <本地文件>`
- 生成私有下载链接：`uv run --no-project --python python scripts/python/qiniu/generate_private_download_url.py --key <对象key> --expires-in 600`

## 输出约定

- 输出 JSON 至少包含：
  - `storage_provider`
  - `bucket`
  - `object_key`
  - `public_url`
  - 可选 `private_url`

## 配置

- OpenClaw 环境变量优先：
  - `QINIU_ACCESS_KEY`
  - `QINIU_SECRET_KEY`
  - `QINIU_BUCKET`
  - `QINIU_PUBLIC_DOMAIN`
- 本地调试回退：`api_key/qiniu.json`

## 协作方式

- 它通常是图片/视频工作流的后处理步骤
- 当用户只要求上传已有文件时，也可以直接单独调用
- 它不应决定前置内容由哪个 AI 供应商生成
