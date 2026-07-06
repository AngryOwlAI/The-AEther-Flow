#!/usr/bin/env python3
"""Validate the v17 P11-T02 reproducibility documentation packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
CONTRIBUTING_PATH = REPO_ROOT / "CONTRIBUTING.md"
REQUIREMENTS_DEV_PATH = REPO_ROOT / "requirements-dev.txt"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def contains_all(text: str, required: list[str]) -> list[str]:
    lowered = text.lower()
    return [item for item in required if item.lower() not in lowered]


def validate() -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    contributing = read_text(CONTRIBUTING_PATH)
    requirements_dev = read_text(REQUIREMENTS_DEV_PATH)

    if not CONTRIBUTING_PATH.exists():
        errors.append("missing CONTRIBUTING.md")
    if not REQUIREMENTS_DEV_PATH.exists():
        errors.append("missing requirements-dev.txt")

    required_sections = [
        "Supported Python",
        "Local Environment",
        "Validation Commands",
        "Generated-Output Policy",
        "Interpreting Validation",
    ]
    missing_sections = contains_all(contributing, required_sections)
    for section in missing_sections:
        errors.append(f"CONTRIBUTING.md missing section: {section}")

    required_phrases = [
        "CPython 3.12",
        "python3.12 -m venv .venv",
        ".venv/bin/python -m pip install -r requirements-dev.txt",
        "make PYTHON=.venv/bin/python validate-project-control",
        "bootstrap_memory_system.py --validate-only",
        "continue_research_memory_preflight.py --json",
        "continue_research.py",
        "bootstrap_memory_system.py",
        "validate_research_control.py --check-diff",
        "Do not hand-edit generated wiki notes",
        ".local/",
        "operational receipt",
        "not physics proof authority",
        "does not establish source-law adoption",
        "MetricData(E)",
        "g_eff",
        "matter coupling",
        "Einstein equations",
        "benchmark promotion",
        "Gate Chair",
        "completed derivation",
    ]
    missing_phrases = contains_all(contributing, required_phrases)
    for phrase in missing_phrases:
        errors.append(f"CONTRIBUTING.md missing required phrase: {phrase}")

    requirement_lines = [
        line.strip()
        for line in requirements_dev.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if requirement_lines != ["-r requirements.txt"]:
        errors.append("requirements-dev.txt must contain only '-r requirements.txt' as an active dependency line")

    if "PyMuPDF" not in read_text(REPO_ROOT / "requirements.txt"):
        warnings.append("requirements.txt does not mention PyMuPDF")

    return {
        "schema_id": "p11_t02_reproducibility_docs_validation_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "checked_paths": [
            "CONTRIBUTING.md",
            "requirements-dev.txt",
            "requirements.txt",
        ],
        "required_sections": required_sections,
        "required_phrases_checked": required_phrases,
        "requirements_dev_active_lines": requirement_lines,
        "physics_proof_authority": False,
        "physics_promotion_authorized": False,
        "operational_receipt_only": True,
        "no_new_third_party_dependencies": requirement_lines == ["-r requirements.txt"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Write report JSON to this path.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate()
    if args.output:
        output = REPO_ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

