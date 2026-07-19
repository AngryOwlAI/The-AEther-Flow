#!/usr/bin/env python3
"""Finite support validator for RT-20260718-025.

This validator checks finite combinatorics and required control markers. A PASS
is operational support only; it is not physics proof or adoption authority.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260718-025"
ARTIFACTS = TASK / "artifacts"
REPORT = ARTIFACTS / "eqsrc_source_rooted_quotient_selector_refuter_stress_validation.json"
OBJECTS = tuple(range(4))
BASE_PROFILE = (0, 1, 2, 3)


def partition(profile: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    blocks: dict[int, list[int]] = {0: [], 1: []}
    for obj, value in enumerate(profile):
        blocks[value % 2].append(obj)
    return tuple(sorted(tuple(sorted(block)) for block in blocks.values()))


def transported_profile(profile: tuple[int, ...], perm: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(perm)
    for source, target in enumerate(perm):
        inverse[target] = source
    return tuple(profile[inverse[target]] for target in OBJECTS)


def relation(profile: tuple[int, ...], a: int, b: int) -> bool:
    return profile[a] % 2 == profile[b] % 2


def is_equivalence(profile: tuple[int, ...]) -> bool:
    reflexive = all(relation(profile, a, a) for a in OBJECTS)
    symmetric = all(
        relation(profile, a, b) == relation(profile, b, a)
        for a in OBJECTS
        for b in OBJECTS
    )
    transitive = all(
        not (relation(profile, a, b) and relation(profile, b, c))
        or relation(profile, a, c)
        for a in OBJECTS
        for b in OBJECTS
        for c in OBJECTS
    )
    return reflexive and symmetric and transitive


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    profiles = list(itertools.permutations(range(4)))
    partitions: dict[tuple[tuple[int, ...], ...], int] = {}
    for profile in profiles:
        key = partition(profile)
        partitions[key] = partitions.get(key, 0) + 1

    permutations = list(itertools.permutations(OBJECTS))
    base_partition = partition(BASE_PROFILE)
    active_stabilizer = [
        perm
        for perm in permutations
        if tuple(sorted(tuple(sorted(perm[obj] for obj in block)) for block in base_partition))
        == base_partition
    ]
    transported_equivariance = all(
        relation(transported_profile(BASE_PROFILE, perm), perm[a], perm[b])
        == relation(BASE_PROFILE, a, b)
        for perm in permutations
        for a in OBJECTS
        for b in OBJECTS
    )

    shifts = list(itertools.product(range(4), repeat=4))
    varied_profiles = [
        tuple((BASE_PROFILE[obj] + shift[obj]) % 4 for obj in OBJECTS)
        for shift in shifts
    ]
    additive_stabilizer = [
        shift
        for shift, profile in zip(shifts, varied_profiles)
        if partition(profile) == base_partition
    ]
    declared_v_h = [shift for shift in shifts if all(value in {0, 2} for value in shift)]
    relation_changing = [
        shift
        for shift, profile in zip(shifts, varied_profiles)
        if partition(profile) != base_partition
    ]
    bijective_relation_changing = [
        profile
        for profile in profiles
        if partition(profile) != base_partition
    ]
    equivalence_checks = all(is_equivalence(profile) for profile in profiles)

    required_paths = [
        ARTIFACTS / "child_phys_math_eqsrc_quotient_selector_refuter_stress.yaml",
        ARTIFACTS / "child_phys_phil_eqsrc_quotient_selector_refuter_stress.yaml",
        ARTIFACTS / "parent_conflict_review_eqsrc_quotient_selector_refuter_stress.yaml",
        ARTIFACTS / "parent_fusion_notes_eqsrc_quotient_selector_refuter_stress.md",
        ARTIFACTS / "eqsrc_source_rooted_quotient_selector_refuter_stress.tex",
        ARTIFACTS / "eqsrc_source_rooted_quotient_selector_refuter_stress_receipt.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in required_paths)
    required_markers = [
        "scoped_obstruction",
        "blocked_adoption_open_continuation",
        "physical covariance",
        "future source-extension impossibility",
        "Theoretical Continuation Selector",
    ]

    checks = {
        "bijective_profiles_24": len(profiles) == 24,
        "three_partitions": len(partitions) == 3,
        "eight_profiles_per_partition": sorted(partitions.values()) == [8, 8, 8],
        "active_stabilizer_8": len(active_stabilizer) == 8,
        "partition_orbit_3": len(permutations) // len(active_stabilizer) == 3,
        "transported_equivariance_all_24": transported_equivariance,
        "additive_variations_256": len(shifts) == 256,
        "additive_stabilizer_32": len(additive_stabilizer) == 32,
        "declared_v_h_16": len(declared_v_h) == 16,
        "declared_v_h_subset": set(declared_v_h).issubset(set(additive_stabilizer)),
        "relation_changing_224": len(relation_changing) == 224,
        "bijective_relation_changing_16": len(bijective_relation_changing) == 16,
        "all_profile_relations_equivalence": equivalence_checks,
        "explicit_counterprofile_changes_partition": partition((0, 2, 1, 3)) != base_partition,
        "required_paths_exist": all(path.is_file() for path in required_paths),
        "required_control_markers": all(marker in text for marker in required_markers),
    }
    report = {
        "schema": "eqsrc-source-rooted-quotient-selector-refuter-stress-validation.v1",
        "task_id": "RT-20260718-025",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "support_only": True,
        "counts": {
            "bijective_profiles": len(profiles),
            "distinct_partitions": len(partitions),
            "active_permutation_stabilizer": len(active_stabilizer),
            "additive_variations": len(shifts),
            "additive_relation_stabilizer": len(additive_stabilizer),
            "declared_v_h": len(declared_v_h),
            "relation_changing_additive_variations": len(relation_changing),
            "bijective_relation_changing_profiles": len(bijective_relation_changing),
        },
        "checks": checks,
        "authority_note": "Operational finite support only; not physics proof, ontology adoption, or claim-promotion authority.",
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
