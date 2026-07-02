#!/usr/bin/env python3
"""Audit frontier inventory coverage against current frontier and ledger."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


TASK_ID = "RT-20260702-016"
JOB_ID = "AJ-RT-20260702-016-001"
GENERATED_AT = "2026-07-02T05:36:14Z"

ROOT = Path(__file__).resolve().parents[4]
INVENTORY_PATH = ROOT / "research_control/design/frontier_theorem_inventory.md"
CURRENT_FRONTIER_PATH = ROOT / "research_control/current_frontier.md"
LEDGER_PATH = ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv"
ALIAS_PATH = ROOT / "research_control/design/distance_to_gr_status_aliases.yaml"
RECEIPT_PATH = ROOT / f"research_control/tasks/{TASK_ID}/artifacts/p7_t05_inventory_frontier_ledger_cross_check.md"

ITEM_RE = re.compile(r"^### Item (?P<number>[0-9]+[A-Z]?): (?P<header>[A-Za-z0-9_]+)\s*$")
FIELD_RE = re.compile(r"^- `(?P<field>[A-Za-z0-9_]+)`: ?(?P<value>.*)$")

LEDGER_TO_INVENTORY = {
    "source_ontology_primitives": ["source_ontology_primitives"],
    "source_equivalence_eqsrc": ["source_equivalence_eqsrc"],
    "retain_h": ["retain_h"],
    "gen_h": ["gen_h"],
    "obsloc_lc": ["obsloc_lc"],
    "resp_lc": ["resp_lc"],
    "m_src": ["m_src_gsc"],
    "g_eff": ["g_eff_gsc_cand"],
    "matter_coupling": [
        "matter_coupling_bridge_target_v1",
        "matter_coupling_precondition_evidence",
        "rr_e_theorem_target_v1",
        "rr_e_underdetermination_obstruction",
        "rr_e_factor_through_conditional_lemma",
        "rr_e_separation_obstruction_witness_v1",
        "rr_e_transport_completeness_or_invariance_law_v1",
        "matter_coupling_precondition_assembly_v1",
        "source_coupling_law_candidate_cand_v1",
        "ms_stable_partition_precondition_v1",
        "ms_stable_matter_semantics_bridge_v1",
        "source_matter_semantics_adoption_readiness_law_v1",
        "positive_source_matter_semantics_target_v1",
        "positive_ms_profile_v1",
    ],
    "einstein_equations": ["einstein_equations"],
    "finite_variation_robustness": ["finite_variation_robustness"],
    "benchmark_promotion": ["benchmark_promotion", "gate_chair_benchmark_closure"],
    "gate_chair_status": ["gate_chair_benchmark_closure"],
    "finite_toy_metric_response": ["finite_toy_metric_response"],
}

BLOCKED_PROMOTION_TOKENS = [
    "no_source_law_adoption",
    "no_matter_coupling_derivation",
    "no_einstein_equations",
    "no_benchmark_promotion",
    "no_completed_derivation",
    "no_future_source_extension_impossibility",
    "no_global_theory_rejection",
]


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean(value: str) -> str:
    text = value.strip()
    if text.startswith("`") and text.endswith("`") and text.count("`") == 2:
        text = text[1:-1]
    text = text.replace("`", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_tokens(value: str) -> list[str]:
    text = clean(value).replace("<br>", ";")
    parts = re.split(r"[;,]\s*", text)
    return [part.strip().rstrip(".") for part in parts if part.strip()]


def md_escape(value: str) -> str:
    text = clean(value)
    text = text.replace("|", r"\|")
    return text or "none"


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

        if current_field and line.startswith("  ") and not FIELD_RE.match(line.lstrip()):
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


def parse_ledger(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {row["burden_id"]: row for row in rows}


def parse_current_frontier_high_risk(path: Path) -> list[str]:
    rows: list[str] = []
    in_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "High-risk rows:":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            match = re.match(r"^- `([^`]+)`:", line)
            if match:
                rows.append(match.group(1))
    return rows


def parse_alias_rows(path: Path) -> list[str]:
    rows: list[str] = []
    in_row_aliases = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() == "row_aliases:":
            in_row_aliases = True
            continue
        if in_row_aliases and re.match(r"^[A-Za-z0-9_]+:", line):
            break
        if in_row_aliases:
            match = re.match(r"^  ([a-z0-9_]+):\s*$", line)
            if match:
                rows.append(match.group(1))
    return rows


def items_for(row_id: str, inventory: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    return [inventory[item_id] for item_id in LEDGER_TO_INVENTORY.get(row_id, []) if item_id in inventory]


def audit_ledger_coverage(
    ledger: dict[str, dict[str, str]],
    inventory: dict[str, dict[str, str]],
    high_risk_rows: set[str],
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for row_id, row in ledger.items():
        mapped_ids = LEDGER_TO_INVENTORY.get(row_id, [])
        present_items = items_for(row_id, inventory)
        result = "PASS" if mapped_ids and len(present_items) == len(mapped_ids) else "FAIL"
        results.append(
            {
                "row_id": row_id,
                "milestone": row.get("milestone", ""),
                "high_risk": row_id in high_risk_rows,
                "mapped_ids": mapped_ids,
                "present_ids": [clean(item["frontier_item_id"]) for item in present_items],
                "result": result,
            }
        )
    return results


def audit_current_frontier_support(
    current_rows: list[str],
    inventory: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for row_id in current_rows:
        mapped_ids = LEDGER_TO_INVENTORY.get(row_id, [])
        present_items = items_for(row_id, inventory)
        result = "PASS" if mapped_ids and present_items else "FAIL"
        results.append(
            {
                "row_id": row_id,
                "mapped_ids": mapped_ids,
                "present_ids": [clean(item["frontier_item_id"]) for item in present_items],
                "result": result,
            }
        )
    return results


def audit_guard_compatibility(
    ledger: dict[str, dict[str, str]],
    inventory: dict[str, dict[str, str]],
    high_risk_rows: set[str],
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for row_id in sorted(high_risk_rows):
        row = ledger.get(row_id)
        if not row:
            results.append({"row_id": row_id, "result": "FAIL", "reason": "missing ledger row"})
            continue
        ledger_guards = set(split_tokens(row.get("overread_guard", "")))
        inventory_items = items_for(row_id, inventory)
        inventory_guards: set[str] = set()
        for item in inventory_items:
            inventory_guards.update(split_tokens(item.get("overread_guard", "")))
        missing = sorted(ledger_guards - inventory_guards)
        results.append(
            {
                "row_id": row_id,
                "ledger_guards": sorted(ledger_guards),
                "inventory_guards": sorted(inventory_guards),
                "missing": missing,
                "result": "PASS" if not missing else "FAIL",
            }
        )
    return results


def audit_overclaim(inventory: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for item_id, item in inventory.items():
        tier = clean(item.get("three_tier_classification", ""))
        tier_normalized = tier.rstrip(".")
        guards = set(split_tokens(item.get("overread_guard", "")))
        object_type = clean(item.get("object_type", ""))

        if tier_normalized == "accepted_evidence_precondition":
            present = sorted(token for token in BLOCKED_PROMOTION_TOKENS if token in guards)
            result = "PASS" if present else "FAIL"
            results.append(
                {
                    "item_id": item_id,
                    "tier": tier_normalized,
                    "object_type": object_type,
                    "result": result,
                    "reason": "non-promotion guard present" if result == "PASS" else "missing explicit non-promotion guard",
                }
            )
        elif tier_normalized == "adopted_object":
            authority = clean(item.get("authority_level", "")).lower()
            source_authority = clean(item.get("source_authority_type", "")).lower()
            scoped = "scoped" in authority or "gate_chair" in source_authority
            allowed = item_id in {"m_src_gsc", "g_eff_gsc_cand"}
            result = "PASS" if scoped and allowed else "FAIL"
            results.append(
                {
                    "item_id": item_id,
                    "tier": tier_normalized,
                    "object_type": object_type,
                    "result": result,
                    "reason": "scoped adopted object matches ledger authority" if result == "PASS" else "adopted-object scope mismatch",
                }
            )
    return results


def audit_scoped_objects(
    ledger: dict[str, dict[str, str]],
    inventory: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    expectations = {
        "m_src": {
            "inventory_id": "m_src_gsc",
            "required_control_status": "gate_review_completed",
            "required_mathematical_status": "scoped_source_only_adopted_object",
            "required_promotion_status": "scoped_source_object_only",
        },
        "g_eff": {
            "inventory_id": "g_eff_gsc_cand",
            "required_control_status": "gate_review_completed",
            "required_mathematical_status": "scoped_source_extension_geff_object",
            "required_promotion_status": "scoped_source_object_only",
        },
    }
    for row_id, expectation in expectations.items():
        row = ledger[row_id]
        item = inventory[expectation["inventory_id"]]
        status_ok = (
            row.get("control_status") == expectation["required_control_status"]
            and row.get("mathematical_status") == expectation["required_mathematical_status"]
            and row.get("promotion_status") == expectation["required_promotion_status"]
        )
        tier_ok = clean(item.get("three_tier_classification", "")).rstrip(".") == "adopted_object"
        authority_ok = "gate_chair" in clean(item.get("source_authority_type", "")).lower()
        results.append(
            {
                "row_id": row_id,
                "inventory_id": expectation["inventory_id"],
                "reader_facing_status_ok": str(status_ok).lower(),
                "inventory_tier_ok": str(tier_ok).lower(),
                "source_authority_ok": str(authority_ok).lower(),
                "result": "PASS" if status_ok and tier_ok and authority_ok else "FAIL",
            }
        )
    return results


def render_list(values: list[str]) -> str:
    if not values:
        return "none"
    return "<br>".join(f"`{md_escape(value)}`" for value in values)


def render_receipt(
    *,
    generated_at: str,
    hashes: dict[str, str],
    ledger_coverage: list[dict[str, object]],
    frontier_support: list[dict[str, object]],
    guard_compatibility: list[dict[str, object]],
    overclaim: list[dict[str, str]],
    scoped_objects: list[dict[str, str]],
    high_risk_rows: set[str],
    alias_rows: list[str],
    current_rows: list[str],
) -> str:
    ledger_rows = [
        "| `{row_id}` | `{milestone}` | {high_risk} | {mapped} | {present} | {result} |".format(
            row_id=md_escape(str(row["row_id"])),
            milestone=md_escape(str(row["milestone"])),
            high_risk="yes" if row["high_risk"] else "no",
            mapped=render_list(list(row["mapped_ids"])),
            present=render_list(list(row["present_ids"])),
            result=row["result"],
        )
        for row in ledger_coverage
    ]
    frontier_rows = [
        "| `{row_id}` | {mapped} | {present} | {result} |".format(
            row_id=md_escape(str(row["row_id"])),
            mapped=render_list(list(row["mapped_ids"])),
            present=render_list(list(row["present_ids"])),
            result=row["result"],
        )
        for row in frontier_support
    ]
    guard_rows = [
        "| `{row_id}` | {missing} | {result} |".format(
            row_id=md_escape(str(row["row_id"])),
            missing=render_list(list(row.get("missing", []))),
            result=row["result"],
        )
        for row in guard_compatibility
    ]
    overclaim_rows = [
        "| `{item_id}` | `{tier}` | {object_type} | {result} | {reason} |".format(
            item_id=md_escape(row["item_id"]),
            tier=md_escape(row["tier"]),
            object_type=md_escape(row["object_type"]),
            result=row["result"],
            reason=md_escape(row["reason"]),
        )
        for row in overclaim
    ]
    scoped_rows = [
        "| `{row_id}` | `{inventory_id}` | {status_ok} | {tier_ok} | {authority_ok} | {result} |".format(
            row_id=md_escape(row["row_id"]),
            inventory_id=md_escape(row["inventory_id"]),
            status_ok=row["reader_facing_status_ok"],
            tier_ok=row["inventory_tier_ok"],
            authority_ok=row["source_authority_ok"],
            result=row["result"],
        )
        for row in scoped_objects
    ]

    all_sections = ledger_coverage + frontier_support + guard_compatibility + overclaim + scoped_objects
    status = "PASS" if all(row["result"] == "PASS" for row in all_sections) else "FAIL"

    return "\n".join(
        [
            "<!-- authority: derivative-control -->",
            "",
            "# P7-T05 Inventory Frontier Ledger Cross-Check",
            "",
            "## Boundary",
            "",
            f"- Task ID: `{TASK_ID}`.",
            f"- Job ID: `{JOB_ID}`.",
            f"- Generated at: `{generated_at}`.",
            "- Authority: task-local process audit receipt only.",
            "- Canonical sources remain `research_control/design/frontier_theorem_inventory.md`, `research_control/current_frontier.md`, and `registries/DISTANCE_TO_GR_LEDGER.csv`.",
            "- Claim rule: this receipt confirms consistency only; it does not adopt source laws, matter semantics, detector semantics, coupling laws, matter coupling, Einstein equations, benchmark promotion, or completed derivation.",
            "",
            "## Source Hashes",
            "",
            "| Source | SHA-256 |",
            "| --- | --- |",
            f"| `research_control/design/frontier_theorem_inventory.md` | `{hashes['inventory']}` |",
            f"| `research_control/current_frontier.md` | `{hashes['current_frontier']}` |",
            f"| `registries/DISTANCE_TO_GR_LEDGER.csv` | `{hashes['ledger']}` |",
            f"| `research_control/design/distance_to_gr_status_aliases.yaml` | `{hashes['aliases']}` |",
            "",
            "## Audit Scope",
            "",
            f"- Current-frontier high-risk rows: {render_list(current_rows)}.",
            f"- Alias-map high-risk rows: {render_list(alias_rows)}.",
            f"- Combined audited high-risk rows: {render_list(sorted(high_risk_rows))}.",
            "",
            "## Ledger Coverage",
            "",
            "| Ledger row | Milestone | High risk | Mapped inventory IDs | Present inventory IDs | Result |",
            "| --- | --- | --- | --- | --- | --- |",
            *ledger_rows,
            "",
            "## Current-Frontier Support",
            "",
            "| Current-frontier high-risk row | Mapped inventory IDs | Present inventory IDs | Result |",
            "| --- | --- | --- | --- |",
            *frontier_rows,
            "",
            "## Overread Guard Compatibility",
            "",
            "| High-risk row | Missing ledger guards in mapped inventory | Result |",
            "| --- | --- | --- |",
            *guard_rows,
            "",
            "## Inventory Overclaim Check",
            "",
            "| Inventory item | Tier | Object type | Result | Reason |",
            "| --- | --- | --- | --- | --- |",
            *overclaim_rows,
            "",
            "## Scoped M_src And g_eff Check",
            "",
            "| Ledger row | Inventory item | Reader status OK | Tier OK | Source authority OK | Result |",
            "| --- | --- | --- | --- | --- | --- |",
            *scoped_rows,
            "",
            "## Acceptance Criteria",
            "",
            "| Criterion | Result | Evidence |",
            "| --- | --- | --- |",
            f"| Every high-risk ledger row has matching inventory item or explicit reason | {'PASS' if all(row['result'] == 'PASS' for row in ledger_coverage if row['high_risk']) else 'FAIL'} | Combined high-risk rows are mapped in the ledger coverage matrix. |",
            f"| Every high-risk current-frontier claim has source inventory support | {'PASS' if all(row['result'] == 'PASS' for row in frontier_support) else 'FAIL'} | Current-frontier support matrix has no missing mapped inventory rows. |",
            f"| Inventory does not overclaim beyond ledger or Gate Chair artifacts | {'PASS' if all(row['result'] == 'PASS' for row in overclaim) else 'FAIL'} | Adopted objects are scoped to M_src/g_eff and accepted evidence/preconditions carry promotion guards. |",
            f"| Inventory does not underclaim scoped M_src or g_eff | {'PASS' if all(row['result'] == 'PASS' for row in scoped_objects) else 'FAIL'} | Scoped object matrix confirms reader status, tier, and Gate Chair authority fields. |",
            "",
            "## Result",
            "",
            f"`{status}`",
            "",
            "## Next Route",
            "",
            "Run one bounded v14 P7-T06 P7 inventory validation packet before P8 route-orbit freeze hardening or downstream physics routes.",
            "",
        ]
    )


def main() -> None:
    generated_at = GENERATED_AT

    inventory = parse_inventory(INVENTORY_PATH)
    ledger = parse_ledger(LEDGER_PATH)
    current_rows = parse_current_frontier_high_risk(CURRENT_FRONTIER_PATH)
    alias_rows = parse_alias_rows(ALIAS_PATH)
    high_risk_rows = set(current_rows) | set(alias_rows)

    missing_ledger_rows = sorted(set(LEDGER_TO_INVENTORY) - set(ledger))
    if missing_ledger_rows:
        raise SystemExit(f"Mapping references missing ledger rows: {missing_ledger_rows}")

    missing_inventory_ids = sorted(
        item_id for item_ids in LEDGER_TO_INVENTORY.values() for item_id in item_ids if item_id not in inventory
    )
    if missing_inventory_ids:
        raise SystemExit(f"Mapping references missing inventory items: {missing_inventory_ids}")

    hashes = {
        "inventory": sha256_path(INVENTORY_PATH),
        "current_frontier": sha256_path(CURRENT_FRONTIER_PATH),
        "ledger": sha256_path(LEDGER_PATH),
        "aliases": sha256_path(ALIAS_PATH),
    }
    ledger_coverage = audit_ledger_coverage(ledger, inventory, high_risk_rows)
    frontier_support = audit_current_frontier_support(current_rows, inventory)
    guard_compatibility = audit_guard_compatibility(ledger, inventory, high_risk_rows)
    overclaim = audit_overclaim(inventory)
    scoped_objects = audit_scoped_objects(ledger, inventory)

    receipt_text = render_receipt(
        generated_at=generated_at,
        hashes=hashes,
        ledger_coverage=ledger_coverage,
        frontier_support=frontier_support,
        guard_compatibility=guard_compatibility,
        overclaim=overclaim,
        scoped_objects=scoped_objects,
        high_risk_rows=high_risk_rows,
        alias_rows=alias_rows,
        current_rows=current_rows,
    )
    RECEIPT_PATH.write_text(receipt_text, encoding="utf-8")
    receipt_hash = sha256_path(RECEIPT_PATH)

    status = "PASS"
    for section in (ledger_coverage, frontier_support, guard_compatibility, overclaim, scoped_objects):
        if any(row["result"] != "PASS" for row in section):
            status = "FAIL"
            break

    print(
        json.dumps(
            {
                "status": status,
                "generated_at": generated_at,
                "receipt_path": str(RECEIPT_PATH.relative_to(ROOT)),
                "receipt_hash": receipt_hash,
                "inventory_hash": hashes["inventory"],
                "current_frontier_hash": hashes["current_frontier"],
                "ledger_hash": hashes["ledger"],
                "aliases_hash": hashes["aliases"],
                "ledger_rows_checked": len(ledger_coverage),
                "current_frontier_rows_checked": len(frontier_support),
                "high_risk_rows_checked": len(high_risk_rows),
                "overclaim_rows_checked": len(overclaim),
                "scoped_object_rows_checked": len(scoped_objects),
            },
            indent=2,
            sort_keys=True,
        )
    )

    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
