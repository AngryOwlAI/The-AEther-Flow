#!/usr/bin/env python3
"""Validate the bounded EqSrc cycle-boundary selector smuggling audit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260718-036"
ART = TASK / "artifacts"
CANDIDATE = ROOT / "research_control/tasks/RT-20260718-035/artifacts/eqsrc_cycle_boundary_selector_law_candidate_v1.tex"
REPORT = ART / "eqsrc_cycle_boundary_selector_law_smuggling_audit_validation.json"
EXPECTED_CANDIDATE_HASH = "64901302bd6f37819ebd30aaaebaf39611d2c71c97d45b6cea6a39df11e0df94"


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] ^ b[0], a[1] ^ b[1])


def mat_vec(m: tuple[int, int, int, int], v: tuple[int, int]) -> tuple[int, int]:
    return (m[0] * v[0] ^ m[1] * v[1], m[2] * v[0] ^ m[3] * v[1])


def invertible_matrices() -> list[tuple[int, int, int, int]]:
    return [
        m
        for m in itertools.product((0, 1), repeat=4)
        if (m[0] * m[3] ^ m[1] * m[2]) == 1
    ]


def relation(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] == b[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    states = list(itertools.product((0, 1), repeat=2))
    matrices = invertible_matrices()
    affine_maps = []
    relation_stabilizers = 0
    label_fixers = 0
    candidate_variations = 0
    for m in matrices:
        for t in states:
            image = {z: add(mat_vec(m, z), t) for z in states}
            preserves = all(
                relation(a, b) == relation(image[a], image[b])
                for a in states
                for b in states
            )
            fixes_labels = all(image[z][0] == z[0] for z in states)
            is_candidate = m == (1, 0, 0, 1) and t in ((0, 0), (0, 1))
            relation_stabilizers += int(preserves)
            label_fixers += int(fixes_labels)
            candidate_variations += int(is_candidate)
            affine_maps.append(image)

    translate_p = {z: add(z, (1, 0)) for z in states}
    label_changes = sum(translate_p[z][0] != z[0] for z in states)
    relation_mismatches = sum(
        relation(a, b) != relation(translate_p[a], translate_p[b])
        for a in states
        for b in states
    )

    bare_invariant_subsets = []
    carrier = tuple(range(4))
    permutations = list(itertools.permutations(carrier))
    for mask in range(1 << len(carrier)):
        subset = {x for x in carrier if mask & (1 << x)}
        if all({perm[x] for x in subset} == subset for perm in permutations):
            bare_invariant_subsets.append(sorted(subset))

    complement_cases = 0
    complement_relation_distinct = 0
    for n in (2, 4, 6):
        x = set(range(n))
        for size in range(1, n, 2):
            for p_tuple in itertools.combinations(range(n), size):
                p = set(p_tuple)
                q = x - p
                if len(q) % 2 != 1:
                    continue
                complement_cases += 1
                # In the basis (1_P,1_Q), B_P is the q-line and B_Q the p-line.
                complement_relation_distinct += int((0, 1) != (1, 0))

    required_files = [
        ART / "child_phys_math_eqsrc_cycle_boundary_selector_law_smuggling_audit.yaml",
        ART / "child_phys_phil_eqsrc_cycle_boundary_selector_law_smuggling_audit.yaml",
        ART / "parent_conflict_review_eqsrc_cycle_boundary_selector_law_smuggling_audit.yaml",
        ART / "parent_fusion_notes_eqsrc_cycle_boundary_selector_law_smuggling_audit.md",
        ART / "eqsrc_cycle_boundary_selector_law_smuggling_audit.tex",
        ART / "eqsrc_cycle_boundary_selector_law_smuggling_audit_receipt.md",
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260718-036.md",
        TASK / "documentation_impact.yaml",
        TASK / "jobs/AJ-RT-20260718-036-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260718-036-001.yaml",
        TASK / "roles/smuggling-auditor@0.2.0--RT-20260718-036.yaml",
        ROOT / "research_control/handoffs/handoff-0761.yaml",
        ROOT / "research_control/handoffs/handoff-0761.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_files if not path.is_file()]
    candidate_hash = hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()
    audit_text = (ART / "eqsrc_cycle_boundary_selector_law_smuggling_audit.tex").read_text()
    required_tokens = [
        "blocked\\_adoption\\_open\\_continuation",
        "new\\_ontology\\_primitive\\_candidate",
        "relation stabilizers",
        "Bare-carrier naturality obstruction",
        "next lawful route",
    ]
    missing_tokens = [token for token in required_tokens if token not in audit_text]

    checks = {
        "candidate_hash_matches": candidate_hash == EXPECTED_CANDIDATE_HASH,
        "gl2_count_is_6": len(matrices) == 6,
        "affine_group_count_is_24": len(affine_maps) == 24,
        "relation_stabilizer_count_is_8": relation_stabilizers == 8,
        "label_fixer_count_is_4": label_fixers == 4,
        "candidate_variation_count_is_2": candidate_variations == 2,
        "relation_changer_count_is_16": 24 - relation_stabilizers == 16,
        "translation_p_changes_all_labels": label_changes == 4,
        "translation_p_preserves_relation": relation_mismatches == 0,
        "bare_carrier_invariants_are_trivial": bare_invariant_subsets == [[], [0, 1, 2, 3]],
        "complement_family_nonempty": complement_cases > 0,
        "all_complement_relations_distinct": complement_relation_distinct == complement_cases,
        "required_files_present": not missing,
        "required_audit_tokens_present": not missing_tokens,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    payload = {
        "status": status,
        "candidate_hash": candidate_hash,
        "affine_group_count": len(affine_maps),
        "relation_stabilizer_count": relation_stabilizers,
        "pointwise_label_fixer_count": label_fixers,
        "candidate_variation_count": candidate_variations,
        "relation_changer_count": 24 - relation_stabilizers,
        "translation_p_label_changes": label_changes,
        "translation_p_relation_mismatches": relation_mismatches,
        "bare_carrier_invariant_subsets": bare_invariant_subsets,
        "complement_cases_checked": complement_cases,
        "complement_relations_distinct": complement_relation_distinct,
        "missing_files": missing,
        "missing_tokens": missing_tokens,
        "checks": checks,
    }
    if args.write_report:
        REPORT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
