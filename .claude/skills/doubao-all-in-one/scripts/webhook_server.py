# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "flask",
# ]
# ///

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, request, jsonify

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_DB_PATH = PROJECT_ROOT / "outputs" / "doubao" / "video_tasks.db"


def create_app(db_path: Path | str | None = None) -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)
    db = str(db_path or DEFAULT_DB_PATH)
    db_path_obj = Path(db)
    db_path_obj.parent.mkdir(parents=True, exist_ok=True)

    log_file = db_path_obj.parent / "webhook.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(str(log_file)), logging.StreamHandler()],
    )

    def get_conn() -> sqlite3.Connection:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db() -> None:
        conn = get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS video_generation_tasks (
                task_id TEXT PRIMARY KEY,
                model TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL,
                service_tier TEXT NOT NULL,
                execution_expires_after INTEGER NOT NULL,
                video_url TEXT,
                last_callback_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        logging.info("Database initialized")

    init_db()

    @app.route("/webhook/callback", methods=["POST"])
    def video_task_callback() -> tuple[Any, int]:
        """Core interface for receiving Ark callback."""
        try:
            callback_data = request.get_json(force=True, silent=True)
            if not callback_data:
                logging.error("Callback request body empty or non-JSON")
                return jsonify({"code": 400, "msg": "Invalid JSON data"}), 400

            required_fields = [
                "id", "model", "status", "created_at",
                "updated_at", "service_tier", "execution_expires_after",
            ]
            missing = [f for f in required_fields if f not in callback_data]
            if missing:
                logging.error(f"Missing fields: {missing}")
                return jsonify({"code": 400, "msg": f"Missing fields: {missing}"}), 400

            task_id = callback_data["id"]
            status = callback_data["status"]
            model = callback_data["model"]
            logging.info(f"Task callback | id={task_id} | status={status} | model={model}")

            # Extract video_url if present (succeeded tasks)
            video_url = ""
            content = callback_data.get("content")
            if isinstance(content, dict):
                video_url = content.get("video_url", "")

            conn = get_conn()
            conn.execute("""
                INSERT INTO video_generation_tasks (
                    task_id, model, status, created_at, updated_at,
                    service_tier, execution_expires_after, video_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET
                    status = excluded.status,
                    updated_at = excluded.updated_at,
                    video_url = COALESCE(excluded.video_url, video_generation_tasks.video_url),
                    last_callback_at = CURRENT_TIMESTAMP
            """, (
                task_id, model, status,
                callback_data["created_at"], callback_data["updated_at"],
                callback_data["service_tier"], callback_data["execution_expires_after"],
                video_url,
            ))
            conn.commit()
            conn.close()

            output = {
                "type": "video",
                "scene": "webhook_callback",
                "provider": "doubao",
                "task_id": task_id,
                "status": status,
            }
            if video_url:
                output["video_url"] = video_url

            print(json.dumps(output, ensure_ascii=False, indent=2))
            return jsonify({"code": 200, "msg": "ok", "task_id": task_id}), 200

        except Exception as e:
            logging.error(f"Callback processing failed: {e}", exc_info=True)
            # Always return 200 to avoid Ark API retry storms
            return jsonify({"code": 200, "msg": "received (internal error)"}), 200

    @app.route("/tasks/<task_id>", methods=["GET"])
    def get_task_status(task_id: str) -> tuple[Any, int]:
        """Query latest status of a task."""
        conn = get_conn()
        row = conn.execute(
            "SELECT * FROM video_generation_tasks WHERE task_id = ?", (task_id,)
        ).fetchone()
        conn.close()
        if not row:
            return jsonify({"code": 404, "msg": "Task not found"}), 404
        return jsonify({"code": 200, "data": dict(row)}), 200

    @app.route("/tasks", methods=["GET"])
    def list_tasks() -> tuple[Any, int]:
        """List all tasks, optional ?status= filter."""
        status_filter = request.args.get("status")
        conn = get_conn()
        if status_filter:
            rows = conn.execute(
                "SELECT * FROM video_generation_tasks WHERE status = ? ORDER BY last_callback_at DESC",
                (status_filter,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM video_generation_tasks ORDER BY last_callback_at DESC"
            ).fetchall()
        conn.close()
        return jsonify({"code": 200, "data": [dict(r) for r in rows]}), 200

    return app


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="豆包视频生成 Webhook 回调服务器")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=8888, help="监听端口")
    parser.add_argument("--db", default=None, help="SQLite 数据库路径")
    args = parser.parse_args()

    app = create_app(db_path=args.db)
    logging.info(f"Starting webhook server on {args.host}:{args.port}")
    print(f"Webhook server listening on http://{args.host}:{args.port}")
    print(f"POST /webhook/callback — 接收 Ark 回调")
    print(f"GET  /tasks/<task_id>  — 查询任务状态")
    print(f"GET  /tasks            — 列出所有任务")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
