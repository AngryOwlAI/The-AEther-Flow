#!/usr/bin/env python3
"""Validate P12-T05 durable scientific-quality metrics and integration."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_ai_methodology_metrics_dashboard as dashboard_renderer  # noqa: E402
import report_physics_progress_metrics as metrics_reporter  # noqa: E402
import scientific_quality_metrics  # noqa: E402


ARTIFACT_DIR = Path(__file__).resolve().parent
FIXTURE_PATH = ARTIFACT_DIR / "fixtures" / "scientific_quality_metric_cases.json"
TAXONOMY_PATH = ARTIFACT_DIR / "scientific_quality_metric_taxonomy_v1.md"
POLICY_PATH = ARTIFACT_DIR / "scientific_quality_calibration_warning_policy_v1.md"
REPORT_PATH = ARTIFACT_DIR / "scientific_quality_validation_report.json"
RECEIPT_PATH = ARTIFACT_DIR / "scientific_quality_compact_receipt.json"
SCHEMA_ID = "p12_t05_scientific_quality_validation_report_v1"
RECEIPT_SCHEMA_ID = "p12_t05_scientific_quality_compact_receipt_v1"
SOURCE_PATHS = [
    "scripts/research_control/scientific_quality_metrics.py",
    "scripts/research_control/report_physics_progress_metrics.py",
    "scripts/research_control/render_ai_methodology_metrics_dashboard.py",
    "research_control/tasks/RT-20260723-004/artifacts/"
    "scientific_quality_metric_taxonomy_v1.md",
    "research_control/tasks/RT-20260723-004/artifacts/"
    "scientific_quality_calibration_warning_policy_v1.md",
    "research_control/tasks/RT-20260723-004/artifacts/fixtures/"
    "scientific_quality_metric_cases.json",
    "research_control/tasks/RT-20260723-004/artifacts/"
    "validate_scientific_quality_metrics.py",
    scientific_quality_metrics.ATTEMPT_LEDGER_PATH,
    scientific_quality_metrics.CANDIDATE_LINEAGE_REGISTRY_PATH,
]


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def source_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for relative in SOURCE_PATHS:
        path = REPO_ROOT / relative
        if path.is_file():
            hashes[relative] = sha256_path(path)
    return hashes


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    fixture_suite = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    check(
        "fixture_schema",
        fixture_suite.get("schema_id")
        == "durable_scientific_quality_metric_fixture_suite_v1",
        "fixture suite identity is exact",
    )
    cases = fixture_suite.get("cases", [])
    check(
        "fixture_case_count",
        isinstance(cases, list) and len(cases) >= 14,
        f"fixture cases={len(cases) if isinstance(cases, list) else 0}",
    )
    covered: set[str] = set()
    for case in cases if isinstance(cases, list) else []:
        case_id = str(case.get("case_id", ""))
        metric_id = str(case.get("metric_id", ""))
        covered.add(metric_id)
        result = scientific_quality_metrics.evaluate_metric(
            metric_id,
            case.get("evidence", {}),
        )
        warning_codes = sorted(
            warning["code"] for warning in result["warnings"]
        )
        expected_codes = sorted(case.get("expected_warning_codes", []))
        matches = (
            result["status"] == case.get("expected_status")
            and result["value"] == case.get("expected_value")
            and warning_codes == expected_codes
        )
        check(
            f"fixture:{case_id}",
            matches,
            (
                f"status={result['status']} value={result['value']} "
                f"warnings={warning_codes}"
            ),
        )
    check(
        "all_metric_families_covered",
        covered == set(scientific_quality_metrics.REQUIRED_METRIC_IDS),
        f"covered={sorted(covered)}",
    )

    taxonomy = TAXONOMY_PATH.read_text(encoding="utf-8")
    policy = POLICY_PATH.read_text(encoding="utf-8")
    normalized_taxonomy = " ".join(taxonomy.split())
    normalized_policy = " ".join(policy.split())
    for metric_id in scientific_quality_metrics.REQUIRED_METRIC_IDS:
        check(
            f"taxonomy_metric:{metric_id}",
            f"`{metric_id}`" in taxonomy,
            "metric identity appears in canonical taxonomy",
        )
    for phrase in (
        "No aggregate scientific-truth score is permitted.",
        "not an artifact count",
        "cannot substitute for an eligible-set quality diagnostic",
    ):
        check(
            f"taxonomy_boundary:{hashlib.sha256(phrase.encode()).hexdigest()[:8]}",
            phrase in normalized_taxonomy,
            phrase,
        )
    for phrase in (
        "`not_measured`: the denominator is unknown or known-empty",
        "`artifact_splitting_or_alias`",
        "Raw volume is operational context only.",
        "Keep all claim, ontology, benchmark, proof, Gate Chair, publication",
    ):
        check(
            f"policy_boundary:{hashlib.sha256(phrase.encode()).hexdigest()[:8]}",
            phrase in normalized_policy,
            phrase,
        )

    metrics_report = metrics_reporter.build_report(REPO_ROOT)
    live = metrics_report["metrics"]["durable_scientific_quality_metrics"]
    check(
        "live_report_status",
        live.get("status") == "PASS",
        f"live status={live.get('status')}",
    )
    check(
        "live_metric_count",
        live.get("metric_count") == 8,
        f"metric_count={live.get('metric_count')}",
    )
    check(
        "live_no_invalid_metrics",
        live.get("status_counts", {}).get("invalid") == 0,
        f"status_counts={live.get('status_counts')}",
    )
    check(
        "live_measured_and_not_measured_visible",
        (
            live.get("status_counts", {}).get("measured", 0) > 0
            and live.get("status_counts", {}).get("not_measured", 0) > 0
        ),
        f"status_counts={live.get('status_counts')}",
    )
    values = [
        record.get("value")
        for record in live.get("metrics", {}).values()
        if record.get("value") is not None
    ]
    check(
        "live_logical_ranges",
        all(isinstance(value, (int, float)) and 0 <= value <= 1 for value in values),
        f"measured_values={values}",
    )
    check(
        "live_unknowns_not_zero_filled",
        all(
            record.get("value") is None
            for record in live.get("metrics", {}).values()
            if record.get("status") == "not_measured"
        ),
        "every not_measured value is null",
    )
    check(
        "no_aggregate_metric",
        live.get("aggregate_metric") is None,
        "aggregate metric remains absent",
    )
    check(
        "volume_demoted",
        (
            live.get("raw_volume_is_primary_quality") is False
            and metrics_report["metrics"]["physics_progress_integration_metrics"].get(
                "primary_scientific_quality_surface"
            )
            is False
            and metrics_report["authority_boundary"].get(
                "raw_volume_is_primary_scientific_quality"
            )
            is False
        ),
        "raw volume is operational context only",
    )
    check(
        "authority_boundary",
        all(
            live.get("authority_boundary", {}).get(field) is False
            for field in (
                "aggregate_scientific_truth_score_created",
                "scientific_claims_changed",
                "distance_to_gr_delta_changed",
                "theorem_truth_inferred",
                "candidate_adoption_authorized",
                "candidate_rejection_authorized",
                "ontology_or_source_law_adopted",
                "benchmark_promotion_authorized",
                "physics_promotion_authorized",
                "gate_chair_verdict_created",
                "proof_authority",
                "publication_authority",
                "completed_derivation_authorized",
            )
        ),
        "all scientific and protected-authority flags remain false",
    )

    dashboard = dashboard_renderer.build_dashboard(REPO_ROOT)
    rendered_dashboard = dashboard_renderer.render_markdown(dashboard)
    check(
        "dashboard_primary_quality_rows",
        (
            len(dashboard.get("durable_quality_metric_rows", [])) == 8
            and dashboard.get("claim_boundary", {}).get(
                "durable_quality_is_primary_quality_surface"
            )
            is True
        ),
        "dashboard carries eight primary durable-quality rows",
    )
    check(
        "dashboard_volume_context",
        (
            dashboard.get("claim_boundary", {}).get(
                "raw_volume_is_primary_scientific_quality"
            )
            is False
            and "raw volume is operational context only" in rendered_dashboard
        ),
        "dashboard explicitly demotes raw volume",
    )
    check(
        "dashboard_order",
        (
            rendered_dashboard.index("## Durable Scientific-Quality Diagnostics")
            < rendered_dashboard.index("## Payload-Ratio Diagnostics")
        ),
        "durable-quality diagnostics precede raw volume diagnostics",
    )

    failures = [item for item in checks if item["status"] == "FAIL"]
    warning_count = len(live.get("warnings", []))
    return {
        "schema_id": SCHEMA_ID,
        "task_id": "RT-20260723-004",
        "plan_task_id": "P12-T05",
        "status": "FAIL" if failures else "PASS",
        "check_count": len(checks),
        "failure_count": len(failures),
        "warning_count": warning_count,
        "fixture_case_count": len(cases) if isinstance(cases, list) else 0,
        "metric_count": live.get("metric_count"),
        "live_status_counts": live.get("status_counts", {}),
        "checks": checks,
        "source_hashes": source_hashes(),
        "claim_boundary_summary": (
            "Eight denominator-bound identity metrics remain advisory; unknown "
            "populations are not_measured, raw volume is operational context, "
            "no aggregate truth score exists, and no scientific or protected "
            "authority changes."
        ),
    }


def build_receipt(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": RECEIPT_SCHEMA_ID,
        "task_id": "RT-20260723-004",
        "plan_task_id": "P12-T05",
        "status": report["status"],
        "result_status": "implemented_and_validated"
        if report["status"] == "PASS"
        else "repair_required",
        "metric_count": report["metric_count"],
        "fixture_case_count": report["fixture_case_count"],
        "check_count": report["check_count"],
        "failure_count": report["failure_count"],
        "warning_count": report["warning_count"],
        "live_status_counts": report["live_status_counts"],
        "validator_ids": [
            "p12_t05_scientific_quality_fixture_validator",
            "p12_t05_live_identity_binding_validator",
            "p12_t05_dashboard_demotion_validator",
            "p12_t05_authority_boundary_validator",
        ],
        "report_path": REPORT_PATH.relative_to(REPO_ROOT).as_posix(),
        "report_sha256": hashlib.sha256(
            canonical_json(report).encode("utf-8")
        ).hexdigest(),
        "source_hashes": report["source_hashes"],
        "claim_boundary_summary": report["claim_boundary_summary"],
        "authority": {
            "scientific_claims_changed": False,
            "distance_to_gr_delta_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_authority": False,
            "completed_derivation_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    receipt = build_receipt(report)
    stale: list[str] = []
    if args.write:
        REPORT_PATH.write_text(canonical_json(report), encoding="utf-8")
        RECEIPT_PATH.write_text(canonical_json(receipt), encoding="utf-8")
        metrics_snapshot = metrics_reporter.build_metrics_snapshot(REPO_ROOT)
        (REPO_ROOT / "output/physics_progress_metrics.json").write_text(
            metrics_snapshot.report_json,
            encoding="utf-8",
        )
        (REPO_ROOT / "output/physics_progress_metrics.md").write_text(
            metrics_snapshot.report_markdown,
            encoding="utf-8",
        )
        dashboard = dashboard_renderer.build_dashboard(REPO_ROOT)
        dashboard_renderer.write_outputs(
            dashboard,
            REPO_ROOT,
            dashboard_renderer.DEFAULT_JSON_PATH,
            dashboard_renderer.DEFAULT_MARKDOWN_PATH,
            dashboard_renderer.DEFAULT_WIKI_MARKDOWN_PATH,
        )
    else:
        expected_report = canonical_json(report)
        expected_receipt = canonical_json(receipt)
        if not REPORT_PATH.is_file():
            stale.append("validation report is missing")
        elif REPORT_PATH.read_text(encoding="utf-8") != expected_report:
            stale.append("validation report is stale")
        if not RECEIPT_PATH.is_file():
            stale.append("compact receipt is missing")
        elif RECEIPT_PATH.read_text(encoding="utf-8") != expected_receipt:
            stale.append("compact receipt is stale")

    summary = {
        "status": "FAIL" if report["status"] != "PASS" or stale else "PASS",
        "check_count": report["check_count"],
        "failure_count": report["failure_count"],
        "warning_count": report["warning_count"],
        "fixture_case_count": report["fixture_case_count"],
        "metric_count": report["metric_count"],
        "stale_findings": stale,
        "report_path": REPORT_PATH.relative_to(REPO_ROOT).as_posix(),
        "receipt_path": RECEIPT_PATH.relative_to(REPO_ROOT).as_posix(),
    }
    if args.json:
        print(canonical_json(summary), end="")
    else:
        print(
            f"Scientific-quality metric validation: {summary['status']} "
            f"({summary['check_count']} checks)"
        )
        for finding in stale:
            print(f"- {finding}", file=sys.stderr)
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
