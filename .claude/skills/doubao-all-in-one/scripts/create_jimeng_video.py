# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "requests",
# ]
# ///

from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import json
import mimetypes
import os
import time
from pathlib import Path

import requests

from common import (
    OUTPUT_ROOT,
    default_output_path,
    download_file,
    get_trace_id,
    log_params,
    setup_logging,
)

setup_logging()

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

HOST = "visual.volcengineapi.com"
REGION = "cn-north-1"
ENDPOINT = f"https://{HOST}"
SERVICE = "cv"
VERSION = "2022-08-31"

DEFAULT_PROMPT = "小猫对着镜头打哈欠，镜头缓缓拉出"

# req_key 映射表：(scene, resolution) -> req_key
REQ_KEY_MAP: dict[tuple[str, str], str] = {
    ("text_to_video", "720p"): "jimeng_t2v_v30",
    ("text_to_video", "1080p"): "jimeng_t2v_v30_1080p",
    ("first_frame_to_video", "720p"): "jimeng_i2v_first_v30",
    ("first_frame_to_video", "1080p"): "jimeng_i2v_first_v30_1080",
    ("first_last_frame_to_video", "720p"): "jimeng_i2v_first_tail_v30",
    ("first_last_frame_to_video", "1080p"): "jimeng_i2v_first_tail_v30_1080",
}


# ---------------------------------------------------------------------------
# V4 签名
# ---------------------------------------------------------------------------

