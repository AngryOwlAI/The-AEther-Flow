#!/usr/bin/env python3
"""Validate and materialize the V22 P1-T01 governance receipts.

The process-integrity review is an independent deterministic rule path, not a
human review, external specialist review, or independent scientific
replication.  Every PASS emitted here is operational control evidence only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.research_control import v22_track_governance as governance  # noqa: E402


TASK_ID = "RT-20260809-001"
JOB_ID = "AJ-RT-20260809-001-001"
PLAN_ID = "recommendations_implementation_plan_continue_task-v22"
PLAN_TASK_ID = "P1-T01"
CREATED_AT = "2026-08-09T00:54:25Z"
ARTIFACTS = ROOT / f"research_control/tasks/{TASK_ID}/artifacts"
VALIDATION_PATH = ARTIFACTS / "v22_p1_t01_three_track_validation.json"
COMPACT_RECEIPT_PATH = ARTIFACTS / "v22_p1_t01_compact_receipt.json"
PROCESS_REVIEW_PATH = ARTIFACTS / "v22_p1_t01_process_integrity_review.yaml"
SOURCE_PATHS = [
    governance.DESIGN_PATHS["charter"],
    governance.DESIGN_PATHS["authority"],
    governance.DESIGN_PATHS["assignment"],
    governance.DESIGN_PATHS["budget"],
    governance.DESIGN_PATHS["cross_track"],
    governance.DESIGN_PATHS["repository"],
    governance.DESIGN_PATHS["backlog"],
    *governance.SCORECARD_PATHS.values(),
    governance.FIXTURE_PATH,
    "scripts/research_control/v22_track_governance.py",
    "tests/test_v22_track_governance.py",
]


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _yaml_bytes(value: Any) -> bytes:
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True).encode("utf-8")


def _independent_process_review() -> dict[str, Any]:
    """Recheck P1-T01 acceptance directly, without calling the production checks."""

    assignment = _load(ROOT / governance.DESIGN_PATHS["assignment"])
    authority = _load(ROOT / governance.DESIGN_PATHS["authority"])
    budget = _load(ROOT / governance.DESIGN_PATHS["budget"])
    cross_track = _load(ROOT / governance.DESIGN_PATHS["cross_track"])
    repository = _load(ROOT / governance.DESIGN_PATHS["repository"])
    fixture = _load(ROOT / governance.FIXTURE_PATH)
    scorecards = {
        track_id: _load(ROOT / path)
        for track_id, path in governance.SCORECARD_PATHS.items()
    }

    assignments = _list(assignment.get("assignments"))
    ids = [str(_mapping(row).get("plan_task_id", "")) for row in assignments]
    tracks = [str(_mapping(row).get("primary_track", "")) for row in assignments]
    counts = Counter(tracks)
    matrix_tracks = _mapping(authority.get("tracks"))
    track_b_forbidden = set(
        _list(_mapping(matrix_tracks.get("track_b")).get("forbidden_gate_evidence_classes"))
    )
    required_forbidden = {
        "track_a_interpretive_coherence", "target_side_exact_gr_agreement",
        "track_c_methodology_success", "workflow_pass", "validator_pass",
        "checkpoint_pass", "control_traceability",
    }
    namespaces = [str(scorecards[key].get("metric_namespace", "")) for key in governance.TRACK_IDS]
    dashboards = [str(scorecards[key].get("dashboard_id", "")) for key in governance.TRACK_IDS]
    lanes = [str(scorecards[key].get("publication_lane_id", "")) for key in governance.TRACK_IDS]
    budget_centers = _mapping(budget.get("cost_centers"))
    budget_counts = {
        key: _mapping(budget_centers.get(key)).get("planned_task_count")
        for key in governance.TRACK_IDS
    }
    negative_cases = [case for case in _list(fixture.get("cases")) if _mapping(case).get("expected_valid") is False]

    raw_checks = [
        (
            "exact_assignment_cardinality",
            len(ids) == 40 and len(set(ids)) == 40 and "" not in ids and
            set(tracks).issubset(set(governance.TRACK_IDS)),
            "40 unique packages each carry one scalar allowed primary_track",
        ),
        (
            "declared_assignment_counts",
            counts == Counter({"track_a": 1, "track_b": 22, "track_c": 3,
                               "shared_control": 14}),
            "primary assignment counts are A=1 B=22 C=3 shared=14",
        ),
        (
            "disjoint_scorecard_surfaces",
            all(len(values) == 4 and "" not in values and len(set(values)) == 4
                for values in (namespaces, dashboards, lanes)),
            "metric namespaces dashboard IDs and publication lanes are pairwise disjoint",
        ),
        (
            "non_track_b_distance_lock",
            all(_mapping(matrix_tracks.get(key)).get("distance_to_gr_effect") == "none"
                and scorecards[key].get("distance_to_gr_effect_policy") == "forbidden"
                for key in ("track_a", "track_c", "shared_control")),
            "Track A Track C and shared control have no Distance-to-GR effect",
        ),
        (
            "track_b_gate_evidence_lock",
            required_forbidden.issubset(track_b_forbidden) and
            required_forbidden.issubset(
                set(_list(scorecards["track_b"].get("forbidden_gate_evidence_classes")))
            ),
            "interpretive methodology workflow validator checkpoint and traceability evidence are barred from Track B Gates",
        ),
        (
            "four_dimension_budget_separation",
            set(_list(budget.get("resource_dimensions"))) == set(governance.RESOURCE_DIMENSIONS)
            and sum(value for value in budget_counts.values() if isinstance(value, int)) == 40
            and budget_counts == {"track_a": 1, "track_b": 22, "track_c": 3,
                                  "shared_control": 14}
            and budget.get("cross_track_reference_reallocates_cost") is False,
            "task count elapsed effort compute and financial cost use one primary cost center",
        ),
        (
            "cross_track_links_are_nonpromotional",
            set(_mapping(cross_track.get("fixed_values")).values()) == {"none"},
            "cross-track references have no authority evidence Gate Distance-to-GR or resource effect",
        ),
        (
            "negative_fixture_coverage",
            len(negative_cases) >= 10 and all(_list(_mapping(case).get("expected_errors"))
                                              for case in negative_cases),
            "prohibited promotion ambiguity double-counting and blended-publication cases are explicit",
        ),
        (
            "repository_split_remains_unexecuted",
            repository.get("current_decision") == "retain_monorepo"
            and repository.get("automatic_split_authorized") is False
            and _mapping(repository.get("decision_rule")).get("sufficient_for_execution") is False
            and "separate human authorization" in _list(
                _mapping(repository.get("decision_rule")).get("execution_requires")
            ),
            "split execution requires measured criteria provenance parity and separate human authority",
        ),
    ]
    checks = [
        {"check_id": check_id, "status": "PASS" if passed else "FAIL", "finding": finding}
        for check_id, passed, finding in raw_checks
    ]
    blocking = [check["check_id"] for check in checks if check["status"] != "PASS"]
    return {
        "schema_id": "v22_p1_t01_process_integrity_review_v1",
        "review_id": "PIR-V22-P1-T01-001",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_id": PLAN_ID,
        "plan_task_id": PLAN_TASK_ID,
        "status": "PASS" if not blocking else "FAIL",
        "review_class": "deterministic_process_integrity_independent_rule_path",
        "reviewer": "process_integrity_auditor_rule_path_v1",
        "review_scope": "P1-T01 assignment, authority, scorecard, resource, link, publication, and repository-separation controls only",
        "implementation_validator_reused": False,
        "external_review_completed": False,
        "epistemically_independent_human_review": False,
        "independent_scientific_replication": False,
        "checks": checks,
        "blocking_findings": blocking,
        "stop_conditions": {
            "shared_metric_with_ambiguous_authority": False if not blocking else None,
            "double_counted_budget": False if not blocking else None,
            "blended_publication_language": False if not blocking else None,
        },
        "authority_limits": {
            "review_is_scientific_peer_review": False,
            "review_is_external_specialist_review": False,
            "review_is_independent_scientific_replication": False,
            "review_changes_distance_to_gr": False,
            "review_issues_gate_verdict": False,
            "review_authorizes_publication_release_or_repository_split": False,
        },
    }


def build_outputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    combined = governance.build_validation_report(ROOT)
    process_review = _independent_process_review()
    source_hashes = [
        {"path": path, "sha256": _sha256(ROOT / path)}
        for path in SOURCE_PATHS
    ]
    overall_status = (
        "PASS"
        if combined["status"] == "PASS" and process_review["status"] == "PASS"
        else "FAIL"
    )
    validation = {
        "schema_id": "v22_p1_t01_three_track_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_id": PLAN_ID,
        "plan_task_id": PLAN_TASK_ID,
        "created_at": CREATED_AT,
        "status": overall_status,
        "production_validation": combined,
        "process_integrity_review_summary": {
            "review_id": process_review["review_id"],
            "status": process_review["status"],
            "review_class": process_review["review_class"],
            "blocking_findings": process_review["blocking_findings"],
            "external_review_completed": False,
            "independent_scientific_replication": False,
        },
        "source_hashes": source_hashes,
        "acceptance_summary": {
            "package_assignment_count": combined["governance"]["assignment_count"],
            "package_assignment_counts": combined["governance"]["assignment_counts"],
            "separate_scorecard_schema_count": combined["governance"]["scorecard_schema_count"],
            "fixture_case_count": combined["fixtures"]["fixture_case_count"],
            "fixture_failure_count": combined["fixtures"]["fixture_failure_count"],
            "resource_dimensions": combined["governance"]["resource_dimensions"],
            "repository_decision": combined["governance"]["repository_decision"],
        },
        "authority_limits": combined["authority_limits"],
    }
    validation_bytes = _json_bytes(validation)
    review_bytes = _yaml_bytes(process_review)
    compact = {
        "schema_id": "v22_p1_t01_compact_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_id": PLAN_ID,
        "plan_task_id": PLAN_TASK_ID,
        "created_at": CREATED_AT,
        "status": overall_status,
        "validation_path": str(VALIDATION_PATH.relative_to(ROOT)),
        "validation_sha256": hashlib.sha256(validation_bytes).hexdigest(),
        "process_integrity_review_path": str(PROCESS_REVIEW_PATH.relative_to(ROOT)),
        "process_integrity_review_sha256": hashlib.sha256(review_bytes).hexdigest(),
        "assignment_count": combined["governance"]["assignment_count"],
        "assignment_counts": combined["governance"]["assignment_counts"],
        "scorecard_schema_count": combined["governance"]["scorecard_schema_count"],
        "fixture_case_count": combined["fixtures"]["fixture_case_count"],
        "fixture_failure_count": combined["fixtures"]["fixture_failure_count"],
        "repository_decision": combined["governance"]["repository_decision"],
        "external_review_completed": False,
        "independent_scientific_replication_completed": False,
        "scientific_status_changed": False,
        "distance_to_gr_changed": False,
        "physics_promotion_authorized": False,
        "repository_split_authorized": False,
        "publication_authorized": False,
        "external_action_authorized": False,
    }
    return validation, process_review, compact


def _write_or_compare(path: Path, payload: bytes, write: bool, errors: list[str]) -> None:
    if write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    elif not path.is_file():
        errors.append(f"missing_output:{path.relative_to(ROOT)}")
    elif path.read_bytes() != payload:
        errors.append(f"output_drift:{path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validation, process_review, compact = build_outputs()
    errors: list[str] = []
    _write_or_compare(VALIDATION_PATH, _json_bytes(validation), args.write, errors)
    _write_or_compare(PROCESS_REVIEW_PATH, _yaml_bytes(process_review), args.write, errors)
    _write_or_compare(COMPACT_RECEIPT_PATH, _json_bytes(compact), args.write, errors)
    result = {
        "status": "PASS" if validation["status"] == "PASS" and not errors else "FAIL",
        "validation_status": validation["status"],
        "process_integrity_review_status": process_review["status"],
        "output_errors": errors,
        "validation_path": str(VALIDATION_PATH.relative_to(ROOT)),
        "compact_receipt_path": str(COMPACT_RECEIPT_PATH.relative_to(ROOT)),
        "process_integrity_review_path": str(PROCESS_REVIEW_PATH.relative_to(ROOT)),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"status={result['status']}")
        for error in errors:
            print(error)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
