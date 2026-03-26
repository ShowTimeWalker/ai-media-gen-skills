from __future__ import annotations

import base64
import hashlib
import hmac
import json
import mimetypes
import os
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

DEFAULT_UPLOAD_DOMAIN = "https://upload-z2.qiniup.com"

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "api_key" / "qiniu.json"
ENV_FIELD_MAP = {
    "access_key": "QINIU_ACCESS_KEY",
    "secret_key": "QINIU_SECRET_KEY",
    "bucket": "QINIU_BUCKET",
    "public_domain": "QINIU_PUBLIC_DOMAIN",
}


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> dict[str, str]:
    file_config: dict[str, str] = {}
    if config_path.exists():
        file_config = json.loads(config_path.read_text(encoding="utf-8"))

    config: dict[str, str] = {}
    missing: list[str] = []
    for field, env_name in ENV_FIELD_MAP.items():
        value = os.getenv(env_name, "").strip() or str(file_config.get(field, "")).strip()
        if value:
            config[field] = value
        else:
            missing.append(field)

    if missing:
        raise RuntimeError(
            f"七牛配置缺少字段: {', '.join(missing)}，请设置环境变量或填写 {config_path}"
        )
    return config


def urlsafe_base64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8")


def normalize_domain(domain: str) -> str:
    return domain.rstrip("/")


def build_public_url(domain: str, object_key: str) -> str:
    return f"{normalize_domain(domain)}/{quote(object_key)}"


def build_private_download_url(
    *,
    access_key: str,
    secret_key: str,
    base_url: str,
    expires_in: int = 600,
) -> str:
    deadline = int(time.time()) + expires_in
    separator = "&" if "?" in base_url else "?"
    signing_url = f"{base_url}{separator}e={deadline}"

    digest = hmac.new(
        secret_key.encode("utf-8"),
        signing_url.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    encoded_sign = urlsafe_base64_encode(digest)
    token = f"{access_key}:{encoded_sign}"
    return f"{signing_url}&token={token}"


def build_upload_token(
    *,
    access_key: str,
    secret_key: str,
    bucket: str,
    object_key: str,
    expires_in: int = 3600,
) -> str:
    deadline = int(time.time()) + expires_in
    policy = {
        "scope": f"{bucket}:{object_key}",
        "deadline": deadline,
    }
    encoded_policy = urlsafe_base64_encode(
        json.dumps(policy, separators=(",", ":")).encode("utf-8")
    )
    digest = hmac.new(
        secret_key.encode("utf-8"),
        encoded_policy.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    encoded_sign = urlsafe_base64_encode(digest)
    return f"{access_key}:{encoded_sign}:{encoded_policy}"


def encode_multipart_form(
    *,
    fields: list[tuple[str, str]],
    file_field: str,
    file_path: Path,
) -> tuple[bytes, str]:
    boundary = "----CodexQiniuFormBoundary7MA4YWxkTrZu0gW"
    chunks: list[bytes] = []

    for key, value in fields:
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8")
        )
        chunks.append(value.encode("utf-8"))
        chunks.append(b"\r\n")

    mime_type, _ = mimetypes.guess_type(file_path.name)
    if mime_type is None:
        mime_type = "application/octet-stream"

    chunks.append(f"--{boundary}\r\n".encode("utf-8"))
    chunks.append(
        (
            f'Content-Disposition: form-data; name="{file_field}"; '
            f'filename="{file_path.name}"\r\n'
        ).encode("utf-8")
    )
    chunks.append(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    chunks.append(file_path.read_bytes())
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), boundary


def upload_file(
    *,
    file_path: Path,
    object_key: str,
    upload_domain: str | None = None,
    token_expires_in: int = 3600,
) -> dict[str, str]:
    config = load_config()
    token = build_upload_token(
        access_key=config["access_key"],
        secret_key=config["secret_key"],
        bucket=config["bucket"],
        object_key=object_key,
        expires_in=token_expires_in,
    )
    body, boundary = encode_multipart_form(
        fields=[("token", token), ("key", object_key)],
        file_field="file",
        file_path=file_path,
    )
    request = Request(
        upload_domain or DEFAULT_UPLOAD_DOMAIN,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))
