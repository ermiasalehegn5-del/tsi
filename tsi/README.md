# Tsi's birthday site — with a Python backend

The guestbook is now backed by a real Python server (Flask) and a
SQLite database file (`guestbook.db`), instead of browser-only storage.
Messages persist as long as this folder and `guestbook.db` exist —
including across different visitors, browsers, and devices, as long
as they're hitting the same running server.

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser.

## What's inside

- `app.py` — the Flask server. Serves `index.html` and exposes:
  - `GET /api/guestbook` — returns all signed messages as JSON
  - `POST /api/guestbook` — adds a new message, expects `{"name": "...", "message": "..."}`
- `index.html` — the site itself; its guestbook JS now calls the two
  endpoints above with `fetch` instead of using in-browser storage.
- `guestbook.db` — created automatically the first time you run
  `app.py`. Delete it if you ever want to wipe all messages and start over.

## Sharing it with Tsi

`localhost` only works on your own machine. To let her actually sign
it from her phone or computer, you'll need to host `app.py` somewhere
reachable — a small always-on server, or a free host that supports
Python (PythonAnywhere, Render, Railway, etc.). Happy to help set
that up if you want to go that route.
