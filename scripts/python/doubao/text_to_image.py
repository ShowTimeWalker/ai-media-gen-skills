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

from common import create_client, default_output_path, generate_image_with_fallback, save_image_payload

DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_PROMPT = (
    "充满活力的特写编辑肖像，模特眼神锐利，头戴雕塑感帽子，"
    "色彩拼接丰富，眼部焦点锐利，景深较浅，具备 Vogue 杂志封面的美学风格，"
    "采用中画幅拍摄，工作室灯光效果强烈。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="豆包文生图测试脚本")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="文生图提示词")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="首选模型 ID")
    parser.add_argument("--size", default="2K", help="输出尺寸，默认 2K")
    parser.add_argument(
        "--output",
        type=Path,
        help="输出文件路径，默认写入 outputs/doubao/images/text_to_image/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client()
    output_path = args.output or default_output_path("images", "text_to_image")

    response, used_model = generate_image_with_fallback(
        client,
        model=args.model,
        prompt=args.prompt,
        size=args.size,
        response_format="b64_json",
        watermark=False,
    )

    saved_path = save_image_payload(response.data[0], output_path)
    result = {
        "type": "image",
        "scene": "text_to_image",
        "provider": "doubao",
        "used_model": used_model,
        "local_path": str(saved_path),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
