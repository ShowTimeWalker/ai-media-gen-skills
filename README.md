# AI Media Skills

基于 Claude Code 的 AI 多媒体创作技能集，覆盖从创意策划、内容生成、后期编辑到交付上线的完整工作流。

## Skills

| 技能 | 说明 |
|---|---|
| **content-generation-workflow** | 统一内容生成工作流，编排图片、视频、音乐等多种内容的生成与交付 |
| **short-video-script-master** | 剧本创作大师，通过结构化对话引导完成核心框架定调和故事创作 |
| **video-prompt-craft** | 引导用户逐步写出专业的 AI 视频生成提示词 |
| **doubao-all-in-one** | 使用豆包（火山引擎）生成图片或视频 |
| **juzi-image-video-generation** | 使用橘子 AI 生成图片或视频 |
| **tianpuyue-music** | 使用天谱乐 AI 生成纯音乐、歌曲或歌词 |
| **ffmpeg-multimedia-editing** | 使用 FFmpeg 进行视频剪辑、拼接、转码、音频处理等 20 种操作 |
| **qiniu-object-storage** | 上传文件到七牛对象存储，返回可交付的下载链接 |

## 典型工作流

```
剧本创作 → 视频提示词 → AI 生图/生视频 → AI 生音乐 → FFmpeg 后期 → 上传交付
```

## 模型供应商

| 供应商 | 用途 | 官网 |
|---|---|---|
| 豆包（火山引擎） | 图片生成、视频生成 | [火山引擎](https://www.volcengine.com/docs/82379/1399008?lang=zh) |
| 橘子 AI | 图片生成、视频生成 | [橘子 AI](https://www.juziaigc.com/) |
| 天谱乐 | 音乐生成、歌曲生成、歌词创作 | [天谱乐](https://platform.tianpuyue.cn/home) |
| 七牛云 | 对象存储、文件分发 | [七牛云](https://www.qiniu.com/) |

## 使用

需要 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 并接入大模型提供商（推荐以下两家，与内容生成供应商独立）：

| 大模型提供商 | 官网 |
|---|---|
| 智谱 AI（GLM） | [open.bigmodel.cn](https://open.bigmodel.cn) |
| MiniMax | [platform.minimaxi.com](https://platform.minimaxi.com) |

## docs 目录

存放各内容生成供应商的官方 API 文档离线副本，供开发参考：

| 目录 | 说明 |
|---|---|
| doubao-api-docs | 豆包（火山引擎）API 文档 |
| hailuo-video | 海螺视频 API 文档 |
| juzi | 橘子 AI API 文档 |
| tianpule | 天谱乐 API 文档 |
| openclaw-skills | OpenClaw 技能开发文档 |
| openclaw-workspace | OpenClaw 工作空间文档 |

## 许可

MIT
