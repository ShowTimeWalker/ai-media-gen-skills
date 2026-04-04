# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse

from common import log_params, pretty_json, query_video_task, setup_logging

setup_logging()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="橘子视频进度查询测试脚本")
    parser.add_argument("--juzi-id", required=True, help="视频任务 juzi_id")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    log_params("查询视频状态", juzi_id=args.juzi_id)
    response = query_video_task(args.juzi_id)
    log_params("查询视频状态完成", juzi_id=args.juzi_id)
    print(pretty_json(response))


if __name__ == "__main__":
    main()
