---
name: doubao-all-in-one
description: 使用豆包（火山引擎 Ark）生成图片或视频，将结果保存到本地。当用户提到"豆包生图""豆包图片""豆包生视频""豆包视频""Doubao""Seedance""火山引擎图片""火山引擎视频""即梦视频""即梦""Jimeng"时引用。
metadata:
  openclaw:
    requires:
      bins:
        - uv
      anyBins:
        - python
        - python3
        - py
      env:
        - ARK_API_KEY
        - OUTPUT_ROOT
    primaryEnv: ARK_API_KEY
    pythonDeps:
      - "volcengine-python-sdk[ark]"
---

# 豆包图片与视频生成

这个 skill 提供豆包（火山引擎 Ark）的图片生成和视频生成能力，结果保存到本地。

适用场景：

- 用户明确指定使用豆包生成图片或视频
- 需要文生图、图生图、文生视频、首帧图生视频等

脚本位于 skill 目录内的 `scripts/`，运行时始终使用绝对路径。

设 `DOUBAO_SKILL_DIR` 为 `.claude/skills/doubao-all-in-one` 的绝对路径：

### 图片

- 文生图：`uv run python $DOUBAO_SKILL_DIR/scripts/text_to_image.py`
- 图生图：`uv run python $DOUBAO_SKILL_DIR/scripts/image_to_image.py`

### 视频

- 创建视频任务：`uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py`
- 查询视频任务：`uv run python $DOUBAO_SKILL_DIR/scripts/query_video_task.py`
- 批量查询任务：`uv run python $DOUBAO_SKILL_DIR/scripts/list_video_tasks.py`
- 取消/删除任务：`uv run python $DOUBAO_SKILL_DIR/scripts/delete_video_task.py`
- 下载视频：`uv run python $DOUBAO_SKILL_DIR/scripts/download_video.py`
- Webhook 回调服务器：`uv run python $DOUBAO_SKILL_DIR/scripts/webhook_server.py`

### 即梦 3.0 视频

- 创建即梦视频任务：`uv run python $DOUBAO_SKILL_DIR/scripts/create_jimeng_video.py`
- 查询即梦视频任务：`uv run python $DOUBAO_SKILL_DIR/scripts/query_jimeng_video.py`

---

## 快速调用

### 文生图

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/text_to_image.py \
  --prompt "一张电影感写实人像海报，光影强烈，构图干净" \
  --name "写实人像海报"
```

### 图生图

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/image_to_image.py \
  --image resources/images/climb1.jpeg \
  --prompt "保留主体动作，改为日落暖光的写实摄影风格" \
  --name "日落暖光人像"
```

### 文生视频（创建 + 轮询 + 下载一步完成）

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py \
  --prompt "写实风格，晴朗的蓝天之下，一大片白色的雏菊花田，镜头逐渐拉近，最终定格在一朵雏菊花的特写上，花瓣上有几颗晶莹的露珠" \
  --name "雏菊花田特写" \
  --ratio 16:9 --duration 5 --poll
```

### 首帧图生视频

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py \
  --prompt "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头" \
  --name "女孩抱狐狸" \
  --first-frame-url "https://example.com/first_frame.png" \
  --ratio adaptive --duration 5 --poll
```

### 首帧+尾帧图生视频

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py \
  --prompt "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头" \
  --name "女孩抱狐狸" \
  --first-frame-url "https://example.com/first_frame.png" \
  --last-frame-url "https://example.com/last_frame.png" \
  --ratio adaptive --duration 5 --poll
```

### 仅创建任务（异步工作流场景）

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py \
  --prompt "小猫对着镜头打哈欠" --name "猫咪打哈欠" --ratio 16:9 --duration 5
```

### 创建任务 + Webhook 回调（替代轮询）

```shell
# 先启动 Webhook 服务器
uv run python $DOUBAO_SKILL_DIR/scripts/webhook_server.py

# 再创建任务，传入回调地址（不传则自动检测本机 8888 端口）
uv run python $DOUBAO_SKILL_DIR/scripts/create_video_task.py \
  --prompt "小猫对着镜头打哈欠" --name "猫咪打哈欠" --ratio 16:9 --duration 5
```

### 即梦文生视频（720p）

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_jimeng_video.py \
  --prompt "写实风格，晴朗的蓝天之下，一大片白色的雏菊花田，镜头逐渐拉近，最终定格在一朵雏菊花的特写上" \
  --name "雏菊花田特写" --poll
```

### 即梦文生视频（1080p）

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_jimeng_video.py \
  --prompt "写实风格，晴朗的蓝天之下，一大片白色的雏菊花田，镜头逐渐拉近" \
  --name "雏菊花田特写" --resolution 1080p --poll
```

