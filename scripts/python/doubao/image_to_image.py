# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
from pathlib import Path

from common import (
    PROJECT_ROOT,
    create_client,
    default_output_path,
    generate_image_with_fallback,
    resolve_image_source,
    save_image_payload,
)

DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_IMAGE_PATH = PROJECT_ROOT / "resources" / "images" / "climb1.jpeg"
DEFAULT_PROMPT = (
    "保持人物主体和攀岩动作不变。"
    "将整体画面调整为日落时分的自然暖光效果。"
    "服装改成更有层次感的户外冲锋衣，岩壁纹理更清晰。"
    "整体风格保持写实摄影。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="豆包图生图测试脚本")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="图生图提示词")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="首选模型 ID")
    parser.add_argument(
        "--image",
        default=str(DEFAULT_IMAGE_PATH),
        help="输入图片路径或 URL，默认使用 resources/images/ 里的本地示例图",
    )
    parser.add_argument("--size", default="2K", help="输出尺寸，默认 2K")
    parser.add_argument(
        "--output",
        type=Path,
        help="输出文件路径，默认写入 outputs/doubao/image_to_image/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client()
    output_path = args.output or default_output_path("image_to_image")
    image_source = resolve_image_source(args.image)

    response, used_model = generate_image_with_fallback(
        client,
        model=args.model,
        prompt=args.prompt,
        image=image_source,
        size=args.size,
        response_format="b64_json",
        watermark=False,
    )

    saved_path = save_image_payload(response.data[0], output_path)
    print(f"使用模型: {used_model}")
    print(f"已保存到: {saved_path}")


if __name__ == "__main__":
    main()
