#!/usr/bin/env python3
"""Validate the RT-20260703-004 P5-T01 dependency audit artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260703-004"
ARTIFACT_DIR = TASK_DIR / "artifacts"
AUDIT_PATH = ARTIFACT_DIR / "eqsrc_retainh_genh_dependency_audit_v1.tex"


REQUIRED_FILES = [
    ARTIFACT_DIR / "child_phys_math_eqsrc_retainh_genh_dependency_audit.yaml",
    ARTIFACT_DIR / "child_phys_phil_eqsrc_retainh_genh_dependency_audit.yaml",
    ARTIFACT_DIR / "parent_conflict_review_eqsrc_retainh_genh_dependency_audit.yaml",
    ARTIFACT_DIR / "parent_fusion_notes_eqsrc_retainh_genh_dependency_audit.md",
    AUDIT_PATH,
]

REQUIRED_TERMS = [
    r"\EqSrc",
    r"\RetainH",
    r"\GenH",
    "not\\_required\\_for\\_current\\_scope",
    "conditionally\\_required",
    "general source-equivalence theorem",
    "retention law",
    "generator law",
    "P5-T02 dependency consequence selector",
]

FORBIDDEN_PROMOTION_PHRASES = [
    "general \\EqSrc is adopted",
    "\\RetainH is adopted",
    "\\GenH is adopted",
    "matter coupling is derived",
    "Einstein equations are derived",
    "completed derivation is established",
]


def check(condition: bool, check_id: str, detail: str) -> dict[str, object]:
    return {"id": check_id, "status": "PASS" if condition else "FAIL", "detail": detail}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Path to write JSON report.")
    parser.add_argument("--json", action="store_true", help="Print JSON report to stdout.")
    args = parser.parse_args()

    checks: list[dict[str, object]] = []

    for required_file in REQUIRED_FILES:
        checks.append(
            check(
                required_file.exists(),
                f"file_exists:{required_file.relative_to(ROOT)}",
                "required task artifact exists",
            )
        )

    text = AUDIT_PATH.read_text(encoding="utf-8") if AUDIT_PATH.exists() else ""

    for term in REQUIRED_TERMS:
        checks.append(check(term in text, f"required_term:{term}", "required audit term is present"))

    for phrase in FORBIDDEN_PROMOTION_PHRASES:
        checks.append(
            check(
                phrase not in text,
                f"forbidden_promotion_phrase:{phrase}",
                "forbidden promotion phrase is absent",
            )
        )

    checks.append(
        check(
            "This audit changes no Distance-to-GR ledger row" in text,
            "distance_to_gr_no_delta",
            "audit explicitly records no Distance-to-GR ledger delta",
        )
    )
    checks.append(
        check(
            "None of the three broad upstream dependencies is classified as" in text
            and "already\\_supplied\\_by\\_tracked\\_source" in text,
            "already_supplied_boundary",
            "audit blocks already-supplied overread for broad upstream dependencies",
        )
    )
    checks.append(
        check(
            "not require general" in text and "as a premise" in text,
            "scoped_avoidance_lemma",
            "scoped avoidance lemma states P2 theorem does not require upstream primitives",
        )
    )

    failed = [item for item in checks if item["status"] != "PASS"]
    report = {
        "task_id": "RT-20260703-004",
        "artifact": str(AUDIT_PATH.relative_to(ROOT)),
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
    }

    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
