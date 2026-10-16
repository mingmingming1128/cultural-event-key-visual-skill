#!/usr/bin/env python3
"""Validate JSON exported by the cultural-event intake form."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FOR_CONCEPT = {
    "deliverable.type": "deliverable.type",
    "deliverable.languages": "deliverable.languages",
    "content_master.event_name": "content_master.event_name",
    "communication.goal": "communication.goal",
    "communication.audience": "communication.audience",
    "communication.channels": "communication.channels",
}

REQUIRED_V2 = (
    "activity.type",
    "activity.name",
    "communication.audience",
    "communication.goal",
    "delivery.languages",
    "delivery.items",
)

FACTS_TO_REVIEW = (
    "content_master.organizer",
    "content_master.event_date",
    "content_master.venue",
    "deliverable.width",
    "deliverable.height",
)


def get_path(data: dict[str, Any], path: str) -> Any:
    value: Any = data
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", type=Path)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--stage", choices=("intake", "imagegen", "concept"), default="imagegen")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    generation_stage = args.stage in ("imagegen", "concept")
    try:
        data = json.loads(args.brief.read_text(encoding="utf-8"))
    except Exception as exc:
        result = {"valid": False, "errors": [f"Cannot read JSON: {exc}"], "warnings": []}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0])
        return 1

    if not isinstance(data, dict):
        result = {"valid": False, "errors": ["Brief JSON must be an object"], "warnings": []}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.as_json else result["errors"][0])
        return 1

    is_v21 = data.get("schema_version") == "2.1"
    is_v22 = data.get("schema_version") == "2.2"
    is_v23 = data.get("schema_version") == "2.3"
    is_v24 = data.get("schema_version") == "2.4"
    is_v21_or_later = is_v21 or is_v22 or is_v23 or is_v24
    is_v22_or_later = is_v22 or is_v23 or is_v24
    is_v23_or_later = is_v23 or is_v24
    is_v2 = data.get("schema_version") in ("2.0", "2.1", "2.2", "2.3", "2.4")
    required = {path: path for path in REQUIRED_V2} if is_v2 else REQUIRED_FOR_CONCEPT
    for label, path in required.items():
        value = get_path(data, path)
        if value is None or value == "" or value == []:
            if is_v2:
                warnings.append(f"Optional field is blank; infer when needed: {label}")
            else:
                (errors if generation_stage else warnings).append(
                    f"Missing field to clarify: {label}"
                )

    facts_to_review = () if is_v2 else FACTS_TO_REVIEW
    for path in facts_to_review:
        if get_path(data, path) in (None, ""):
            warnings.append(f"Confirm whether this fact is required: {path}")

    confirmation = data.get("confirmation", {})
    if not isinstance(confirmation, dict):
        errors.append("confirmation must be an object")
        confirmation = {}
    if generation_stage:
        if confirmation.get("status") != "confirmed":
            errors.append("Demand analysis has not been explicitly confirmed")
        if not confirmation.get("reviewer"):
            errors.append("confirmation.reviewer is required before ImageGen generation")
    if not is_v2 and get_path(data, "intake.open_questions"):
        warnings.append("Open questions remain; reviewer must decide whether they affect ImageGen generation")

    if is_v2:
        delivery = data.get("delivery", {})
        if not isinstance(delivery, dict):
            errors.append("delivery must be an object")
            delivery = {}
        languages = delivery.get("languages", [])
        if not isinstance(languages, list):
            errors.append("delivery.languages must be a list")
            languages = []
        if "other" in languages and not str(delivery.get("other_language", "")).strip():
            warnings.append("Other language is selected but delivery.other_language is empty")
        items = delivery.get("items", [])
        if not isinstance(items, list):
            errors.append("delivery.items must be a list")
            items = []
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"delivery.items[{index}] must be an object")
                continue
            for field in ("type", "channel", "specification"):
                if not str(item.get(field, "")).strip():
                    warnings.append(f"Optional delivery field is blank; infer when needed: delivery.items[{index}].{field}")
            allowed_delivery_values = {
                "type": {"key-visual", "poster", "social-post", "social-cover", "banner", "invitation", "signage", "digital-screen", "other"},
                "channel": {"print", "venue", "wechat-official", "wechat-moments", "xiaohongshu", "weibo", "douyin", "website", "digital-display", "other"},
                "specification": {"1080x1080", "1242x1660", "1080x1350", "1080x1920", "1920x1080", "2:3", "3:2", "A3-portrait", "A2-portrait", "A1-portrait", "other"},
            }
            for field, allowed in allowed_delivery_values.items():
                value = str(item.get(field, "")).strip()
                if value and value not in allowed:
                    warnings.append(f"Delivery {field} uses a legacy or custom value: delivery.items[{index}].{field}")
        text_materials = data.get("text_materials", [])
        if not isinstance(text_materials, list):
            errors.append("text_materials must be a list")
            text_materials = []
        text_ids: set[str] = set()
        for index, item in enumerate(text_materials):
            if not isinstance(item, dict):
                errors.append(f"text_materials[{index}] must be an object")
                continue
            item_id = item.get("id")
            if not item_id or item_id in text_ids:
                errors.append(f"Missing or duplicate text material id: {item_id}")
            text_ids.add(item_id)
            allowed_categories = (
                "headline",
                "event-description",
                "event-time",
                "event-location",
                "organizer",
                "curatorial",
                "background",
                "person-work",
                "program",
                "participation",
                "credit",
                "legal",
                "translation",
                "other",
            ) if is_v21_or_later else ("background", "other", "verbatim")
            if item.get("category") not in allowed_categories:
                warnings.append(f"Text material category is blank or unrecognized; infer when needed: {item_id}")
            if is_v24:
                category_groups = {
                    "promotional-copy": ("headline", "event-description"),
                    "event-facts": ("event-time", "event-location", "organizer", "program", "participation"),
                    "cultural-content": ("curatorial", "background", "person-work"),
                    "credits-compliance": ("credit", "legal"),
                    "language-other": ("translation", "other"),
                }
                purpose_group = item.get("purpose_group")
                if purpose_group not in category_groups:
                    warnings.append(f"Text material purpose group is blank or unrecognized; infer when needed: {item_id}")
                elif item.get("category") and item.get("category") not in category_groups[purpose_group]:
                    errors.append(
                        f"Text material category does not match its purpose group: {item_id}"
                    )
            if is_v21_or_later:
                processing = item.get("processing")
                allowed_processing = ("editable", "full-verbatim", "generation-prompt") if is_v22_or_later else ("editable", "excerpt-verbatim", "full-verbatim")
                if processing not in allowed_processing:
                    warnings.append(f"Text processing requirement is blank or unrecognized; infer when needed: {item_id}")
                if is_v21 and processing == "excerpt-verbatim" and not str(item.get("verbatim_excerpt", "")).strip():
                    (errors if generation_stage else warnings).append(
                        f"Verbatim excerpt is empty: {item_id}"
                    )
                if is_v21 and processing == "excerpt-verbatim" and item.get("verbatim_excerpt") and item["verbatim_excerpt"] not in str(item.get("content", "")):
                    (errors if generation_stage else warnings).append(
                        f"Verbatim excerpt is absent from its text block: {item_id}"
                    )
            if not is_v21_or_later and item.get("missing_file_name"):
                warnings.append(f"{item_id}: reselect text file {item['missing_file_name']}")
            if not is_v21_or_later and args.project_root and item.get("saved_name"):
                expected = args.project_root / "source" / "text-materials" / item["saved_name"]
                if not expected.exists():
                    errors.append(f"Missing text material file: {expected}")
        if is_v21_or_later:
            communication = data.get("communication", {})
            qr_code = communication.get("qr_code", {}) if isinstance(communication, dict) else {}
            if qr_code.get("missing_file_name"):
                warnings.append("QR code image must be reselected")
            if args.project_root and qr_code.get("saved_name"):
                expected = args.project_root / "source" / "participation" / qr_code["saved_name"]
                if not expected.exists():
                    errors.append(f"Missing QR code image: {expected}")
            if is_v22_or_later and qr_code.get("saved_name") and qr_code.get("do_not_redraw") is not True:
                (errors if generation_stage else warnings).append(
                    "QR code must remain the original uploaded image"
                )
        if is_v21:
            supplementary = data.get("supplementary_sources", {})
            if not isinstance(supplementary, dict):
                errors.append("supplementary_sources must be an object")
                supplementary = {}
            for item in supplementary.get("pending_files", []):
                warnings.append(f"Reselect supplementary file: {item.get('original_name', '')}")
            for item in supplementary.get("files", []):
                if args.project_root and item.get("saved_name"):
                    expected = args.project_root / "source" / "supplementary-materials" / item["saved_name"]
                    if not expected.exists():
                        errors.append(f"Missing supplementary file: {expected}")
    else:
        width = get_path(data, "deliverable.width")
        height = get_path(data, "deliverable.height")
        if width is not None and (not isinstance(width, (int, float)) or width <= 0):
            errors.append("deliverable.width must be positive")
        if height is not None and (not isinstance(height, (int, float)) or height <= 0):
            errors.append("deliverable.height must be positive")

    assets = data.get("assets", [])
    if not isinstance(assets, list):
        errors.append("assets must be a list")
        assets = []
    ids: set[str] = set()
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append(f"assets[{index}] must be an object")
            continue
        asset_id = asset.get("id")
        if not asset_id:
            errors.append(f"assets[{index}] has no id")
        elif asset_id in ids:
            errors.append(f"Duplicate asset id: {asset_id}")
        else:
            ids.add(asset_id)
        if is_v2 and asset.get("role") not in ("required", "visual-reference"):
            warnings.append(f"Image use mode is blank; infer conservatively: {asset_id or index}")
        if is_v23_or_later and asset.get("purpose") not in (
            "hero",
            "background",
            "color-reference",
            "layout-reference",
            "style-reference",
            "composition-reference",
            "motif-reference",
            "other",
            None,
            "",
        ):
            warnings.append(f"Image purpose is unrecognized; infer when needed: {asset_id or index}")
        if args.project_root and asset.get("saved_name"):
            expected = args.project_root / "source" / "supplied-assets" / asset["saved_name"]
            if not expected.exists():
                errors.append(f"Missing supplied asset: {expected}")

    result = {"valid": not errors, "errors": errors, "warnings": warnings}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("VALID" if result["valid"] else "INVALID")
        for message in errors:
            print(f"ERROR: {message}")
        for message in warnings:
            print(f"WARNING: {message}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
