# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import PROJECT_ROOT, default_output_path, download_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="下载豆包 Seedance 视频到本地")
    parser.add_argument("--url", required=True, help="视频下载 URL")
    parser.add_argument("--output", help="输出文件路径，默认写入 outputs/doubao/videos/")
    parser.add_argument("--scene", default="text_to_video", help="场景子目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = default_output_path("videos", args.scene, suffix=".mp4")

    download_file(args.url, output_path)

    result = {
        "type": "video",
        "provider": "doubao",
        "local_path": str(output_path.relative_to(PROJECT_ROOT)),
        "source_url": args.url,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
