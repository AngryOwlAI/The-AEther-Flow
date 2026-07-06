#!/usr/bin/env python3
"""Validate v17 P5-T02 metric-use ledger initial population."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LEDGER = ROOT / "registries" / "METRIC_USE_LEDGER.csv"
REPORT = (
    ROOT
    / "research_control"
    / "tasks"
    / "RT-20260706-007"
    / "artifacts"
    / "p5_t02_metric_use_ledger_population_report.json"
)

EXPECTED_HEADER = [
    "use_id",
    "task_id",
    "artifact_path",
    "object_used",
    "use_category",
    "declared_scope",
    "allowed_use",
    "forbidden_interpretations",
    "no_target_guard_path",
    "audit_status",
    "stress_status",
    "created_at",
    "notes",
]

ALLOWED_CATEGORIES = {
    "scoped_source_extension_context",
    "source_side_relation_input_candidate",
    "finite_local_witness_context",
    "blocked_physical_metric_use",
    "forbidden_import_detected",
}

FORBIDDEN_USES = {
    "physical_lorentzian_metric",
    "proper_time_normalization",
    "detector_calibration",
    "stress_energy_semantics",
    "matter_action_premise",
    "Einstein_equation_premise",
    "benchmark_fit_premise",
}

RECOMMENDED_AUDIT = {
    "not_audited",
    "audited_clean",
    "forbidden_import_detected",
    "blocked_by_scope",
}

RECOMMENDED_STRESS = {
    "not_stressed",
    "stress_survived",
    "repair_required",
    "scoped_obstruction",
    "not_applicable",
}

REQUIRED_PATHS = {
    "research_control/tasks/RT-20260614-222/artifacts/251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex": 5,
    "research_control/tasks/RT-20260704-021/artifacts/source_side_coupling_law_target_specification_v1.tex": 3,
    "research_control/tasks/RT-20260705-047/artifacts/source_side_coupling_law_candidate_v1.tex": 3,
    "research_control/current_frontier.md": 4,
    "registries/DISTANCE_TO_GR_LEDGER.csv": 4,
}

NO_USE_JUSTIFIED_PATHS = {
    "research_control/tasks/RT-20260704-021/artifacts/source_side_coupling_law_target_specification_v1.tex",
    "research_control/tasks/RT-20260705-047/artifacts/source_side_coupling_law_candidate_v1.tex",
}


def split_semicolon(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    rows: list[dict[str, str]] = []

    if not LEDGER.exists():
        fail(errors, f"missing ledger: {LEDGER}")
    else:
        with LEDGER.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != EXPECTED_HEADER:
                fail(errors, f"unexpected header: {reader.fieldnames}")
            rows = list(reader)

    if len(rows) != 19:
        fail(errors, f"expected 19 populated rows and found {len(rows)}")

    seen_ids: set[str] = set()
    path_counts = {path: 0 for path in REQUIRED_PATHS}
    for index, row in enumerate(rows, start=2):
        use_id = row.get("use_id", "")
        if not use_id:
            fail(errors, f"line {index}: blank use_id")
        elif use_id in seen_ids:
            fail(errors, f"line {index}: duplicate use_id {use_id}")
        seen_ids.add(use_id)

        if not re.fullmatch(r"MUL-RT-20260706-007-\d{3}", use_id):
            fail(errors, f"line {index}: unexpected P5-T02 use_id format {use_id}")

        if row.get("task_id") != "RT-20260706-007":
            fail(errors, f"line {index}: task_id must be RT-20260706-007")

        artifact_path = row.get("artifact_path", "")
        if artifact_path in path_counts:
            path_counts[artifact_path] += 1
        else:
            fail(errors, f"line {index}: artifact_path outside required scope {artifact_path}")

        if row.get("use_category") not in ALLOWED_CATEGORIES:
            fail(errors, f"line {index}: invalid use_category {row.get('use_category')}")

        forbidden = split_semicolon(row.get("forbidden_interpretations", ""))
        unknown = forbidden - FORBIDDEN_USES
        if unknown:
            fail(errors, f"line {index}: unknown forbidden_interpretations {sorted(unknown)}")
        if not forbidden:
            fail(errors, f"line {index}: empty forbidden_interpretations")

        if not row.get("declared_scope") or not row.get("allowed_use"):
            fail(errors, f"line {index}: declared_scope and allowed_use must be nonblank")

        if not row.get("no_target_guard_path"):
            fail(errors, f"line {index}: no_target_guard_path must be nonblank")

        if row.get("audit_status") not in RECOMMENDED_AUDIT:
            fail(errors, f"line {index}: audit_status outside recommended values")
        if row.get("stress_status") not in RECOMMENDED_STRESS:
            fail(errors, f"line {index}: stress_status outside recommended values")

        category = row.get("use_category")
        object_used = row.get("object_used", "")
        if "g_eff" in object_used and category != "scoped_source_extension_context":
            fail(errors, f"line {index}: g_eff row must remain scoped source-extension context")
        if "MetricData" in object_used and category != "blocked_physical_metric_use":
            if category != "source_side_relation_input_candidate":
                fail(errors, f"line {index}: MetricData row has unsafe category {category}")

        lower_payload = " ".join(row.values()).lower()
        if "proper_time" in lower_payload and "proper_time_normalization" not in forbidden:
            fail(errors, f"line {index}: proper_time row missing proper_time_normalization block")
        if "detector" in lower_payload and "detector_calibration" not in forbidden:
            fail(errors, f"line {index}: detector row missing detector_calibration block")
        if "stress" in lower_payload and "stress_energy_semantics" not in forbidden:
            fail(errors, f"line {index}: stress row missing stress_energy_semantics block")
        if "einstein" in lower_payload and "Einstein_equation_premise" not in forbidden:
            fail(errors, f"line {index}: Einstein row missing Einstein_equation_premise block")
        if "benchmark" in lower_payload and "benchmark_fit_premise" not in forbidden:
            fail(errors, f"line {index}: benchmark row missing benchmark_fit_premise block")

        promotion_phrases = [
            "scope expanded",
            "adopted metricdata",
            "physical lorentzian metric authorized",
            "proper time normalized",
            "detectors calibrated",
            "stress energy imported",
            "matter action defined",
            "einstein equations derived",
            "benchmark promoted",
            "completed derivation",
        ]
        for phrase in promotion_phrases:
            if phrase in lower_payload:
                fail(errors, f"line {index}: promotional phrase detected: {phrase}")

    for path, minimum in REQUIRED_PATHS.items():
        if path_counts[path] < minimum:
            fail(errors, f"{path} has {path_counts[path]} rows but expected at least {minimum}")

    for path in NO_USE_JUSTIFIED_PATHS:
        source_text = (ROOT / path).read_text(encoding="utf-8")
        if "g_eff" in source_text or "MetricData(E)" in source_text:
            warnings.append(f"{path} no-use justification should be rechecked after source drift")

    status = "PASS" if not errors else "FAIL"
    report = {
        "status": status,
        "ledger_path": str(LEDGER.relative_to(ROOT)),
        "row_count": len(rows),
        "required_path_counts": path_counts,
        "allowed_categories": sorted(ALLOWED_CATEGORIES),
        "forbidden_metric_uses": sorted(FORBIDDEN_USES),
        "errors": errors,
        "warnings": warnings,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
