# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json
import time

from common import (
    create_video_task,
    default_output_path,
    download_file,
    extract_video_result_url,
    get_trace_id,
    log_params,
    setup_logging,
    wait_for_video_task,
)

setup_logging()

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
    pipeline_start = time.monotonic()
    args = parse_args()
    log_params("视频生成开始", model=args.model, prompt=args.prompt, aspect_ratio=args.aspect_ratio)
    create_response = create_video_task(
        model=args.model,
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        image_urls=args.image_urls,
    )
    juzi_id = str(create_response["data"]["juzi_id"])
    print(f"视频任务已创建: {juzi_id}")
    log_params("视频任务已创建", juzi_id=juzi_id)

    final_response = wait_for_video_task(
        juzi_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    log_params("视频生成成功", juzi_id=juzi_id)
    result_url = extract_video_result_url(final_response)
    local_path = default_output_path("videos", juzi_id, result_url, ".mp4")
    download_file(result_url, local_path)

    total_elapsed = round(time.monotonic() - pipeline_start, 3)
    log_params("视频生成完成", juzi_id=juzi_id, total_elapsed=total_elapsed)
    result = {
        "type": "video",
        "provider": "juzi",
        "juzi_id": juzi_id,
        "local_path": str(local_path),
        "source_url": result_url,
        "final_response": final_response,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
