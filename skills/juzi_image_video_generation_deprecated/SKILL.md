---
name: juzi_image_video_generation_deprecated
description: Deprecated combined Juzi plus Qiniu workflow. Prefer the new juzi_image_video_generation and qiniu_object_storage skills.
user-invocable: false
disable-model-invocation: true
metadata: {"openclaw":{"requires":{"bins":["uv"],"anyBins":["python","python3","py"],"env":["JUZI_API_KEY","QINIU_ACCESS_KEY","QINIU_SECRET_KEY","QINIU_BUCKET","QINIU_PUBLIC_DOMAIN"]},"primaryEnv":"JUZI_API_KEY"}}
---

# 已弃用：橘子图片视频一体化

这个 skill 已废弃，不再作为推荐入口。

## 原因

旧实现同时处理：

- 橘子图片/视频生成
- 本地下载
- 七牛上传
- 七牛分享链接生成

这会把“内容生成”和“对象存储分发”耦合在一起，不利于复用和维护。

## 迁移方式

- 纯生成与状态查询：使用 `juzi_image_video_generation`
- 文件上传与分享链接：使用 `qiniu_object_storage`

如果需要完整链路，应按顺序组合这两个 skill，而不是继续使用这个 deprecated 版本。
