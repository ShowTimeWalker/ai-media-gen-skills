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
    create_video_task,
    default_output_path,
    download_file,
    extract_video_result_url,
    wait_for_video_task,
)

DEFAULT_MODEL = "VEO 3.1 Fast 多参考版"
DEFAULT_PROMPT = "一辆红色跑车在夜晚城市街道中高速穿行，电影感镜头，光影反射明显。"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_POLL_INTERVAL = 15
DEFAULT_TIMEOUT = 900


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Juzi 视频生成并下载到本地")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="视频模型")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="提示词")
    parser.add_argument("--aspect-ratio", default=DEFAULT_ASPECT_RATIO, help="视频比例")
    parser.add_argument(
        "--image-url",
        action="append",
        dest="image_urls",
        help="参考图 URL，可传多次",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=DEFAULT_POLL_INTERVAL,
        help="轮询间隔秒数，默认 15",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="超时秒数，默认 900",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    create_response = create_video_task(
        model=args.model,
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        image_urls=args.image_urls,
    )
    juzi_id = str(create_response["data"]["juzi_id"])
    print(f"视频任务已创建: {juzi_id}")

    final_response = wait_for_video_task(
        juzi_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    result_url = extract_video_result_url(final_response)
    local_path = default_output_path("videos", juzi_id, result_url, ".mp4")
    download_file(result_url, local_path)

    result = {
        "type": "video",
        "juzi_id": juzi_id,
        "local_path": str(local_path),
        "source_url": result_url,
        "final_response": final_response,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
