#!/usr/bin/env python3
"""Validate the v14 P11-T02 matter-coupling pre-adoption checklist."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
GENERATED_AT = "2026-07-02T11:01:31Z"
DOC_PATH = "research_control/design/matter_coupling_pre_adoption_checklist.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
RECEIPT_PATH = (
    "research_control/tasks/RT-20260702-035/artifacts/"
    "p11_t02_pre_adoption_checklist_receipt.md"
)

REQUIRED_SECTIONS = [
    "Exact object proposed for adoption",
    "Status before adoption request",
    "Source files inspected",
    "Accepted evidence/preconditions used",
    "Missing laws or semantics",
    "No-target certificate hygiene check",
    "`RR_E` separation check",
    "Stress/audit history",
    "Red-team status",
    "Literature comparison status",
    "Required Gate Chair authority",
    "Forbidden adjacent promotions",
]

REQUIRED_PHRASES = [
    "<!-- authority: control -->",
    "matter_coupling_pre_adoption_checklist",
    "checklist_version: \"v14_p11_t02\"",
    "external_resemblance_as_validation: false",
    "adoption_verdict_after_packet: \"not_adopted\"",
    "Human authorization to run implementation-plan packets does not by itself",
    "P11-T03",
]

FORBIDDEN_PROMOTIONS = [
    "canonical ontology edit",
    "source-law adoption",
    "`SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption",
    "`PositiveMSProfile_v1` adoption as matter semantics",
    "`RR_ETransportCompletenessOrInvarianceLaw_v1` adoption as a source law",
    "`MetricData(E)` adoption",
    "`g_eff` adoption or scope expansion",
    "coupling-law adoption",
    "matter-semantics adoption",
    "detector-semantics adoption",
    "matter-coupling derivation or adoption",
    "stress-energy semantics, stress-energy tensor, or matter action",
    "Einstein equations",
    "benchmark promotion",
    "completed derivation",
    "future source-extension impossibility",
    "broad theory rejection",
]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_receipt(doc_hash: str, plan_hash: str) -> str:
    sections = "\n".join(f"- {section}" for section in REQUIRED_SECTIONS)
    promotions = "\n".join(f"- {item}" for item in FORBIDDEN_PROMOTIONS)
    receipt = f"""<!-- authority: control -->

# P11-T02 Pre-Adoption Checklist Receipt

Generated at: `{GENERATED_AT}`

## Verdict

PASS. The checklist contains all v14 P11-T02 required sections and preserves
the boundary that adoption-facing packets must name exact objects, evidence,
missing semantics, no-target hygiene, `RR_E` separation, stress and review
history, literature status, Gate Chair authority, and forbidden adjacent
promotions.

## Hashes

| Source | SHA-256 |
| --- | --- |
| `{DOC_PATH}` | `{doc_hash}` |
| `{PLAN_PATH}` | `{plan_hash}` |

## Required Sections Confirmed

{sections}

## Forbidden Adjacent Promotions Confirmed

{promotions}

## Next Route

P11-T03 should select one narrow theorem or precondition route rather than
direct matter-coupling derivation.
"""
    receipt_path = REPO_ROOT / RECEIPT_PATH
    receipt_path.write_text(receipt, encoding="utf-8")
    return sha256_text(receipt)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    doc_text = read_text(DOC_PATH)
    plan_text = read_text(PLAN_PATH)

    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in doc_text:
            errors.append(f"{DOC_PATH} missing checklist section: {section}")
    for phrase in REQUIRED_PHRASES:
        if phrase not in doc_text:
            errors.append(f"{DOC_PATH} missing required phrase: {phrase}")
    for item in FORBIDDEN_PROMOTIONS:
        if item not in doc_text:
            errors.append(f"{DOC_PATH} missing forbidden adjacent promotion: {item}")

    doc_hash = sha256_text(doc_text)
    plan_hash = sha256_text(plan_text)
    receipt_hash = ""
    if not errors:
        receipt_hash = write_receipt(doc_hash=doc_hash, plan_hash=plan_hash)

    result = {
        "status": "PASS" if not errors else "FAIL",
        "generated_at": GENERATED_AT,
        "doc_path": DOC_PATH,
        "doc_hash": doc_hash,
        "plan_path": PLAN_PATH,
        "plan_hash": plan_hash,
        "required_section_count": len(REQUIRED_SECTIONS),
        "required_phrase_count": len(REQUIRED_PHRASES),
        "forbidden_promotion_count": len(FORBIDDEN_PROMOTIONS),
        "receipt_path": RECEIPT_PATH if not errors else "",
        "receipt_hash": receipt_hash,
        "errors": errors,
    }
    output_path = REPO_ROOT / args.output
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
