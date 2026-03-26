# 使用说明

## 目录假设

当前 skill 默认位于：

`skills/juzi_image_video_generation/`

skill 内脚本会按当前项目目录结构推导这些路径：

- `api_key/juzi.json`
- `api_key/qiniu.json`
- `outputs/juzi/images/`
- `outputs/juzi/videos/`
- `skills/juzi_image_video_generation/scripts/`

如果你移动了 skill 目录，先检查脚本中的路径推导逻辑是否仍然成立。

## OpenClaw 配置方式

`SKILL.md` 已声明：

- `metadata.openclaw.requires.bins = ["uv"]`
- `metadata.openclaw.requires.anyBins = ["python", "python3", "py"]`
- `metadata.openclaw.requires.env = ["JUZI_API_KEY", "QINIU_ACCESS_KEY", "QINIU_SECRET_KEY", "QINIU_BUCKET", "QINIU_PUBLIC_DOMAIN"]`
- `metadata.openclaw.primaryEnv = "JUZI_API_KEY"`

推荐在 `~/.openclaw/openclaw.json` 中这样配置：

```json
{
  "skills": {
    "entries": {
      "juzi_image_video_generation": {
        "enabled": true,
        "env": {
          "JUZI_API_KEY": "YOUR_JUZI_API_KEY",
          "QINIU_ACCESS_KEY": "YOUR_QINIU_ACCESS_KEY",
          "QINIU_SECRET_KEY": "YOUR_QINIU_SECRET_KEY",
          "QINIU_BUCKET": "noah-ai-generate",
          "QINIU_PUBLIC_DOMAIN": "http://your-download-domain"
        }
      }
    }
  }
}
```

OpenClaw 会在每次 agent run 开始时，把这些值注入到进程环境。

## 当前脚本的回退行为

当前脚本读取配置的顺序是：

1. OpenClaw 注入的环境变量
2. `api_key/juzi.json` 或 `api_key/qiniu.json`

第二项只是当前项目里的本地调试回退，不是 OpenClaw 规范下的首选方式。

## 输出策略

- 图片默认下载到 `outputs/juzi/images/`
- 视频默认下载到 `outputs/juzi/videos/`
- 七牛对象 key 默认写入：
  - `juzi/images/...`
  - `juzi/videos/...`
- 默认返回 10 分钟有效的分享链接

## 运行建议

- 一律使用 `uv run --no-project --python python`
- 如果用户已经提供 `juzi_id`，优先使用状态查询脚本，不要重复创建任务
- 如果空间是公开空间，时效链接只是“可分享链接”；如果需要真正过期失效，应切回私有空间
- 如果在 OpenClaw 中更新了 `SKILL.md` 或 `openclaw.json`，新开一个 session 再测试，确保技能快照刷新
