from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OUTPUT_ROOT = Path(os.environ.get("OUTPUT_ROOT", "~/")).expanduser().resolve()
BASE_URL = "https://api.tianpuyue.cn"
DEFAULT_OUTPUT_DIR = OUTPUT_ROOT / "outputs" / "tianpuyue"

DUMMY_CALLBACK_URL = "https://example.com/callback"


def load_api_key() -> str:
    api_key = os.getenv("TIANPUYUE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("未设置环境变量 TIANPUYUE_API_KEY")
    return api_key


def get_callback_url() -> str:
    return os.getenv("TIANPUYUE_CALLBACK_URL", DUMMY_CALLBACK_URL).strip()


def auth_header() -> dict[str, str]:
    return {"Authorization": load_api_key()}


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


def post_json(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    headers = auth_header()
    headers["Content-Type"] = "application/json"
    request = Request(
        f"{BASE_URL}{path}",
        data=data,
        headers=headers,
        method="POST",
    )
    return _open_request(request)


def ensure_success(response: dict[str, Any], context: str) -> dict[str, Any]:
    code = response.get("status")
    if code != 200000:
        raise RuntimeError(f"{context}失败: {json.dumps(response, ensure_ascii=False)}")
    return response


# --- 纯音乐 ---

def create_music_task(*, prompt: str, model: str) -> dict[str, Any]:
    payload = {
        "prompt": prompt,
        "model": model,
        "callback_url": get_callback_url(),
    }
    resp = ensure_success(post_json("/open-apis/v1/instrumental/generate", payload), "纯音乐生成")
    item_ids = resp.get("data", {}).get("item_ids", [])
    if not item_ids:
        raise RuntimeError(f"纯音乐生成未返回 item_id: {json.dumps(resp, ensure_ascii=False)}")
    return resp


def query_music_task(item_id: str) -> dict[str, Any]:
    payload = {"item_ids": [item_id]}
    resp = ensure_success(post_json("/open-apis/v1/instrumental/query", payload), "纯音乐状态查询")
    instrumentals = resp.get("data", {}).get("instrumentals", [])
    if not instrumentals:
        raise RuntimeError(f"纯音乐查询未返回结果: {json.dumps(resp, ensure_ascii=False)}")
    return instrumentals[0]


def wait_for_music_task(
    item_id: str,
    *,
    poll_interval: int = 15,
    timeout: int = 900,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status: str | None = None

    while time.monotonic() < deadline:
        item = query_music_task(item_id)
        status = str(item.get("status", ""))

        if status != last_status:
            print(f"纯音乐任务状态: {status}")
            last_status = status

        if status in ("succeeded", "main_succeeded", "part_failed"):
            return item
        if status == "failed":
            raise RuntimeError(f"纯音乐任务失败: {json.dumps(item, ensure_ascii=False)}")

        time.sleep(poll_interval)

    raise TimeoutError(f"纯音乐任务超时，item_id={item_id}")


# --- 歌曲 ---

def create_song_task(
    *,
    prompt: str,
    model: str,
    lyrics: str | None = None,
    voice_id: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "prompt": prompt,
        "model": model,
        "callback_url": get_callback_url(),
    }
    if lyrics is not None:
        payload["lyrics"] = lyrics
    if voice_id is not None:
        payload["voice_id"] = voice_id
    resp = ensure_success(post_json("/open-apis/v1/song/generate", payload), "歌曲生成")
    item_ids = resp.get("data", {}).get("item_ids", [])
    if not item_ids:
        raise RuntimeError(f"歌曲生成未返回 item_id: {json.dumps(resp, ensure_ascii=False)}")
    return resp


def query_song_task(item_id: str) -> dict[str, Any]:
    payload = {"item_ids": [item_id]}
    resp = ensure_success(post_json("/open-apis/v1/song/query", payload), "歌曲状态查询")
    songs = resp.get("data", {}).get("songs", [])
    if not songs:
        raise RuntimeError(f"歌曲查询未返回结果: {json.dumps(resp, ensure_ascii=False)}")
    return songs[0]


def wait_for_song_task(
    item_id: str,
    *,
    poll_interval: int = 15,
    timeout: int = 900,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status: str | None = None

    while time.monotonic() < deadline:
        item = query_song_task(item_id)
        status = str(item.get("status", ""))

        if status != last_status:
            print(f"歌曲任务状态: {status}")
            last_status = status

        if status in ("succeeded", "main_succeeded", "part_failed"):
            return item
        if status == "failed":
            raise RuntimeError(f"歌曲任务失败: {json.dumps(item, ensure_ascii=False)}")

        time.sleep(poll_interval)

    raise TimeoutError(f"歌曲任务超时，item_id={item_id}")


# --- 歌词 ---

def create_lyrics_task(*, prompt: str, song_model: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "prompt": prompt,
        "callback_url": get_callback_url(),
    }
    if song_model is not None:
        payload["song_model"] = song_model
    resp = ensure_success(post_json("/open-apis/v1/lyrics/generate", payload), "歌词生成")
    item_ids = resp.get("data", {}).get("item_ids", [])
    if not item_ids:
        raise RuntimeError(f"歌词生成未返回 item_id: {json.dumps(resp, ensure_ascii=False)}")
    return resp


def query_lyrics_task(item_id: str) -> dict[str, Any]:
    payload = {"item_ids": [item_id]}
    resp = ensure_success(post_json("/open-apis/v1/lyrics/query", payload), "歌词状态查询")
    lyrics_list = resp.get("data", {}).get("lyrics", [])
    if not lyrics_list:
        raise RuntimeError(f"歌词查询未返回结果: {json.dumps(resp, ensure_ascii=False)}")
    return lyrics_list[0]


def wait_for_lyrics_task(
    item_id: str,
    *,
    poll_interval: int = 10,
    timeout: int = 300,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status: str | None = None

    while time.monotonic() < deadline:
        item = query_lyrics_task(item_id)
        status = str(item.get("status", ""))

        if status != last_status:
            print(f"歌词任务状态: {status}")
            last_status = status

        if status == "succeeded":
            return item
        if status == "failed":
            raise RuntimeError(f"歌词任务失败: {json.dumps(item, ensure_ascii=False)}")

        time.sleep(poll_interval)

    raise TimeoutError(f"歌词任务超时，item_id={item_id}")


# --- 通用工具 ---

def extract_audio_url(item: dict[str, Any]) -> str:
    url = str(item.get("audio_url", "")).strip()
    if not url:
        raise RuntimeError(f"结果中缺少 audio_url: {json.dumps(item, ensure_ascii=False)}")
    return url


def download_file(url: str, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, method="GET")
    with urlopen(request) as response:
        output_path.write_bytes(response.read())
    return output_path


def default_output_path(scene: str, item_id: str, suffix: str) -> Path:
    return ensure_scene_output_dir(scene) / f"{item_id}{suffix}"


def pretty_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)
