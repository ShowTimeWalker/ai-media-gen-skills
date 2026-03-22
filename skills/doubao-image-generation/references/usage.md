# 使用说明

## 目录假设

当前 skill 默认位于：

`skills/doubao-image-generation/`

skill 内脚本会按当前项目目录结构推导这些路径：

- `api_key/doubao.json`
- `resources/images/`
- `outputs/doubao/`
- `skills/doubao-image-generation/scripts/`

如果你移动了 skill 目录，先检查脚本中的路径推导逻辑是否仍然成立。

## OpenClaw 配置方式

`SKILL.md` 已声明：

- `metadata.openclaw.requires.bins = ["uv"]`
- `metadata.openclaw.requires.env = ["ARK_API_KEY"]`
- `metadata.openclaw.primaryEnv = "ARK_API_KEY"`

推荐在 `~/.openclaw/openclaw.json` 中这样配置：

```json
{
  "skills": {
    "entries": {
      "doubao-image-generation": {
        "enabled": true,
        "env": {
          "ARK_API_KEY": "YOUR_ARK_API_KEY"
        }
      }
    }
  }
}
```

如果你使用 OpenClaw 的密钥管理能力，也可以改成：

```json
{
  "skills": {
    "entries": {
      "doubao-image-generation": {
        "enabled": true,
        "apiKey": {
          "source": "env",
          "provider": "default",
          "id": "ARK_API_KEY"
        }
      }
    }
  }
}
```

OpenClaw 会在每次 agent run 开始时，把这里配置的值注入到进程环境中的 `ARK_API_KEY`。

## 当前脚本的回退行为

当前脚本读取密钥的顺序是：

1. `ARK_API_KEY`
2. `api_key/doubao.json`

第二项只是当前项目里的本地调试回退，不是 OpenClaw 规范下的首选方式。

## 模型策略

首选模型和降级顺序如下：

1. `doubao-seedream-5-0-260128`
2. `doubao-seedream-4-5-251128`
3. `doubao-seedream-4-0-250828`

只有在额度不足、余额不足、`credit`、`quota`、`resource exhausted` 等错误时，才会自动降级。

## 输出策略

- 默认关闭新增 AI 水印
- 文生图输出到 `outputs/doubao/text_to_image/`
- 图生图输出到 `outputs/doubao/image_to_image/`
- 默认文件名使用时间戳

## 运行建议

- 一律使用 `uv run --project <项目根目录>`
- 缺依赖时优先使用 `uv add`
- 如果在 OpenClaw 中更新了 `SKILL.md` 或 `openclaw.json`，新开一个 session 再测试，确保技能快照刷新
