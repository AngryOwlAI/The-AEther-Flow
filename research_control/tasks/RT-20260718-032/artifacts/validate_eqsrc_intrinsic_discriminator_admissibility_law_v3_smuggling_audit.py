#!/usr/bin/env python3
"""Validate the bounded RT-20260718-032 v3 smuggling-audit packet."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260718-032"
ART = TASK / "artifacts"
REPORT = ART / "eqsrc_intrinsic_discriminator_admissibility_law_v3_smuggling_audit_validation.json"

REQUIRED = {
    "audit": ART / "eqsrc_intrinsic_discriminator_admissibility_law_v3_smuggling_audit.tex",
    "receipt": ART / "eqsrc_intrinsic_discriminator_admissibility_law_v3_smuggling_audit_receipt.md",
    "math_child": ART / "child_phys_math_eqsrc_intrinsic_discriminator_v3_smuggling_audit.yaml",
    "phil_child": ART / "child_phys_phil_eqsrc_intrinsic_discriminator_v3_smuggling_audit.yaml",
    "review": ART / "parent_conflict_review_eqsrc_intrinsic_discriminator_v3_smuggling_audit.yaml",
    "fusion": ART / "parent_fusion_notes_eqsrc_intrinsic_discriminator_v3_smuggling_audit.md",
}

TOKENS = [
    "source_pure_as_written_formal_repair_verified_pending_bounded_refuter_stress",
    "new_ontology_primitive_candidate",
    "blocked_adoption_open_continuation",
    "candidate_audited_pending_stress",
    "Set",
    "injective",
    "4096",
    "256",
    "192",
    "zero mismatches",
    "Refuter",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relation(x: int, y: int) -> bool:
    return (x // 2) == (y // 2)


def induced_class(function: tuple[int, ...], source_class: int) -> int | None:
    values = {function[x] // 2 for x in range(4) if x // 2 == source_class}
    return next(iter(values)) if len(values) == 1 else None


def census() -> dict[str, int]:
    preserving = reflecting = factor_mismatch = injective_mismatch = 0
    for function in itertools.product(range(8), repeat=4):
        pres = all(not relation(x, y) or relation(function[x], function[y])
                   for x in range(4) for y in range(4))
        refl = all(not relation(function[x], function[y]) or relation(x, y)
                   for x in range(4) for y in range(4))
        bars = [induced_class(function, c) for c in range(2)]
        factors = all(value is not None for value in bars)
        inj = factors and len(set(bars)) == 2
        preserving += int(pres)
        reflecting += int(pres and refl)
        factor_mismatch += int(pres != factors)
        injective_mismatch += int(pres and (refl != inj))
    return {
        "total_functions": 8**4,
        "preserving_functions": preserving,
        "preserving_and_reflecting_functions": reflecting,
        "preservation_factorization_mismatches": factor_mismatch,
        "reflection_injectivity_mismatches": injective_mismatch,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    hashes: dict[str, str] = {}
    corpus = ""
    for label, path in REQUIRED.items():
        if not path.is_file():
            errors.append(f"missing {label}: {path.relative_to(ROOT)}")
            continue
        hashes[label] = sha(path)
        corpus += "\n" + path.read_text(encoding="utf-8")
    for token in TOKENS:
        if token not in corpus:
            errors.append(f"required token absent: {token}")
    candidate = ROOT / "research_control/tasks/RT-20260718-031/artifacts/eqsrc_intrinsic_discriminator_admissibility_law_candidate_v3.tex"
    expected_hash = "ed865297c417cadf4d030717d5c1a9c6c84335939c6fe9cee215192050bc30dd"
    if not candidate.is_file() or sha(candidate) != expected_hash:
        errors.append("exact v3 candidate hash mismatch")
    counts = census()
    expected = {
        "total_functions": 4096,
        "preserving_functions": 256,
        "preserving_and_reflecting_functions": 192,
        "preservation_factorization_mismatches": 0,
        "reflection_injectivity_mismatches": 0,
    }
    if counts != expected:
        errors.append(f"cross-complex census mismatch: {counts}")
    result = {
        "task_id": "RT-20260718-032",
        "job_id": "AJ-RT-20260718-032-001",
        "status": "PASS" if not errors else "FAIL",
        "audit_result": "source_pure_as_written_formal_repair_verified_pending_bounded_refuter_stress",
        "next_required_role": "refuter@0.2.0",
        "candidate_hash": expected_hash,
        "artifact_hashes": hashes,
        "cross_complex_census": counts,
        "errors": errors,
    }
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
