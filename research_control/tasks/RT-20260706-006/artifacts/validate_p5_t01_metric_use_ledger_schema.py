#!/usr/bin/env python3
"""Validate the v17 P5-T01 metric-use ledger schema packet."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = REPO_ROOT / "research_control/design/metric_use_ledger_schema_v1.md"
REGISTRY_PATH = REPO_ROOT / "registries/METRIC_USE_LEDGER.csv"
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260706-006/artifacts/p5_t01_metric_use_ledger_schema_report.json"
)

REQUIRED_COLUMNS = [
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

ALLOWED_CATEGORIES = [
    "scoped_source_extension_context",
    "source_side_relation_input_candidate",
    "finite_local_witness_context",
    "blocked_physical_metric_use",
    "forbidden_import_detected",
]

FORBIDDEN_USES = [
    "physical_lorentzian_metric",
    "proper_time_normalization",
    "detector_calibration",
    "stress_energy_semantics",
    "matter_action_premise",
    "Einstein_equation_premise",
    "benchmark_fit_premise",
]

BLOCKED_PROMOTION_TERMS = [
    "physical Lorentzian metric",
    "proper-time normalizer",
    "detector calibration object",
    "stress-energy premise",
    "matter-action premise",
    "Einstein-equation premise",
    "benchmark-fit premise",
]


def main() -> int:
    errors: list[str] = []

    if not SCHEMA_PATH.exists():
        errors.append(f"missing schema path: {SCHEMA_PATH.relative_to(REPO_ROOT)}")
        schema_text = ""
    else:
        schema_text = SCHEMA_PATH.read_text(encoding="utf-8")

    if not REGISTRY_PATH.exists():
        errors.append(f"missing registry path: {REGISTRY_PATH.relative_to(REPO_ROOT)}")
        registry_header: list[str] = []
        registry_rows: list[dict[str, str]] = []
    else:
        with REGISTRY_PATH.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            registry_header = reader.fieldnames or []
            registry_rows = list(reader)

    if registry_header != REQUIRED_COLUMNS:
        errors.append(
            "registry header mismatch: "
            + ",".join(registry_header)
            + " != "
            + ",".join(REQUIRED_COLUMNS)
        )

    for column in REQUIRED_COLUMNS:
        if f"`{column}`" not in schema_text and column not in schema_text:
            errors.append(f"schema missing required column: {column}")

    for category in ALLOWED_CATEGORIES:
        if category not in schema_text:
            errors.append(f"schema missing allowed category: {category}")

    for forbidden_use in FORBIDDEN_USES:
        if forbidden_use not in schema_text:
            errors.append(f"schema missing forbidden metric use: {forbidden_use}")

    for term in BLOCKED_PROMOTION_TERMS:
        if term not in schema_text:
            errors.append(f"schema missing blocked-promotion prose term: {term}")

    if "does not populate the ledger" not in schema_text:
        errors.append("schema must state that P5-T01 does not populate the ledger")

    if registry_rows:
        for index, row in enumerate(registry_rows, start=2):
            row_category = row.get("use_category", "")
            if row_category not in ALLOWED_CATEGORIES:
                errors.append(f"row {index} has invalid use_category: {row_category}")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "schema_path": SCHEMA_PATH.relative_to(REPO_ROOT).as_posix(),
        "registry_path": REGISTRY_PATH.relative_to(REPO_ROOT).as_posix(),
        "required_columns": REQUIRED_COLUMNS,
        "allowed_use_categories": ALLOWED_CATEGORIES,
        "forbidden_metric_uses": FORBIDDEN_USES,
        "registry_data_rows": len(registry_rows),
        "population_deferred_to": "P5-T02",
        "physics_delta_allowed": False,
        "errors": errors,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
