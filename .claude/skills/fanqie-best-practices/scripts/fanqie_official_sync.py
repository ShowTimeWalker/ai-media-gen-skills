"""
从番茄小说等公开页生成一次只读快照，供维护本 Skill 时人工合并参考。

脚本位置：本 Skill 内 `.claude/skills/fanqie-best-practices/scripts/fanqie_official_sync.py`

用法（在工作区根目录执行，依赖已写入工作区 pyproject.toml）：
  set OUTPUT_ROOT=你的输出根目录
  uv run python .claude/skills/fanqie-best-practices/scripts/fanqie_official_sync.py

可选环境变量：
  FANQIE_BASE_URL   首页地址，默认 https://fanqienovel.com/
  FANQIE_SYNC_URLS  额外 URL，英文逗号分隔
  FANQIE_HEADLESS   默认 1；设为 0 时使用有头模式便于调试
  FANQIE_TIMEOUT_MS 页面超时毫秒，默认 60000
  FANQIE_DELAY_S    页面之间间隔秒数，默认 2.0
  FANQIE_HTTP_ONLY  设为 1 时跳过 Playwright，仅用 HTTP 拉取 HTML（无 JS 渲染）
  FANQIE_HTTP_TIMEOUT_S  HTTP 请求超时秒数，默认 30
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

DEFAULT_BASE = "https://fanqienovel.com/"


def _output_root() -> Path:
    raw = os.environ.get("OUTPUT_ROOT", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return Path.cwd().resolve()


def _run_dir(root: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    d = root / "outputs" / "fanqie_skill_sync" / stamp
    d.mkdir(parents=True, exist_ok=True)
    return d


def _setup_logging(run_dir: Path) -> logging.Logger:
    log_path = run_dir / "errors.log"
    logger = logging.getLogger("fanqie_official_sync")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(fh)
    return logger


def fetch_robots_txt(base: str, logger: logging.Logger) -> str | None:
    try:
        parsed = base.rstrip("/") + "/robots.txt"
        req = urllib.request.Request(
            parsed,
            headers={"User-Agent": "fanqie-official-sync/1.0 (personal snapshot)"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return body
    except (urllib.error.URLError, OSError, ValueError) as e:
        logger.warning("无法获取 robots.txt: %s", e)
        return None


def _parse_extra_urls() -> list[str]:
    raw = os.environ.get("FANQIE_SYNC_URLS", "").strip()
    if not raw:
        return []
    parts = [p.strip() for p in raw.split(",")]
    return [p for p in parts if p.startswith("http")]


def _snapshot_from_html(html: str, url: str, logger: logging.Logger, fetch_mode: str) -> dict:
    out: dict = {
        "url": url,
        "title": None,
        "links": [],
        "text_preview": None,
        "error": None,
        "fetch_mode": fetch_mode,
    }
    try:
        soup = BeautifulSoup(html, "html.parser")
        if soup.title and soup.title.string:
            out["title"] = soup.title.string.strip()
        seen: set[tuple[str, str]] = set()
        for a in soup.find_all("a", href=True):
            href = a.get("href", "").strip()
            text = re.sub(r"\s+", " ", a.get_text(" ", strip=True))[:120]
            if not href or len(text) < 1:
                continue
            key = (href, text)
            if key in seen:
                continue
            seen.add(key)
            out["links"].append({"href": href[:500], "text": text})
            if len(out["links"]) >= 80:
                break
        raw_text = soup.get_text("\n", strip=True)
        out["text_preview"] = raw_text[:8000] if raw_text else None
    except Exception as e:
        out["error"] = repr(e)
        logger.exception("解析 HTML 失败: %s", url)
    return out


def snapshot_page_http(url: str, logger: logging.Logger) -> dict:
    try:
        timeout = int(os.environ.get("FANQIE_HTTP_TIMEOUT_S", "30"))
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        return _snapshot_from_html(html, url, logger, "http")
    except Exception as e:
        logger.exception("HTTP 抓取失败: %s", url)
        return {
            "url": url,
            "title": None,
            "links": [],
            "text_preview": None,
            "error": repr(e),
            "fetch_mode": "http",
        }


async def snapshot_page(
    page,
    url: str,
    timeout_ms: int,
    logger: logging.Logger,
) -> dict:
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        await asyncio.sleep(min(3.0, float(os.environ.get("FANQIE_DELAY_S", "2.0"))))
        html = await page.content()
        return _snapshot_from_html(html, url, logger, "playwright")
    except Exception as e:
        logger.exception("页面抓取失败: %s", url)
        return {
            "url": url,
            "title": None,
            "links": [],
            "text_preview": None,
            "error": repr(e),
            "fetch_mode": "playwright",
        }


def snapshot_pages_http_all(urls: list[str], logger: logging.Logger) -> list[dict]:
    delay = float(os.environ.get("FANQIE_DELAY_S", "2.0"))
    pages: list[dict] = []
    for i, url in enumerate(urls):
        if i:
            time.sleep(delay)
        pages.append(snapshot_page_http(url, logger))
    return pages


def write_digest(run_dir: Path, payload: dict, logger: logging.Logger) -> None:
    lines: list[str] = []
    lines.append("# 番茄公开页同步摘要\n")
    lines.append(f"- **抓取 UTC 时间**：{payload['fetched_at_utc']}\n")
    lines.append(f"- **输出根目录**：{payload['output_root']}\n")
    if payload.get("robots_txt_excerpt"):
        lines.append("\n## robots.txt（节选）\n\n```\n")
        lines.append(payload["robots_txt_excerpt"][:4000])
        lines.append("\n```\n")
    for pg in payload.get("pages", []):
        lines.append(f"\n## 页面：{pg.get('url')}\n")
        if pg.get("fetch_mode"):
            lines.append(f"- **抓取方式**：{pg['fetch_mode']}\n")
        if pg.get("error"):
            lines.append(f"- **错误**：`{pg['error']}`\n")
        if pg.get("title"):
            lines.append(f"- **标题**：{pg['title']}\n")
        if pg.get("links"):
            lines.append("\n### 部分链接（截断）\n")
            for link in pg["links"][:25]:
                lines.append(f"- [{link['text']}]({link['href']})\n")
        if pg.get("text_preview"):
            lines.append("\n### 正文预览（截断）\n\n```\n")
            lines.append(pg["text_preview"][:2500])
            lines.append("\n```\n")
    path = run_dir / "digest.md"
    path.write_text("".join(lines), encoding="utf-8")
    logger.info("已写入 digest: %s", path)


async def main_async() -> int:
    root = _output_root()
    run_dir = _run_dir(root)
    logger = _setup_logging(run_dir)

    base = os.environ.get("FANQIE_BASE_URL", DEFAULT_BASE).strip() or DEFAULT_BASE
    timeout_ms = int(os.environ.get("FANQIE_TIMEOUT_MS", "60000"))
    headless = os.environ.get("FANQIE_HEADLESS", "1").strip() != "0"

    urls = [base]
    for u in _parse_extra_urls():
        if u not in urls:
            urls.append(u)

    robots = fetch_robots_txt(base, logger)
    robots_excerpt = robots[:6000] if robots else None

    pages: list[dict] = []
    http_only = os.environ.get("FANQIE_HTTP_ONLY", "").strip() == "1"

    if http_only:
        logger.info("FANQIE_HTTP_ONLY=1，使用 HTTP 抓取（无 JS 渲染）")
        pages = snapshot_pages_http_all(urls, logger)
    else:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=headless,
                    args=["--disable-blink-features=AutomationControlled"],
                )
                context = await browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                    locale="zh-CN",
                )
                page = await context.new_page()
                delay = float(os.environ.get("FANQIE_DELAY_S", "2.0"))
                for i, url in enumerate(urls):
                    if i:
                        await asyncio.sleep(delay)
                    pages.append(await snapshot_page(page, url, timeout_ms, logger))
                await browser.close()
        except Exception as e:
            logger.exception("Playwright 启动或浏览失败，改用 HTTP 回退: %s", e)
            pages = snapshot_pages_http_all(urls, logger)

        if pages and all(p.get("error") for p in pages):
            logger.warning("Playwright 全部页面失败，改用 HTTP 回退")
            pages = snapshot_pages_http_all(urls, logger)

    payload = {
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "output_root": str(root),
        "base_url": base,
        "urls": urls,
        "robots_txt_excerpt": robots_excerpt,
        "pages": pages,
    }
    (run_dir / "raw.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_digest(run_dir, payload, logger)
    if pages and all(p.get("error") for p in pages):
        print(f"已写入快照目录（全部 URL 均失败）：{run_dir}", file=sys.stderr)
        if not http_only:
            print(
                "可尝试：uv run playwright install chromium，或设置 FANQIE_HTTP_ONLY=1 使用 HTTP 回退",
                file=sys.stderr,
            )
        return 2
    print(f"完成。输出目录：{run_dir}")
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(main_async()))


if __name__ == "__main__":
    main()
