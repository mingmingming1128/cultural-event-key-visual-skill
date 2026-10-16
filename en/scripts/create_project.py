#!/usr/bin/env python3
"""Create a cultural-event key-visual project with a fillable intake form."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


def slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
    if not value:
        raise ValueError("Project name must contain letters or digits.")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name")
    parser.add_argument("--output-root", type=Path, default=Path.cwd())
    parser.add_argument("--prefill", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    project = args.output_root.resolve() / slug(args.project_name)
    template = Path(__file__).resolve().parent.parent / "assets" / "intake-form-template.html"
    server_template = Path(__file__).resolve().parent / "serve_project.py"
    target = project / "intake-form.html"

    if target.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing form: {target}")

    prefill: object = {}
    if args.prefill:
        with args.prefill.open("r", encoding="utf-8") as stream:
            prefill = json.load(stream)

    project.mkdir(parents=True, exist_ok=True)
    for relative in (
        "source/supplied-assets",
        "generations/high-fi",
        "approved",
        "svg-reconstruction",
        "final",
        "previews",
    ):
        (project / relative).mkdir(parents=True, exist_ok=True)

    html = template.read_text(encoding="utf-8")
    embedded = json.dumps(prefill, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__PREFILL_JSON__", embedded)
    target.write_text(html, encoding="utf-8")
    shutil.copy2(server_template, project / "serve-form.py")

    manifest = {
        "project_slug": project.name,
        "stage": "intake",
        "imagegen_revision": 0,
        "imagegen_approved": False,
        "approved_imagegen_version": None,
        "svg_reconstruction_started": False,
        "svg_validated": False,
    }
    (project / "workflow-state.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(target)
    print(f"Run: python {project / 'serve-form.py'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
