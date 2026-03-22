# 使用说明

## 目录假设

这个 skill 默认放在当前项目的：

`skills/doubao-image-generation/`

脚本通过相对路径推导项目根目录，因此依赖以下目录约定：

- `api_key/doubao.json`
- `resources/images/`
- `outputs/doubao/`
- `skills/doubao-image-generation/scripts/`

如果你把 skill 挪到别的位置，需要同步调整脚本中的 `PROJECT_ROOT` 推导逻辑。

## 模型策略

首选模型和降级顺序如下：

1. `doubao-seedream-5-0-260128`
2. `doubao-seedream-4-5-251128`
3. `doubao-seedream-4-0-250828`

只有在错误信息表现为额度不足、余额不足、credit/quota/resource exhausted 等情况时，才会自动降级。

## 输出策略

- 默认关闭水印
- 文生图输出到 `outputs/doubao/text_to_image/`
- 图生图输出到 `outputs/doubao/image_to_image/`
- 默认文件名使用时间戳

## 运行建议

- 一律使用 `uv run --project <项目根目录>`
- 缺依赖时优先使用 `uv add`
- 如果 VSCode 提示缺包，确认解释器已切到项目 `.venv`
