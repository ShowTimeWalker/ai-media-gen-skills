# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
import json

from common import create_client, query_video_task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查询豆包 Seedance 视频任务状态")
    parser.add_argument("--task-id", required=True, help="视频任务 ID（cgt-xxxx）")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client()

    result = query_video_task(client, args.task_id)
    status = result.get("status", "unknown")
    content = result.get("content", {})

    output = {
        "task_id": args.task_id,
        "status": status,
    }

    if status == "succeeded":
        video_url = ""
        if isinstance(content, dict):
            video_url = content.get("video_url", "")
        else:
            video_url = getattr(content, "video_url", "")
        output["video_url"] = str(video_url)
        output["model"] = result.get("model", "")
        output["duration"] = result.get("duration", "")
        output["ratio"] = result.get("ratio", "")
        output["resolution"] = result.get("resolution", "")
    elif status == "failed":
        output["error"] = result.get("error", {})

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
