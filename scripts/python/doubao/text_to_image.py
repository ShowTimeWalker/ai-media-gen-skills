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
    create_client,
    default_output_path,
    default_qiniu_object_key,
    generate_image_with_fallback,
    save_image_payload,
)
from qiniu.common import (  # type: ignore[import-not-found]
    build_public_url,
    load_config as load_qiniu_config,
    upload_file,
)

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
    object_key = default_qiniu_object_key(saved_path)
    upload_response = upload_file(file_path=saved_path, object_key=object_key)
    qiniu_config = load_qiniu_config()
    public_url = build_public_url(qiniu_config["public_domain"], object_key)

    result = {
        "type": "image",
        "scene": "text_to_image",
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
