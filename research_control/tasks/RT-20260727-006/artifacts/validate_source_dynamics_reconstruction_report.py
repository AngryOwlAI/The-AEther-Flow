#!/usr/bin/env python3
"""Validate the bounded P15-T04 report packet.

This validator checks source hashes, displayed calculation controls, status
separation, review provenance, and task-local packet consistency. A PASS is
operational evidence only and is not theorem truth or physics promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260727-006"
ARTIFACTS = TASK_DIR / "artifacts"
REPORT_PATH = ARTIFACTS / "source_dynamics_reconstruction_technical_report_v1.tex"
MODEL_PATH = ARTIFACTS / "source_dynamics_reconstruction_model_archive_v1.py"
MANIFEST_PATH = ARTIFACTS / "source_dynamics_reconstruction_model_manifest_v1.yaml"
ASSUMPTION_PATH = ARTIFACTS / "source_dynamics_reconstruction_assumption_ledger_v1.yaml"
REVIEW_PATH = ARTIFACTS / "source_dynamics_reconstruction_review_packet_v1.yaml"
CHILD_MATH_PATH = ARTIFACTS / "child_phys_math_p15_t04_report.yaml"
CHILD_PHIL_PATH = ARTIFACTS / "child_phys_phil_p15_t04_report.yaml"
CONFLICT_PATH = ARTIFACTS / "parent_conflict_review_p15_t04_report.yaml"
FUSION_PATH = ARTIFACTS / "parent_fusion_notes_p15_t04_report.md"
VALIDATION_PATH = ARTIFACTS / "source_dynamics_reconstruction_validation_v1.json"
TASK_PATH = TASK_DIR / "00_TASK.yaml"
JOB_PATH = TASK_DIR / "jobs/AJ-RT-20260727-006-001.yaml"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def load_model_result() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("p15_t04_model_archive", MODEL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load model archive")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run_checks()
    if not isinstance(result, dict):
        raise ValueError("model archive result must be a mapping")
    return result


def make_check(
    checks: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    detail: str,
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
    )


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required_paths = [
        REPORT_PATH,
        MODEL_PATH,
        MANIFEST_PATH,
        ASSUMPTION_PATH,
        REVIEW_PATH,
        CHILD_MATH_PATH,
        CHILD_PHIL_PATH,
        CONFLICT_PATH,
        FUSION_PATH,
        TASK_PATH,
        JOB_PATH,
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_paths if not path.is_file()]
    make_check(
        checks,
        "required_artifacts",
        not missing,
        "all required task-local report artifacts exist"
        if not missing
        else f"missing: {missing}",
    )

    if missing:
        return finalize(checks, {}, {})

    task = load_yaml(TASK_PATH)
    job = load_yaml(JOB_PATH)
    manifest = load_yaml(MANIFEST_PATH)
    assumptions = load_yaml(ASSUMPTION_PATH)
    review = load_yaml(REVIEW_PATH)
    child_math = load_yaml(CHILD_MATH_PATH)
    child_phil = load_yaml(CHILD_PHIL_PATH)
    conflict = load_yaml(CONFLICT_PATH)
    report_text = REPORT_PATH.read_text(encoding="utf-8")
    fusion_text = FUSION_PATH.read_text(encoding="utf-8")

    make_check(
        checks,
        "control_identity",
        task.get("task_id") == "RT-20260727-006"
        and job.get("job_id") == "AJ-RT-20260727-006-001"
        and task.get("plan_task_id") == "P15-T04"
        and job.get("plan_task_id") == "P15-T04",
        "task, AgentJob, and v21 plan identity agree",
    )
    make_check(
        checks,
        "milestone_contract",
        job.get("target_derivation_milestone") == "effective_metric_g_eff"
        and job.get("milestone_burden")
        == "Create a coherent scientific record whether the result is positive or obstructed.",
        "effective_metric_g_eff reporting burden is explicit",
    )
    decomposition = job.get("role_decomposition", {})
    children = decomposition.get("children", [])
    make_check(
        checks,
        "parent_child_decomposition",
        decomposition.get("mode") == "parent_child_parallel_synthesis"
        and len(children) == 2
        and {item.get("execution_unit_id") for item in children}
        == {"child_phys_math", "child_phys_phil"},
        "one outer AgentJob contains exactly two required internal execution units",
    )

    required_report_tokens = [
        "P15T04-THM-FIXED-PACKAGE-COMPOSED-STATUS-BARRIER",
        "blocked\\_adoption\\_open\\_continuation",
        "Gate B remains zero of eight",
        "rank D\\mathcal R_u\\leq1",
        "ScopedMetricStructureRecord\\_src",
        "not certify",
        "not a global no-go theorem",
        "The reporting burden is discharged",
        "The effective-metric derivation burden is not",
    ]
    absent_report_tokens = [token for token in required_report_tokens if token not in report_text]
    make_check(
        checks,
        "report_required_content",
        not absent_report_tokens,
        "theorem, status, Gate-B, naming, and burden boundaries are present"
        if not absent_report_tokens
        else f"absent tokens: {absent_report_tokens}",
    )
    forbidden_overreads = [
        "Gate B passed",
        "a physical metric has been derived",
        "independent replication is complete",
        "the derivation is complete",
        "all future source extensions are impossible",
    ]
    present_overreads = [phrase for phrase in forbidden_overreads if phrase in report_text]
    make_check(
        checks,
        "report_forbidden_overreads",
        not present_overreads,
        "no forbidden promotional or global overread appears"
        if not present_overreads
        else f"present overreads: {present_overreads}",
    )

    source_rows = manifest.get("primary_source_hashes", [])
    mismatches: list[str] = []
    for row in source_rows:
        path = ROOT / str(row.get("path", ""))
        expected = str(row.get("sha256", ""))
        if not path.is_file() or sha256(path) != expected:
            mismatches.append(str(row.get("object_id", row.get("path", ""))))
    make_check(
        checks,
        "primary_source_hashes",
        len(source_rows) >= 16 and not mismatches,
        f"{len(source_rows)} primary source hashes match"
        if not mismatches
        else f"hash mismatches: {mismatches}",
    )

    model_result = load_model_result()
    make_check(
        checks,
        "model_archive",
        model_result.get("status") == "PASS"
        and all(model_result.get("checks", {}).values()),
        "all bounded P5/P6 calculation controls pass",
    )

    assumption_delta = assumptions.get("assumption_delta", {})
    assumption_entries = assumptions.get("entries", [])
    make_check(
        checks,
        "assumption_ledger",
        assumption_delta.get("changed") is False
        and len(assumption_entries) >= 14
        and assumptions.get("composed_theorem", {}).get("global_no_go_claimed")
        is False
        and assumptions.get("freeze", {}).get("inherited_status")
        == "blocked_adoption_open_continuation",
        "no premise delta, fourteen status-separated entries, and inherited freeze",
    )

    math_review_context = child_math.get("review_context") or child_math.get(
        "review_provenance", {}
    ).get("review_context_classification")
    math_promotion = child_math.get("physics_promotion_authorized")
    if math_promotion is None:
        math_promotion = child_math.get("final_disposition", {}).get(
            "physics_promotion_authorized"
        )
    child_status_ok = (
        child_math.get("status") == "completed"
        and child_phil.get("status") == "completed"
        and math_review_context == "same_context_internal_role_review"
        and child_phil.get("review_context") == "same_context_internal_role_review"
        and math_promotion is False
        and child_phil.get("physics_promotion_authorized") is False
    )
    make_check(
        checks,
        "child_review_provenance",
        child_status_ok,
        "both child reviews are completed and calibrated as same-context internal review",
    )

    make_check(
        checks,
        "parent_conflict_review",
        conflict.get("status") == "resolved"
        and conflict.get("resolution_rounds") in {1, 2}
        and conflict.get("unresolved_conflicts") == []
        and conflict.get("physics_promotion_authorized") is False,
        "parent records and resolves child differences without promotion",
    )
    make_check(
        checks,
        "parent_fusion",
        "same-context" in fusion_text
        and "zero of eight" in fusion_text
        and "blocked_adoption_open_continuation" in fusion_text
        and "No canonical ontology" in fusion_text,
        "fusion notes preserve provenance, Gate-B result, freeze, and authority limits",
    )

    gate_b = review.get("gate_b", {})
    review_authority = review.get("authority_limits", {})
    status_schema = review.get("status_schema", {})
    make_check(
        checks,
        "review_packet",
        review.get("status") == "completed"
        and gate_b.get("criterion_count") == 8
        and gate_b.get("met_count") == 0
        and gate_b.get("lawful_p7_effective_geometry_input_exists") is False
        and status_schema.get("complete") is True
        and review.get("review_provenance", {}).get("independent_replication_completed")
        is False
        and review_authority.get("physics_promotion_authorized") is False,
        "review packet is status-complete, Gate B is 0/8, and review is non-independent",
    )

    source_summary = {
        "manifest_source_count": len(source_rows),
        "manifest_sha256": sha256(MANIFEST_PATH),
        "assumption_ledger_sha256": sha256(ASSUMPTION_PATH),
        "report_sha256": sha256(REPORT_PATH),
        "model_archive_sha256": sha256(MODEL_PATH),
        "review_packet_sha256": sha256(REVIEW_PATH),
    }
    return finalize(checks, source_summary, model_result)


def finalize(
    checks: list[dict[str, Any]],
    source_summary: dict[str, Any],
    model_result: dict[str, Any],
) -> dict[str, Any]:
    failed = [item["check_id"] for item in checks if item["status"] != "PASS"]
    return {
        "schema_id": "v21_p15_t04_source_dynamics_reconstruction_validation_v1",
        "task_id": "RT-20260727-006",
        "job_id": "AJ-RT-20260727-006-001",
        "validator_id": "VAL-P15T04-SOURCE-DYNAMICS-RECONSTRUCTION-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "failed_check_ids": failed,
        "checks": checks,
        "source_summary": source_summary,
        "model_summary": {
            "status": model_result.get("status", "NOT_RUN"),
            "checks": model_result.get("checks", {}),
        },
        "authority_limits": {
            "validator_pass_is_operational_evidence_only": True,
            "theorem_truth_inferred": False,
            "canonical_ontology_modified": False,
            "source_law_adopted": False,
            "physical_metric_adopted": False,
            "physics_promotion_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        VALIDATION_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        if not VALIDATION_PATH.is_file():
            report["status"] = "FAIL"
            report["failed_check_count"] = report.get("failed_check_count", 0) + 1
            report.setdefault("failed_check_ids", []).append("validation_report_exists")
        else:
            recorded = json.loads(VALIDATION_PATH.read_text(encoding="utf-8"))
            if recorded != report:
                report["status"] = "FAIL"
                report["failed_check_count"] = report.get("failed_check_count", 0) + 1
                report.setdefault("failed_check_ids", []).append(
                    "validation_report_matches"
                )

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
