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
    resolve_access_mode,
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
    parser = argparse.ArgumentParser(description="上传本地文件到七牛并返回交付链接")
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
    access_mode_group = parser.add_mutually_exclusive_group()
    access_mode_group.add_argument(
        "--private-url",
        action="store_true",
        help="强制返回带签名的私有下载链接",
    )
    access_mode_group.add_argument(
        "--public-url",
        action="store_true",
        help="强制返回公网链接",
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
    if args.expires_in <= 0:
        raise ValueError("--expires-in 必须大于 0")

    object_key = args.key or infer_object_key(file_path, args.prefix)
    upload_response = upload_file(file_path=file_path, object_key=object_key)
    config = load_config()
    base_url = build_public_url(config["public_domain"], object_key)
    access_mode = resolve_access_mode(
        is_private_bucket=bool(config["is_private"]),
        prefer_private=args.private_url,
        prefer_public=args.public_url,
    )

    result: dict[str, object] = {
        "storage_provider": "qiniu",
        "bucket": config["bucket"],
        "object_key": object_key,
        "local_path": str(file_path),
        "upload_response": upload_response,
        "is_private_bucket": bool(config["is_private"]),
        "access_mode": access_mode,
        "base_url": base_url,
    }

    if access_mode == "private":
        private_url = build_private_download_url(
            access_key=config["access_key"],
            secret_key=config["secret_key"],
            base_url=base_url,
            expires_in=args.expires_in,
        )
        result["private_url"] = private_url
        result["delivery_url"] = private_url
        result["expires_in"] = args.expires_in
    else:
        result["public_url"] = base_url
        result["delivery_url"] = base_url

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
