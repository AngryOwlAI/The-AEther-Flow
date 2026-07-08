#!/usr/bin/env python3
"""Validate the v18 P6-T04 finite toy response v2 model-zoo integration."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260708-017"
ENTRY = TASK_DIR / "artifacts" / "finite_toy_response_v2_model_zoo_entry.yaml"
SCHEMA = ROOT / "research_control" / "design" / "source_model_zoo_schema_v18_extension.md"
REGISTRY = ROOT / "registries" / "SOURCE_MODEL_ZOO_REGISTRY.csv"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260708-017-001.yaml"
REPORT = TASK_DIR / "artifacts" / "p6_t04_finite_toy_response_v2_model_zoo_integration_report.json"


ENTRY_MARKERS = [
    'zoo_entry_id: "FTMR-V2-PATH3"',
    'model_id: "SMZ-FTRV2-PATH3-001"',
    'model_kind: "finite_toy_metric_response_model"',
    'plan_task_id: "P6-T04"',
    'task_type: "finite_toy_response_v2_model_zoo_integration"',
    'finite_source_set: "S_v2 = {a,b,c}"',
    'source_relation_family: "A_v2 = {{a,b},{b,c}}"',
    'induced_response_relation: "R_v2({x,y}) = d_A(x,y)"',
    'model_result: "positive_toy_model_constructed"',
    'stress_result: "survives_as_finite_toy_model"',
    'freeze_status: "not_frozen"',
    'target_import_status: "blocked"',
    'benchmark_status: "blocked"',
    'physics_promotion_authorized: false',
    'claim_boundary_preserved: true',
    'no_target_metric_import: true',
    'not_g_eff: true',
    'not_matter_coupling: true',
    'not_einstein_equations: true',
    'not_benchmark_promotion: true',
    'next_plan_task_id: "P6-T05"',
]

SCHEMA_MARKERS = [
    "Source Model Zoo Schema v18 Extension",
    "plan_task_id:",
    "finite_toy_metric_response_model",
    "registries/SOURCE_MODEL_ZOO_REGISTRY.csv",
    "R_v2({x,y}) = d_A(x,y)",
    "physics_promotion_authorized: false",
]

COMPLETION_MARKERS = [
    'plan_task_id: "P6-T04"',
    'objective_result: "completed"',
    'claim_boundary_preserved: true',
    'selected_next_plan_task_id: "P6-T05"',
]


def require_markers(path: Path, markers: list[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [marker for marker in markers if marker not in text]


def validate_registry() -> list[str]:
    if not REGISTRY.exists():
        return ["missing SOURCE_MODEL_ZOO_REGISTRY.csv"]
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    matches = [row for row in rows if row.get("zoo_entry_id") == "FTMR-V2-PATH3"]
    if len(matches) != 1:
        return [f"expected exactly one FTMR-V2-PATH3 row found {len(matches)}"]
    row = matches[0]
    checks = {
        "model_id": "SMZ-FTRV2-PATH3-001",
        "model_kind": "finite_toy_metric_response_model",
        "entry_status": "draft_control",
        "task_id": "RT-20260708-017",
        "model_result": "positive_toy_model_constructed",
        "stress_result": "survives_as_finite_toy_model",
        "freeze_status": "not_frozen",
        "target_import_status": "blocked",
        "benchmark_status": "blocked",
        "validation_status": "PASS",
    }
    failures: list[str] = []
    for key, expected in checks.items():
        if row.get(key) != expected:
            failures.append(f"registry {key} expected {expected!r} got {row.get(key)!r}")
    forbidden = row.get("forbidden_overreads", "")
    for phrase in ["g_eff construction", "matter coupling", "Einstein equations", "completed derivation"]:
        if phrase not in forbidden:
            failures.append(f"registry forbidden_overreads missing {phrase!r}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    for path in [ENTRY, SCHEMA, REGISTRY, COMPLETION]:
        if not path.exists():
            failures.append(f"missing {path.relative_to(ROOT)}")

    if ENTRY.exists():
        failures.extend(f"entry missing marker: {marker}" for marker in require_markers(ENTRY, ENTRY_MARKERS))
    if SCHEMA.exists():
        failures.extend(f"schema missing marker: {marker}" for marker in require_markers(SCHEMA, SCHEMA_MARKERS))
    if COMPLETION.exists():
        failures.extend(f"completion missing marker: {marker}" for marker in require_markers(COMPLETION, COMPLETION_MARKERS))
    failures.extend(validate_registry())

    report = {
        "task_id": "RT-20260708-017",
        "plan_task_id": "P6-T04",
        "validator": "validate_p6_t04_finite_toy_response_v2_model_zoo_integration",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "checked_paths": [
            str(ENTRY.relative_to(ROOT)),
            str(SCHEMA.relative_to(ROOT)),
            str(REGISTRY.relative_to(ROOT)),
            str(COMPLETION.relative_to(ROOT)),
        ],
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
