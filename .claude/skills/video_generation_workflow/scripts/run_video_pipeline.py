# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
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
from qiniu.common import (  # type: ignore[import-not-found]
    build_private_download_url,
    build_public_url,
    load_config as load_qiniu_config,
    upload_file,
)

DEFAULT_MODEL = "VEO 3.1 Fast 多参考版"
DEFAULT_PROMPT = "一辆红色跑车在夜晚城市街道中高速穿行，电影感镜头，光影反射明显。"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_IMAGE_URLS = [
    "https://juziai.oss-cn-shenzhen.aliyuncs.com/uploads/20260301/f06aed0cb2ff8e1a131dd9ca6a56c781.png",
    "https://juziai.oss-cn-shenzhen.aliyuncs.com/uploads/20260301/0da76274207a04aae53423a753de15ab.png",
]
DEFAULT_EXPIRES_IN = 600
DEFAULT_POLL_INTERVAL = 15
DEFAULT_TIMEOUT = 900
DEFAULT_OBJECT_PREFIX = "juzi/videos"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="视频生成一键工作流")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="视频模型")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="提示词")
    parser.add_argument("--aspect-ratio", default=DEFAULT_ASPECT_RATIO, help="视频比例")
    parser.add_argument(
        "--image-url",
        action="append",
        dest="image_urls",
        help="参考图 URL，可传多次；默认使用文档示例图",
    )
    parser.add_argument(
        "--no-reference-images",
        action="store_true",
        help="不使用默认参考图",
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
    parser.add_argument(
        "--expires-in",
        type=int,
        default=DEFAULT_EXPIRES_IN,
        help="七牛私有链接有效期秒数，默认 600",
    )
    parser.add_argument(
        "--object-prefix",
        default=DEFAULT_OBJECT_PREFIX,
        help="七牛对象 key 前缀",
    )
    return parser.parse_args()


def build_object_key(prefix: str, juzi_id: str, local_path: Path) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    clean_prefix = prefix.strip("/").replace("\\", "/")
    return f"{clean_prefix}/{juzi_id}-{timestamp}{local_path.suffix}"


def main() -> None:
    args = parse_args()
    image_urls = [] if args.no_reference_images else (
        args.image_urls if args.image_urls is not None else DEFAULT_IMAGE_URLS
    )
    create_response = create_video_task(
        model=args.model,
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        image_urls=image_urls,
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
    print(f"已下载到本地: {local_path}")

    object_key = build_object_key(args.object_prefix, juzi_id, local_path)
    upload_response = upload_file(file_path=local_path, object_key=object_key)
    qiniu_config = load_qiniu_config()
    public_url = build_public_url(qiniu_config["public_domain"], object_key)
    private_url = build_private_download_url(
        access_key=qiniu_config["access_key"],
        secret_key=qiniu_config["secret_key"],
        base_url=public_url,
        expires_in=args.expires_in,
    )

    result = {
        "type": "video",
        "juzi_id": juzi_id,
        "local_path": str(local_path),
        "source_url": result_url,
        "bucket": qiniu_config["bucket"],
        "object_key": object_key,
        "upload_response": upload_response,
        "share_url": private_url,
        "expires_in": args.expires_in,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
