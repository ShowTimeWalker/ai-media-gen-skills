# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse

from common import create_image_task, pretty_json

DEFAULT_MODEL = "nano-banana-2"
DEFAULT_PROMPT = "一只戴着飞行员护目镜的柴犬，3D卡通风格，背景简洁。"
DEFAULT_RATIO = "1:1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="橘子图片生成测试脚本")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名称")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="提示词")
    parser.add_argument("--ratio", default=DEFAULT_RATIO, help="图片比例，默认 1:1")
    parser.add_argument("--quality", help="输出质量，可选")
    parser.add_argument(
        "--url",
        action="append",
        dest="urls",
        help="参考图 URL，可传多次",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    response = create_image_task(
        model=args.model,
        prompt=args.prompt,
        ratio=args.ratio,
        urls=args.urls,
        quality=args.quality,
    )
    print(pretty_json(response))


if __name__ == "__main__":
    main()
