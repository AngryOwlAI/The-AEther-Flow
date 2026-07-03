#!/usr/bin/env python3
"""Validate the v15 P11-T03 CI validation maintainer guide packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
GUIDE_PATH = REPO_ROOT / "research_control/README.md"

REQUIRED_PHRASES = [
    "Local Validation Pipeline",
    "run_full_research_control_validation.py --json",
    "--output <path>",
    "--include-smoke-tests",
    "before checkpointing",
    "A PASS result means",
    "A PASS result does not",
    "claim_language_changed_lint",
    "research_control_validation",
    "registry consistency",
    "generated derivative drift",
    "documentation_impact_validation",
    "operational receipt evidence only",
]

FORBIDDEN_PHRASES = [
    "PASS proves",
    "PASS validates the physics derivation",
    "PASS authorizes source-law adoption",
    "PASS authorizes route freeze",
]


def validate() -> dict[str, object]:
    errors: list[str] = []
    text = GUIDE_PATH.read_text(encoding="utf-8") if GUIDE_PATH.exists() else ""
    lower = text.lower()

    if not GUIDE_PATH.exists():
        errors.append(f"missing guide: {GUIDE_PATH.relative_to(REPO_ROOT)}")

    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower:
            errors.append(f"guide missing required phrase: {phrase}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower:
            errors.append(f"guide contains forbidden promotion phrase: {phrase}")

    return {
        "schema_id": "p11_t03_ci_validation_maintainer_guide_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "guide_path": str(GUIDE_PATH.relative_to(REPO_ROOT)),
        "required_phrase_count": len(REQUIRED_PHRASES),
        "forbidden_phrase_count": len(FORBIDDEN_PHRASES),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
