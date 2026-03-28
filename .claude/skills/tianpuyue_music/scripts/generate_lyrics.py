# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json

from common import (
    PROJECT_ROOT,
    create_lyrics_task,
    default_output_path,
    pretty_json,
    wait_for_lyrics_task,
)

DEFAULT_SONG_MODEL = "TemPolor v4.5"
DEFAULT_PROMPT = (
    "一首关于夏天校园回忆的中文流行歌曲，充满青春和怀旧感"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="天谱乐歌词生成")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="歌词生成的提示文本")
    parser.add_argument("--song-model", default=DEFAULT_SONG_MODEL, help="适配的歌曲模型名称")
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="轮询间隔秒数，默认 10",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="超时秒数，默认 300",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    create_response = create_lyrics_task(
        prompt=args.prompt,
        song_model=args.song_model,
    )
    item_id = create_response["data"]["item_ids"][0]
    print(f"歌词任务已创建: {item_id}")

    item = wait_for_lyrics_task(
        item_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )

    title = item.get("title", "")
    lyric = item.get("lyric", "")

    local_path = default_output_path("lyrics", item_id, ".md")
    local_path.write_text(f"# {title}\n\n{lyric}", encoding="utf-8")

    result = {
        "type": "lyrics",
        "provider": "tianpuyue",
        "item_id": item_id,
        "local_path": str(local_path.relative_to(PROJECT_ROOT)),
        "title": title,
        "lyric": lyric,
        "task_info": item,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
