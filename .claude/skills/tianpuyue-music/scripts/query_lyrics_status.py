# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json

from common import query_lyrics_task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查询天谱乐歌词任务状态")
    parser.add_argument("--item-id", required=True, help="作品 ID")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    item = query_lyrics_task(args.item_id)
    print(json.dumps(item, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
