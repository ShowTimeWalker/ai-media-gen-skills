# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import (
    PROJECT_ROOT,
    build_common_payload,
    create_video_task,
    default_output_path,
    download_video,
    resolve_image_source,
    wait_for_task,
)

DEFAULT_MODEL = "S2V-01"
DEFAULT_PROMPT = "保持人物主体一致，人物朝镜头微笑并自然眨眼，动作轻微，镜头稳定。"
DEFAULT_SUBJECT_IMAGE = PROJECT_ROOT / "resources" / "images" / "climb1.jpeg"


def str_to_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"无法识别的布尔值: {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="海螺角色专注视频测试脚本")
    parser.add_argument(
        "--subject-image",
        default=str(DEFAULT_SUBJECT_IMAGE),
        help="主体参考图路径、URL 或 Data URL",
    )
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="视频提示词")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型 ID，默认 S2V-01")
    parser.add_argument(
        "--prompt-optimizer",
        type=str_to_bool,
        default=True,
        help="是否启用提示词优化，默认 true",
    )
    parser.add_argument(
        "--aigc-watermark",
        type=str_to_bool,
        default=False,
        help="是否添加 AIGC 水印，默认 false",
    )
    parser.add_argument("--poll-interval", type=int, default=10, help="轮询间隔秒数，默认 10")
    parser.add_argument("--timeout", type=int, default=900, help="任务超时秒数，默认 900")
    parser.add_argument(
        "--output",
        type=Path,
        help="输出文件路径，默认写入 outputs/hailuo/subject_reference_to_video/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_common_payload(args)
    payload["subject_reference"] = [
        {
            "type": "character",
            "image": [resolve_image_source(args.subject_image)],
        }
    ]
    output_path = args.output or default_output_path("subject_reference_to_video")

    print(f"使用模型: {args.model}")
    print(
        "请求参数: "
        + json.dumps(
            {
                **payload,
                "subject_reference": [{"type": "character", "image": ["<image>"]}],
            },
            ensure_ascii=False,
        )
    )
    task_id = create_video_task(payload)
    print(f"任务已创建: {task_id}")

    task_result = wait_for_task(
        task_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    file_id = str(task_result["file_id"])
    print(f"任务成功，file_id: {file_id}")

    saved_path = download_video(file_id, output_path)
    print(f"已保存到: {saved_path}")


if __name__ == "__main__":
    main()
