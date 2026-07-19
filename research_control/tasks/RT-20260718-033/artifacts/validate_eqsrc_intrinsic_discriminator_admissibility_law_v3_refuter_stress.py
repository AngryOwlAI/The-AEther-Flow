#!/usr/bin/env python3
"""Finite support validator for RT-20260718-033.

The checks support one bounded draft/control Refuter packet. A PASS is not
physics proof, ontology adoption, or claim-promotion authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260718-033"
ARTIFACTS = TASK / "artifacts"
REPORT = ARTIFACTS / (
    "eqsrc_intrinsic_discriminator_admissibility_law_v3_"
    "refuter_stress_validation.json"
)
VECTORS = tuple(range(4))
DIFFERENTIAL_IMAGES = VECTORS


def boundary(image: int) -> frozenset[int]:
    return frozenset({0}) if image == 0 else frozenset({0, image})


def relation(image: int) -> frozenset[tuple[int, int]]:
    subspace = boundary(image)
    return frozenset(
        (left, right)
        for left in VECTORS
        for right in VECTORS
        if left ^ right in subspace
    )


def is_equivalence(pairs: frozenset[tuple[int, int]]) -> bool:
    reflexive = all((item, item) in pairs for item in VECTORS)
    symmetric = all((right, left) in pairs for left, right in pairs)
    transitive = all(
        (left, final) in pairs
        for left in VECTORS
        for middle in VECTORS
        for final in VECTORS
        if (left, middle) in pairs and (middle, final) in pairs
    )
    return reflexive and symmetric and transitive


def translation_preserves_and_reflects(image: int, shift: int) -> bool:
    pairs = relation(image)
    return all(
        (((left ^ shift), (right ^ shift)) in pairs) == ((left, right) in pairs)
        for left in VECTORS
        for right in VECTORS
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    relations = {image: relation(image) for image in DIFFERENTIAL_IMAGES}
    equality = relations[0]
    nonzero = [relations[image] for image in DIFFERENTIAL_IMAGES if image]
    equality_differences = [
        len(equality.symmetric_difference(candidate)) for candidate in nonzero
    ]
    nonzero_differences = [
        len(nonzero[first].symmetric_difference(nonzero[second]))
        for first in range(len(nonzero))
        for second in range(first + 1, len(nonzero))
    ]

    # Identity E_0 -> E_a: equality preservation is automatic; reflection
    # fails because 0 and a are destination-related but source-unrelated.
    identity_preserves = all(
        (left, right) in relations[1]
        for left, right in equality
    )
    identity_reflects = all(
        (left, right) in equality
        for left, right in relations[1]
    )
    induced_h1_injective = all(
        not (left ^ right in boundary(1)) or left == right
        for left in VECTORS
        for right in VECTORS
    )

    # All subspaces of F2^2: zero, three lines, and the full space. The
    # representation theorem assigns congruence modulo each subspace.
    all_subspaces = [
        frozenset({0}),
        frozenset({0, 1}),
        frozenset({0, 2}),
        frozenset({0, 3}),
        frozenset(VECTORS),
    ]
    represented_congruences = {
        frozenset(
            (left, right)
            for left in VECTORS
            for right in VECTORS
            if left ^ right in subspace
        )
        for subspace in all_subspaces
    }

    required_paths = [
        ARTIFACTS / "child_phys_math_eqsrc_intrinsic_discriminator_v3_refuter_stress.yaml",
        ARTIFACTS / "child_phys_phil_eqsrc_intrinsic_discriminator_v3_refuter_stress.yaml",
        ARTIFACTS / "parent_conflict_review_eqsrc_intrinsic_discriminator_v3_refuter_stress.yaml",
        ARTIFACTS / "parent_fusion_notes_eqsrc_intrinsic_discriminator_v3_refuter_stress.md",
        ARTIFACTS / "eqsrc_intrinsic_discriminator_admissibility_law_v3_refuter_stress.tex",
        ARTIFACTS / "eqsrc_intrinsic_discriminator_admissibility_law_v3_refuter_stress_receipt.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in required_paths)
    required_markers = [
        "scoped_obstruction",
        "blocked_adoption_open_continuation",
        "construction-relative",
        "Mistyped maps",
        "future source-extension impossibility",
        "Theoretical Continuation Selector",
    ]

    checks = {
        "four_valid_chain_packages": len(DIFFERENTIAL_IMAGES) == 4,
        "four_distinct_relations": len(set(relations.values())) == 4,
        "equality_has_4_related_pairs": len(equality) == 4,
        "nonzero_relations_have_8_related_pairs": all(
            len(candidate) == 8 for candidate in nonzero
        ),
        "all_relations_are_equivalences": all(
            is_equivalence(candidate) for candidate in relations.values()
        ),
        "equality_to_nonzero_symmetric_difference_4": equality_differences == [4, 4, 4],
        "distinct_nonzero_symmetric_difference_8": nonzero_differences == [8, 8, 8],
        "declared_translations_preserve_and_reflect": all(
            translation_preserves_and_reflects(image, shift)
            for image in DIFFERENTIAL_IMAGES
            for shift in boundary(image)
        ),
        "identity_chain_map_preserves": identity_preserves,
        "identity_chain_map_does_not_reflect": not identity_reflects,
        "induced_h1_is_noninjective": not induced_h1_injective,
        "five_linear_congruences_represented": len(represented_congruences) == 5,
        "nontrivial_instance_has_two_classes": len(VECTORS) // len(boundary(1)) == 2,
        "required_paths_exist": all(path.is_file() for path in required_paths),
        "required_control_markers": all(marker in text for marker in required_markers),
    }
    report = {
        "schema": "eqsrc-intrinsic-discriminator-v3-refuter-stress-validation.v1",
        "task_id": "RT-20260718-033",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "support_only": True,
        "counts": {
            "fixed_carrier_differentials": len(DIFFERENTIAL_IMAGES),
            "distinct_relations": len(set(relations.values())),
            "equality_related_pairs": len(equality),
            "nonzero_related_pairs": [len(candidate) for candidate in nonzero],
            "represented_f2_2_linear_congruences": len(represented_congruences),
        },
        "checks": checks,
        "authority_note": (
            "Operational finite support only; not physics proof, ontology "
            "adoption, or claim-promotion authority."
        ),
    }
    if args.write_report:
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
