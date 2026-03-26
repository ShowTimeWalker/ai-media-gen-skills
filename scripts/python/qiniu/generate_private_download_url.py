# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse

from common import build_private_download_url, build_public_url, load_config

DEFAULT_OBJECT_KEY = "juzi/d477a35b-bb65-44f1-8e14-0bfb8b36fa84-20260326-134923.mp4"
DEFAULT_EXPIRES_IN = 600


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成七牛私有下载链接")
    parser.add_argument(
        "--key",
        default=DEFAULT_OBJECT_KEY,
        help="对象 key，默认使用当前测试视频",
    )
    parser.add_argument(
        "--expires-in",
        type=int,
        default=DEFAULT_EXPIRES_IN,
        help="有效期秒数，默认 600 秒",
    )
    parser.add_argument(
        "--domain",
        help="下载域名，默认读取 api_key/qiniu.json 中的 public_domain",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()
    domain = args.domain or config["public_domain"]
    public_url = build_public_url(domain, args.key)
    signed_url = build_private_download_url(
        access_key=config["access_key"],
        secret_key=config["secret_key"],
        base_url=public_url,
        expires_in=args.expires_in,
    )

    print(f"bucket: {config['bucket']}")
    print(f"key: {args.key}")
    print(f"expires_in: {args.expires_in}")
    print(signed_url)


if __name__ == "__main__":
    main()
