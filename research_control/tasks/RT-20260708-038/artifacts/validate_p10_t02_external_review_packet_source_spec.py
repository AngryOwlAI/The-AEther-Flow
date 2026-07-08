#!/usr/bin/env python3
"""Validate the v18 P10-T02 external-review packet source spec."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SPEC_PATH = REPO_ROOT / "markdown/external-review-specs/eqsrc_family_closure_review_packet_spec_v1.md"
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260708-038/artifacts/p10_t02_external_review_packet_source_spec_report.json"
)

REVIEW_QUESTION = (
    "Does the conditional source-only `EqSrc_T` family-closure theorem candidate have\n"
    "a valid path from record-local `EqSrc` witnesses to family-level closure without\n"
    "adding or assuming a primitive equivalent to the supplied H1-H7 closure and\n"
    "ledger structure, especially inverse closure, composition closure, `RetainH`\n"
    "for H-retention, or `GenH` for H-generated families?"
)

REQUIRED_HEADINGS = [
    "## 1. Review Question",
    "## 2. What the Project Is Not Claiming",
    "## 3. Minimal Definitions",
    "## 4. Record-Local Theorem Summary",
    "## 5. Typed Source-Equivalence Object Summary",
    "## 6. Family-Closure Obstruction",
    "## 7. `RetainH` and `GenH` Boundary",
    "## 8. What Feedback Is Requested",
    "## 9. What Feedback Is Not Requested",
    "## 10. Source Paths",
    "## 11. Non-Authority and Non-Endorsement Statement",
]

REQUIRED_SOURCE_TOKENS = [
    "research_control/tasks/RT-20260708-037/artifacts/external_review_question_selector_receipt.md",
    "research_control/design/source_equivalence_typed_object_schema_v1.md",
    "research_control/tasks/RT-20260707-015/artifacts/source_equivalence_typed_object_v1.tex",
    "research_control/tasks/RT-20260707-020/artifacts/eqsrc_family_closure_theorem_or_countermodel_v1.tex",
    "research_control/tasks/RT-20260707-021/artifacts/retainh_genh_primitive_boundary_v1.tex",
    "research_control/tasks/RT-20260707-022/artifacts/eqsrc_family_closure_smuggling_audit_v1.tex",
    "research_control/tasks/RT-20260707-023/artifacts/eqsrc_family_closure_refuter_stress_v1.tex",
    "implementations_plans/recommendations_implementation_plan_continue_task-v18.md",
]

REQUIRED_BOUNDARY_TOKENS = [
    "external_outreach_performed: false",
    "reviewer_named: false",
    "next_route: \"P10-T03\"",
    "This packet does not claim a general `EqSrc` discharge.",
    "This packet does not claim that `RetainH` or `GenH` is adopted.",
    "No broad repository tour is requested.",
    "This source spec is an internal project-control source",
]

FORBIDDEN_PHRASES = [
    "external outreach performed",
    "reviewer accepted",
    "reviewer endorsed",
    "general EqSrc is discharged",
    "RetainH is adopted",
    "GenH is adopted",
    "source law is adopted",
    "Einstein equations are derived",
    "completed derivation is established",
    "completed derivation has been achieved",
    "we have completed derivation",
    "please inspect the whole repository",
    "review the whole repository",
]


def validate() -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not SPEC_PATH.exists():
        errors.append(f"missing spec: {SPEC_PATH.relative_to(REPO_ROOT)}")
        return {"status": "FAIL", "errors": errors, "warnings": warnings}

    text = SPEC_PATH.read_text(encoding="utf-8")
    normalized = " ".join(text.split())
    normalized_question = " ".join(REVIEW_QUESTION.split())

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")

    if normalized_question not in normalized:
        errors.append("selected P10-T01 review question is not present exactly enough")

    for token in REQUIRED_SOURCE_TOKENS:
        if token not in text:
            errors.append(f"missing bounded source path: {token}")

    for token in REQUIRED_BOUNDARY_TOKENS:
        if token not in text:
            errors.append(f"missing boundary token: {token}")

    lower_text = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"forbidden phrase present: {phrase}")

    if len(text.split()) > 1800:
        warnings.append("spec is longer than preferred concise-review target")

    if "`external_review_packets/eqsrc_family_closure_review_packet_v1.md`" not in text:
        errors.append("missing expected P10-T03 packet output path")

    return {
        "status": "PASS" if not errors else "FAIL",
        "spec_path": str(SPEC_PATH.relative_to(REPO_ROOT)),
        "word_count": len(text.split()),
        "required_heading_count": len(REQUIRED_HEADINGS),
        "required_source_path_count": len(REQUIRED_SOURCE_TOKENS),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate()
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
