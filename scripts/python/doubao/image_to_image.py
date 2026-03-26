# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PYTHON_DIR = CURRENT_DIR.parent

if str(PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIR))

from common import (  # type: ignore[import-not-found]
    PROJECT_ROOT,
    create_client,
    default_output_path,
    default_qiniu_object_key,
    generate_image_with_fallback,
    resolve_image_source,
    save_image_payload,
)
from qiniu.common import (  # type: ignore[import-not-found]
    build_public_url,
    load_config as load_qiniu_config,
    upload_file,
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
        help="输入图片路径或 URL，默认使用 resources/images/ 里的本地图",
    )
    parser.add_argument("--size", default="2K", help="输出尺寸，默认 2K")
    parser.add_argument(
        "--output",
        type=Path,
        help="输出文件路径，默认写入 outputs/doubao/images/image_to_image/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = create_client()
    output_path = args.output or default_output_path("images", "image_to_image")
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
    object_key = default_qiniu_object_key(saved_path)
    upload_response = upload_file(file_path=saved_path, object_key=object_key)
    qiniu_config = load_qiniu_config()
    public_url = build_public_url(qiniu_config["public_domain"], object_key)

    result = {
        "type": "image",
        "scene": "image_to_image",
        "used_model": used_model,
        "local_path": str(saved_path),
        "bucket": qiniu_config["bucket"],
        "object_key": object_key,
        "upload_response": upload_response,
        "url": public_url,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
