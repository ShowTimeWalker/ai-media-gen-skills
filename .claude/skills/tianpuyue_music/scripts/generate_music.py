# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json

from common import (
    PROJECT_ROOT,
    create_music_task,
    default_output_path,
    download_file,
    extract_audio_url,
    pretty_json,
    wait_for_music_task,
)

DEFAULT_MODEL = "TemPolor i3.5"
DEFAULT_PROMPT = (
    "Genre: Electronic Dance Music (EDM), House, Techno\n"
    "Style: Instrumental, Beat-driven, Club-oriented\n"
    "Mood: Energetic, Vibrant, Hypnotic"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="天谱乐纯音乐生成并下载到本地")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="音乐描述提示词")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名称")
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=15,
        help="轮询间隔秒数，默认 15",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="超时秒数，默认 900",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    create_response = create_music_task(prompt=args.prompt, model=args.model)
    item_id = create_response["data"]["item_ids"][0]
    print(f"纯音乐任务已创建: {item_id}")

    item = wait_for_music_task(
        item_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    audio_url = extract_audio_url(item)
    local_path = default_output_path("music", item_id, ".mp3")
    download_file(audio_url, local_path)

    result = {
        "type": "music",
        "provider": "tianpuyue",
        "item_id": item_id,
        "local_path": str(local_path.relative_to(PROJECT_ROOT)),
        "source_url": audio_url,
        "title": item.get("title", ""),
        "style": item.get("style", ""),
        "duration": item.get("duration"),
        "model": item.get("model", ""),
        "task_info": item,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
