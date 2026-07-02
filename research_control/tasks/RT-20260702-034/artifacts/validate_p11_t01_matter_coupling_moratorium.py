#!/usr/bin/env python3
"""Validate the v14 P11-T01 matter-coupling moratorium note."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
GENERATED_AT = "2026-07-02T10:49:21Z"
DOC_PATH = "research_control/design/matter_coupling_derivation_moratorium.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
RECEIPT_PATH = (
    "research_control/tasks/RT-20260702-034/artifacts/"
    "p11_t01_matter_coupling_moratorium_receipt.md"
)

REQUIRED_PHRASES = [
    "<!-- authority: control -->",
    "Direct universal matter-coupling derivation is blocked",
    "not a claim that matter coupling is impossible",
    "Allowed Narrower Routes",
    "source-side matter-semantics equivalence-class theorem",
    "`PositiveMSProfile_v1` stability theorem",
    "`RR_E` separation-preservation theorem",
    "no-target certificate hygiene theorem",
    "coupling-law target formalization only",
    "detector-semantics alternative target formalization only",
    "matter_coupling_moratorium_check",
    "direct route blocked; narrow route allowed",
    "P11-T02",
]

REQUIRED_PREREQUISITES = [
    "adopted or explicitly authorized matter semantics",
    "detector semantics or an explicitly source-side replacement",
    "a coupling-law target and candidate",
    "stress-energy semantics or an explicit reason",
    "a matter action or an explicit alternative dynamics path",
    "`RR_E` separation, transport, and invariance handling",
    "no-target certificate hygiene",
    "protected Gate Chair or selector routing",
]

FORBIDDEN_OVERREADS = [
    "source-law adoption",
    "`SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption",
    "`PositiveMSProfile_v1` adoption as matter semantics",
    "`RR_ETransportCompletenessOrInvarianceLaw_v1` adoption as a source law",
    "`MetricData(E)` adoption",
    "`g_eff` scope expansion",
    "coupling-law adoption",
    "matter-semantics adoption",
    "detector-semantics adoption",
    "matter-coupling derivation or adoption",
    "stress-energy semantics, stress-energy tensor, or matter action",
    "Einstein equations",
    "benchmark promotion",
    "completed derivation",
    "future source-extension impossibility",
    "broad rejection of the theory",
]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_receipt(doc_hash: str, plan_hash: str) -> str:
    prerequisites = "\n".join(f"- {item}" for item in REQUIRED_PREREQUISITES)
    overreads = "\n".join(f"- {item}" for item in FORBIDDEN_OVERREADS)
    receipt = f"""<!-- authority: control -->

# P11-T01 Matter-Coupling Moratorium Receipt

Generated at: `{GENERATED_AT}`

## Verdict

PASS. The moratorium note blocks direct universal matter-coupling derivation
until listed tracked prerequisites exist. It allows lower-authority theorem,
precondition, audit, selector, and checklist routes. It does not declare matter
coupling impossible.

## Hashes

| Source | SHA-256 |
| --- | --- |
| `{DOC_PATH}` | `{doc_hash}` |
| `{PLAN_PATH}` | `{plan_hash}` |

## Prerequisites Confirmed

{prerequisites}

## Forbidden Overreads Confirmed

{overreads}

## Next Route

P11-T02 should create the matter-coupling pre-adoption checklist before P11-T03
selects any narrow theorem or precondition route.
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
    for phrase in REQUIRED_PHRASES:
        if phrase not in doc_text:
            errors.append(f"{DOC_PATH} missing required phrase: {phrase}")
    for item in REQUIRED_PREREQUISITES:
        if item not in doc_text:
            errors.append(f"{DOC_PATH} missing prerequisite: {item}")
    for item in FORBIDDEN_OVERREADS:
        if item not in doc_text:
            errors.append(f"{DOC_PATH} missing forbidden overread: {item}")

    if "matter coupling is impossible." in doc_text:
        errors.append(f"{DOC_PATH} contains an unqualified impossibility claim")

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
        "required_phrase_count": len(REQUIRED_PHRASES),
        "required_prerequisite_count": len(REQUIRED_PREREQUISITES),
        "forbidden_overread_count": len(FORBIDDEN_OVERREADS),
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
