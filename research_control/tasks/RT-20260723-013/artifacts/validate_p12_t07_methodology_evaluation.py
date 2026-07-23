#!/usr/bin/env python3
"""Validate deterministic P12-T07 methodology-evaluation artifacts."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_ROOT = ROOT / "research_control/tasks/RT-20260723-013/artifacts"
BUILDER_PATH = ARTIFACT_ROOT / "build_p12_t07_methodology_evaluation.py"
REPORT_PATH = ARTIFACT_ROOT / "p12_t07_methodology_validation.json"


def load_builder():
    spec = importlib.util.spec_from_file_location("p12_t07_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load P12-T07 builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def check(
    checks: list[dict[str, str]],
    check_id: str,
    condition: bool,
    detail: str,
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        }
    )


def build_report() -> dict[str, Any]:
    builder = load_builder()
    expected_outputs = builder.build_outputs()
    checks: list[dict[str, str]] = []

    for relative_path, content in expected_outputs.items():
        path = ROOT / relative_path
        exists = path.is_file()
        check(checks, f"output_exists:{relative_path}", exists, f"exists={exists}")
        if exists:
            observed = path.read_text(encoding="utf-8")
            check(
                checks,
                f"output_deterministic:{relative_path}",
                observed == content,
                f"observed_sha256={sha256_bytes(observed.encode('utf-8'))}",
            )

    results_path = ROOT / builder.OUTPUT_PATHS["results"]
    results = json.loads(results_path.read_text(encoding="utf-8"))
    mechanisms = {row["mechanism_id"]: row for row in results["mechanisms"]}

    payload = mechanisms["physics_payload_admission_gate"]["control_on"]
    check(
        checks,
        "payload_gate_counts",
        payload
        == {
            "case_count": 10,
            "rejected_case_count": 5,
            "admitted_case_count": 4,
            "legacy_readable_case_count": 1,
            "rejected_case_ids": [
                "prospective_missing_block",
                "selector_only_rejected",
                "process_receipt_rejected_as_physics",
                "project_system_mislabeled_physics",
                "authority_overread_rejected",
            ],
        },
        f"payload={payload}",
    )

    family = mechanisms["family_freeze_and_reopening_gate"]["control_on"]
    check(
        checks,
        "family_freeze_counts",
        family["case_count"] == 11
        and family["repeated_cycle_suppression_count"] == 3
        and family["lawful_route_preservation_count"] == 6
        and family["frozen_family_count"] == 5
        and family["global_no_go_inferred"] is False,
        f"family={family}",
    )

    route = mechanisms["dual_budget_and_ordinary_route_guard"]["control_on"]
    check(
        checks,
        "ordinary_route_counts",
        route["dual_budget_fixture_case_count"] == 12
        and route["dual_budget_admitted_count"] == 5
        and route["dual_budget_rejected_count"] == 7
        and route["dual_budget_rejected_error_count"] == 8
        and route["system_success_counts_as_physics"] is False
        and route["system_success_counts_as_distance_to_gr"] is False
        and route["fixture_case_count"] == 12
        and route["fixture_fail_expected_count"] == 6
        and route["fixture_warn_expected_count"] == 1
        and route["fixture_pass_expected_count"] == 5
        and route["live_consecutive_project_system_tasks"] == 9
        and route["live_selected_plan_task_id"] == "P12-T07",
        f"route={route}",
    )

    review = mechanisms["review_context_diversity"]["control_on"]
    check(
        checks,
        "review_context_counts",
        review["review_record_count"] == 4
        and review["reviewed_object_count"] == 2
        and review["eligible_cross_context_axis_count"] == 10
        and review["assessment_disagreement_count"] == 3
        and review["exact_agreement_count"] == 7
        and review["false_consensus_risk_count"] == 7
        and review["context_classification_counts"].get(
            "different_model_review", 0
        )
        == 0,
        f"review={review}",
    )

    quality = mechanisms[
        "denominator_bound_scientific_quality_metrics"
    ]["control_on"]
    check(
        checks,
        "quality_metric_counts",
        quality["metric_count"] == 8
        and quality["live_measured_count"] == 3
        and quality["live_not_measured_count"] == 5
        and quality["live_invalid_count"] == 0
        and quality["fixture_case_count"] == 14
        and quality["check_count"] == 44,
        f"quality={quality}",
    )
    quality_mismatches = quality["live_source_hash_mismatches"]
    check(
        checks,
        "quality_source_integrity_defect_preserved",
        quality["live_source_binding_status"] == "stale"
        and quality["live_source_hash_mismatch_count"] == 3
        and {
            row["path"] for row in quality_mismatches
        }
        == {
            "research_control/tasks/RT-20260723-004/artifacts/fixtures/scientific_quality_metric_cases.json",
            "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_calibration_warning_policy_v1.md",
            "research_control/tasks/RT-20260723-004/artifacts/scientific_quality_metric_taxonomy_v1.md",
        },
        f"quality_mismatches={quality_mismatches}",
    )

    attempts = results["attempt_rework_visibility"]
    check(
        checks,
        "attempt_rework_counts",
        attempts["event_count"] == 8
        and attempts["represented_task_count"] == 7
        and attempts["validation_catch_count"] == 1
        and attempts["audit_objection_count"] == 1
        and attempts["repair_event_count"] == 2
        and attempts["physics_failure_count"] == 0
        and attempts["abandonment_status"] == "not_measured",
        f"attempts={attempts}",
    )

    check(
        checks,
        "causal_identifiability_guard",
        results["evaluation_design"]["causal_inference_status"]
        == "not_identified"
        and results["cross_mechanism_assessment"][
            "causal_superiority_established_count"
        ]
        == 0
        and results["authority_boundary"]["causal_superiority_established"]
        is False,
        f"design={results['evaluation_design']}",
    )

    for child_id in ("child_phys_math", "child_phys_phil"):
        relative_path = builder.CHILD_PATHS[child_id]
        child = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
        check(
            checks,
            f"{child_id}_complete",
            child.get("status") == "completed"
            and child.get("execution_unit_id") == child_id,
            f"status={child.get('status')}",
        )
        authority = child.get("authority_boundary", {})
        check(
            checks,
            f"{child_id}_authority",
            all(value is False for value in authority.values()),
            f"authority={authority}",
        )

    conflict = yaml.safe_load(
        (ROOT / builder.CHILD_PATHS["conflict_review"]).read_text(
            encoding="utf-8"
        )
    )
    check(
        checks,
        "parent_conflict_review",
        conflict.get("verdict") == "resolved"
        and conflict.get("unresolved_conflicts") == [],
        f"verdict={conflict.get('verdict')} unresolved={conflict.get('unresolved_conflicts')}",
    )

    memo = (ROOT / builder.OUTPUT_PATHS["memo"]).read_text(encoding="utf-8")
    for phrase in (
        "causal improvement in scientific truth",
        "not physics evidence",
        "independent-replication counts remain zero",
        "source-integrity defect",
        "P12-T07 is therefore complete",
    ):
        check(
            checks,
            f"memo_phrase:{phrase[:24]}",
            phrase in memo,
            f"phrase={phrase!r}",
        )

    authority = results["authority_boundary"]
    check(
        checks,
        "authority_boundary",
        all(value is False for value in authority.values()),
        f"authority={authority}",
    )
    check(
        checks,
        "source_hash_exactness",
        all(
            builder.sha256_path(path) == expected
            for path, expected in builder.SOURCE_HASHES.items()
        ),
        f"source_count={len(builder.SOURCE_HASHES)}",
    )

    failure_count = sum(1 for item in checks if item["status"] != "PASS")
    return {
        "schema_id": "v21_p12_t07_methodology_validation_v1",
        "task_id": "RT-20260723-013",
        "plan_task_id": "P12-T07",
        "status": "PASS" if failure_count == 0 else "FAIL",
        "check_count": len(checks),
        "failure_count": failure_count,
        "checks": checks,
        "source_hashes": dict(sorted(builder.SOURCE_HASHES.items())),
        "output_hashes": {
            path: sha256_bytes(content.encode("utf-8"))
            for path, content in expected_outputs.items()
        },
        "claim_boundary_summary": "Reproducible bounded methodology evaluation only; causal scientific superiority external review theorem truth ontology Distance-to-GR promotion proof and publication authority remain false.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.write_report == args.check:
        parser.error("choose exactly one of --write-report or --check")

    report = build_report()
    rendered = canonical_json(report)
    if args.write_report:
        REPORT_PATH.write_text(rendered, encoding="utf-8")
    else:
        if not REPORT_PATH.is_file():
            report["status"] = "FAIL"
            report["failure_count"] += 1
            report["checks"].append(
                {
                    "check_id": "validation_report_exists",
                    "status": "FAIL",
                    "detail": "validation report does not exist",
                }
            )
        elif REPORT_PATH.read_text(encoding="utf-8") != rendered:
            report["status"] = "FAIL"
            report["failure_count"] += 1
            report["checks"].append(
                {
                    "check_id": "validation_report_deterministic",
                    "status": "FAIL",
                    "detail": "stored validation report differs from current result",
                }
            )
    if args.json:
        print(canonical_json(report), end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
