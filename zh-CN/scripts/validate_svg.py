#!/usr/bin/env python3
"""Validate editable-SVG requirements for cultural-event key visuals."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


SVG_NS = "http://www.w3.org/2000/svg"
XLINK = "{http://www.w3.org/1999/xlink}href"
FORBIDDEN_TAGS = {"script", "foreignObject", "animate", "animateMotion", "animateTransform", "set"}
VECTOR_TAGS = {"path", "rect", "circle", "ellipse", "polygon", "polyline", "line"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def numeric_dimension(value: str | None) -> bool:
    return bool(value and re.fullmatch(r"\s*\d+(?:\.\d+)?(?:px|pt|mm|cm|in)?\s*", value))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg", type=Path)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    try:
        root = ET.parse(args.svg).getroot()
    except Exception as exc:
        result = {"valid": False, "errors": [f"Cannot parse SVG/XML: {exc}"], "warnings": []}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0])
        return 1

    if local_name(root.tag) != "svg":
        errors.append("Root element is not svg")
    if not numeric_dimension(root.get("width")):
        errors.append("Root width is missing or non-numeric")
    if not numeric_dimension(root.get("height")):
        errors.append("Root height is missing or non-numeric")
    view_box = root.get("viewBox")
    if not view_box or len(view_box.replace(",", " ").split()) != 4:
        errors.append("viewBox must contain four numbers")

    groups: list[str] = []
    text_count = 0
    image_count = 0
    unnamed_images = 0
    visual_base_count = 0
    original_asset_count = 0
    unclassified_images = 0
    vector_count = 0

    for element in root.iter():
        name = local_name(element.tag)
        if name in FORBIDDEN_TAGS:
            errors.append(f"Forbidden SVG element: {name}")
        if name == "g":
            group_id = element.get("id")
            if group_id:
                groups.append(group_id)
        elif name in {"text", "tspan"}:
            text_count += 1
        elif name == "image":
            image_count += 1
            image_id = element.get("id")
            if not image_id:
                unnamed_images += 1
            href = element.get("href") or element.get(XLINK) or ""
            source_kind = element.get("data-source-kind", "")
            if source_kind == "imagegen-visual-base":
                visual_base_count += 1
                if image_id != "imagegen-visual-base":
                    errors.append("The cleaned ImageGen base must use id=imagegen-visual-base")
                href_lower = href.lower()
                if not (href_lower.startswith("data:image/png") or href_lower.split("?", 1)[0].endswith(".png")):
                    errors.append("The ImageGen visual base must reference PNG data")
            elif source_kind == "original-upload":
                original_asset_count += 1
            else:
                unclassified_images += 1
            parsed = urlparse(href)
            if parsed.scheme in {"http", "https"}:
                errors.append(f"Remote image URL is not portable: {href}")
            elif href and not href.startswith("data:") and args.project_root:
                candidate = (args.svg.parent / href).resolve()
                if not candidate.exists():
                    errors.append(f"Missing linked image: {candidate}")
        elif name in VECTOR_TAGS:
            vector_count += 1

        for attribute in element.attrib:
            if local_name(attribute).lower().startswith("on"):
                errors.append(f"Event-handler attribute is forbidden: {attribute}")

    if not groups:
        errors.append("No named group layers found")
    elif len(groups) < 3:
        warnings.append("Fewer than three named groups; editability may be poor")
    for required_group in ("visual-base", "original-assets", "editable-text"):
        if required_group not in groups:
            errors.append(f"Missing required SVG group: {required_group}")
    if text_count == 0:
        errors.append("No editable text elements found")
    if visual_base_count != 1:
        errors.append(f"Exactly one cleaned ImageGen visual base is required; found: {visual_base_count}")
    if unclassified_images:
        errors.append(f"Every image must declare data-source-kind; unclassified images: {unclassified_images}")
    if unnamed_images:
        errors.append(f"Image material must use named independent layers; unnamed image elements: {unnamed_images}")
    if len(set(groups)) != len(groups):
        errors.append("Duplicate group IDs found")

    result = {
        "valid": not errors,
        "metrics": {
            "named_groups": len(groups),
            "editable_text_elements": text_count,
            "image_elements": image_count,
            "unnamed_image_elements": unnamed_images,
            "imagegen_visual_base_elements": visual_base_count,
            "original_upload_elements": original_asset_count,
            "unclassified_image_elements": unclassified_images,
            "vector_elements": vector_count,
        },
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("VALID" if result["valid"] else "INVALID")
        print(json.dumps(result["metrics"], ensure_ascii=False))
        for message in result["errors"]:
            print(f"ERROR: {message}")
        for message in result["warnings"]:
            print(f"WARNING: {message}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
