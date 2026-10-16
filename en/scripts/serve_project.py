#!/usr/bin/env python3
"""Serve the intake form and save its data directly into the project workspace."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


MAX_BRIEF_BYTES = 5 * 1024 * 1024
MAX_ASSET_BYTES = 200 * 1024 * 1024
ASSET_NAME = re.compile(r"^ASSET-\d+_[^/\\]+$")


class ProjectFormHandler(BaseHTTPRequestHandler):
    project_root: Path

    def _send_json(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self, limit: int) -> bytes:
        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            raise ValueError("Missing Content-Length")
        length = int(raw_length)
        if length < 0 or length > limit:
            raise ValueError(f"Request body exceeds the {limit} byte limit")
        body = self.rfile.read(length)
        if len(body) != length:
            raise ValueError("Incomplete request body")
        return body

    @staticmethod
    def _atomic_write(path: Path, data: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        temporary.replace(path)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/status":
            self._send_json(
                200,
                {
                    "ready": True,
                    "project_root": str(self.project_root),
                },
            )
            return
        if path in ("/", "/intake-form.html"):
            form = self.project_root / "intake-form.html"
            if not form.is_file():
                self._send_json(404, {"error": f"Missing form: {form}"})
                return
            body = form.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        self._send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            if path == "/api/brief":
                payload = json.loads(self._read_body(MAX_BRIEF_BYTES).decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("Brief must be a JSON object")
                destination = self.project_root / "brief.json"
                encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
                self._atomic_write(destination, encoded)
                self._send_json(
                    200,
                    {
                        "saved": str(destination),
                        "project_root": str(self.project_root),
                    },
                )
                return

            prefix = "/api/assets/"
            if path.startswith(prefix):
                filename = unquote(path[len(prefix) :])
                if not ASSET_NAME.fullmatch(filename):
                    raise ValueError("Invalid supplied-asset filename")
                body = self._read_body(MAX_ASSET_BYTES)
                destination = self.project_root / "source" / "supplied-assets" / filename
                self._atomic_write(destination, body)
                self._send_json(
                    200,
                    {
                        "saved": str(destination),
                        "project_root": str(self.project_root),
                    },
                )
                return

            self._send_json(404, {"error": "Not found"})
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            self._send_json(400, {"error": str(exc)})
        except OSError as exc:
            self._send_json(500, {"error": f"Cannot save project data: {exc}"})

    def log_message(self, format: str, *args: object) -> None:
        print(f"[form] {self.address_string()} - {format % args}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project_root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Project directory containing intake-form.html",
    )
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    form = project_root / "intake-form.html"
    if not form.is_file():
        raise SystemExit(f"Missing intake form: {form}")

    handler = type(
        "BoundProjectFormHandler",
        (ProjectFormHandler,),
        {"project_root": project_root},
    )
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Project workspace: {project_root}")
    print(f"Open: http://127.0.0.1:{args.port}/intake-form.html")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

