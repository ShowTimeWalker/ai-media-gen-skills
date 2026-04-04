from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from uuid import uuid4

logger = logging.getLogger("juzi")


def log_params(event: str, **kwargs: Any) -> None:
    """Log an event with a provider prefix and JSON payload."""
    params_str = json.dumps(kwargs, ensure_ascii=False, default=str)
    logger.info("橘子 - %s | %s", event, params_str)


_trace_id: str = ""


def generate_trace_id() -> str:
    return uuid4().hex


def get_trace_id() -> str:
    global _trace_id
    if not _trace_id:
        _trace_id = generate_trace_id()
    return _trace_id


class _TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id()
        return True


OUTPUT_ROOT = Path(os.environ.get("OUTPUT_ROOT", "~/")).expanduser().resolve()
BASE_URL = "http://juziaigc.com"
DEFAULT_OUTPUT_DIR = OUTPUT_ROOT / "outputs" / "juzi"
LOG_DIR = OUTPUT_ROOT / "outputs" / "logs"


def setup_logging() -> None:
    if logger.handlers:
        return
    trace_filter = _TraceIdFilter()
    log_fmt = "%(asctime)s [%(trace_id)s] %(levelname)s %(message)s"
    fmt = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    file_handler = logging.FileHandler(LOG_DIR / f"{today}.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    file_handler.addFilter(trace_filter)
    logger.addHandler(file_handler)
    error_handler = logging.FileHandler(LOG_DIR / f"{today}.error.log", encoding="utf-8")
    error_handler.setFormatter(fmt)
    error_handler.addFilter(trace_filter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)


def load_api_key() -> str:
    api_key = os.getenv("JUZI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("未设置环境变量 JUZI_API_KEY")
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
            log_params("视频任务状态", juzi_id=juzi_id, status=status, progress=progress)
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
            log_params("图片任务状态", juzi_id=juzi_id, status=status, progress=progress)
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
    log_params("文件下载开始", url=url, output_path=str(output_path.name))
    request = Request(url, method="GET")
    with urlopen(request) as response:
        output_path.write_bytes(response.read())
    size = output_path.stat().st_size
    log_params("文件下载完成", url=url, output_path=str(output_path.name), size=size)
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
