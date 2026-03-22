# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
from pathlib import Path

from doubao_common import create_client, default_output_path, save_image_payload

DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_IMAGE_URL = (
    "https://ark-project.tos-cn-beijing.volces.com/doc_image/"
    "seedream4_5_imageToimage.png"
)
DEFAULT_PROMPT = (
    "保持模特姿势和液态服装的流动形状不变。"
    "将服装材质从银色金属改为完全透明的清水或玻璃。"
    "透过液态水流，可以看到模特的皮肤细节。"
    "光影从反射变为折射。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="豆包图生图测试脚本")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="图生图提示词")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型 ID")
    parser.add_argument(
        "--image-url",
        default=DEFAULT_IMAGE_URL,
        help="输入图片 URL，默认使用文档示例图",
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

    response = client.images.generate(
        model=args.model,
        prompt=args.prompt,
        image=args.image_url,
        size=args.size,
        response_format="b64_json",
        watermark=False,
    )

    saved_path = save_image_payload(response.data[0], output_path)
    print(f"已保存到: {saved_path}")


if __name__ == "__main__":
    main()
