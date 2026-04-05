# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "requests",
# ]
# ///

from __future__ import annotations

import argparse
import datetime
import hashlib
import hmac
import json
import os
import time
from pathlib import Path

import requests

from common import OUTPUT_ROOT, get_trace_id, log_params, setup_logging

setup_logging()

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

HOST = "visual.volcengineapi.com"
REGION = "cn-north-1"
ENDPOINT = f"https://{HOST}"
SERVICE = "cv"
VERSION = "2022-08-31"


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
    action: str,
    access_key: str,
    secret_key: str,
    body: str,
) -> dict[str, str]:
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
        f"POST\n{canonical_uri}\n{canonical_querystring}\n"
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

    config_path = OUTPUT_ROOT / "api_key" / "jimeng.json"
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        ak = config.get("access_key", "")
        sk = config.get("secret_key", "")
        if ak and sk:
            return ak, sk

    raise OSError(f"未设置环境变量 VOLC_ACCESS_KEY/VOLC_SECRET_KEY，也未找到配置文件: {config_path}")


def query_task(ak: str, sk: str, req_key: str, task_id: str) -> dict:
    body = json.dumps({"req_key": req_key, "task_id": task_id}, ensure_ascii=False)
    signed = _sign_request("CVSync2AsyncGetResult", ak, sk, body)
    resp = requests.post(signed["url"], headers=signed["headers"], data=body, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# 参数解析
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查询即梦 3.0 视频任务状态")
    parser.add_argument("--task-id", required=True, help="即梦任务 ID")
    parser.add_argument(
        "--req-key",
        default="jimeng_t2v_v30",
        help="模型 req_key，默认 jimeng_t2v_v30（720p 文生视频）",
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

    log_params("查询即梦视频任务", task_id=args.task_id, req_key=args.req_key)
    api_start = time.monotonic()
    result = query_task(ak, sk, args.req_key, args.task_id)
    api_elapsed = time.monotonic() - api_start

    data = result.get("data", {})
    status = data.get("status", "") if isinstance(data, dict) else ""

    output: dict = {
        "trace_id": trace_id,
        "task_id": args.task_id,
        "req_key": args.req_key,
        "code": result.get("code"),
        "status": status,
    }

    if status == "done":
        video_url = data.get("video_url", "") if isinstance(data, dict) else ""
        if video_url:
            output["video_url"] = video_url
    elif result.get("code") not in (10000, None):
        output["message"] = result.get("message", "")

    log_params(
        "即梦查询完成",
        task_id=args.task_id,
        status=status,
        code=result.get("code"),
        api_elapsed=round(api_elapsed, 3),
    )

    total_elapsed = time.monotonic() - pipeline_start
    output["timing"] = {
        "total_elapsed": round(total_elapsed, 3),
        "api_elapsed": round(api_elapsed, 3),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
