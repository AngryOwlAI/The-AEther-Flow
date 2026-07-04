#!/usr/bin/env python3
"""Validate the v15 P14-T02 epistemic category glossary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
GLOSSARY_PATH = REPO_ROOT / "research_control/design/epistemic_category_glossary.md"

REQUIRED_CATEGORIES = [
    "Interpretation",
    "Model",
    "Physical theory",
    "Exact-GR benchmark compatibility",
    "First-principles recovery",
    "Derivation",
    "Scoped source object",
    "Physical object",
    "Evidence/precondition",
    "Adoption",
    "Promotion",
    "Validator receipt",
    "Scientific proof",
    "Publication surface",
    "Authority source",
]

REQUIRED_DISTINCTIONS = [
    "Interpretation Versus Derivation",
    "Model Versus Physical Theory",
    "Exact-GR Benchmark Compatibility Versus First-Principles Recovery",
    "Scoped Source Object Versus Physical Object",
    "Evidence/Precondition Versus Adoption",
    "Validator Receipt Versus Scientific Proof",
    "Publication Surface Versus Authority Source",
]

REQUIRED_GUARDS = [
    "GR is not derived",
    "not an established physical ontology",
    "`M_src` is not a target manifold",
    "`g_eff` is not an unscoped Lorentzian metric",
    "Validator receipts are not scientific proof",
    "Publication surfaces are not independent authority sources",
    "Benchmark promotion and completed derivation remain blocked",
]

REQUIRED_SOURCES = [
    "registries/DISTANCE_TO_GR_LEDGER.csv",
    "research_control/design/scoped_positive_claim_vocabulary.md",
    "research_control/design/einstein_equation_route_moratorium_v1.md",
    "research_control/design/public_status_exists_does_not_exist_source_spec.md",
    "implementations_plans/recommendations_implementation_plan_continue_task-v15.md",
]


def validate() -> dict[str, object]:
    text = GLOSSARY_PATH.read_text(encoding="utf-8")
    findings: list[str] = []

    for category in REQUIRED_CATEGORIES:
        if f"| {category} |" not in text:
            findings.append(f"missing category row: {category}")

    for distinction in REQUIRED_DISTINCTIONS:
        if f"### {distinction}" not in text:
            findings.append(f"missing distinction section: {distinction}")

    for guard in REQUIRED_GUARDS:
        if guard not in text:
            findings.append(f"missing public-overread guard: {guard}")

    for source in REQUIRED_SOURCES:
        if source not in text:
            findings.append(f"missing source material: {source}")

    forbidden_affirmative_phrases = [
        "GR is derived",
        "benchmark is promoted",
        "matter coupling is derived",
        "validator receipts prove",
        "publication surfaces are authority sources",
    ]
    for phrase in forbidden_affirmative_phrases:
        if phrase in text:
            findings.append(f"forbidden affirmative overread phrase present: {phrase}")

    return {
        "status": "PASS" if not findings else "FAIL",
        "glossary_path": str(GLOSSARY_PATH.relative_to(REPO_ROOT)),
        "required_category_count": len(REQUIRED_CATEGORIES),
        "required_distinction_count": len(REQUIRED_DISTINCTIONS),
        "required_guard_count": len(REQUIRED_GUARDS),
        "physics_delta": "none",
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate()
    payload = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
