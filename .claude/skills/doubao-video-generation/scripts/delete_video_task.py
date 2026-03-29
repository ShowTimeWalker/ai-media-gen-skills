# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
import json

from common import create_client, delete_video_task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="取消或删除豆包 Seedance 视频任务")
    parser.add_argument("--task-id", required=True, help="视频任务 ID（cgt-xxxx）")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client()

    print(f"正在取消/删除任务: {args.task_id}")
    delete_video_task(client, args.task_id)
    print(json.dumps({
        "task_id": args.task_id,
        "status": "deleted",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
