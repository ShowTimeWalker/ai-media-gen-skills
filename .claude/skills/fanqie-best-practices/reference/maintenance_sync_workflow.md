# 维护同步流程（模式 B）

> 在用户明确要求「同步官网 / 更新本 Skill」时执行。须遵守法律法规与目标站点规则；自动化访问可能触发风控或违反服务条款，**由使用者自行评估与承担责任**。

## 1. 目标

- 从**公开可访问**页面生成一次可追溯快照（时间戳、URL、摘录）。
- 将经核实的增量合并进本 Skill 的 `reference/`，**禁止**把未经确认的猜测写进正文。

## 2. 环境准备

- 使用 `uv` 时先安装依赖：`uv add playwright beautifulsoup4`（若尚未安装；依赖通常在工作区根目录的 `pyproject.toml` 中）。
- 首次使用需安装浏览器内核（在含依赖的环境中执行）：

```text
uv run playwright install chromium
```

## 3. 同步脚本位置与执行指令

- **可执行文件**（相对本 Skill 根目录 `fanqie-best-practices/`）：`scripts/fanqie_official_sync.py`
- **输出目录**：在环境变量 `OUTPUT_ROOT` 指向的根下创建  
  `{OUTPUT_ROOT}/outputs/fanqie_skill_sync/<时间戳>/`，内含 `digest.md`、`raw.json`、`errors.log`。
- **可选环境变量**：`FANQIE_BASE_URL`、`FANQIE_SYNC_URLS`（英文逗号分隔额外 URL）、`FANQIE_HEADLESS`、`FANQIE_TIMEOUT_MS`、`FANQIE_DELAY_S`、`FANQIE_HTTP_ONLY`（设为 `1` 时跳过 Playwright，仅用 HTTP）、`FANQIE_HTTP_TIMEOUT_S`（HTTP 超时秒数，默认 30）。
- **HTTP 自动回退**：若本机未安装 Playwright Chromium，或 Playwright 启动失败，或所有页面在浏览器内均失败，脚本会**自动**用 `urllib` 拉取 HTML 再解析（`digest` / `raw.json` 中 `fetch_mode` 为 `http`）。站点若为纯前端渲染，正文里可能出现 `You need to enable JavaScript`，此时需装好 Chromium 后改用 Playwright。
- **附录 §7**：若与 `scripts/fanqie_official_sync.py` 不一致，以 `.py` 为准。

**在工作区根目录**打开终端（使 `uv` 能解析工作区依赖），执行示例：

PowerShell：

```powershell
$env:OUTPUT_ROOT = "D:\Your\OutputRoot"
uv run python .claude/skills/fanqie-best-practices/scripts/fanqie_official_sync.py
```

cmd：

```bat
set OUTPUT_ROOT=D:\Your\OutputRoot
uv run python .claude/skills/fanqie-best-practices/scripts/fanqie_official_sync.py
```

- 若所有页面渲染失败，进程退出码为 `2`，并提示安装 Chromium；仍会在上述目录生成 `digest.md` / `raw.json` 便于排查。

## 4. 合并规则

1. **稳定知识**（规则、长期写作指引）：可斟酌合并入 `platform_writing_guide.md` 或 `compliance_and_format.md`，并保证表述为「摘要 + 以平台最新为准」。
2. **易变信息**（活动标题、榜单、短期政策）：写入 `sourced_snapshots_index.md`，格式为：日期、来源 URL、摘录要点；避免把榜单书名写进长期基线正文。
3. **不得**合并：需登录后台才能看到的内容、其他用户隐私、明显未经验证的传言。

## 5. Diff 闸门（必须）

- 在修改任何 `reference/*.md` 或 `SKILL.md` 之前，向用户展示：将改哪些文件、每处改动的理由、原文摘录来源。
- 用户确认后再写入。不要代替用户做 git 提交。

## 6. 失败处理

- 若 `errors.log` 非空或 `raw.json` 中关键字段为空，应优先修复脚本选择器或改用手动摘录，**禁止**用臆造榜单或政策文本凑数。

## 7. 附录：同步脚本全文

> 与 `scripts/fanqie_official_sync.py` 保持一致；**修改逻辑时请同时更新**该 `.py` 与本附录，避免漂移。

```python
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
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import sys
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


async def snapshot_page(
    page,
    url: str,
    timeout_ms: int,
    logger: logging.Logger,
) -> dict:
    out: dict = {"url": url, "title": None, "links": [], "text_preview": None, "error": None}
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        await asyncio.sleep(min(3.0, float(os.environ.get("FANQIE_DELAY_S", "2.0"))))
        html = await page.content()
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
        logger.exception("页面抓取失败: %s", url)
    return out


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
        logger.exception("Playwright 启动或浏览失败: %s", e)
        pages.append(
            {
                "url": base,
                "title": None,
                "links": [],
                "text_preview": None,
                "error": repr(e),
            }
        )

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
        print(f"已写入快照目录（页面渲染失败）：{run_dir}", file=sys.stderr)
        print(
            "请先执行：uv run playwright install chromium",
            file=sys.stderr,
        )
        return 2
    print(f"完成。输出目录：{run_dir}")
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(main_async()))


if __name__ == "__main__":
    main()
```
