# 使用说明

## 适用范围

`qiniu_object_storage` 只负责：

- 上传本地文件到七牛
- 返回公网 URL
- 生成带时效的私有下载链接

它不负责任何图片或视频生成。

## 运行方式

```powershell
uv run --no-project --python python scripts/python/qiniu/upload_file.py --file <本地文件>
uv run --no-project --python python scripts/python/qiniu/upload_file.py --file <本地文件> --private-url --expires-in 600
uv run --no-project --python python scripts/python/qiniu/generate_private_download_url.py --key <对象key> --expires-in 600
```

## 对象 key 规则

- 若文件位于 `outputs/` 目录内，优先复用相对路径作为对象 key
- 若文件位于其他目录，可通过 `--key` 明确指定，或通过 `--prefix` 自动生成

## 输出字段

- `storage_provider=qiniu`
- `bucket`
- `object_key`
- `public_url`
- 可选 `private_url`

## 与其他 skill 的关系

- 它通常被图片/视频 workflow 或 `media-gen` Agent 在交付阶段调用
- 它不应决定生成供应商
