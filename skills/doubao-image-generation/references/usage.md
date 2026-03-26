# 使用说明

## 适用范围

`doubao-image-generation` 只负责两件事：

1. 调用豆包图片生成或编辑接口。
2. 将生成结果上传到七牛并返回图片 URL。

它不负责视频生成，也不负责通用文件管理。

## 运行方式

从项目根目录执行：

```powershell
uv run --no-project --python python scripts/python/doubao/text_to_image.py --prompt "..."
uv run --no-project --python python scripts/python/doubao/image_to_image.py --image resources/images/climb1.jpeg --prompt "..."
```

## 目录约定

- 文生图本地文件：`outputs/doubao/images/text_to_image/`
- 图生图本地文件：`outputs/doubao/images/image_to_image/`
- 七牛对象 key 默认映射为 `doubao/images/...`

## 环境变量

- `ARK_API_KEY`
- `QINIU_ACCESS_KEY`
- `QINIU_SECRET_KEY`
- `QINIU_BUCKET`
- `QINIU_PUBLIC_DOMAIN`

本地调试时仍可从 `api_key/doubao.json` 与 `api_key/qiniu.json` 回退读取。
