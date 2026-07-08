#!/usr/bin/env python3
"""Validate the v18 P4-T02 countermodel-obligation schema and registry."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCHEMA = ROOT / "research_control/design/minimal_countermodel_obligation_schema_v1.md"
REGISTRY = ROOT / "registries/COUNTERMODEL_OBLIGATION_REGISTRY.csv"
REPORT = (
    ROOT
    / "research_control/tasks/RT-20260708-002/artifacts/p4_t02_countermodel_obligation_schema_registry_report.json"
)

REQUIRED_COLUMNS = [
    "obligation_id",
    "task_id",
    "artifact_path",
    "theorem_family",
    "countermodel_slot",
    "status",
    "result_artifact",
    "obstruction_id",
    "scope",
    "global_no_go_claimed",
    "created_at",
    "notes",
]

EXPECTED_OBLIGATION_IDS = {
    "CMO-V18-P3T02-EQSRC-MISSING-INVERSE",
    "CMO-V18-P3T03-EQSRC-RETAINH-NEEDED",
    "CMO-V18-P3T03-EQSRC-GENH-NEEDED",
    "CMO-V18-P3T04-EQSRC-TARGET-IMPORT",
    "CMO-V18-P3T05-EQSRC-MISSING-INVERSE-STRESS",
    "CMO-V18-P3T05-EQSRC-MISSING-COMPOSITION",
    "CMO-V18-P3T05-EQSRC-ADOPTION-OVERREAD",
}

REQUIRED_SCHEMA_TOKENS = [
    "CountermodelObligationRecord_v1",
    "registries/COUNTERMODEL_OBLIGATION_REGISTRY.csv",
    "obligation_id,task_id,artifact_path,theorem_family,countermodel_slot,status,result_artifact,obstruction_id,scope,global_no_go_claimed,created_at,notes",
    "filled",
    "waived_by_ddr",
    "not_applicable_by_ddr",
    "deferred_by_ddr",
    "next_plan_task_id: \"P4-T03\"",
    "a local countermodel is not a program-wide no-go conclusion",
    "physics_promotion_authorized: false",
    "proof_authority: false",
]

SOURCE_EVIDENCE = {
    "CMO-V18-P3T02-EQSRC-MISSING-INVERSE": (
        ROOT / "research_control/tasks/RT-20260707-020/artifacts/eqsrc_family_closure_attempt_receipt.md",
        "missing-inverse countermodel slot",
    ),
    "CMO-V18-P3T03-EQSRC-RETAINH-NEEDED": (
        ROOT / "research_control/tasks/RT-20260707-021/artifacts/retainh_genh_primitive_boundary_receipt.md",
        "RetainH_status_for_H_retention_extension",
    ),
    "CMO-V18-P3T03-EQSRC-GENH-NEEDED": (
        ROOT / "research_control/tasks/RT-20260707-021/artifacts/retainh_genh_primitive_boundary_receipt.md",
        "GenH_status_for_H_generated_extension",
    ),
    "CMO-V18-P3T04-EQSRC-TARGET-IMPORT": (
        ROOT / "research_control/tasks/RT-20260707-022/artifacts/eqsrc_family_closure_smuggling_audit_receipt.md",
        "source-side as written",
    ),
    "CMO-V18-P3T05-EQSRC-MISSING-INVERSE-STRESS": (
        ROOT / "research_control/tasks/RT-20260707-023/jobs/completions/AJC-AJ-RT-20260707-023-001.yaml",
        "remove_inverse_closure: \"finite_countermodel\"",
    ),
    "CMO-V18-P3T05-EQSRC-MISSING-COMPOSITION": (
        ROOT / "research_control/tasks/RT-20260707-023/jobs/completions/AJC-AJ-RT-20260707-023-001.yaml",
        "remove_composition_closure: \"finite_countermodel\"",
    ),
    "CMO-V18-P3T05-EQSRC-ADOPTION-OVERREAD": (
        ROOT / "research_control/tasks/RT-20260707-023/jobs/completions/AJC-AJ-RT-20260707-023-001.yaml",
        "treat_theorem_candidate_as_adopted_EqSrc: \"scoped_obstruction\"",
    ),
}

ALLOWED_STATUSES = {
    "filled",
    "pending",
    "waived_by_ddr",
    "not_applicable_by_ddr",
    "deferred_by_ddr",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not SCHEMA.exists():
        errors.append(f"missing schema path: {rel(SCHEMA)}")
        schema_text = ""
    else:
        schema_text = SCHEMA.read_text(encoding="utf-8")

    for token in REQUIRED_SCHEMA_TOKENS:
        if token not in schema_text:
            errors.append(f"schema missing required token: {token}")

    rows: list[dict[str, str]] = []
    header: list[str] = []
    if not REGISTRY.exists():
        errors.append(f"missing registry path: {rel(REGISTRY)}")
    else:
        with REGISTRY.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            header = reader.fieldnames or []
            rows = list(reader)

    if header != REQUIRED_COLUMNS:
        errors.append(
            "registry header mismatch: " + ",".join(header) + " != " + ",".join(REQUIRED_COLUMNS)
        )

    row_ids = {row.get("obligation_id", "") for row in rows}
    missing_rows = sorted(EXPECTED_OBLIGATION_IDS - row_ids)
    extra_rows = sorted(row_ids - EXPECTED_OBLIGATION_IDS)
    if missing_rows:
        errors.append("missing expected seed rows: " + ";".join(missing_rows))
    if extra_rows:
        warnings.append("extra registry rows present: " + ";".join(extra_rows))

    for row in rows:
        row_id = row.get("obligation_id", "")
        for column in REQUIRED_COLUMNS:
            if column == "obstruction_id":
                continue
            if not row.get(column, "").strip():
                errors.append(f"{row_id} missing required column value: {column}")
        if row.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{row_id} has invalid status: {row.get('status')}")
        if row.get("global_no_go_claimed") != "false":
            errors.append(f"{row_id} must set global_no_go_claimed to false")
        if row.get("theorem_family") != "eqsrc":
            errors.append(f"{row_id} expected theorem_family eqsrc for P3 seed rows")
        for path_column in ("artifact_path", "result_artifact"):
            path_value = row.get(path_column, "")
            if path_value and not (ROOT / path_value).exists():
                errors.append(f"{row_id} {path_column} does not exist: {path_value}")
        if "program-wide no-go" in row.get("notes", "").lower() and "does not authorize" not in row.get(
            "notes", ""
        ).lower() and "forbids" not in row.get("notes", "").lower():
            warnings.append(f"{row_id} references program-wide no-go without explicit denial wording")

    for row_id, (path, token) in SOURCE_EVIDENCE.items():
        if not path.exists():
            errors.append(f"missing source evidence for {row_id}: {rel(path)}")
            continue
        if token not in path.read_text(encoding="utf-8"):
            errors.append(f"source evidence for {row_id} missing token: {token}")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "schema_path": rel(SCHEMA),
        "schema_hash": sha256(SCHEMA) if SCHEMA.exists() else "",
        "registry_path": rel(REGISTRY),
        "registry_hash": sha256(REGISTRY) if REGISTRY.exists() else "",
        "required_columns": REQUIRED_COLUMNS,
        "seed_row_count": len(rows),
        "expected_seed_row_count": len(EXPECTED_OBLIGATION_IDS),
        "all_seed_rows_global_no_go_false": all(
            row.get("global_no_go_claimed") == "false" for row in rows
        ),
        "next_route": "P4-T03",
        "physics_delta_allowed": False,
        "errors": errors,
        "warnings": warnings,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
