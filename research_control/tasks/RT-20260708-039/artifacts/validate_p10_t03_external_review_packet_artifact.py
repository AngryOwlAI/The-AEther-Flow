#!/usr/bin/env python3
"""Validate the v18 P10-T03 external-review packet artifact."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
PACKET_PATH = REPO_ROOT / "external_review_packets/eqsrc_family_closure_review_packet_v1.md"
REGISTRY_PATH = REPO_ROOT / "registries/EXTERNAL_REVIEW_PACKET_REGISTRY.csv"
REPORT_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260708-039/artifacts/p10_t03_external_review_packet_artifact_report.json"
)

REVIEW_QUESTION = (
    "Does the conditional source-only `EqSrc_T` family-closure theorem candidate\n"
    "have a valid path from record-local `EqSrc` witnesses to family-level closure\n"
    "without adding or assuming a primitive equivalent to the supplied H1-H7 closure\n"
    "and ledger structure, especially inverse closure, composition closure,\n"
    "`RetainH` for H-retention, or `GenH` for H-generated families?"
)

REQUIRED_HEADINGS = [
    "## 1. Review Question",
    "## 2. Short Context",
    "## 3. Minimal Objects",
    "## 4. Current Internal Result",
    "## 5. Main Review Target",
    "## 6. Feedback Requested",
    "## 7. Feedback Not Requested",
    "## 8. Source Bundle",
    "## 9. Boundary Statement",
    "## References",
]

REQUIRED_SOURCE_TOKENS = [
    "research_control/tasks/RT-20260708-037/artifacts/external_review_question_selector_receipt.md",
    "markdown/external-review-specs/eqsrc_family_closure_review_packet_spec_v1.md",
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
    "external_review_completed: false",
    "endorsement_claimed: false",
    "next_route: \"P10-T04\"",
    "does not perform external outreach",
    "does not ask for a broad repository tour",
    "It would not by itself prove the physics",
]

FORBIDDEN_PHRASES = [
    "reviewer accepted",
    "reviewer endorsed",
    "reviewed externally",
    "external acceptance proves",
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
    "Dear reviewer",
]

REGISTRY_REQUIRED_COLUMNS = [
    "packet_id",
    "packet_path",
    "source_spec_id",
    "source_spec_path",
    "plan_task_id",
    "task_id",
    "status",
    "review_question_family",
    "source_bundle_paths",
    "constraints_satisfied",
    "external_outreach_performed",
    "reviewer_named",
    "external_review_completed",
    "endorsement_claimed",
    "claim_boundary_id",
    "validation_status",
    "created_at",
    "updated_at",
    "notes",
]


def read_registry() -> tuple[list[str], list[dict[str, str]]]:
    if not REGISTRY_PATH.exists():
        return [], []
    with REGISTRY_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def validate() -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not PACKET_PATH.exists():
        errors.append(f"missing packet: {PACKET_PATH.relative_to(REPO_ROOT)}")
        return {"status": "FAIL", "errors": errors, "warnings": warnings}

    text = PACKET_PATH.read_text(encoding="utf-8")
    word_count = len(text.split())
    normalized = " ".join(text.split())
    normalized_question = " ".join(REVIEW_QUESTION.split())

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing heading: {heading}")

    if normalized_question not in normalized:
        errors.append("selected P10-T02 review question is not present exactly enough")

    for token in REQUIRED_SOURCE_TOKENS:
        if token not in text:
            errors.append(f"missing bounded source path: {token}")

    if "does not perform external outreach" not in normalized:
        errors.append("missing no-outreach boundary statement")
    for token in REQUIRED_BOUNDARY_TOKENS:
        if token.startswith("does not perform"):
            continue
        if token not in text:
            errors.append(f"missing boundary token: {token}")

    lower_text = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lower_text:
            errors.append(f"forbidden phrase present: {phrase}")

    if word_count < 650:
        errors.append("packet is shorter than the focused 2-5 page target")
    if word_count > 1800:
        warnings.append("packet is longer than the focused 2-5 page target")

    fieldnames, rows = read_registry()
    if not fieldnames:
        errors.append(f"missing registry: {REGISTRY_PATH.relative_to(REPO_ROOT)}")
    else:
        for column in REGISTRY_REQUIRED_COLUMNS:
            if column not in fieldnames:
                errors.append(f"registry missing column: {column}")
        packet_rows = [row for row in rows if row.get("packet_id") == "ERP-EQSRC-FAMILY-CLOSURE-V1"]
        if len(packet_rows) != 1:
            errors.append("registry must contain exactly one ERP-EQSRC-FAMILY-CLOSURE-V1 row")
        else:
            row = packet_rows[0]
            expected = {
                "packet_path": "external_review_packets/eqsrc_family_closure_review_packet_v1.md",
                "source_spec_path": "markdown/external-review-specs/eqsrc_family_closure_review_packet_spec_v1.md",
                "plan_task_id": "P10-T03",
                "task_id": "RT-20260708-039",
                "external_outreach_performed": "false",
                "reviewer_named": "false",
                "external_review_completed": "false",
                "endorsement_claimed": "false",
                "validation_status": "PASS",
            }
            for key, value in expected.items():
                if row.get(key) != value:
                    errors.append(f"registry row {key} expected {value!r} got {row.get(key)!r}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "packet_path": str(PACKET_PATH.relative_to(REPO_ROOT)),
        "registry_path": str(REGISTRY_PATH.relative_to(REPO_ROOT)),
        "word_count": word_count,
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
