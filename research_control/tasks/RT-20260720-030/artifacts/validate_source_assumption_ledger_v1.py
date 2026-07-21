#!/usr/bin/env python3
"""Focused validator for the v21 P4-T01 source-assumption ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260720-030"
ART = TASK / "artifacts"
MATRIX_PATH = ART / "frontier_object_assumption_matrix_v1.yaml"
TEX_PATH = ART / "comprehensive_source_assumption_ledger_v1.tex"
AMBIGUITY_PATH = ART / "source_assumption_unresolved_ambiguities_v1.md"
RECEIPT_PATH = ART / "source_assumption_ledger_compact_receipt_v1.json"
REPORT_PATH = ART / "source_assumption_ledger_validation_v1.json"
INVENTORY_PATH = ROOT / "research_control/design/frontier_theorem_inventory.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})

    matrix = yaml.safe_load(MATRIX_PATH.read_text(encoding="utf-8"))
    inventory_text = INVENTORY_PATH.read_text(encoding="utf-8")
    tex_text = TEX_PATH.read_text(encoding="utf-8")
    ambiguity_text = AMBIGUITY_PATH.read_text(encoding="utf-8")
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))

    inventory_ids = re.findall(r"^- `frontier_item_id`: `([^`]+)`", inventory_text, re.MULTILINE)
    object_rows = matrix["objects"]
    object_ids = [row["frontier_item_id"] for row in object_rows]
    dimensions = matrix["required_dimensions"]
    profiles = matrix["profiles"]
    assumptions = matrix["assumption_catalog"]
    sources = {row["source_id"]: row for row in matrix["source_catalog"]}
    structural_vocab = set(matrix["status_vocabulary"]["structural_role"])
    authority_vocab = set(matrix["status_vocabulary"]["authority_status"])

    check("inventory_count", len(inventory_ids) == 27, f"inventory item count={len(inventory_ids)}")
    check("object_count", len(object_rows) == 27, f"matrix object count={len(object_rows)}")
    check("unique_objects", len(set(object_ids)) == len(object_ids), "frontier item IDs are unique")
    check("exact_inventory_coverage", set(object_ids) == set(inventory_ids), "matrix and canonical inventory IDs match exactly")
    check("dimension_count", len(dimensions) == 13 and len(set(dimensions)) == 13, f"required dimension count={len(dimensions)}")
    check("declared_matrix_cells", matrix["matrix_cell_count"] == 351, f"declared cells={matrix['matrix_cell_count']}")
    check("resolved_matrix_cells", len(object_rows) * len(dimensions) == 351, "27 by 13 cells resolve through profiles")

    bad_profiles = {name: sorted(set(profile) ^ set(dimensions)) for name, profile in profiles.items() if set(profile) != set(dimensions)}
    check("profiles_total", not bad_profiles, f"profile key differences={bad_profiles}")
    bad_profile_refs = [row for row in object_rows if row["profile"] not in profiles]
    check("object_profile_refs", not bad_profile_refs, f"bad object profile refs={len(bad_profile_refs)}")
    bad_assumption_refs = [
        f"{profile_name}:{dimension}:{assumption_id}"
        for profile_name, profile in profiles.items()
        for dimension, assumption_id in profile.items()
        if assumption_id not in assumptions
    ]
    check("profile_assumption_refs", not bad_assumption_refs, f"bad assumption refs={bad_assumption_refs}")

    bad_structural = {key: row.get("structural_role") for key, row in assumptions.items() if row.get("structural_role") not in structural_vocab}
    bad_authority = {key: row.get("authority_status") for key, row in assumptions.items() if row.get("authority_status") not in authority_vocab}
    bad_object_authority = [row["frontier_item_id"] for row in object_rows if row["object_authority_status"] not in authority_vocab]
    check("structural_status_vocab", not bad_structural, f"invalid structural statuses={bad_structural}")
    check("assumption_authority_vocab", not bad_authority, f"invalid assumption authority statuses={bad_authority}")
    check("object_authority_vocab", not bad_object_authority, f"invalid object authority statuses={bad_object_authority}")

    no_provenance = [key for key, row in assumptions.items() if not row.get("provenance") and not row.get("missing_source_marker")]
    check("provenance_or_marker", not no_provenance, f"assumptions without provenance or marker={no_provenance}")
    unknown_sources = [
        f"{key}:{source_id}"
        for key, row in assumptions.items()
        for source_id in row.get("provenance", [])
        if source_id not in sources
    ]
    check("known_provenance_sources", not unknown_sources, f"unknown source refs={unknown_sources}")
    source_hash_failures = []
    for source_id, source in sources.items():
        path = ROOT / source["path"]
        if not path.is_file() or sha256(path) != source["sha256"]:
            source_hash_failures.append(source_id)
    check("canonical_source_hashes", not source_hash_failures, f"source hash failures={source_hash_failures}")

    high_impact_ids = {row["assumption_id"] for row in matrix["high_impact_assumptions"]}
    check("high_impact_dimension", "SRC_DIM_4D" in high_impact_ids, "four-dimensionality is explicitly high impact")
    check("high_impact_smoothness", "SRC_DIFF_SMOOTH" in high_impact_ids, "differentiability is explicitly high impact")
    check("high_impact_order", "SRC_ORDER_PHI" in high_impact_ids, "ordered motion is explicitly high impact")
    check("circularity_findings", len(matrix["circularity_findings"]) == 4, f"circularity finding count={len(matrix['circularity_findings'])}")
    check("no_status_upgrade", matrix["assumption_delta"]["status_upgrades"] == 0, "no assumption status upgrades")
    check("no_adoption_delta", matrix["assumption_delta"]["assumptions_adopted"] == 0, "no assumption adoptions")

    ambiguity_ids = set(re.findall(r"`(AMB-P4T01-\d{3})`", ambiguity_text))
    check("ambiguity_count", len(ambiguity_ids) == 9, f"ambiguity count={len(ambiguity_ids)}")
    check("well_founded_theorem", "Circular provenance cannot upgrade status" in tex_text, "ranked no-circular-upgrade theorem present")
    check("all_objects_in_tex", all(identifier.replace("_", r"\_") in tex_text for identifier in object_ids), "all object IDs appear in registered TeX")
    check("no_external_source", bool(re.search(r"No external source was\s+used", tex_text)), "external-source boundary recorded")

    child_files = [
        ART / "child_phys_math_source_assumption_ledger.yaml",
        ART / "child_phys_phil_source_assumption_ledger.yaml",
    ]
    child_statuses = [yaml.safe_load(path.read_text(encoding="utf-8"))["status"] for path in child_files]
    conflict = yaml.safe_load((ART / "parent_conflict_review_source_assumption_ledger.yaml").read_text(encoding="utf-8"))
    check("child_outputs", child_statuses == ["completed", "completed"], f"child statuses={child_statuses}")
    check("conflict_resolution", conflict["status"] == "resolved" and not conflict["unresolved_conflicts"], "parent conflict review resolved")

    check("receipt_object_count", receipt["finding_counts"]["frontier_objects"] == 27, "receipt object count is 27")
    check("receipt_matrix_cells", receipt["finding_counts"]["matrix_cells"] == 351, "receipt matrix cell count is 351")
    check("receipt_claim_boundary", receipt["claim_boundary_id"] == matrix["claim_boundary_id"], "receipt and matrix claim boundary agree")

    failed = [row for row in checks if row["status"] == "FAIL"]
    report = {
        "schema_id": "v21_p4_t01_source_assumption_ledger_validation_v1",
        "task_id": "RT-20260720-030",
        "job_id": "AJ-RT-20260720-030-001",
        "status": "PASS" if not failed else "FAIL",
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "checks": checks,
        "boundary": "Operational validation only; no physics proof, ontology adoption, or promotion authority.",
    }
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(report["status"])
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
