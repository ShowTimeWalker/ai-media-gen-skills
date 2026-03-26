# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse

from juzi_common import pretty_json, query_image_task


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="橘子图片进度查询测试脚本")
    parser.add_argument("--juzi-id", required=True, help="图片任务 juzi_id")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(pretty_json(query_image_task(args.juzi_id)))


if __name__ == "__main__":
    main()
