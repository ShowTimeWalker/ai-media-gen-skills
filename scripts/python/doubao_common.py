from __future__ import annotations

import base64
import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from volcenginesdkarkruntime import Ark

BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "api_key" / "doubao.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "doubao"


def load_api_key(config_path: Path = DEFAULT_CONFIG_PATH) -> str:
    api_key = os.getenv("ARK_API_KEY")
    if api_key:
        return api_key

    if not config_path.exists():
        raise RuntimeError(
            "未找到 ARK_API_KEY 环境变量，且缺少配置文件："
            f"{config_path}"
        )

    config = json.loads(config_path.read_text(encoding="utf-8"))
    api_key = config.get("api_key")
    if not api_key:
        raise RuntimeError(f"配置文件中缺少 api_key：{config_path}")
    return api_key


def create_client(api_key: str | None = None) -> Ark:
    return Ark(
        base_url=BASE_URL,
        api_key=api_key or load_api_key(),
    )


def ensure_output_dir(subdir: str) -> Path:
    target_dir = DEFAULT_OUTPUT_DIR / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def default_output_path(subdir: str, suffix: str = ".png") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return ensure_output_dir(subdir) / f"{timestamp}{suffix}"


def save_image_payload(image_data: Any, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    b64_json = getattr(image_data, "b64_json", None)
    if b64_json:
        output_path.write_bytes(base64.b64decode(b64_json))
        return output_path

    url = getattr(image_data, "url", None)
    if url:
        with urllib.request.urlopen(url) as response:
            output_path.write_bytes(response.read())
        return output_path

    raise RuntimeError("接口返回中既没有 b64_json，也没有 url，无法保存图片。")
