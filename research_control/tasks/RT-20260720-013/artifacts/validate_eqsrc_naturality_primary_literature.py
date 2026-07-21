#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260720-013"
ARTIFACTS = TASK / "artifacts"
REPORT = ARTIFACTS / "eqsrc_naturality_primary_literature_validation.json"
EXPECTED_IMMUTABLE_HASHES = {
    "research_control/tasks/RT-20260720-012/artifacts/eqsrc_canonical_selection_naturality_target_v1.tex": "c5aaaa70f4d7ce216a35d17af674e94e3f2866c1bdcfb28787a40d9f6636516c",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61",
    "registries/METRIC_USE_LEDGER.csv": "a33349c7a153c4fbadb70c7c38b17cf0eebb7672b8e1f692702fc91edf17efcf",
    "ontology/tex/aether_flow_foundations.tex": "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping in {path}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail})
        if not condition:
            failures.append(f"{check_id}: {detail}")

    bibliography = load_yaml(ARTIFACTS / "eqsrc_naturality_primary_literature_bibliography.yaml")
    entries = bibliography.get("source_entries", [])
    check("primary_source_count", len(entries) == 8, f"observed={len(entries)} expected=8")
    check("all_sources_primary", all(item.get("primary_source") is True for item in entries), "every source must be primary")
    check("apa7_metadata", all("https://" in item.get("citation_apa7", "") for item in entries), "every APA 7 candidate must include a stable HTTPS locator")
    check("exact_scope_fields", all(item.get("exact_hypotheses") and item.get("established_conclusion") and item.get("transfer_boundary") for item in entries), "hypotheses conclusion and transfer boundary are required")
    topics = {topic for item in entries for topic in item.get("topics", [])}
    required_topics = {"naturality", "symmetry", "leader election", "gauge choice", "quotient construction", "spontaneous symmetry breaking", "canonical reconstruction"}
    check("topic_coverage", required_topics <= topics, f"covered={sorted(topics)}")
    check("no_quotations", bibliography.get("quotation_count") == 0, "review must use scoped paraphrase rather than quotations")

    with (ARTIFACTS / "eqsrc_naturality_claim_comparison_matrix.csv").open(newline="", encoding="utf-8") as handle:
        matrix = list(csv.DictReader(handle))
    check("matrix_row_count", len(matrix) == 8, f"observed={len(matrix)} expected=8")
    required_columns = {"source_id", "exact_hypotheses", "established_conclusion", "reuse_class", "aeether_flow_adaptation_needed", "forbidden_overread", "source_url"}
    check("matrix_schema", bool(matrix) and required_columns <= set(matrix[0]), f"columns={sorted(matrix[0]) if matrix else []}")
    check("matrix_source_parity", {row["source_id"] for row in matrix} == {item["source_id"] for item in entries}, "bibliography and matrix source IDs must match")

    review = (ARTIFACTS / "eqsrc_naturality_primary_literature_review.md").read_text(encoding="utf-8")
    for phrase in ("literature basis, not project proof", "P2-T01", "local slices do not imply a global natural section", "quotient-first", "does not prove a global EqSrc no-go"):
        check(f"review_phrase_{hashlib.sha256(phrase.encode()).hexdigest()[:8]}", phrase.casefold() in review.casefold(), phrase)

    math_child = load_yaml(ARTIFACTS / "child_phys_math_eqsrc_naturality_literature_review.yaml")
    phil_child = load_yaml(ARTIFACTS / "child_phys_phil_eqsrc_naturality_literature_review.yaml")
    conflict = load_yaml(ARTIFACTS / "parent_conflict_review_eqsrc_naturality_literature_review.yaml")
    fusion = (ARTIFACTS / "parent_fusion_notes_eqsrc_naturality_literature_review.md").read_text(encoding="utf-8")
    check("parent_child_status", math_child.get("status") == phil_child.get("status") == "completed", "both child outputs completed")
    check("conflict_resolution", conflict.get("status") == "resolved" and conflict.get("unresolved_conflicts") == [], "parent conflict review resolved")
    check("fusion_route", "P2-T01" in fusion and "grants no proof" in fusion, "fusion selects P2-T01 and preserves authority boundary")

    immutable_hashes: dict[str, str] = {}
    for relative, expected in EXPECTED_IMMUTABLE_HASHES.items():
        observed = sha256(ROOT / relative)
        immutable_hashes[relative] = observed
        check(f"immutable_{Path(relative).name}", observed == expected, f"observed={observed} expected={expected}")

    artifact_paths = [
        ARTIFACTS / "eqsrc_naturality_primary_literature_bibliography.yaml",
        ARTIFACTS / "eqsrc_naturality_claim_comparison_matrix.csv",
        ARTIFACTS / "eqsrc_naturality_primary_literature_review.md",
        ARTIFACTS / "child_phys_math_eqsrc_naturality_literature_review.yaml",
        ARTIFACTS / "child_phys_phil_eqsrc_naturality_literature_review.yaml",
        ARTIFACTS / "parent_conflict_review_eqsrc_naturality_literature_review.yaml",
        ARTIFACTS / "parent_fusion_notes_eqsrc_naturality_literature_review.md",
    ]
    report = {
        "status": "PASS" if not failures else "FAIL",
        "task_id": "RT-20260720-013",
        "plan_task_id": "P1-T05",
        "checks": checks,
        "metrics": {
            "check_count": len(checks),
            "primary_source_count": len(entries),
            "matrix_row_count": len(matrix),
            "terminology_conflict_count": len(phil_child.get("terminology_conflicts", [])),
            "selected_next_plan_task": "P2-T01",
        },
        "artifact_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in artifact_paths},
        "immutable_surface_hashes": immutable_hashes,
        "failures": failures,
        "claim_boundary": "Operational validation of a bounded literature basis only; no project proof ontology authority scientific-ledger delta or promotion authority.",
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
