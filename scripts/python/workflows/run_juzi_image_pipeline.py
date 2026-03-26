# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PYTHON_DIR = CURRENT_DIR.parent

if str(PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIR))

from juzi.common import (  # type: ignore[import-not-found]
    create_image_task,
    default_output_path,
    download_file,
    extract_image_result_url,
    wait_for_image_task,
)

DEFAULT_MODEL = "nano-banana-fast"
DEFAULT_PROMPT = "一只戴着飞行员护目镜的哈士奇，写实风格，背景简洁。"
DEFAULT_RATIO = "1:1"
DEFAULT_POLL_INTERVAL = 5
DEFAULT_TIMEOUT = 120


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Juzi 图片生成并下载到本地")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="图片模型")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="提示词")
    parser.add_argument("--ratio", default=DEFAULT_RATIO, help="图片比例")
    parser.add_argument("--quality", help="输出质量，可选")
    parser.add_argument("--url", action="append", dest="urls", help="参考图 URL，可传多次")
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=DEFAULT_POLL_INTERVAL,
        help="轮询间隔秒数，默认 5",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="超时秒数，默认 120",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    create_response = create_image_task(
        model=args.model,
        prompt=args.prompt,
        ratio=args.ratio,
        urls=args.urls,
        quality=args.quality,
    )
    juzi_id = str(create_response["data"]["juzi_id"])
    print(f"图片任务已创建: {juzi_id}")

    final_response = wait_for_image_task(
        juzi_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    result_url = extract_image_result_url(final_response)
    local_path = default_output_path("images", juzi_id, result_url, ".png")
    download_file(result_url, local_path)

    result = {
        "type": "image",
        "juzi_id": juzi_id,
        "local_path": str(local_path),
        "source_url": result_url,
        "final_response": final_response,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
