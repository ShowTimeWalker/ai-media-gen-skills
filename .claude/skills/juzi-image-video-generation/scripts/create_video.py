# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse

from common import create_video_task, pretty_json

DEFAULT_MODEL = "VEO 3.1 Fast 多参考版"
DEFAULT_PROMPT = "一辆红色跑车在夜晚城市街道中高速穿行，电影感镜头，光影反射明显。"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_IMAGE_URLS = [
    "https://juziai.oss-cn-shenzhen.aliyuncs.com/uploads/20260301/f06aed0cb2ff8e1a131dd9ca6a56c781.png",
    "https://juziai.oss-cn-shenzhen.aliyuncs.com/uploads/20260301/0da76274207a04aae53423a753de15ab.png",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="橘子视频生成测试脚本")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名称")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="提示词")
    parser.add_argument(
        "--aspect-ratio",
        default=DEFAULT_ASPECT_RATIO,
        help="视频比例，默认 16:9",
    )
    parser.add_argument(
        "--image-url",
        action="append",
        dest="image_urls",
        help="参考图 URL，可传多次；默认使用文档示例图",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_urls = args.image_urls if args.image_urls is not None else DEFAULT_IMAGE_URLS
    response = create_video_task(
        model=args.model,
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        image_urls=image_urls,
    )
    print(pretty_json(response))


if __name__ == "__main__":
    main()
