# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
from pathlib import Path

from doubao_common import (
    create_client,
    default_output_path,
    generate_image_with_fallback,
    save_image_payload,
)

DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_PROMPT = (
    "一张写实风格的户外品牌海报，主体清晰，光影干净，构图完整，"
    "具有广告摄影质感，细节丰富，画面自然。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="豆包文生图脚本")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="文生图提示词")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="首选模型 ID")
    parser.add_argument("--size", default="2K", help="输出尺寸，默认 2K")
    parser.add_argument(
        "--output",
        type=Path,
        help="输出文件路径，默认写入 outputs/doubao/text_to_image/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client()
    output_path = args.output or default_output_path("text_to_image")

    response, used_model = generate_image_with_fallback(
        client,
        model=args.model,
        prompt=args.prompt,
        size=args.size,
        response_format="b64_json",
        watermark=False,
    )

    saved_path = save_image_payload(response.data[0], output_path)
    print(f"使用模型: {used_model}")
    print(f"已保存到: {saved_path}")


if __name__ == "__main__":
    main()
