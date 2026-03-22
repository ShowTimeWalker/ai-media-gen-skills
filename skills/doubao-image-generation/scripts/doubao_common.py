from __future__ import annotations

import base64
import json
import mimetypes
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from volcenginesdkarkruntime import Ark

BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
SKILL_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SKILL_ROOT.parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "api_key" / "doubao.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "doubao"

IMAGE_MODEL_FALLBACKS = [
    "doubao-seedream-5-0-260128",
    "doubao-seedream-4-5-251128",
    "doubao-seedream-4-0-250828",
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
)


def load_api_key(config_path: Path = DEFAULT_CONFIG_PATH) -> str:
    api_key = os.getenv("ARK_API_KEY")
    if api_key:
        return api_key

    if not config_path.exists():
        raise RuntimeError(
            f"未找到 ARK_API_KEY 环境变量，且缺少配置文件：{config_path}"
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


def resolve_image_source(image_source: str | Path) -> str:
    source = Path(image_source)
    if not source.exists():
        return str(image_source)

    mime_type, _ = mimetypes.guess_type(source.name)
    if mime_type is None:
        mime_type = "application/octet-stream"

    encoded = base64.b64encode(source.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


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
    last_exc: Exception | None = None

    for index, candidate in enumerate(candidates):
        try:
            response = client.images.generate(model=candidate, **kwargs)
            return response, candidate
        except Exception as exc:
            last_exc = exc
            has_next = index + 1 < len(candidates)
            if not has_next or not is_quota_error(exc):
                raise

            next_model = candidates[index + 1]
            print(f"模型 {candidate} 额度不足，自动切换到 {next_model}")

    if last_exc is not None:
        raise last_exc

    raise RuntimeError("未能完成图像生成请求。")


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
