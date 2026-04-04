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

## 输出目录

所有生成的文件统一输出到 `OUTPUT_ROOT/outputs/` 下：

```
outputs/
├── doubao/images/          # 豆包图片
├── doubao/videos/          # 豆包视频
├── juzi/images/            # 橘子图片
├── juzi/videos/            # 橘子视频
├── tianpuyue/music/        # 天谱乐纯音乐
├── tianpuyue/songs/        # 天谱乐歌曲
├── tianpuyue/lyrics/       # 天谱乐歌词
├── ffmpeg/<operation>/     # FFmpeg 处理结果
├── logs/                   # 运行日志
└── scripts/<project>/      # 工作流产出
```

## 环境变量

> API 密钥仅需在**使用对应功能时**配置，无需全部填写。

### 全局

| 变量 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `OUTPUT_ROOT` | 否 | `~`（用户主目录） | 输出根目录 |

### 豆包（火山引擎）— 使用豆包生图/生视频时需要

| 变量 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `ARK_API_KEY` | 是 | — | 火山引擎 Ark API 密钥 |

### 橘子 AI — 使用橘子生图/生视频时需要

| 变量 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `JUZI_API_KEY` | 是 | — | 橘子 AI API 密钥 |

### 天谱乐 — 使用天谱乐生成音乐/歌曲/歌词时需要

| 变量 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `TIANPUYUE_API_KEY` | 是 | — | 天谱乐 API 密钥 |
| `TIANPUYUE_CALLBACK_URL` | 否 | `https://example.com/callback` | 回调地址（轮询模式下可用占位值） |

### 七牛对象存储 — 使用七牛上传/交付时需要

| 变量 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `QINIU_ACCESS_KEY` | 是 | — | 七牛 Access Key |
| `QINIU_SECRET_KEY` | 是 | — | 七牛 Secret Key |
| `QINIU_BUCKET` | 是 | — | 存储空间名称 |
| `QINIU_PUBLIC_DOMAIN` | 是 | — | 公网访问域名 |
| `QINIU_IS_PRIVATE` | 否 | `false` | 是否为私有空间 |

### FFmpeg — 无需 API 密钥

仅需在系统 PATH 中安装 FFmpeg 和 ffprobe（full build 8.1+）。

## 许可

MIT
