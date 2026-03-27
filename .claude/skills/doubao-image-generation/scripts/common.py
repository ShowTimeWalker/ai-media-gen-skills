from __future__ import annotations

import base64
import mimetypes
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from volcenginesdkarkruntime import Ark

BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "doubao"

IMAGE_MODEL_FALLBACKS = [
    "doubao-seedream-5-0-260128",
    "doubao-seedream-4-5-251128",
]

QUOTA_ERROR_KEYWORDS = (
    "quota",
    "insufficient",
    "credit",
    "balance",
    "额度",
    "余额",
    "欠费",
    "用量",
    "resource exhausted",
    "ratelimit",
    "rate limit",
    "setlimitexceeded",
    "429",
)


def load_api_key() -> str:
    api_key = os.getenv("ARK_API_KEY")
    if api_key:
        return api_key
    raise OSError("未设置环境变量 ARK_API_KEY")


def create_client(api_key: str | None = None) -> Ark:
    return Ark(
        base_url=BASE_URL,
        api_key=api_key or load_api_key(),
    )


def ensure_output_dir(*parts: str) -> Path:
    target_dir = DEFAULT_OUTPUT_DIR.joinpath(*parts)
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def default_output_path(*parts: str, suffix: str = ".png") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return ensure_output_dir(*parts) / f"{timestamp}{suffix}"


def resolve_image_source(image_source: str | Path) -> str:
    source = Path(image_source)
    if source.exists():
        mime_type, _ = mimetypes.guess_type(source.name)
        if mime_type is None:
            mime_type = "application/octet-stream"
        encoded = base64.b64encode(source.read_bytes()).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"

    if "://" in str(image_source):
        return str(image_source)

    raise FileNotFoundError(
        f"图片路径不存在，也不是有效的 URL: {image_source}"
    )


def build_model_candidates(
    preferred_model: str,
    fallback_models: Sequence[str] = IMAGE_MODEL_FALLBACKS,
) -> list[str]:
    candidates = [preferred_model]
    for model in fallback_models:
        if model not in candidates:
            candidates.append(model)
    return candidates


def is_quota_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return any(keyword in message for keyword in QUOTA_ERROR_KEYWORDS)


def generate_image_with_fallback(
    client: Ark,
    *,
    model: str,
    fallback_models: Sequence[str] = IMAGE_MODEL_FALLBACKS,
    **kwargs: Any,
) -> tuple[Any, str]:
    candidates = build_model_candidates(model, fallback_models)

    for index, candidate in enumerate(candidates):
        try:
            response = client.images.generate(model=candidate, **kwargs)
            return response, candidate
        except Exception as exc:
            has_next = index + 1 < len(candidates)
            if not has_next or not is_quota_error(exc):
                raise

            next_model = candidates[index + 1]
            print(f"模型 {candidate} 额度不足，自动切换到 {next_model}")


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
