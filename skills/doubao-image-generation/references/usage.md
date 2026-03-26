# 使用说明

## 适用范围

`doubao-image-generation` 只负责：

1. 调用豆包图片生成接口
2. 调用豆包图片编辑接口
3. 将结果保存到本地

它不负责：

- 视频生成
- 对象存储上传
- 返回公网 URL
- 工作流编排

## 运行方式

从项目根目录执行：

```powershell
uv run --no-project --python python scripts/python/doubao/text_to_image.py --prompt "..."
uv run --no-project --python python scripts/python/doubao/image_to_image.py --image resources/images/climb1.jpeg --prompt "..."
```

## 输出约定

- 文生图目录：`outputs/doubao/images/text_to_image/`
- 图生图目录：`outputs/doubao/images/image_to_image/`
- 输出字段：
  - `provider=doubao`
  - `scene`
  - `used_model`
  - `local_path`

## 环境变量

- `ARK_API_KEY`

本地调试时仍可从 `api_key/doubao.json` 回退读取。

## 与其他 skill 的关系

- 若需要交付 URL，应再调用 `qiniu_object_storage`
- 若用户只表达“帮我生成图片”而未指定供应商，优先由工作流或 `media-gen` Agent 决定是否命中本 skill
