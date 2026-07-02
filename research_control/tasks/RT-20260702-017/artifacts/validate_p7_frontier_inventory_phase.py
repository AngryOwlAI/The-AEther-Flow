#!/usr/bin/env python3
"""Validate the v14 P7 frontier theorem inventory phase."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


TASK_ID = "RT-20260702-017"
JOB_ID = "AJ-RT-20260702-017-001"
GENERATED_AT = "2026-07-02T05:51:10Z"

ROOT = Path(__file__).resolve().parents[4]
PLAN_PATH = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
CURRENT_FRONTIER_PATH = ROOT / "research_control/current_frontier.md"
INVENTORY_PATH = ROOT / "research_control/design/frontier_theorem_inventory.md"
SCHEMA_PATH = ROOT / "research_control/design/frontier_theorem_inventory_schema_v1.md"
MARKDOWN_REGISTRY_PATH = ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"
RESEARCH_TASK_REGISTRY_PATH = ROOT / "registries/RESEARCH_TASK_REGISTRY.csv"
COMPACT_TABLE_PATH = ROOT / "research_control/tasks/RT-20260702-015/artifacts/p7_t04_frontier_theorem_inventory_compact_table.md"
P7_T05_RECEIPT_PATH = ROOT / "research_control/tasks/RT-20260702-016/artifacts/p7_t05_inventory_frontier_ledger_cross_check.md"
RECEIPT_PATH = ROOT / f"research_control/tasks/{TASK_ID}/artifacts/p7_t06_frontier_theorem_inventory_validation_receipt.md"

ITEM_RE = re.compile(r"^### Item (?P<number>[0-9]+[A-Z]?): (?P<header>[A-Za-z0-9_]+)\s*$")
FIELD_RE = re.compile(r"^- `(?P<field>[A-Za-z0-9_]+)`: ?(?P<value>.*)$")

REQUIRED_INVENTORY_FIELDS = [
    "frontier_item_id",
    "frontier_item_class",
    "milestone",
    "object_type",
    "object_or_claim_name",
    "status_layer_summary",
    "three_tier_classification",
    "linter_status",
    "source_artifact_path",
    "authority_level",
    "source_authority_type",
    "assumptions",
    "definitions_used",
    "statement_or_decision",
    "mathematical_conclusion",
    "physical_non_conclusions",
    "allowed_reuse",
    "blocked_reuse",
    "dependency_items",
    "missing_theorem_or_primitive",
    "candidate_next_task",
    "overread_guard",
    "external_review_notes",
]

P7_TASKS = {
    "P7-T01": "RT-20260702-012",
    "P7-T02": "RT-20260702-013",
    "P7-T03": "RT-20260702-014",
    "P7-T04": "RT-20260702-015",
    "P7-T05": "RT-20260702-016",
}


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean(value: str) -> str:
    text = value.strip().replace("`", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text.rstrip(".")


def md_escape(value: str) -> str:
    return clean(value).replace("|", r"\|") or "none"


def append_continuation(current: str, line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("- "):
        stripped = stripped[2:].strip()
    return f"{current} {stripped}".strip()


def parse_inventory(path: Path) -> dict[str, dict[str, str]]:
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
            current[field] = field_match.group("value").strip()
            current_field = field
            continue

        if current_field and line.startswith("  "):
            current[current_field] = append_continuation(current[current_field], line)

    by_id: dict[str, dict[str, str]] = {}
    for item in items:
        item_id = clean(item.get("frontier_item_id", ""))
        if not item_id:
            raise SystemExit(f"Inventory item {item.get('_item_number')} lacks frontier_item_id")
        if item_id in by_id:
            raise SystemExit(f"Duplicate inventory frontier_item_id: {item_id}")
        by_id[item_id] = item
    return by_id


def read_csv_by_key(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle)}


def result(name: str, passed: bool, evidence: str) -> dict[str, str]:
    return {"criterion": name, "result": "PASS" if passed else "FAIL", "evidence": evidence}


def validate() -> tuple[list[dict[str, str]], dict[str, str]]:
    inventory = parse_inventory(INVENTORY_PATH)
    markdown_rows = read_csv_by_key(MARKDOWN_REGISTRY_PATH, "object_id")
    task_rows = read_csv_by_key(RESEARCH_TASK_REGISTRY_PATH, "task_id")
    current_frontier = CURRENT_FRONTIER_PATH.read_text(encoding="utf-8")
    compact_table = COMPACT_TABLE_PATH.read_text(encoding="utf-8")
    p7_t05_receipt = P7_T05_RECEIPT_PATH.read_text(encoding="utf-8")

    inventory_hash = sha256_path(INVENTORY_PATH)
    schema_hash = sha256_path(SCHEMA_PATH)
    current_hash = sha256_path(CURRENT_FRONTIER_PATH)
    compact_hash = sha256_path(COMPACT_TABLE_PATH)
    p7_t05_hash = sha256_path(P7_T05_RECEIPT_PATH)

    outcomes: list[dict[str, str]] = []

    completed_tasks = [
        f"{plan_task}:{task_id}"
        for plan_task, task_id in P7_TASKS.items()
        if task_rows.get(task_id, {}).get("status") == "completed"
    ]
    outcomes.append(
        result(
            "P7 task chain completed through P7-T05",
            len(completed_tasks) == len(P7_TASKS),
            "; ".join(completed_tasks),
        )
    )

    missing_fields = [
        f"{item_id}:{field}"
        for item_id, item in inventory.items()
        for field in REQUIRED_INVENTORY_FIELDS
        if not item.get(field)
    ]
    outcomes.append(
        result(
            "Inventory rows expose required v14 fields",
            not missing_fields and len(inventory) == 27,
            f"item_count={len(inventory)} missing_fields={';'.join(missing_fields[:10]) or 'none'}",
        )
    )

    inventory_row = markdown_rows.get("MD-RESEARCH-CONTROL-DESIGN-FRONTIER-THEOREM-INVENTORY", {})
    schema_row = markdown_rows.get("MD-RESEARCH-CONTROL-DESIGN-FRONTIER-THEOREM-INVENTORY-SCHEMA-V1", {})
    registry_ok = (
        inventory_row.get("source_hash") == inventory_hash
        and inventory_row.get("related_source") == "MD-RESEARCH-CONTROL-DESIGN-FRONTIER-THEOREM-INVENTORY-SCHEMA-V1"
        and schema_row.get("source_hash") == schema_hash
    )
    outcomes.append(
        result(
            "Inventory and schema registry rows are current",
            registry_ok,
            f"inventory_hash={inventory_hash} schema_hash={schema_hash}",
        )
    )

    compact_ids = set(re.findall(r"\| [0-9]+[A-Z]? \| `([^`]+)` \|", compact_table))
    outcomes.append(
        result(
            "Compact table covers every inventory item",
            compact_ids == set(inventory),
            f"compact_rows={len(compact_ids)} compact_hash={compact_hash}",
        )
    )

    p7_t05_ok = (
        "`PASS`" in p7_t05_receipt
        and "| Every high-risk ledger row has matching inventory item or explicit reason | PASS |" in p7_t05_receipt
        and "| Every high-risk current-frontier claim has source inventory support | PASS |" in p7_t05_receipt
        and "| Inventory does not overclaim beyond ledger or Gate Chair artifacts | PASS |" in p7_t05_receipt
        and "| Inventory does not underclaim scoped M_src or g_eff | PASS |" in p7_t05_receipt
    )
    outcomes.append(
        result(
            "P7-T05 cross-check acceptance criteria passed",
            p7_t05_ok,
            f"p7_t05_receipt_hash={p7_t05_hash}",
        )
    )

    rr_e = inventory["rr_e_transport_completeness_or_invariance_law_v1"]
    positive_ms = inventory["positive_ms_profile_v1"]
    m_src = inventory["m_src_gsc"]
    g_eff = inventory["g_eff_gsc_cand"]
    claim_boundary_ok = (
        clean(rr_e.get("three_tier_classification", "")) == "accepted_evidence_precondition"
        and "no_rr_e_transport_law_adoption" in rr_e.get("overread_guard", "")
        and clean(positive_ms.get("three_tier_classification", "")) == "accepted_evidence_precondition"
        and "no_matter_coupling_derivation" in positive_ms.get("overread_guard", "")
        and clean(m_src.get("three_tier_classification", "")) == "adopted_object"
        and clean(g_eff.get("three_tier_classification", "")) == "adopted_object"
        and "gate_chair_artifact" in m_src.get("source_authority_type", "")
        and "gate_chair_artifact" in g_eff.get("source_authority_type", "")
    )
    outcomes.append(
        result(
            "High-risk claim boundaries remain scoped",
            claim_boundary_ok,
            "RR_E and PositiveMSProfile_v1 remain evidence/preconditions; M_src and g_eff remain scoped adopted objects.",
        )
    )

    next_route_ok = (
        "Run one bounded v14 P7-T06 P7 inventory validation packet" in current_frontier
        or "Run one bounded v14 P8-T01 route signature definition packet" in current_frontier
    )
    outcomes.append(
        result(
            "Active frontier routes through P7-T06 to P8-T01",
            next_route_ok,
            f"current_frontier_hash={current_hash}",
        )
    )

    hashes = {
        "plan_hash": sha256_path(PLAN_PATH),
        "current_frontier_hash": current_hash,
        "inventory_hash": inventory_hash,
        "schema_hash": schema_hash,
        "compact_table_hash": compact_hash,
        "p7_t05_receipt_hash": p7_t05_hash,
        "markdown_registry_hash": sha256_path(MARKDOWN_REGISTRY_PATH),
    }
    return outcomes, hashes


def render_receipt(outcomes: list[dict[str, str]], hashes: dict[str, str]) -> str:
    status = "PASS" if all(row["result"] == "PASS" for row in outcomes) else "FAIL"
    rows = [
        f"| {md_escape(row['criterion'])} | {row['result']} | {md_escape(row['evidence'])} |"
        for row in outcomes
    ]
    hash_rows = [f"| `{key}` | `{value}` |" for key, value in sorted(hashes.items())]
    return "\n".join(
        [
            "<!-- authority: derivative-control -->",
            "",
            "# P7-T06 Frontier Theorem Inventory Validation Receipt",
            "",
            "## Boundary",
            "",
            f"- Task ID: `{TASK_ID}`.",
            f"- Job ID: `{JOB_ID}`.",
            f"- Generated at: `{GENERATED_AT}`.",
            "- Authority: phase-validation receipt only.",
            "- Claim rule: validation PASS is not physics proof, source-law adoption, matter-coupling derivation, Einstein equations, benchmark promotion, or completed derivation.",
            "",
            "## Source Hashes",
            "",
            "| Source | SHA-256 |",
            "| --- | --- |",
            *hash_rows,
            "",
            "## Validation Matrix",
            "",
            "| Criterion | Result | Evidence |",
            "| --- | --- | --- |",
            *rows,
            "",
            "## Result",
            "",
            f"`{status}`",
            "",
            "## Next Route",
            "",
            "Run one bounded v14 P8-T01 route signature definition packet before route-history extraction or downstream physics routes.",
            "",
        ]
    )


def main() -> None:
    outcomes, hashes = validate()
    receipt_text = render_receipt(outcomes, hashes)
    RECEIPT_PATH.write_text(receipt_text, encoding="utf-8")
    receipt_hash = sha256_path(RECEIPT_PATH)
    status = "PASS" if all(row["result"] == "PASS" for row in outcomes) else "FAIL"
    print(
        json.dumps(
            {
                "status": status,
                "generated_at": GENERATED_AT,
                "receipt_path": str(RECEIPT_PATH.relative_to(ROOT)),
                "receipt_hash": receipt_hash,
                "outcome_count": len(outcomes),
                "hashes": hashes,
            },
            indent=2,
            sort_keys=True,
        )
    )
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
