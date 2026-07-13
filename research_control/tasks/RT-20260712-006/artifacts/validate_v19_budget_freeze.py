#!/usr/bin/env python3
"""Validate the bounded P0-T05 budget policy and review receipt."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
BUDGET_PATH = ROOT / "research_control/design/v19_validation_performance_and_safety_budget.md"
RECEIPT_PATH = ROOT / "research_control/tasks/RT-20260712-006/artifacts/v19_budget_review_receipt.yaml"

PERFORMANCE_IDS = {
    "V19-PERF-FULL-001",
    "V19-PERF-AFFECTED-001",
    "V19-PERF-CHECKPOINT-001",
    "V19-PERF-CI-001",
    "V19-PERF-TRACE-001",
    "V19-DUP-IDENTITY-001",
    "V19-OUT-PASS-001",
    "V19-OUT-FAIL-001",
    "V19-OUT-FINDINGS-001",
}
SAFETY_IDS = {
    "V19-SAFE-STAGED-ALLOWLIST-001",
    "V19-SAFE-AUTHORITY-001",
    "V19-SAFE-CLAIMS-001",
    "V19-SAFE-RESIDUE-001",
    "V19-SAFE-WHITESPACE-001",
    "V19-SAFE-SOURCE-AUTHORITY-001",
    "V19-SAFE-LIVE-SUBSYSTEM-001",
    "V19-SAFE-SCHEDULED-FULL-001",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.parse_args()

    text = BUDGET_PATH.read_text(encoding="utf-8")
    receipt = yaml.safe_load(RECEIPT_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    lines = text.splitlines()
    for budget_id in sorted(PERFORMANCE_IDS | SAFETY_IDS):
        definitions = [line for line in lines if line.startswith(f"| `{budget_id}` |")]
        if len(definitions) != 1:
            errors.append(f"{budget_id}: expected exactly one policy definition")

    required_phrases = (
        "Target",
        "Hard guard",
        "Advisory trend",
        "Measurement method",
        "Comparable measurement protocol",
        "Rollback threshold",
        "performance gain never compensates",
        "operational evidence only",
        "handoff-0740",
    )
    normalized_text = " ".join(text.split()).lower()
    for phrase in required_phrases:
        if phrase.lower() not in normalized_text:
            errors.append(f"missing policy phrase: {phrase}")

    receipt_ids = set(receipt.get("budget_ids", []))
    expected_ids = PERFORMANCE_IDS | SAFETY_IDS
    if receipt_ids != expected_ids:
        errors.append("receipt budget_ids do not exactly match frozen policy IDs")

    if receipt.get("budget_document", {}).get("sha256") != sha256(BUDGET_PATH):
        errors.append("receipt budget document hash is stale")

    checks = receipt.get("review_checks", {})
    required_checks = {
        "every_budget_has_measurement_method",
        "every_budget_has_comparable_rule",
        "every_budget_has_rollback_threshold",
        "unique_invariant_deletion_forbidden",
        "baseline_and_post_change_receipts_required",
        "physics_authority_created",
    }
    if set(checks) != required_checks:
        errors.append("receipt review_checks keys are incomplete or unexpected")
    if any(checks.get(key) is not True for key in required_checks - {"physics_authority_created"}):
        errors.append("one or more required review checks are not true")
    if checks.get("physics_authority_created") is not False:
        errors.append("physics_authority_created must be false")

    if receipt.get("status") != "PASS":
        errors.append("receipt status must be PASS")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    print(
        "PASS v19 budget freeze: "
        f"performance_output_budgets={len(PERFORMANCE_IDS)} "
        f"safety_budgets={len(SAFETY_IDS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
