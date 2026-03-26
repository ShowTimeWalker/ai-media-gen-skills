# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import (
    PROJECT_ROOT,
    build_private_download_url,
    build_public_url,
    load_config,
    upload_file,
)

DEFAULT_FILE = PROJECT_ROOT / "outputs" / "juzi" / "videos" / "6f62ebf1-ad5b-499b-bc98-4e44568cb396.mp4"
DEFAULT_PREFIX = "uploads"
DEFAULT_EXPIRES_IN = 600


def infer_object_key(file_path: Path, prefix: str) -> str:
    outputs_root = (PROJECT_ROOT / "outputs").resolve()
    resolved = file_path.resolve()
    try:
        return resolved.relative_to(outputs_root).as_posix()
    except ValueError:
        clean_prefix = prefix.strip("/").replace("\\", "/")
        return f"{clean_prefix}/{file_path.name}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="上传本地文件到七牛并返回 URL")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_FILE,
        help="本地文件路径",
    )
    parser.add_argument(
        "--key",
        help="对象 key；不传则优先复用 outputs 下的相对路径",
    )
    parser.add_argument(
        "--prefix",
        default=DEFAULT_PREFIX,
        help="未提供 --key 且文件不在 outputs 下时使用的对象 key 前缀",
    )
    parser.add_argument(
        "--private-url",
        action="store_true",
        help="额外返回带时效签名的私有下载链接",
    )
    parser.add_argument(
        "--expires-in",
        type=int,
        default=DEFAULT_EXPIRES_IN,
        help="私有下载链接有效期，默认 600 秒",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    file_path = args.file.expanduser().resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"未找到本地文件: {file_path}")

    object_key = args.key or infer_object_key(file_path, args.prefix)
    upload_response = upload_file(file_path=file_path, object_key=object_key)
    config = load_config()
    public_url = build_public_url(config["public_domain"], object_key)

    result: dict[str, object] = {
        "bucket": config["bucket"],
        "object_key": object_key,
        "local_path": str(file_path),
        "upload_response": upload_response,
        "public_url": public_url,
    }

    if args.private_url:
        result["private_url"] = build_private_download_url(
            access_key=config["access_key"],
            secret_key=config["secret_key"],
            base_url=public_url,
            expires_in=args.expires_in,
        )
        result["expires_in"] = args.expires_in

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