### 即梦首帧图生视频

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_jimeng_video.py \
  --prompt "女孩睁开眼，温柔地看向镜头" \
  --name "女孩睁眼" \
  --first-frame-url "https://example.com/first_frame.png" --poll
```

### 即梦首帧+尾帧图生视频

```shell
uv run python $DOUBAO_SKILL_DIR/scripts/create_jimeng_video.py \
  --prompt "女孩从睡梦中慢慢醒来，睁开眼睛" \
  --name "女孩醒来" \
  --first-frame-url "https://example.com/first_frame.png" \
  --last-frame-url "https://example.com/last_frame.png" --poll
```

---

## 图片输入与输出

### 输入

| 参数 | 说明 | 文生图 | 图生图 |
|------|------|--------|--------|
| `--prompt` | 提示词 | 是 | 是 |
| `--name` | 文件名描述（不超过 10 个中文字） | 否 | 否 |
| `--model` | 模型 ID，默认 `doubao-seedream-5-0-260128` | 否 | 否 |
| `--image` | 输入图片路径或 URL，可多次传 | - | 是 |
| `--size` | 输出尺寸：2K / 3K / 4K / 2048x2048，默认 2K | 否 | 否 |
| `--response-format` | 返回格式：b64_json / url，默认 b64_json | 否 | 否 |
| `--output-format` | 输出文件格式：png / jpeg（仅 5.0 lite） | 否 | 否 |
| `--guidance-scale` | 文本权重，范围 [1, 10]（仅 3.0 系列） | 否 | 否 |
| `--watermark` | 添加水印 | 否 | 否 |
| `--sequential-image-generation` | 组图模式：auto / disabled，默认 disabled | 否 | 否 |
| `--max-images` | 组图最大数量，范围 [1, 15]，默认 15 | 否 | 否 |
| `--optimize-prompt` | 提示词优化：standard / fast（仅 5.0 lite/4.5/4.0） | 否 | 否 |
| `--web-search` | 启用联网搜索（仅 5.0 lite） | 否 | 否 |
| `--output` | 输出文件路径 | 否 | 否 |

### 本地输出目录

所有路径相对于 `OUTPUT_ROOT`（由环境变量注入，兜底为用户主目录）：

- `outputs/doubao/images/text_to_image/`
- `outputs/doubao/images/image_to_image/`

### 脚本输出 JSON

```json
{
  "type": "image",
  "scene": "text_to_image",
  "provider": "doubao",
  "used_model": "doubao-seedream-5-0-260128",
  "local_path": "outputs/doubao/images/text_to_image/20260330_120000.png",
  "image_count": 1,
  "generated_images": 1,
  "usage": {"generated_images": 1, "output_tokens": 0, "total_tokens": 0}
}
```

---

## 视频输入与输出

### 输入

| 参数 | 说明 | 必需 |
|------|------|------|
| `--prompt` | 提示词 | 是 |
| `--name` | 文件名描述（不超过 10 个中文字） | 否 |
| `--model` | 模型 ID，默认 `doubao-seedance-1-5-pro-251215` | 否 |
| `--first-frame-url` | 首帧图片 URL 或本地路径 | 否 |
| `--last-frame-url` | 尾帧图片 URL 或本地路径 | 否 |
| `--ratio` | 宽高比：16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive | 否，默认 16:9 |
| `--duration` | 视频时长（秒）：2~12（1.5 pro 支持 -1 由模型自选） | 否，默认 5 |
| `--resolution` | 分辨率：480p, 720p, 1080p（1.0 lite 参考图不支持 1080p） | 否，默认 480p |
| `--seed` | 随机种子，范围 [-1, 2^32-1] | 否 |
| `--frames` | 视频帧数，格式 25+4n，范围 [29, 289]（1.5 pro 暂不支持） | 否 |
| `--generate-audio` | 生成有声视频（仅 1.5 pro，API 默认 true） | 否 |
| `--watermark` | 添加水印 | 否 |
| `--camera-fixed` | 固定摄像头（参考图场景不支持） | 否 |
| `--return-last-frame` | 返回视频尾帧图像（可用于连续视频拼接） | 否 |
| `--draft` | 生成样片（仅 1.5 pro，固定 480p，不支持离线） | 否 |
| `--execution-expires-after` | 任务超时秒数，范围 [3600, 259200]，默认 172800（48h） | 否 |
| `--service-tier` | 推理模式：default（在线）/ flex（离线，50% 价格） | 否 |
| `--poll` | 创建后自动轮询直到完成并下载 | 否 |
| `--poll-interval` | 轮询间隔秒数，默认 10 | 否 |
| `--timeout` | 轮询超时秒数，默认 900 | 否 |
| `--callback-url` | Webhook 回调地址；不传时自动检测 | 否 |

### 本地输出目录

所有路径相对于 `OUTPUT_ROOT`（由环境变量注入，兜底为用户主目录）：

- `outputs/doubao/videos/text_to_video/`
- `outputs/doubao/videos/first_frame_to_video/`
- `outputs/doubao/videos/first_last_frame_to_video/`

### 视频脚本输出 JSON

创建任务返回：
```json
{
  "type": "video",
  "scene": "text_to_video",
  "provider": "doubao",
  "task_id": "cgt-2025xxxx",
  "status": "queued"
}
```

轮询完成并下载后返回：
```json
{
  "type": "video",
  "scene": "text_to_video",
  "provider": "doubao",
  "task_id": "cgt-2025xxxx",
  "used_model": "doubao-seedance-1-5-pro-251215",
  "local_path": "outputs/doubao/videos/text_to_video/20260330_120000_cgt-xxx.mp4",
  "source_url": "https://...",
  "resolution": "480p",
  "ratio": "16:9",
  "duration": 5
}
```

查询任务返回：
```json
{
  "task_id": "cgt-2025xxxx",
  "model": "doubao-seedance-1-5-pro-251215",
  "status": "succeeded",
  "created_at": 1743300000,
  "updated_at": 1743300120,
  "video_url": "https://...",
  "last_frame_url": "https://...",
  "resolution": "480p",
  "ratio": "16:9",
  "duration": 5,
  "seed": 12345,
  "generate_audio": true,
  "draft": false,
  "service_tier": "default",
  "execution_expires_after": 172800,
  "usage": {"completion_tokens": 100, "total_tokens": 100}
}
```

---

## 模型选择

### 图片模型

| 模型 | Model ID | 特点 |
|------|----------|------|
| Seedream 5.0 | `doubao-seedream-5-0-260128` | 默认首选 |
| Seedream 4.5 | `doubao-seedream-4-5-251128` | 额度不足时自动 fallback |

### 视频模型

| 模型 | Model ID | 特点 |
|------|----------|------|
| Seedance 1.5 Pro | `doubao-seedance-1-5-pro-251215` | 最高质量，支持有声视频、样片模式、返回尾帧、4~12秒 |

### 即梦 3.0 视频模型

| 模式 | 分辨率 | req_key | 特点 |
|------|--------|---------|------|
| 文生视频 | 720p | `jimeng_t2v_v30` | 默认首选 |
| 文生视频 | 1080p | `jimeng_t2v_v30_1080p` | 高清渲染 |
| 首帧图生视频 | 720p | `jimeng_i2v_first_v30` | 宽高比由图片决定 |
| 首帧图生视频 | 1080p | `jimeng_i2v_first_v30_1080` | 高清渲染 |
| 首尾帧图生视频 | 720p | `jimeng_i2v_first_tail_v30` | 尾帧需与首帧比例一致 |
| 首尾帧图生视频 | 1080p | `jimeng_i2v_first_tail_v30_1080` | 高清渲染 |

---

## 提示词最佳实践

调用生成脚本前，**默认**读取 `references/prompt_best_practices.md` 并审核优化用户提示词。用户明确指定"不优化""直接生成""跳过优化"时跳过。

| 场景 | 参考文档 | 核心公式 |
|------|----------|----------|
| 图片生成（Seedream） | `references/seedream_prompt_guide.md` | 主体 + 行为 + 环境 + 风格/光影/构图 |
| 视频生成（Seedance） | `references/seedance_1_5_pro_prompt_guide.md` | 主体 + 运动 + 环境 + 运镜/切镜 + 美学 + 声音 |
| 视频生成（即梦 3.0） | `references/jimeng_3_0_prompt_guide.md` | 主体 + 运动 + 环境 + 运镜/切镜 + 美学（无声音） |

完整规则（检查清单、拒绝条件、自动补充策略等）见 `references/prompt_best_practices.md`。

---

## 配置

- 环境变量：`ARK_API_KEY`（Seedance 视频和图片生成必需，未设置时直接报错）
- 环境变量：`OUTPUT_ROOT`（可选，输出根目录，支持 `~` 展开，默认为用户主目录）
- 即梦 3.0 凭据：从 `api_key/jimeng.json` 读取 `access_key` 和 `secret_key`（也可通过环境变量 `VOLC_ACCESS_KEY` / `VOLC_SECRET_KEY` 覆盖）

## 协作方式

- 图片生成可直接完成任务
- 视频生成使用 `--poll` 模式可直接完成任务；异步工作流可分步操作
- Webhook 模式：先启动 `webhook_server.py`（默认端口 8888），创建任务时自动检测回调地址（优先级：手动 `--callback-url` > 环境变量 `VIDEO_CALLBACK_BASE_URL` > 自动检测本机 IP + 8888 端口）
- 如果用户还需要公网链接或临时下载链接，应由后续的交付环节继续处理
