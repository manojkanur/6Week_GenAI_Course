"""
Flask API that triggers desktop editor automation (pyautogui).

Run locally:
  pip install flask pyautogui
  python app.py

Then:
  curl -s -X POST http://127.0.0.1:5000/api/type -H "Content-Type: application/json" -d '{"text":"Hi"}'

macOS: grant Accessibility to the terminal app running this server.
"""

from __future__ import annotations

import os

import pyautogui
from flask import Flask, jsonify, request

from open_editor_and_type import DEFAULT_TEXT, run_automation

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/api/type")
def api_type():
    """Open the text editor and type the given text (or default sample text)."""
    payload = request.get_json(silent=True)
    if payload is None and request.content_length not in (None, 0):
        return jsonify(error="Expected JSON body"), 400

    data = payload or {}
    text = data.get("text", DEFAULT_TEXT)
    if not isinstance(text, str):
        return jsonify(error="Field 'text' must be a string"), 400

    interval = data.get("interval", 0.02)
    try:
        interval = float(interval)
    except (TypeError, ValueError):
        return jsonify(error="Field 'interval' must be a number"), 400
    if interval < 0 or interval > 1:
        return jsonify(error="Field 'interval' must be between 0 and 1"), 400

    try:
        run_automation(text, interval=interval)
    except pyautogui.FailSafeException:
        return jsonify(error="pyautogui failsafe (mouse moved to screen corner)"), 500
    except Exception as exc:  # noqa: BLE001 — surface automation failures to client
        return jsonify(error=str(exc)), 500

    return jsonify(ok=True)


def main() -> None:
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    # debug=False: avoids reloader spawning a second process (bad for GUI automation)
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
