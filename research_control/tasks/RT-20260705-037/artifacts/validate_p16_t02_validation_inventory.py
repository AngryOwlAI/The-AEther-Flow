#!/usr/bin/env python3
"""Validate the P16-T02 validation-command inventory update.

This task-local validator checks only operational inventory coverage. It does
not evaluate physics claims and does not grant proof authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
INVENTORY_PATH = REPO_ROOT / "research_control/design/validation_command_inventory_v16.md"

REQUIRED_TERMS = {
    "minimum payload validation": "minimum physics payload validation",
    "route-orbit hard-gate check": "route-orbit hard-gate check",
    "target-import attack validation": "target-import fixture validation",
    "compact frontier check": "compact frontier render check",
    "claim graph validation": "claim graph validation",
    "current frontier render check": "current frontier render check",
    "dependency graph check": "dependency graph render check",
    "documentation impact": "documentation impact",
    "claim-language linter": "claim-language linter",
    "memory bootstrap": "memory bootstrap",
    "research-control validation": "research-control validation",
}

REQUIRED_AUTHORITY_LEVELS = {
    "required-gate",
    "required-render-check",
    "advisory-diagnostic",
    "support-only",
    "ci-smoke",
}

FORBIDDEN_PROOF_AUTHORITY_PHRASES = {
    "validator result proves",
    "pass proves",
    "pass establishes matter coupling",
    "pass authorizes",
    "proof authority: true",
    "physics_promotion_authorized: true",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_inventory(text: str) -> dict[str, object]:
    lowered = text.lower()
    missing_terms = [
        label for label, needle in REQUIRED_TERMS.items() if needle.lower() not in lowered
    ]
    missing_levels = [
        level for level in sorted(REQUIRED_AUTHORITY_LEVELS) if f"`{level}`" not in text
    ]
    forbidden_hits = [
        phrase for phrase in sorted(FORBIDDEN_PROOF_AUTHORITY_PHRASES) if phrase in lowered
    ]
    authority_boundary_present = (
        "These commands are operational controls" in text
        and "do not create physics authority" in text
        and "completed derivation" in text
    )

    checks = {
        "required_v16_checks_present": not missing_terms,
        "required_authority_levels_present": not missing_levels,
        "proof_authority_guard_present": authority_boundary_present,
        "forbidden_proof_authority_phrases_absent": not forbidden_hits,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "status": status,
        "inventory_path": str(INVENTORY_PATH.relative_to(REPO_ROOT)),
        "inventory_hash": sha256_text(text),
        "required_terms_checked": REQUIRED_TERMS,
        "missing_terms": missing_terms,
        "required_authority_levels": sorted(REQUIRED_AUTHORITY_LEVELS),
        "missing_authority_levels": missing_levels,
        "forbidden_hits": forbidden_hits,
        "checks": checks,
        "operational_receipt_only": True,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate P16-T02 validation command inventory coverage."
    )
    parser.add_argument("--output", type=Path, help="Optional JSON report output path.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    args = parser.parse_args()

    text = INVENTORY_PATH.read_text(encoding="utf-8")
    report = validate_inventory(text)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(report["status"])

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
