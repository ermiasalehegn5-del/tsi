"""
Backend for Tsi's birthday site.

Serves the static page and a tiny REST API that backs the guestbook
with a real SQLite database instead of browser storage.

Run:
    pip install -r requirements.txt
    python app.py

Then open http://localhost:5000 in a browser.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, g, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "guestbook.db"

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")


def get_db():
    """Open (or reuse) a SQLite connection for this request."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the guestbook table if it doesn't exist yet."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS guestbook (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


# ---------- page ----------

@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


# ---------- guestbook API ----------

@app.route("/api/guestbook", methods=["GET"])
def list_entries():
    db = get_db()
    rows = db.execute(
        "SELECT id, name, message, created_at FROM guestbook ORDER BY id ASC"
    ).fetchall()
    entries = [dict(row) for row in rows]
    return jsonify(entries)


@app.route("/api/guestbook", methods=["POST"])
def add_entry():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    name = (data.get("name") or "").strip() or "Anonymous"

    if not message:
        return jsonify({"error": "message is required"}), 400
    if len(message) > 280:
        return jsonify({"error": "message is too long (280 char max)"}), 400
    if len(name) > 40:
        return jsonify({"error": "name is too long (40 char max)"}), 400

    created_at = datetime.now(timezone.utc).isoformat()

    db = get_db()
    cur = db.execute(
        "INSERT INTO guestbook (name, message, created_at) VALUES (?, ?, ?)",
        (name, message, created_at),
    )
    db.commit()

    entry = {
        "id": cur.lastrowid,
        "name": name,
        "message": message,
        "created_at": created_at,
    }
    return jsonify(entry), 201


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
