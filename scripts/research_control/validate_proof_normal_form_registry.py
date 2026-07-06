#!/usr/bin/env python3
"""Validate the proof-normal-form registry.

This validator is project-control tooling. A PASS result means the registry
rows satisfy the declared proof-normal-form schema and boundary guards; it does
not create proof authority or promote physics claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY_PATH = "registries/PROOF_NORMAL_FORM_REGISTRY.csv"

REQUIRED_HEADER = [
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

ALLOWED_CLAIM_TYPES = {
    "definition",
    "lemma",
    "theorem",
    "proposition",
    "obstruction",
    "decision",
    "boundary",
    "nonconclusion",
}
ALLOWED_AUTHORITY_STATUSES = {"science_draft", "scientific_gate", "control", "support_only"}
ALLOWED_STATUSES = {
    "draft_control",
    "scoped_evidence",
    "scoped_adopted",
    "blocked",
    "frozen_negative",
    "not_started",
}
BOOLEAN_VALUES = {"true", "false"}

HIGH_RISK_TERMS = (
    "eqsrc",
    "retainh",
    "genh",
    "source law adoption",
    "source-law adoption",
    "source_law_adoption",
    "metricdata(e)",
    "metricdata",
    "g_eff",
    "matter semantics",
    "matter-semantics",
    "detector semantics",
    "detector-semantics",
    "coupling law",
    "coupling-law",
    "matter coupling",
    "matter-coupling",
    "stress energy semantics",
    "stress-energy semantics",
    "stress energy tensor",
    "stress-energy tensor",
    "matter action",
    "einstein equations",
    "benchmark promotion",
    "gate chair",
    "completed derivation",
)

PROMOTION_PATTERNS = (
    "matter coupling is derived",
    "matter-coupling is derived",
    "einstein equations are derived",
    "benchmark is promoted",
    "benchmark promoted",
    "completed derivation is established",
    "proof_authority=true",
    "proof authority: true",
    "is proof authority",
    "has proof authority",
)

GENERATED_OR_LOCAL_PREFIXES = (".local/", "wiki/", "output/", "html/")


class ProofNormalFormRegistryError(RuntimeError):
    """Raised when proof-normal-form registry validation fails."""

    def __init__(self, errors: list[str], receipt: dict[str, Any]) -> None:
        super().__init__("\n".join(errors))
        self.errors = errors
        self.receipt = receipt


def split_semicolon_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def normalize(value: str) -> str:
    return value.lower().replace("_", " ").replace("-", " ")


def is_high_risk(row: dict[str, str]) -> bool:
    text = normalize(
        " ".join(
            [
                row.get("object_id", ""),
                row.get("conclusion", ""),
                row.get("scope", ""),
                row.get("allowed_uses", ""),
            ]
        )
    )
    return any(normalize(term) in text for term in HIGH_RISK_TERMS)


def claims_proof_authority(text: str) -> bool:
    lowered = normalize(text)
    if "not proof authority" in lowered or "no proof authority" in lowered:
        return False
    return any(normalize(pattern) in lowered for pattern in PROMOTION_PATTERNS)


def load_rows(registry_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with registry_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [{key: value or "" for key, value in row.items()} for row in reader]


def validate_header(header: list[str], errors: list[str]) -> None:
    if header != REQUIRED_HEADER:
        errors.append(f"header mismatch: expected {REQUIRED_HEADER}, found {header}")


def validate_source_path(repo_root: Path, row_id: str, rel_path: str, status: str, errors: list[str]) -> None:
    if not rel_path:
        errors.append(f"{row_id}: missing source_artifact_path")
        return
    path = Path(rel_path)
    if path.is_absolute():
        errors.append(f"{row_id}: source_artifact_path must be repository-relative")
        return
    if ".." in path.parts:
        errors.append(f"{row_id}: source_artifact_path must not traverse outside the repository")
        return
    if rel_path.startswith(GENERATED_OR_LOCAL_PREFIXES):
        errors.append(f"{row_id}: generated or local path cannot be source authority: {rel_path}")
    if status != "not_started" and not (repo_root / rel_path).exists():
        errors.append(f"{row_id}: source_artifact_path does not exist: {rel_path}")


def validate_forbidden_premises(row: dict[str, str], row_id: str, errors: list[str]) -> None:
    premises = split_semicolon_list(row.get("premises", ""))
    forbidden = split_semicolon_list(row.get("forbidden_premises", ""))
    premise_items = {normalize(item) for item in premises}
    premise_text = normalize(row.get("premises", ""))
    for forbidden_item in forbidden:
        normalized_forbidden = normalize(forbidden_item)
        if normalized_forbidden in premise_items or normalized_forbidden in premise_text:
            errors.append(f"{row_id}: forbidden premise appears in premises: {forbidden_item}")


def validate_scientific_gate_row(row: dict[str, str], row_id: str, errors: list[str]) -> None:
    if row.get("authority_status") != "scientific_gate":
        if row.get("status") == "scoped_adopted":
            errors.append(f"{row_id}: non-gate row may not claim scoped_adopted status")
        return

    if row.get("claim_type") != "decision":
        errors.append(f"{row_id}: scientific_gate row must be a decision")
    if row.get("status") != "scoped_adopted":
        errors.append(f"{row_id}: scientific_gate row must remain scoped_adopted")
    conclusion = normalize(row.get("conclusion", ""))
    scope = normalize(row.get("scope", ""))
    if "only" not in conclusion and "scoped" not in conclusion:
        errors.append(f"{row_id}: scientific_gate conclusion must use scoped or only language")
    if "scope" not in scope and "scoped" not in scope and "source" not in scope:
        errors.append(f"{row_id}: scientific_gate row must declare a bounded scope")
    if not row.get("non_conclusions", "").strip():
        errors.append(f"{row_id}: scientific_gate row must preserve non_conclusions")


def validate_support_only_boundary(row: dict[str, str], row_id: str, errors: list[str]) -> None:
    text = " ".join(
        [
            row.get("conclusion", ""),
            row.get("scope", ""),
            row.get("allowed_uses", ""),
            row.get("notes", ""),
        ]
    )
    if row.get("authority_status") == "support_only" and claims_proof_authority(text):
        errors.append(f"{row_id}: support_only row claims proof authority")
    if claims_proof_authority(row.get("conclusion", "")):
        errors.append(f"{row_id}: conclusion claims proof authority or promotion")


def validate_row(repo_root: Path, row: dict[str, str], row_ids: set[str], errors: list[str]) -> None:
    row_id = row.get("proof_normal_form_row_id", "")
    if not row_id:
        errors.append("row missing proof_normal_form_row_id")
        row_id = "<missing-row-id>"
    elif row_id in row_ids:
        errors.append(f"{row_id}: duplicate proof_normal_form_row_id")
    row_ids.add(row_id)

    for field in ("object_id", "claim_type", "authority_status", "status", "conclusion", "scope", "allowed_uses", "created_at"):
        if not row.get(field, "").strip():
            errors.append(f"{row_id}: missing required field {field}")

    if row.get("claim_type") not in ALLOWED_CLAIM_TYPES:
        errors.append(f"{row_id}: invalid claim_type {row.get('claim_type')}")
    if row.get("authority_status") not in ALLOWED_AUTHORITY_STATUSES:
        errors.append(f"{row_id}: invalid authority_status {row.get('authority_status')}")
    if row.get("status") not in ALLOWED_STATUSES:
        errors.append(f"{row_id}: invalid status {row.get('status')}")
    if row.get("machine_checkable_fragment") not in BOOLEAN_VALUES:
        errors.append(f"{row_id}: machine_checkable_fragment must be true or false")

    validate_source_path(repo_root, row_id, row.get("source_artifact_path", ""), row.get("status", ""), errors)
    high_risk = is_high_risk(row)
    if high_risk:
        if not row.get("forbidden_premises", "").strip():
            errors.append(f"{row_id}: high-risk row missing forbidden_premises")
        if not row.get("non_conclusions", "").strip():
            errors.append(f"{row_id}: high-risk row missing non_conclusions")

    validate_forbidden_premises(row, row_id, errors)
    validate_scientific_gate_row(row, row_id, errors)
    validate_support_only_boundary(row, row_id, errors)


def validate_registry(
    registry_path: str | Path = DEFAULT_REGISTRY_PATH,
    *,
    repo_root: str | Path = REPO_ROOT,
) -> dict[str, Any]:
    root = Path(repo_root)
    registry = Path(registry_path)
    if not registry.is_absolute():
        registry = root / registry
    errors: list[str] = []

    if not registry.exists():
        raise ProofNormalFormRegistryError(
            [f"missing registry: {registry}"],
            {
                "status": "FAIL",
                "errors": [f"missing registry: {registry}"],
                "proof_authority": False,
                "support_only": True,
            },
        )

    header, rows = load_rows(registry)
    validate_header(header, errors)

    row_ids: set[str] = set()
    high_risk_count = 0
    scientific_gate_count = 0
    support_only_count = 0
    for row in rows:
        if is_high_risk(row):
            high_risk_count += 1
        if row.get("authority_status") == "scientific_gate":
            scientific_gate_count += 1
        if row.get("authority_status") == "support_only":
            support_only_count += 1
        validate_row(root, row, row_ids, errors)

    receipt = {
        "status": "PASS" if not errors else "FAIL",
        "registry_path": str(registry.relative_to(root) if registry.is_relative_to(root) else registry),
        "checked_row_count": len(rows),
        "high_risk_row_count": high_risk_count,
        "scientific_gate_row_count": scientific_gate_count,
        "support_only_row_count": support_only_count,
        "support_only": True,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "authority_boundary_status": "proof_authority_false_preserved",
        "errors": errors,
    }
    if errors:
        raise ProofNormalFormRegistryError(errors, receipt)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the proof-normal-form registry.")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY_PATH, help="Registry path to validate.")
    parser.add_argument("--json", action="store_true", help="Emit JSON receipt.")
    parser.add_argument("--json-output", help="Optional path for JSON receipt output.")
    args = parser.parse_args(argv)

    try:
        receipt = validate_registry(args.registry)
        exit_code = 0
    except ProofNormalFormRegistryError as exc:
        receipt = exc.receipt
        exit_code = 1

    output = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.json_output:
        Path(args.json_output).write_text(output, encoding="utf-8")
    if args.json:
        print(output, end="")
    elif exit_code:
        for error in receipt["errors"]:
            print(error, file=sys.stderr)
    else:
        print("Proof-normal-form registry validation passed.")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