def _hmac_sha256(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _get_signature_key(secret_key: str, date_stamp: str, region: str, service: str) -> bytes:
    k_date = _hmac_sha256(secret_key.encode("utf-8"), date_stamp)
    k_region = _hmac_sha256(k_date, region)
    k_service = _hmac_sha256(k_region, service)
    k_signing = _hmac_sha256(k_service, "request")
    return k_signing


def _sign_request(
    method: str,
    action: str,
    access_key: str,
    secret_key: str,
    body: str,
) -> dict[str, str]:
    """构建带 V4 签名的请求 headers 和 URL。"""
    now = datetime.datetime.utcnow()
    x_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    canonical_uri = "/"
    canonical_querystring = f"Action={action}&Version={VERSION}"

    payload_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    content_type = "application/json"

    signed_headers = "content-type;host;x-content-sha256;x-date"
    canonical_headers = (
        f"content-type:{content_type}\n"
        f"host:{HOST}\n"
        f"x-content-sha256:{payload_hash}\n"
        f"x-date:{x_date}\n"
    )

    canonical_request = (
        f"{method}\n{canonical_uri}\n{canonical_querystring}\n"
        f"{canonical_headers}\n{signed_headers}\n{payload_hash}"
    )

    algorithm = "HMAC-SHA256"
    credential_scope = f"{date_stamp}/{REGION}/{SERVICE}/request"
    string_to_sign = (
        f"{algorithm}\n{x_date}\n{credential_scope}\n"
        f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    )

    signing_key = _get_signature_key(secret_key, date_stamp, REGION, SERVICE)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    authorization = (
        f"{algorithm} Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    headers = {
        "X-Date": x_date,
        "Authorization": authorization,
        "X-Content-Sha256": payload_hash,
        "Content-Type": content_type,
    }

    url = f"{ENDPOINT}?{canonical_querystring}"
    return {"url": url, "headers": headers}


# ---------------------------------------------------------------------------
# API 调用
# ---------------------------------------------------------------------------

def load_credentials() -> tuple[str, str]:
    """加载即梦 API 凭据 (access_key, secret_key)。

    优先级：环境变量 > api_key/jimeng.json 配置文件
    """
    ak = os.getenv("VOLC_ACCESS_KEY")
    sk = os.getenv("VOLC_SECRET_KEY")
    if ak and sk:
        return ak, sk

    # 从 api_key/jimeng.json 读取
    config_path = OUTPUT_ROOT / "api_key" / "jimeng.json"
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        ak = config.get("access_key", "")
        sk = config.get("secret_key", "")
        if ak and sk:
            return ak, sk

    raise OSError(f"未设置环境变量 VOLC_ACCESS_KEY/VOLC_SECRET_KEY，也未找到配置文件: {config_path}")


def call_api(action: str, body: dict, ak: str, sk: str) -> dict:
    """调用即梦 Visual API。"""
    body_str = json.dumps(body, ensure_ascii=False)
    signed = _sign_request("POST", action, ak, sk, body_str)
    resp = requests.post(signed["url"], headers=signed["headers"], data=body_str, timeout=30)
    if resp.status_code != 200:
        print(f"API 错误: HTTP {resp.status_code}")
        print(f"响应内容: {resp.text[:500]}")
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") not in (10000, None):
        raise RuntimeError(
            f"即梦 API 错误: code={result.get('code')}, "
            f"message={result.get('message', '')}, "
            f"request_id={result.get('request_id', '')}"
        )
    return result


def submit_task(ak: str, sk: str, body: dict) -> dict:
    """提交视频生成任务。"""
    return call_api("CVSync2AsyncSubmitTask", body, ak, sk)


def query_task(ak: str, sk: str, body: dict) -> dict:
    """查询视频任务状态。"""
    return call_api("CVSync2AsyncGetResult", body, ak, sk)


def wait_for_task(
    ak: str,
    sk: str,
    req_key: str,
    task_id: str,
    *,
    poll_interval: int = 10,
    timeout: int = 900,
) -> dict:
    """轮询即梦视频任务直到完成。"""
    deadline = time.monotonic() + timeout
    last_status: str | None = None
    while time.monotonic() < deadline:
        result = query_task(ak, sk, {"req_key": req_key, "task_id": task_id})
        data = result.get("data", {})
        status = data.get("status", "") if isinstance(data, dict) else ""

        if status != last_status:
            print(f"即梦任务状态: {status}")
            log_params("即梦任务状态", status=status)
            last_status = status

        if status == "done":
            return result
        if status in ("not_found", "expired"):
            raise RuntimeError(f"即梦任务{status}，task_id={task_id}")

        time.sleep(poll_interval)

    raise TimeoutError(f"即梦任务超时，task_id={task_id}")


# ---------------------------------------------------------------------------
# 图片处理
# ---------------------------------------------------------------------------

def resolve_image(image_source: str | Path) -> dict:
    """将图片源解析为即梦 API 所需的格式。返回 URL 或 base64。"""
    source = Path(image_source)
    if source.exists():
        mime_type, _ = mimetypes.guess_type(source.name)
        if mime_type is None:
            mime_type = "image/jpeg"
        encoded = base64.b64encode(source.read_bytes()).decode("ascii")
        return {"binary_data_base64": [encoded]}

    url_str = str(image_source)
    if "://" in url_str:
        return {"image_urls": [url_str]}

    raise FileNotFoundError(f"图片路径不存在，也不是有效的 URL: {image_source}")


# ---------------------------------------------------------------------------
# 场景判断
# ---------------------------------------------------------------------------

def determine_scene(
    first_frame_url: str | None = None,
    last_frame_url: str | None = None,
) -> str:
    if not first_frame_url and not last_frame_url:
        return "text_to_video"
    if last_frame_url:
        return "first_last_frame_to_video"
    return "first_frame_to_video"


def resolve_req_key(
    scene: str,
    resolution: str,
    manual_key: str | None = None,
) -> str:
    """获取 req_key：手动指定优先，否则从映射表推导。"""
    if manual_key:
        return manual_key
    key = REQ_KEY_MAP.get((scene, resolution))
    if key is None:
        raise ValueError(f"不支持的组合: scene={scene}, resolution={resolution}")
    return key


# ---------------------------------------------------------------------------
# 构建请求体
# ---------------------------------------------------------------------------

def build_submit_body(
    req_key: str,
    prompt: str,
    first_frame_url: str | None = None,
    last_frame_url: str | None = None,
    seed: int | None = None,
    frames: int | None = None,
    aspect_ratio: str | None = None,
) -> dict:
    """构建提交任务的请求体。"""
    body: dict = {"req_key": req_key, "prompt": prompt}

    # 图片参数
    if first_frame_url and last_frame_url:
        # 首尾帧模式：需要两张图
        first_img = resolve_image(first_frame_url)
        last_img = resolve_image(last_frame_url)
        images = first_img.get("binary_data_base64", []) + last_img.get("binary_data_base64", [])
        urls = first_img.get("image_urls", []) + last_img.get("image_urls", [])
        if images:
            body["binary_data_base64"] = images
        if urls:
            body["image_urls"] = urls
    elif first_frame_url:
        # 首帧模式：只需一张图
        img = resolve_image(first_frame_url)
        body.update(img)
    # 注意：图生视频模式不支持 aspect_ratio

    if seed is not None:
        body["seed"] = seed
    if frames is not None:
        body["frames"] = frames
    if aspect_ratio and not first_frame_url:
        # aspect_ratio 仅在文生视频模式下有效
        body["aspect_ratio"] = aspect_ratio

    return body


# ---------------------------------------------------------------------------
# 参数解析
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="即梦 3.0 视频生成")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="提示词")
    parser.add_argument("--name", default="", help="文件名描述，不超过 10 个中文字")
    parser.add_argument(
        "--first-frame-url",
        help="首帧图片 URL 或本地路径（图生视频）",
    )
    parser.add_argument(
        "--last-frame-url",
        help="尾帧图片 URL 或本地路径（首尾帧图生视频）",
    )
    parser.add_argument(
        "--resolution",
        default="720p",
        choices=["720p", "1080p"],
        help="分辨率，默认 720p",
    )
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument(
        "--frames",
        type=int,
        choices=[121, 241],
        help="总帧数：121(5s) / 241(10s)，默认 121",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        choices=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9"],
        help="视频长宽比（仅文生视频），默认 16:9",
    )
    parser.add_argument(
        "--req-key",
        help="手动指定 req_key，不传则根据模式和分辨率自动推导",
    )
    parser.add_argument(
        "--poll",
        action="store_true",
        default=False,
        help="创建后自动轮询并下载",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="轮询间隔秒数，默认 10",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="轮询超时秒数，默认 900",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main() -> None:
    pipeline_start = time.monotonic()
    args = parse_args()
    ak, sk = load_credentials()
    trace_id = get_trace_id()

    scene = determine_scene(args.first_frame_url, args.last_frame_url)
    req_key = resolve_req_key(scene, args.resolution, args.req_key)

    image_refs = []
    if args.first_frame_url:
        image_refs.append(args.first_frame_url)
    if args.last_frame_url:
        image_refs.append(args.last_frame_url)
    log_params(
        "即梦视频任务开始",
        scene=scene,
        req_key=req_key,
        resolution=args.resolution,
        prompt=args.prompt,
        name=args.name,
        frames=args.frames or "(默认121/5s)",
        aspect_ratio=args.aspect_ratio if not args.first_frame_url else "(图生视频忽略)",
        images=image_refs or "(无)",
    )

    # 构建请求体
    submit_body = build_submit_body(
        req_key=req_key,
        prompt=args.prompt,
        first_frame_url=args.first_frame_url,
        last_frame_url=args.last_frame_url,
        seed=args.seed,
        frames=args.frames,
        aspect_ratio=args.aspect_ratio if not args.first_frame_url else None,
    )

    # 提交任务
    print(f"创建即梦视频任务: req_key={req_key}")
    api_start = time.monotonic()
    submit_result = submit_task(ak, sk, submit_body)
    api_elapsed = time.monotonic() - api_start

    task_id = submit_result.get("data", {}).get("task_id", "")
    print(f"任务已创建: {task_id}")
    log_params("即梦任务创建完成", task_id=task_id, api_elapsed=round(api_elapsed, 3))

    create_output = {
        "type": "video",
        "scene": scene,
        "provider": "jimeng",
        "model_version": "3.0",
        "trace_id": trace_id,
        "task_id": task_id,
        "req_key": req_key,
        "resolution": args.resolution,
        "status": "in_queue",
        "timing": {
            "total_elapsed": round(time.monotonic() - pipeline_start, 3),
            "api_elapsed": round(api_elapsed, 3),
        },
    }
    print(json.dumps(create_output, ensure_ascii=False, indent=2))

    if not args.poll:
        return

    # 轮询
    print(f"\n开始轮询任务: {task_id}")
    log_params("开始轮询即梦任务", task_id=task_id, interval=args.poll_interval, timeout=args.timeout)
    poll_start = time.monotonic()
    final_result = wait_for_task(
        ak, sk, req_key, task_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    poll_elapsed = time.monotonic() - poll_start

    video_url = final_result.get("data", {}).get("video_url", "")
    if not video_url:
        raise RuntimeError(f"即梦任务完成但未返回 video_url: {json.dumps(final_result, ensure_ascii=False)}")
    print(f"视频生成成功，开始下载...")
    log_params("即梦视频生成成功", task_id=task_id, poll_elapsed=round(poll_elapsed, 3))

    output_path = default_output_path("videos", scene, suffix=".mp4", name=args.name, tag=args.resolution)
    download_file(video_url, output_path)
    log_params("即梦视频下载完成", path=str(output_path.name))

    poll_output = {
        "type": "video",
        "scene": scene,
        "provider": "jimeng",
        "model_version": "3.0",
        "trace_id": trace_id,
        "task_id": task_id,
        "req_key": req_key,
        "resolution": args.resolution,
        "local_path": str(output_path.relative_to(OUTPUT_ROOT)),
        "source_url": video_url,
        "timing": {
            "total_elapsed": round(time.monotonic() - pipeline_start, 3),
            "api_elapsed": round(api_elapsed, 3),
            "poll_elapsed": round(poll_elapsed, 3),
        },
    }
    log_params("即梦视频任务完成", task_id=task_id, total_elapsed=round(time.monotonic() - pipeline_start, 3))
    print(json.dumps(poll_output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
