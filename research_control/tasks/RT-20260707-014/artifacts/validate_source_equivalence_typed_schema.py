#!/usr/bin/env python3
"""Validate the v18 P2-T02 source-equivalence typed schema packet."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = REPO_ROOT / "research_control/design/source_equivalence_typed_object_schema_v1.md"
REGISTRY_PATH = REPO_ROOT / "registries/SOURCE_EQUIVALENCE_OBJECT_REGISTRY.csv"
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260707-014/artifacts/source_equivalence_typed_schema_validation.json"
)

REQUIRED_COLUMNS = [
    "object_id",
    "artifact_path",
    "task_id",
    "source_family_symbol",
    "object_set_status",
    "morphism_status",
    "invariant_ledger_status",
    "comparison_rule_status",
    "identity_closure_status",
    "inverse_closure_status",
    "composition_closure_status",
    "retainh_status",
    "genh_status",
    "no_target_guard_status",
    "proof_state",
    "blocked_overread",
    "created_at",
    "notes",
]

REQUIRED_SCHEMA_TOKENS = [
    "source_equivalence_typed_object_v1",
    "source_family",
    "objects",
    "morphisms",
    "invariant_ledger",
    "comparison_rule",
    "closure",
    "retainh",
    "genh",
    "no_target_guard",
    "adopted_by_gate",
    "gate_protected_adoption",
    "target_metric_imported",
    "target_atlas_imported",
    "stress_energy_semantics_imported",
    "matter_action_imported",
    "P2-T03",
]

REQUIRED_ENUM_TOKENS = [
    "declared",
    "missing",
    "partial",
    "countermodel",
    "finite",
    "locally_finite",
    "family_level",
    "explicit",
    "implicit",
    "generated",
    "proven",
    "assumed",
    "refuted",
    "unknown",
    "supplied",
    "derived",
    "not_required",
    "required",
    "candidate",
    "draft_control",
    "gate_blocked",
]

BLOCKED_CLAIM_TOKENS = [
    "This schema is not a theorem",
    "general EqSrc discharge",
    "RetainH adoption",
    "GenH adoption",
    "source-law adoption",
    "benchmark promotion",
    "completed-derivation claim",
    "proof_authority: false",
    "physics_promotion_authorized: false",
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

    if registry_rows:
        errors.append(f"registry must be header-only for P2-T02; found {len(registry_rows)} data rows")

    for column in REQUIRED_COLUMNS:
        if f"`{column}`" not in schema_text and column not in schema_text:
            errors.append(f"schema missing required registry column: {column}")

    for token in REQUIRED_SCHEMA_TOKENS:
        if token not in schema_text:
            errors.append(f"schema missing required token: {token}")

    for token in REQUIRED_ENUM_TOKENS:
        if token not in schema_text:
            errors.append(f"schema missing required enum token: {token}")

    for token in BLOCKED_CLAIM_TOKENS:
        if token not in schema_text:
            errors.append(f"schema missing blocked-claim token: {token}")

    for guard in [
        "target_metric_imported",
        "target_atlas_imported",
        "stress_energy_semantics_imported",
        "matter_action_imported",
    ]:
        marker = f"{guard}:"
        if marker not in schema_text or "must_equal: false" not in schema_text:
            errors.append(f"schema missing false no-target guard for {guard}")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "schema_path": SCHEMA_PATH.relative_to(REPO_ROOT).as_posix(),
        "registry_path": REGISTRY_PATH.relative_to(REPO_ROOT).as_posix(),
        "required_columns": REQUIRED_COLUMNS,
        "registry_data_rows": len(registry_rows),
        "population_deferred_to": "P2-T03",
        "physics_delta_allowed": False,
        "retainh_genh_adoption_gate_protected": True,
        "errors": errors,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
