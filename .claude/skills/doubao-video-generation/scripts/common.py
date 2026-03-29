# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from volcenginesdkarkruntime import Ark

BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "doubao"

VIDEO_MODEL_FALLBACKS: list[str] = []


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


def default_output_path(*parts: str, suffix: str = ".mp4") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return ensure_output_dir(*parts) / f"{timestamp}{suffix}"


def create_video_task(
    client: Ark,
    *,
    model: str,
    content: list[dict[str, Any]],
    **kwargs: Any,
) -> dict[str, Any]:
    """Create a video generation task via the Ark SDK.

    Returns a dict with at least:
      - id: task ID (str)
    """
    params: dict[str, Any] = {"model": model, "content": content}
    params.update(kwargs)
    resp = client.content_generation.tasks.create(**params)
    # resp is an SDK object; normalize to dict
    return _to_dict(resp)


def query_video_task(
    client: Ark,
    task_id: str,
) -> dict[str, Any]:
    """Query the status of a video generation task."""
    resp = client.content_generation.tasks.get(task_id=task_id)
    return _to_dict(resp)


def wait_for_video_task(
    client: Ark,
    task_id: str,
    *,
    poll_interval: int = 10,
    timeout: int = 900,
) -> dict[str, Any]:
    """Poll a video task until succeeded or failed."""
    deadline = __import__("time").monotonic() + timeout
    import time

    last_status: str | None = None
    while time.monotonic() < deadline:
        result = query_video_task(client, task_id)
        status = result.get("status", "")

        if status != last_status:
            print(f"视频任务状态: {status}")
            last_status = status

        if status == "succeeded":
            return result
        if status == "failed":
            error = result.get("error", {})
            raise RuntimeError(
                f"视频任务失败: {json.dumps(error, ensure_ascii=False)}"
            )

        time.sleep(poll_interval)

    raise TimeoutError(f"视频任务超时，task_id={task_id}")


def extract_video_url(result: dict[str, Any]) -> str:
    """Extract the video URL from a succeeded task result."""
    content = result.get("content", {})
    if isinstance(content, dict):
        video_url = content.get("video_url", "")
    else:
        # SDK may return an object with attributes
        video_url = getattr(content, "video_url", "")

    video_url = str(video_url).strip()
    if not video_url:
        raise RuntimeError(
            f"视频结果中缺少 video_url: {json.dumps(result, ensure_ascii=False, default=str)}"
        )
    return video_url


def download_file(url: str, output_path: Path) -> Path:
    """Download a file from URL to local path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request) as response:
        output_path.write_bytes(response.read())
    return output_path


def _to_dict(obj: Any) -> dict[str, Any]:
    """Normalize SDK response objects to plain dict."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return {"raw": str(obj)}
