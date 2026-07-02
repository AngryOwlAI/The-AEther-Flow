#!/usr/bin/env python3
"""Render a derivative compact table from the canonical frontier inventory."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


TASK_ID = "RT-20260702-015"
JOB_ID = "AJ-RT-20260702-015-001"
SOURCE_OBJECT_ID = "MD-RESEARCH-CONTROL-DESIGN-FRONTIER-THEOREM-INVENTORY"
SCHEMA_OBJECT_ID = "MD-RESEARCH-CONTROL-DESIGN-FRONTIER-THEOREM-INVENTORY-SCHEMA-V1"

ROOT = Path(__file__).resolve().parents[4]
INVENTORY_PATH = ROOT / "research_control/design/frontier_theorem_inventory.md"
TABLE_PATH = ROOT / f"research_control/tasks/{TASK_ID}/artifacts/p7_t04_frontier_theorem_inventory_compact_table.md"
RECEIPT_PATH = ROOT / f"research_control/tasks/{TASK_ID}/artifacts/p7_t04_frontier_theorem_inventory_renderer_receipt.md"

ITEM_RE = re.compile(r"^### Item (?P<number>[0-9]+[A-Z]?): (?P<header>[A-Za-z0-9_]+)\s*$")
FIELD_RE = re.compile(r"^- `(?P<field>[A-Za-z0-9_]+)`: ?(?P<value>.*)$")

TABLE_FIELDS = [
    "frontier_item_id",
    "object_or_claim_name",
    "milestone",
    "object_type",
    "three_tier_classification",
    "linter_status",
    "authority_level",
    "source_artifact_path",
    "overread_guard",
    "next_theorem_needed",
]


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strip_markdown_value(value: str) -> str:
    text = value.strip()
    if text.startswith("`") and text.endswith("`") and text.count("`") == 2:
        text = text[1:-1]
    if text.startswith("`") and text.endswith("`.") and text.count("`") == 2:
        text = text[1:-2]
    text = text.replace("`", "")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("|", r"\|")
    return text or "none"


def append_continuation(current: str, line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("- "):
        stripped = stripped[2:].strip()
    return f"{current} {stripped}".strip()


def parse_inventory(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    current_field: str | None = None

    for line in lines:
        item_match = ITEM_RE.match(line)
        if item_match:
            current = {
                "_item_number": item_match.group("number"),
                "_item_header": item_match.group("header"),
            }
            items.append(current)
            current_field = None
            continue

        if current is None:
            continue

        if line.startswith("### "):
            current_field = None
            continue

        field_match = FIELD_RE.match(line)
        if field_match:
            field = field_match.group("field")
            if field not in current:
                current[field] = field_match.group("value").strip()
            current_field = field
            continue

        if current_field and line.startswith("  ") and not FIELD_RE.match(line.lstrip()):
            current[current_field] = append_continuation(current[current_field], line)

    required_missing = [
        f"{item.get('_item_header', 'unknown')}:{field}"
        for item in items
        for field in TABLE_FIELDS
        if not item.get(field)
    ]
    if required_missing:
        joined = ", ".join(required_missing[:20])
        raise SystemExit(f"Missing required compact-table fields: {joined}")

    ids = [item["frontier_item_id"].strip("`. ") for item in items]
    duplicate_ids = sorted({item_id for item_id in ids if ids.count(item_id) > 1})
    if duplicate_ids:
        raise SystemExit(f"Duplicate frontier_item_id values: {duplicate_ids}")

    return items


def render_table(items: list[dict[str, str]], generated_at: str, source_hash: str) -> str:
    rows = []
    for item in items:
        rows.append(
            "| {number} | `{item_id}` | {name} | `{milestone}` | {object_type} | `{tier}` | {linter} | {authority} | `{guard}` | {next_theorem} |".format(
                number=item["_item_number"],
                item_id=strip_markdown_value(item["frontier_item_id"]),
                name=strip_markdown_value(item["object_or_claim_name"]),
                milestone=strip_markdown_value(item["milestone"]),
                object_type=strip_markdown_value(item["object_type"]),
                tier=strip_markdown_value(item["three_tier_classification"]).rstrip("."),
                linter=strip_markdown_value(item["linter_status"]),
                authority=strip_markdown_value(item["authority_level"]),
                guard=strip_markdown_value(item["overread_guard"]),
                next_theorem=strip_markdown_value(item["next_theorem_needed"]),
            )
        )

    return "\n".join(
        [
            "<!-- authority: derivative-control -->",
            "",
            "# P7-T04 Frontier Theorem Inventory Compact Table",
            "",
            "## Boundary",
            "",
            f"- Generated at: `{generated_at}`.",
            f"- Generated by: `{JOB_ID}`.",
            f"- Canonical source object: `{SOURCE_OBJECT_ID}`.",
            f"- Source inventory path: `research_control/design/frontier_theorem_inventory.md`.",
            f"- Source inventory SHA-256: `{source_hash}`.",
            f"- Schema object: `{SCHEMA_OBJECT_ID}`.",
            "- Authority: derivative control artifact only. The canonical inventory, cited source paths, and registries remain authoritative.",
            "- Claim rule: the table copies status vocabulary from inventory fields and does not introduce new theorem, adoption, benchmark, or completed-derivation claims.",
            "",
            "## Compact Table",
            "",
            "Full source paths remain in the canonical inventory item's `source_artifact_path` field.",
            "",
            "| # | Source item ID | Object name | Milestone | Object type | Three-tier classification | Linter status | Authority level | Overread guard | Next theorem needed |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            *rows,
            "",
        ]
    )


def render_receipt(items: list[dict[str, str]], generated_at: str, source_hash: str, table_hash: str) -> str:
    classifications: dict[str, int] = {}
    linter_statuses: dict[str, int] = {}
    for item in items:
        classification = strip_markdown_value(item["three_tier_classification"]).rstrip(".")
        linter = strip_markdown_value(item["linter_status"]).split(";")[0].strip()
        classifications[classification] = classifications.get(classification, 0) + 1
        linter_statuses[linter] = linter_statuses.get(linter, 0) + 1

    return "\n".join(
        [
            "<!-- authority: derivative-control -->",
            "",
            "# P7-T04 Frontier Theorem Inventory Renderer Receipt",
            "",
            "## Inputs",
            "",
            f"- Task ID: `{TASK_ID}`.",
            f"- Job ID: `{JOB_ID}`.",
            f"- Generated at: `{generated_at}`.",
            f"- Source inventory: `research_control/design/frontier_theorem_inventory.md`.",
            f"- Source object ID: `{SOURCE_OBJECT_ID}`.",
            f"- Source inventory SHA-256: `{source_hash}`.",
            f"- Schema object ID: `{SCHEMA_OBJECT_ID}`.",
            "",
            "## Outputs",
            "",
            f"- Compact table: `research_control/tasks/{TASK_ID}/artifacts/p7_t04_frontier_theorem_inventory_compact_table.md`.",
            f"- Compact table SHA-256: `{table_hash}`.",
            f"- Rendered item count: `{len(items)}`.",
            f"- Three-tier classification counts: `{json.dumps(classifications, sort_keys=True)}`.",
            f"- Linter status counts: `{json.dumps(linter_statuses, sort_keys=True)}`.",
            "",
            "## Acceptance Receipt",
            "",
            "| Criterion | Result | Evidence |",
            "| --- | --- | --- |",
            "| Renderer cannot invent claim status | PASS | The renderer reads required status-bearing fields from inventory items and fails if they are missing. |",
            "| Renderer cites source item IDs | PASS | Each table row includes `frontier_item_id` as `Source item ID`. |",
            "| Renderer preserves scoped-positive vocabulary | PASS | `three_tier_classification`, `authority_level`, `linter_status`, and `overread_guard` are copied from inventory fields. |",
            "| Renderer output is derivative only | PASS | Output header marks derivative control authority and points back to canonical inventory and schema IDs. |",
            "",
            "## Claim Boundary",
            "",
            "This renderer does not create canonical ontology edits, source-law adoption, matter-semantics adoption, detector-semantics adoption, matter-coupling derivation or adoption, stress-energy semantics, matter action, Einstein equations, benchmark promotion, or completed derivation.",
            "",
        ]
    )


def main() -> None:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_hash = sha256_path(INVENTORY_PATH)
    items = parse_inventory(INVENTORY_PATH)

    table_text = render_table(items, generated_at, source_hash)
    TABLE_PATH.write_text(table_text, encoding="utf-8")
    table_hash = sha256_path(TABLE_PATH)

    receipt_text = render_receipt(items, generated_at, source_hash, table_hash)
    RECEIPT_PATH.write_text(receipt_text, encoding="utf-8")
    receipt_hash = sha256_path(RECEIPT_PATH)

    print(
        json.dumps(
            {
                "status": "PASS",
                "generated_at": generated_at,
                "source_hash": source_hash,
                "table_path": str(TABLE_PATH.relative_to(ROOT)),
                "table_hash": table_hash,
                "receipt_path": str(RECEIPT_PATH.relative_to(ROOT)),
                "receipt_hash": receipt_hash,
                "item_count": len(items),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
