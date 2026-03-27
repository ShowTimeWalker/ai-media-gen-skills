---
name: image_generation_workflow
description: Coordinate image generation and default delivery without binding to a specific AI or storage provider.
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"]}}}
---

# 图片生成工作流

这个 skill 是协调入口，不绑定具体 AI 供应商，也不绑定具体对象存储供应商。

适用场景：

- 用户表达“生成一张图片”
- 用户需要最终可访问的图片结果
- 用户未明确指定供应商，需要由多媒体内容生成 Agent 按预设选择

## 默认行为

当用户表达图片生成需求时，默认完成态是“返回可访问图片结果”：

1. 由多媒体内容生成 Agent 选择图片生成供应商
2. 生成图片并保存到本地
3. 默认进入对象存储分发步骤
4. 返回可访问链接

## 用户覆盖

以下情况应覆盖默认行为：

- 用户明确指定图片供应商
- 用户明确指定对象存储供应商
- 用户明确要求“只保存本地”
- 用户明确要求“不要上传”
- 用户明确要求临时下载链接而不是公网链接

## 实施方式

- 供应商选择、降级、失败重试由 `media-gen` Agent 负责
- 具体生成由 provider skill 负责，例如 `doubao-image-generation` 或 `juzi_image_video_generation`
- 具体分发由对象存储 skill 负责，例如 `qiniu_object_storage`
