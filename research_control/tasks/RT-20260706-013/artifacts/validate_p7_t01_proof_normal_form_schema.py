#!/usr/bin/env python3
"""Validate the P7-T01 proof-normal-form schema and registry header."""

from __future__ import annotations

import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = REPO_ROOT / "research_control/formalization/proof_normal_form_schema_v1.md"
REGISTRY_PATH = REPO_ROOT / "registries/PROOF_NORMAL_FORM_REGISTRY.csv"
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260706-013/artifacts/p7_t01_proof_normal_form_schema_report.json"
)

EXPECTED_HEADER = [
    "proof_normal_form_row_id",
    "object_id",
    "source_artifact_path",
    "claim_type",
    "authority_status",
    "status",
    "premises",
    "forbidden_premises",
    "conclusion",
    "scope",
    "allowed_uses",
    "non_conclusions",
    "depends_on",
    "eligible_next_routes",
    "machine_checkable_fragment",
    "created_at",
    "notes",
]

REQUIRED_TOKENS = [
    "claim_types:",
    "authority_statuses:",
    "statuses:",
    "definition",
    "lemma",
    "theorem",
    "proposition",
    "obstruction",
    "decision",
    "boundary",
    "nonconclusion",
    "science_draft",
    "scientific_gate",
    "control",
    "support_only",
    "draft_control",
    "scoped_evidence",
    "scoped_adopted",
    "blocked",
    "frozen_negative",
    "not_started",
    "No proof-normal-form row may convert support-only schema work into proof authority.",
]


def main() -> int:
    errors: list[str] = []

    if not SCHEMA_PATH.exists():
        errors.append(f"missing schema: {SCHEMA_PATH.relative_to(REPO_ROOT)}")
        schema_text = ""
    else:
        schema_text = SCHEMA_PATH.read_text(encoding="utf-8")

    for token in REQUIRED_TOKENS:
        if token not in schema_text:
            errors.append(f"schema missing token: {token}")

    if not REGISTRY_PATH.exists():
        errors.append(f"missing registry: {REGISTRY_PATH.relative_to(REPO_ROOT)}")
        header: list[str] = []
        rows: list[list[str]] = []
    else:
        with REGISTRY_PATH.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            try:
                header = next(reader)
            except StopIteration:
                header = []
            rows = list(reader)

    if header != EXPECTED_HEADER:
        errors.append(
            "registry header mismatch: "
            f"expected={EXPECTED_HEADER!r} actual={header!r}"
        )

    if rows:
        errors.append("P7-T01 registry must contain header only; population belongs to P7-T02")

    report = {
        "schema_id": "p7_t01_proof_normal_form_schema_validator_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "schema_path": str(SCHEMA_PATH.relative_to(REPO_ROOT)),
        "registry_path": str(REGISTRY_PATH.relative_to(REPO_ROOT)),
        "header": header,
        "row_count": len(rows),
        "proof_authority": False,
        "support_only": True,
        "physics_promotion_authorized": False,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
