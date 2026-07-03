#!/usr/bin/env python3
"""Validate the v15 P8-T01 Einstein-equation route moratorium note."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
GENERATED_AT = "2026-07-03T09:59:09Z"
DOC_PATH = "research_control/design/einstein_equation_route_moratorium_v1.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v15.md"
RECEIPT_PATH = (
    "research_control/tasks/RT-20260703-012/artifacts/"
    "p8_t01_einstein_equation_moratorium_receipt.md"
)

REQUIRED_PHRASES = [
    "<!-- authority: control -->",
    "No Einstein-equation route may be selected until a tracked source establishes",
    "not a claim that Einstein equations are impossible",
    "direct EFE route from scoped evidence/precondition alone is blocked",
    "This moratorium does not block bounded prerequisite work",
    "Allowed Prerequisite Routes",
    "einstein_equation_route_moratorium_check",
    "direct EFE route blocked; bounded prerequisite work allowed",
    "P8-T02",
]

REQUIRED_PREREQUISITES = [
    "source-side matter semantics",
    "detector semantics or a source-side replacement, if required",
    "coupling-law target",
    "coupling-law candidate",
    "coupling-law audit/stress",
    "matter-coupling derivation or precise obstruction",
    "stress-energy semantics target",
    "stress-energy tensor semantics",
    "matter action or alternative dynamics principle",
    "variation principle or field-equation dynamics",
    "protected Gate Chair authority for any benchmark-promotion step",
]

ALLOWED_PREREQUISITE_ROUTE_PHRASES = [
    "source-side matter-semantics target",
    "detector-semantics target or explicitly source-side replacement",
    "coupling-law target, candidate, audit, stress, or obstruction",
    "matter-coupling derivation, adoption-readiness, or precise obstruction",
    "stress-energy semantics target work",
    "stress-energy tensor semantics work only after",
    "matter action or alternative dynamics-principle target work",
    "variation-principle or field-equation dynamics target work",
    "Gate Chair readiness work",
    "validator, linter, checklist, role-contract, graph, or public-status packets",
]

FORBIDDEN_OVERREADS = [
    "source-law adoption",
    "`RR_ETransportCompletenessOrInvarianceLaw_v1` adoption",
    "unrestricted `RR_E` theorem authority",
    "`PositiveMSProfile_v1` adoption",
    "`SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption",
    "source-extension data adoption beyond exact scoped gate result",
    "`MetricData(E)` adoption",
    "`g_eff` adoption or scope expansion",
    "coupling-law adoption",
    "matter-semantics adoption",
    "detector-semantics adoption",
    "matter-coupling derivation or adoption",
    "stress-energy semantics",
    "stress-energy tensor",
    "matter action",
    "Einstein equations",
    "exact-GR benchmark promotion",
    "Gate Chair verdict",
    "completed derivation",
    "future source-extension impossibility",
    "program-wide no-go conclusion",
]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_receipt(doc_hash: str, plan_hash: str) -> str:
    prerequisites = "\n".join(f"- {item}" for item in REQUIRED_PREREQUISITES)
    allowed_routes = "\n".join(f"- {item}" for item in ALLOWED_PREREQUISITE_ROUTE_PHRASES)
    overreads = "\n".join(f"- {item}" for item in FORBIDDEN_OVERREADS)
    receipt = f"""<!-- authority: control -->

# P8-T01 Einstein-Equation Moratorium Receipt

Generated at: `{GENERATED_AT}`

## Verdict

PASS. The moratorium note blocks a direct EFE route from scoped
evidence/precondition alone until all listed prerequisites are established or
explicitly routed by tracked authority. It preserves bounded prerequisite
work. It does not derive Einstein equations and does not declare Einstein
equations impossible.

## Hashes

| Source | SHA-256 |
| --- | --- |
| `{DOC_PATH}` | `{doc_hash}` |
| `{PLAN_PATH}` | `{plan_hash}` |

## Prerequisites Confirmed

{prerequisites}

## Allowed Prerequisite Route Phrases Confirmed

{allowed_routes}

## Forbidden Overreads Confirmed

{overreads}

## Next Route

P8-T02 should add EFE prerequisite validator/linter fixtures. Those fixtures
may reject premature EFE claims but must not create field-equation authority.
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
    for item in ALLOWED_PREREQUISITE_ROUTE_PHRASES:
        if item not in doc_text:
            errors.append(f"{DOC_PATH} missing allowed prerequisite route phrase: {item}")
    for item in FORBIDDEN_OVERREADS:
        if item not in doc_text:
            errors.append(f"{DOC_PATH} missing forbidden overread: {item}")

    prohibited_phrases = [
        "Einstein equations are impossible.",
        "therefore Einstein equations are impossible",
        "therefore EFE is impossible",
    ]
    for phrase in prohibited_phrases:
        if phrase in doc_text:
            errors.append(f"{DOC_PATH} contains an unqualified impossibility claim: {phrase}")

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
        "allowed_prerequisite_route_phrase_count": len(ALLOWED_PREREQUISITE_ROUTE_PHRASES),
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
