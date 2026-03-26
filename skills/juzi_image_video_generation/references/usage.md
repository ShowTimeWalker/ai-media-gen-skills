# 使用说明

## 适用范围

`juzi_image_video_generation` 只负责橘子侧能力：

- 创建图片任务
- 创建视频任务
- 轮询任务进度
- 下载生成结果到本地

它不负责七牛上传，不生成分享链接。

## 运行方式

```powershell
uv run --no-project --python python scripts/python/workflows/run_juzi_image_pipeline.py --prompt "..."
uv run --no-project --python python scripts/python/workflows/run_juzi_video_pipeline.py --prompt "..."
uv run --no-project --python python scripts/python/juzi/query_image_status.py --juzi-id <ID>
uv run --no-project --python python scripts/python/juzi/query_video_status.py --juzi-id <ID>
```

## 目录约定

- 图片下载目录：`outputs/juzi/images/`
- 视频下载目录：`outputs/juzi/videos/`

## 环境变量

- `JUZI_API_KEY`

本地调试时仍可从 `api_key/juzi.json` 回退读取。
