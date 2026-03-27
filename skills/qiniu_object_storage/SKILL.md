---
name: qiniu_object_storage
description: Upload local files to Qiniu object storage and return delivery links for public or private buckets.
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"],"env":["QINIU_ACCESS_KEY","QINIU_SECRET_KEY","QINIU_BUCKET","QINIU_PUBLIC_DOMAIN","QINIU_IS_PRIVATE"]},"primaryEnv":"QINIU_ACCESS_KEY"}}
---

# 七牛对象存储

这个 skill 只负责文件上传与交付链接，不负责图片或视频生成。

适用场景：

- 已有本地文件，需要上传到七牛
- 需要返回一个可直接交付的下载链接
- 私有空间需要带时效签名链接

## 默认行为

- 如果配置里声明空间是私有的，上传后默认返回签名链接
- 如果配置里声明空间是公开的，上传后默认返回公网链接
- 只有用户明确要求，或脚本显式传 `--private-url` / `--public-url` 时，才覆盖默认行为

## 使用脚本

- 上传文件并按空间配置返回默认交付链接：`uv run --no-project --python python scripts/python/qiniu/upload_file.py --file <本地文件>`
- 强制返回私有签名链接：`uv run --no-project --python python scripts/python/qiniu/upload_file.py --file <本地文件> --private-url --expires-in 600`
- 强制返回公网链接：`uv run --no-project --python python scripts/python/qiniu/upload_file.py --file <本地文件> --public-url`
- 已有对象 key，生成私有签名链接：`uv run --no-project --python python scripts/python/qiniu/generate_private_download_url.py --key <对象key> --expires-in 600`

## 输出约定

- 输出 JSON 至少包含：
  - `storage_provider`
  - `bucket`
  - `object_key`
  - `access_mode`
  - `delivery_url`
- 可能额外包含：
  - `public_url`
  - `private_url`
  - `base_url`
  - `expires_in`

## 配置

- OpenClaw 环境变量优先：
  - `QINIU_ACCESS_KEY`
  - `QINIU_SECRET_KEY`
  - `QINIU_BUCKET`
  - `QINIU_PUBLIC_DOMAIN`
  - `QINIU_IS_PRIVATE`
- 本地调试回退：`api_key/qiniu.json`
- 私有空间建议在配置中声明：`"is_private": true`

## 协作方式

- 它通常是图片或视频 workflow 的交付步骤
- 当用户只要求上传已有文件时，也可以单独调用
- 它不应决定前置内容由哪个 AI 供应商生成
