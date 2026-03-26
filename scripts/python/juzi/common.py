from __future__ import annotations

import json
import mimetypes
import os
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

BASE_URL = "http://juziaigc.com"
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "api_key" / "juzi.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "juzi"

# 测试阶段可直接把 API Key 填在这里。
API_KEY = ""


def load_api_key(config_path: Path = DEFAULT_CONFIG_PATH) -> str:
    env_api_key = os.getenv("JUZI_API_KEY", "").strip()
    if env_api_key:
        return env_api_key

    if API_KEY:
        return API_KEY

    if not config_path.exists():
        raise RuntimeError(f"未找到橘子 API Key 配置文件：{config_path}")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    api_key = str(config.get("api_key", "")).strip()
    if not api_key:
        raise RuntimeError(f"配置文件中缺少 api_key：{config_path}")
    return api_key


def auth_header() -> dict[str, str]:
    return {"Authorization": f"Bearer {load_api_key()}"}


def ensure_output_dir() -> Path:
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_OUTPUT_DIR


def ensure_scene_output_dir(scene: str) -> Path:
    target_dir = ensure_output_dir() / scene
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def _open_request(request: Request) -> dict[str, Any]:
    try:
        with urlopen(request) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"接口请求失败: HTTP {exc.code}, body={error_body}") from exc
    return json.loads(body)


def _encode_form_fields(fields: list[tuple[str, str]]) -> tuple[bytes, str]:
    boundary = "----CodexJuziFormBoundary7MA4YWxkTrZu0gW"
    chunks: list[bytes] = []

    for key, value in fields:
        chunks.append(f"--{boundary}\r\n".encode("utf-8"))
        chunks.append(
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8")
        )
        chunks.append(value.encode("utf-8"))
        chunks.append(b"\r\n")

    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), boundary


def post_form(path: str, fields: list[tuple[str, str]]) -> dict[str, Any]:
    body, boundary = _encode_form_fields(fields)
    headers = auth_header()
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    request = Request(
        f"{BASE_URL}{path}",
        data=body,
        headers=headers,
        method="POST",
    )
    return _open_request(request)


def get_json(path: str, query: dict[str, str]) -> dict[str, Any]:
    url = f"{BASE_URL}{path}?{urlencode(query)}"
    request = Request(url, headers=auth_header(), method="GET")
    return _open_request(request)


def ensure_success(response: dict[str, Any], context: str) -> dict[str, Any]:
    code = response.get("code")
    if code != 200:
        raise RuntimeError(f"{context}失败: {json.dumps(response, ensure_ascii=False)}")
    return response


def create_video_task(
    *,
    model: str,
    prompt: str,
    aspect_ratio: str,
    image_urls: list[str] | None = None,
) -> dict[str, Any]:
    fields: list[tuple[str, str]] = [
        ("model", model),
        ("prompt", prompt),
        ("aspect_ratio", aspect_ratio),
    ]
    for index, image_url in enumerate(image_urls or []):
        if image_url:
            fields.append((f"image_urls[{index}]", image_url))
    return ensure_success(post_form("/open/api/video", fields), "视频生成")


def query_video_task(juzi_id: str) -> dict[str, Any]:
    return ensure_success(
        get_json("/open/api/vNotify", {"juzi_id": juzi_id}),
        "视频进度查询",
    )


def create_image_task(
    *,
    model: str,
    prompt: str,
    ratio: str | None = None,
    urls: list[str] | None = None,
    quality: str | None = None,
) -> dict[str, Any]:
    fields: list[tuple[str, str]] = [
        ("model", model),
        ("prompt", prompt),
    ]
    if ratio:
        fields.append(("ratio", ratio))
    if quality:
        fields.append(("quality", quality))
    for index, image_url in enumerate(urls or []):
        if image_url:
            fields.append((f"urls[{index}]", image_url))
    return ensure_success(post_form("/open/api/images", fields), "图片生成")


def query_image_task(juzi_id: str) -> dict[str, Any]:
    return ensure_success(
        get_json("/open/api/imgNotify", {"juzi_id": juzi_id}),
        "图片进度查询",
    )


def wait_for_video_task(
    juzi_id: str,
    *,
    poll_interval: int = 10,
    timeout: int = 900,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status: str | None = None

    while time.monotonic() < deadline:
        response = query_video_task(juzi_id)
        data = response.get("data", {})
        status = str(data.get("status", ""))
        progress = data.get("progress")

        if status != last_status:
            print(f"视频任务状态: {status} ({progress}%)")
            last_status = status

        if status == "succeeded":
            return response
        if status == "failed":
            raise RuntimeError(f"视频任务失败: {json.dumps(response, ensure_ascii=False)}")

        time.sleep(poll_interval)

    raise TimeoutError(f"视频任务超时，juzi_id={juzi_id}")


def wait_for_image_task(
    juzi_id: str,
    *,
    poll_interval: int = 10,
    timeout: int = 900,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status: str | None = None

    while time.monotonic() < deadline:
        response = query_image_task(juzi_id)
        data = response.get("data", {})
        status = str(data.get("status", ""))
        progress = data.get("progress")

        if status != last_status:
            print(f"图片任务状态: {status} ({progress}%)")
            last_status = status

        if status == "succeeded":
            return response
        if status == "failed":
            raise RuntimeError(f"图片任务失败: {json.dumps(response, ensure_ascii=False)}")

        time.sleep(poll_interval)

    raise TimeoutError(f"图片任务超时，juzi_id={juzi_id}")


def infer_extension_from_url(url: str, default_suffix: str) -> str:
    path = urlparse(url).path
    suffix = Path(path).suffix
    return suffix or default_suffix


def default_output_path(scene: str, juzi_id: str, source_url: str, default_suffix: str) -> Path:
    ext = infer_extension_from_url(source_url, default_suffix)
    return ensure_scene_output_dir(scene) / f"{juzi_id}{ext}"


def download_file(url: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, method="GET")
    with urlopen(request) as response:
        output_path.write_bytes(response.read())
    return output_path


def extract_video_result_url(response: dict[str, Any]) -> str:
    data = response.get("data", {})
    result_url = str(data.get("juzi_url", "")).strip()
    if not result_url:
        raise RuntimeError(f"视频结果中缺少 juzi_url: {json.dumps(response, ensure_ascii=False)}")
    return result_url


def extract_image_result_url(response: dict[str, Any]) -> str:
    data = response.get("data", {})
    sai_url = data.get("sai_url")
    if not isinstance(sai_url, list) or not sai_url:
        raise RuntimeError(f"图片结果中缺少 sai_url: {json.dumps(response, ensure_ascii=False)}")

    first_item = sai_url[0]
    if not isinstance(first_item, dict):
        raise RuntimeError(f"图片结果中的 sai_url 格式异常: {json.dumps(response, ensure_ascii=False)}")

    result_url = str(first_item.get("url", "")).strip()
    if not result_url:
        raise RuntimeError(f"图片结果中缺少 url: {json.dumps(response, ensure_ascii=False)}")
    return result_url


def pretty_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)
