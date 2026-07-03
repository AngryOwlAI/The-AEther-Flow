#!/usr/bin/env python3
"""Validate the v15 P11-T01 validation command inventory artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
INVENTORY_PATH = REPO_ROOT / "research_control/design/validation_command_inventory_v15.md"

REQUIRED_CATEGORIES = [
    "memory bootstrap",
    "memory validate-only",
    "research-control validation",
    "research-control diff validation",
    "claim-language changed-file lint",
    "documentation-impact validation",
    "registry consistency",
    "current frontier render check",
    "dependency graph check",
    "theorem inventory check",
    "route-orbit check",
    "source-extension classification check",
    "project-control smoke tests",
]

REQUIRED_PHRASES = [
    "Command Inventory",
    "Purpose",
    "Authority level",
    "When required",
    "Minimal P11-T02 Local CI Sequence",
    "operational receipts only",
    "No physics delta",
]

FORBIDDEN_PROMOTIONS = [
    "validation proves physics",
    "ci proves physics",
    "tests prove physics",
    "generated registries prove physics",
]


def sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 5:
            rows.append(cells)
    return rows


def validate() -> dict[str, object]:
    errors: list[str] = []
    text = INVENTORY_PATH.read_text(encoding="utf-8") if INVENTORY_PATH.exists() else ""
    lower = text.lower()

    if not INVENTORY_PATH.exists():
        errors.append(f"missing inventory: {INVENTORY_PATH.relative_to(REPO_ROOT)}")

    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower:
            errors.append(f"missing required phrase: {phrase}")

    for category in REQUIRED_CATEGORIES:
        if f"| {category} |" not in lower:
            errors.append(f"missing required category row: {category}")

    rows = inventory_rows(text)
    data_rows = [
        row
        for row in rows
        if row[0].lower() not in {"category", "---", "level"}
        and not all(set(cell) <= {"-"} for cell in row)
    ]
    for row in data_rows:
        if len(row) < 5:
            errors.append(f"inventory row has fewer than five columns: {row}")
            continue
        category, command, purpose, authority_level, when_required = row[:5]
        if category.lower() in {"level"}:
            continue
        for label, value in [
            ("command", command),
            ("purpose", purpose),
            ("authority_level", authority_level),
            ("when_required", when_required),
        ]:
            if not value or value == "---":
                errors.append(f"{category}: missing {label}")

    for phrase in FORBIDDEN_PROMOTIONS:
        if phrase in lower:
            errors.append(f"forbidden promotion phrase present: {phrase}")

    return {
        "schema_id": "p11_t01_validation_command_inventory_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "inventory_path": str(INVENTORY_PATH.relative_to(REPO_ROOT)),
        "inventory_hash": sha256(INVENTORY_PATH) if INVENTORY_PATH.exists() else "",
        "required_categories_checked": REQUIRED_CATEGORIES,
        "required_phrase_count": len(REQUIRED_PHRASES),
        "inventory_row_count": len(data_rows),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
