#!/usr/bin/env python3
"""Validate the bounded P1-T04 EqSrc canonical-selection theorem target."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent
TARGET_ID = "EQSRC-CANONICAL-SELECTION-NATURALITY-TARGET-V1"
EXPECTED_DISTANCE_HASH = "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61"
EXPECTED_METRIC_HASH = "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf"
EXPECTED_SOURCES = {
    "EQSRC-CANONICAL-CHOICE-INTRINSIC-DISCRIMINATOR": (
        "research_control/tasks/RT-20260718-033/artifacts/eqsrc_intrinsic_discriminator_admissibility_law_v3_refuter_stress.tex",
        "b46297ba4c62046ebd856cc0ec36f1083e3486f809d5c40a50db61dbcf31877c",
        "multiple_relation_fixed_points",
    ),
    "EQSRC-CANONICAL-CHOICE-CYCLE-BOUNDARY-LINE": (
        "research_control/tasks/RT-20260718-037/artifacts/eqsrc_cycle_boundary_selector_law_refuter_countermodel.yaml",
        "f3845c3f6c74321d060af3cb8a8a2ef56da01d8ce556f2eca1f97bdccb65e458",
        "no_fixed_point",
    ),
    "EQSRC-CANONICAL-CHOICE-ORIENTATION-TORSOR": (
        "research_control/tasks/RT-20260718-041/artifacts/eqsrc_orientation_torsor_descent_law_refuter_countermodel.yaml",
        "a5bc1af23713145727bfad592a770691b5128d6ce6546966860d80c588a530a6",
        "multiple_relation_fixed_points",
    ),
    "EQSRC-CANONICAL-CHOICE-ROOTED-PARTITION": (
        "research_control/tasks/RT-20260718-045/artifacts/eqsrc_ordered_motion_rooted_partition_law_refuter_countermodel.yaml",
        "9ddce9d042ef187d163043d6c2a98a7d1a796cd01a433d3d258632150a83325e",
        "no_fixed_point",
    ),
    "EQSRC-CANONICAL-CHOICE-GRADED-ORBIT-ROOT": (
        "research_control/tasks/RT-20260720-009/artifacts/eqsrc_flow_generated_graded_orbit_root_smuggling_audit.tex",
        "3d7e49f05727f26ea97a65d88c0323c9721a5f78ebd7e718a6c163fe0fad067b",
        "morphism_or_variation_failure",
    ),
}
REQUIRED_BRANCHES = {
    "no_fixed_point",
    "multiple_relation_fixed_points",
    "choice_irrelevance",
    "relation_unique_existence",
    "morphism_or_variation_failure",
}
REQUIRED_CONTROLS = {
    "CTRL-POS-UNIQUE-FIXED-001",
    "CTRL-NEG-FREE-C2-002",
    "CTRL-NEG-MULTIREL-003",
    "CTRL-POS-IRRELEVANT-004",
    "CTRL-NEG-NONINVERTIBLE-005",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    value = yaml.safe_load((ARTIFACTS / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain one YAML mapping")
    return value


def check(condition: bool, check_id: str, detail: str, checks: list[dict[str, str]]) -> None:
    checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})


def validate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    source_receipts: list[dict[str, str]] = []

    target_path = ARTIFACTS / "eqsrc_canonical_selection_naturality_target_v1.tex"
    math_path = ARTIFACTS / "child_phys_math_eqsrc_canonical_selection_naturality_target.yaml"
    phil_path = ARTIFACTS / "child_phys_phil_eqsrc_canonical_selection_naturality_target.yaml"
    glossary_path = ARTIFACTS / "eqsrc_canonical_selection_notation_glossary.yaml"
    map_path = ARTIFACTS / "eqsrc_prior_countermodel_mapping.csv"
    conflict_path = ARTIFACTS / "parent_conflict_review_eqsrc_canonical_selection_naturality_target.yaml"
    fusion_path = ARTIFACTS / "parent_fusion_notes_eqsrc_canonical_selection_naturality_target.md"
    required_paths = [target_path, math_path, phil_path, glossary_path, map_path, conflict_path, fusion_path]
    check(all(path.is_file() for path in required_paths), "artifact_set", "All seven bounded target artifacts exist.", checks)

    target_text = target_path.read_text(encoding="utf-8")
    math = load_yaml(math_path.name)
    phil = load_yaml(phil_path.name)
    glossary = load_yaml(glossary_path.name)
    conflict = load_yaml(conflict_path.name)
    fusion_text = fusion_path.read_text(encoding="utf-8")

    check(
        all(item.get("theorem_target_id") == TARGET_ID for item in (math, phil, glossary)),
        "target_identity",
        "Math, philosophy, and glossary records share the registered target identity.",
        checks,
    )
    check(
        "Component fixed-point criterion" in target_text
        and "Evaluation and" in target_text
        and "inverse constructions" in target_text
        and "full theorem target remains open" in target_text,
        "theorem_scope",
        "The groupoid component criterion has a proof and the broader theorem target remains explicitly open.",
        checks,
    )
    check(
        math.get("proved_component_criterion", {}).get("statement")
        and math.get("claim_boundary", {}).get("general_theorem_proved") is False
        and math.get("claim_boundary", {}).get("selector_constructed") is False,
        "mathematical_claim_boundary",
        "The structured child separates the proved component criterion from the unproved general theorem and constructs no selector.",
        checks,
    )
    branch_tags = set(glossary.get("branch_tags", []))
    check(branch_tags == REQUIRED_BRANCHES, "branch_vocabulary", "All five required branch tags are present exactly once.", checks)
    control_ids = {item.get("control_id") for item in math.get("finite_controls", [])}
    check(control_ids == REQUIRED_CONTROLS and all(control in target_text for control in REQUIRED_CONTROLS), "finite_controls", "Five structured finite controls match the TeX target.", checks)
    check(
        phil.get("status_vocabulary", {}).get("adoption_status") == "blocked_adoption_open_continuation"
        and phil.get("human_gate_boundary", {}).get("required_before_adoption") is True
        and phil.get("claim_boundary_preserved") is True,
        "ontology_boundary",
        "Proposal-only status, blocked adoption, and the protected human gate are preserved.",
        checks,
    )
    check(
        conflict.get("status") == "completed"
        and not conflict.get("unresolved_blocking_conflicts")
        and all(item.get("status") == "resolved" for item in conflict.get("conflicts", []))
        and "broader" in str(conflict).lower()
        and TARGET_ID in fusion_text,
        "parent_synthesis",
        "Conflict review and fusion notes retain the exact theorem-target identity and proof boundary.",
        checks,
    )

    with map_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    mapped_ids = {row["family_id"] for row in rows}
    map_ok = len(rows) == len(EXPECTED_SOURCES) and mapped_ids == set(EXPECTED_SOURCES)
    for row in rows:
        expected = EXPECTED_SOURCES.get(row["family_id"])
        if expected is None:
            map_ok = False
            continue
        expected_path, expected_hash, expected_branch = expected
        source_path = ROOT / row["source_artifact"]
        actual_hash = digest(source_path) if source_path.is_file() else "missing"
        source_receipts.append({
            "family_id": row["family_id"],
            "path": row["source_artifact"],
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "branch": row["theorem_target_branch"],
        })
        map_ok = map_ok and row["source_artifact"] == expected_path
        map_ok = map_ok and row["source_sha256"] == expected_hash == actual_hash
        map_ok = map_ok and row["theorem_target_branch"] == expected_branch
        map_ok = map_ok and row["mapping_status"] == "mapped"
    check(map_ok, "prior_countermodel_map", "Five scoped prior families map to the target with live source-hash parity.", checks)

    distance_hash = digest(ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv")
    metric_hash = digest(ROOT / "registries/METRIC_USE_LEDGER.csv")
    check(distance_hash == EXPECTED_DISTANCE_HASH, "distance_ledger_unchanged", "Distance-to-GR ledger retains the launch hash.", checks)
    check(metric_hash == EXPECTED_METRIC_HASH, "metric_ledger_unchanged", "Metric-use ledger retains the launch hash.", checks)
    check(
        all(token in target_text for token in (
            "does not prove the broader theorem target",
            "does not reject them",
            "General \\(\\mathsf{EqSrc}\\)",
            "P1-T05",
        )),
        "claim_language",
        "The target blocks proof, rejection, EqSrc discharge, and promotion overreads while naming only P1-T05 next.",
        checks,
    )

    failure_count = sum(item["status"] == "FAIL" for item in checks)
    return {
        "schema_id": "v21_p1_t04_eqsrc_canonical_selection_naturality_target_validation_v1",
        "task_id": "RT-20260720-012",
        "job_id": "AJ-RT-20260720-012-001",
        "plan_task_id": "P1-T04",
        "theorem_target_id": TARGET_ID,
        "aggregate_status": "PASS" if failure_count == 0 else "FAIL",
        "failure_count": failure_count,
        "check_count": len(checks),
        "checks": checks,
        "metrics": {
            "mapped_family_count": len(rows),
            "branch_count": len(branch_tags),
            "finite_control_count": len(control_ids),
            "proved_component_criterion_count": 1,
            "general_theorem_proved": False,
            "selector_constructed": False,
            "distance_to_gr_delta_changed": False,
            "metric_use_ledger_changed": False,
            "physics_promotion_authorized": False,
        },
        "source_receipts": source_receipts,
        "ledger_receipts": {
            "distance_to_gr_sha256": distance_hash,
            "metric_use_sha256": metric_hash,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        report_path = ARTIFACTS / "eqsrc_canonical_selection_naturality_target_validation.json"
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['aggregate_status']}: {report['check_count']} checks, {report['failure_count']} failures")
    return 0 if report["aggregate_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
