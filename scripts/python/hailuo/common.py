from __future__ import annotations

import base64
import json
import mimetypes
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

BASE_URL = "https://api.minimaxi.com"
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "api_key" / "hailuo.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "hailuo"

# 测试阶段可直接把 API Key 填在这里。
API_KEY = "sk-api-432cr4VyyPwhY6GVZvFt_CSjkGtq-Vegwa4dWVOHvQeS9aKJa_ZzVw4H-crHrRbf4EX6lmnZ1fIMYuyLieJJYvEjb1p9_zh_koVk4Ma8aZvDYYAKhY2pWEw"


def load_api_key(config_path: Path = DEFAULT_CONFIG_PATH) -> str:
    if API_KEY:
        return API_KEY

    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        api_key = config.get("api_key", "").strip()
        if api_key:
            return api_key

    raise RuntimeError(
        "未配置海螺 API Key。请在 scripts/python/hailuo/common.py 中填写 API_KEY，"
        f"或创建配置文件 {config_path}。"
    )


def default_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {load_api_key()}",
        "Content-Type": "application/json",
    }


def ensure_output_dir(subdir: str) -> Path:
    target_dir = DEFAULT_OUTPUT_DIR / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def default_output_path(subdir: str, suffix: str = ".mp4") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return ensure_output_dir(subdir) / f"{timestamp}{suffix}"


def _build_url(path: str, query: dict[str, Any] | None = None) -> str:
    url = f"{BASE_URL}{path}"
    if not query:
        return url
    return f"{url}?{urllib.parse.urlencode(query)}"


def _open_json(
    method: str,
    path: str,
    *,
    payload: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    extra_headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    headers = default_headers()
    if extra_headers:
        headers.update(extra_headers)

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        _build_url(path, query),
        data=data,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"接口请求失败: HTTP {exc.code}, body={error_body}") from exc
    return json.loads(body)


def _open_binary(path: str, *, query: dict[str, Any]) -> bytes:
    request = urllib.request.Request(
        _build_url(path, query),
        headers={"Authorization": f"Bearer {load_api_key()}"},
        method="GET",
    )
    with urllib.request.urlopen(request) as response:
        return response.read()


def ensure_success(response: dict[str, Any], context: str) -> dict[str, Any]:
    base_resp = response.get("base_resp", {})
    status_code = base_resp.get("status_code")
    if status_code not in (None, 0):
        status_msg = base_resp.get("status_msg", "unknown error")
        raise RuntimeError(f"{context}失败: status_code={status_code}, status_msg={status_msg}")
    return response


def create_video_task(payload: dict[str, Any]) -> str:
    response = ensure_success(
        _open_json("POST", "/v1/video_generation", payload=payload),
        "创建视频任务",
    )
    task_id = response.get("task_id")
    if not task_id:
        raise RuntimeError(f"创建视频任务成功，但未返回 task_id: {response}")
    return str(task_id)


def query_video_task(task_id: str) -> dict[str, Any]:
    response = ensure_success(
        _open_json(
            "GET",
            "/v1/query/video_generation",
            query={"task_id": task_id},
        ),
        "查询视频任务",
    )
    status = response.get("status")
    if status == "Fail":
        raise RuntimeError(f"视频任务失败: {json.dumps(response, ensure_ascii=False)}")
    return response


def wait_for_task(
    task_id: str,
    *,
    poll_interval: int = 10,
    timeout: int = 900,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status = None

    while time.monotonic() < deadline:
        response = query_video_task(task_id)
        status = response.get("status")
        if status != last_status:
            print(f"任务状态: {status}")
            last_status = status

        if status == "Success":
            return response

        time.sleep(poll_interval)

    raise TimeoutError(f"等待任务超时，task_id={task_id}")


def retrieve_file(file_id: str) -> dict[str, Any]:
    response = ensure_success(
        _open_json(
            "GET",
            "/v1/files/retrieve",
            query={"file_id": file_id},
        ),
        "获取文件信息",
    )
    return response


def retrieve_file_content(file_id: str) -> bytes:
    return _open_binary("/v1/files/retrieve_content", query={"file_id": file_id})


def download_url_file(download_url: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(download_url, method="GET")
    with urllib.request.urlopen(request) as response:
        output_path.write_bytes(response.read())
    return output_path


def download_video(file_id: str, output_path: Path) -> Path:
    file_info = retrieve_file(file_id)
    file_object = file_info.get("file", {})
    download_url = file_object.get("download_url")
    if download_url:
        return download_url_file(str(download_url), output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(retrieve_file_content(file_id))
    return output_path


def resolve_image_source(image_source: str | Path) -> str:
    source_text = str(image_source)
    if source_text.startswith(("http://", "https://", "data:")):
        return source_text

    source = Path(image_source)
    if not source.exists():
        raise FileNotFoundError(f"未找到图片文件: {source}")

    mime_type, _ = mimetypes.guess_type(source.name)
    if mime_type is None:
        mime_type = "application/octet-stream"

    encoded = base64.b64encode(source.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def build_common_payload(args: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"model": args.model}

    if getattr(args, "prompt", None):
        payload["prompt"] = args.prompt

    for name in ("duration", "resolution", "callback_url"):
        value = getattr(args, name, None)
        if value is not None:
            payload[name] = value

    if getattr(args, "prompt_optimizer", None) is not None:
        payload["prompt_optimizer"] = args.prompt_optimizer

    if getattr(args, "fast_pretreatment", None) is not None:
        payload["fast_pretreatment"] = args.fast_pretreatment

    if getattr(args, "aigc_watermark", None) is not None:
        payload["aigc_watermark"] = args.aigc_watermark

    return payload
