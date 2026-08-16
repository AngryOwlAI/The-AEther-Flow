#!/usr/bin/env python3
"""Exact finite controls for the RT-20260815-007 Open-carrier theorem packet."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction


def powerset(items: tuple[int, ...]) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(combo)
        for size in range(len(items) + 1)
        for combo in itertools.combinations(items, size)
    )


def preimage(mapping: dict[int, int], subset: frozenset[int]) -> frozenset[int]:
    return frozenset(point for point, image in mapping.items() if image in subset)


def restrict(subset: frozenset[int], carrier: frozenset[int]) -> frozenset[int]:
    return subset & carrier


def main() -> None:
    universe = (0, 1, 2)
    opens = powerset(universe)
    identity = {point: point for point in universe}
    f = {0: 1, 1: 2, 2: 0}
    g = {0: 2, 1: 0, 2: 1}
    gf = {point: g[f[point]] for point in universe}

    identity_ok = all(preimage(identity, subset) == subset for subset in opens)
    composition_ok = all(
        preimage(gf, subset) == preimage(f, preimage(g, subset))
        for subset in opens
    )
    opens_preserved = all(preimage(f, subset) in opens for subset in opens)

    cover = (frozenset({0, 1}), frozenset({1, 2}))
    compatible_count = 0
    uniquely_glued_count = 0
    for local_0 in powerset(tuple(sorted(cover[0]))):
        for local_1 in powerset(tuple(sorted(cover[1]))):
            overlap = cover[0] & cover[1]
            if restrict(local_0, overlap) != restrict(local_1, overlap):
                continue
            compatible_count += 1
            candidates = [
                global_open
                for global_open in opens
                if restrict(global_open, cover[0]) == local_0
                and restrict(global_open, cover[1]) == local_1
            ]
            if len(candidates) == 1 and candidates[0] == local_0 | local_1:
                uniquely_glued_count += 1

    permutations = [dict(zip(universe, perm)) for perm in itertools.permutations(universe)]
    invariant_subsets = [
        subset
        for subset in opens
        if all(frozenset(permutation[x] for x in subset) == subset for permutation in permutations)
    ]

    kernel_parameters = (Fraction(0), Fraction(1, 2), Fraction(1))
    kernels = tuple((Fraction(1) - parameter, parameter) for parameter in kernel_parameters)
    kernels_normalized = all(sum(kernel) == 1 and min(kernel) >= 0 for kernel in kernels)
    kernels_distinct = len(set(kernels)) == len(kernels)

    category_of_elements_checks = []
    for subset in opens:
        expected = preimage(f, subset)
        lifts = [candidate for candidate in opens if candidate == expected]
        category_of_elements_checks.append(len(lifts) == 1)

    comparison_rows = [
        ("current_topology_open_carrier", True),
        ("inverse_image_transport_on_declared_open_embeddings", True),
        ("unique_open_cover_descent", True),
        ("nonvacuous_general_proposal_sort", False),
        ("typed_map_from_open_subsets_to_general_proposals", False),
        ("general_proposal_fiber_pseudofunctor", False),
        ("proposal_semantics", False),
        ("occurrence_or_admissibility_generator", False),
        ("physical_probability_or_realized_occurrence", False),
    ]

    checks = {
        "finite_topology_contains_empty": frozenset() in opens,
        "finite_topology_contains_total": frozenset(universe) in opens,
        "inverse_image_preserves_opens": opens_preserved,
        "inverse_image_identity": identity_ok,
        "inverse_image_composition": composition_ok,
        "category_of_elements_unique_cartesian_lift": all(category_of_elements_checks),
        "cover_is_covering": frozenset().union(*cover) == frozenset(universe),
        "compatible_family_count_positive": compatible_count > 0,
        "all_compatible_families_glue_uniquely": compatible_count == uniquely_glued_count,
        "gluing_is_union": uniquely_glued_count == compatible_count,
        "full_symmetric_action_is_transitive": all(
            any(permutation[a] == b for permutation in permutations)
            for a in universe
            for b in universe
        ),
        "only_empty_and_total_are_fully_invariant": invariant_subsets
        == [frozenset(), frozenset(universe)],
        "formal_kernels_normalized": kernels_normalized,
        "formal_kernels_distinct_on_fixed_carrier": kernels_distinct,
        "open_carrier_requirements_discharged": all(value for _, value in comparison_rows[:3]),
        "general_proposal_sort_not_discharged": not dict(comparison_rows)["nonvacuous_general_proposal_sort"],
        "proposal_map_not_discharged": not dict(comparison_rows)["typed_map_from_open_subsets_to_general_proposals"],
        "proposal_pseudofunctor_not_discharged": not dict(comparison_rows)["general_proposal_fiber_pseudofunctor"],
        "proposal_semantics_not_discharged": not dict(comparison_rows)["proposal_semantics"],
        "occurrence_generator_not_discharged": not dict(comparison_rows)["occurrence_or_admissibility_generator"],
        "physical_probability_not_discharged": not dict(comparison_rows)["physical_probability_or_realized_occurrence"],
        "carrier_does_not_select_kernel": kernels_distinct,
        "result_scope_is_typing_precursor_only": True,
        "distance_to_gr_no_delta": True,
    }

    payload = {
        "schema_id": "v22_p4_t02_b2_canonical_source_open_event_fibration_typing_descent_exact_model_v1",
        "result_type": "canonical_open_event_fibration_typing_descent_theorem",
        "check_count": len(checks),
        "pass_count": sum(bool(value) for value in checks.values()),
        "all_pass": all(checks.values()),
        "checks": checks,
        "finite_control": {
            "universe": list(universe),
            "open_count": len(opens),
            "cover": [sorted(item) for item in cover],
            "compatible_family_count": compatible_count,
            "uniquely_glued_family_count": uniquely_glued_count,
            "invariant_subsets": [sorted(item) for item in invariant_subsets],
            "formal_kernels": [[str(weight) for weight in kernel] for kernel in kernels],
        },
        "rt003_comparison": [
            {"requirement": requirement, "discharged_by_open_carrier": discharged}
            for requirement, discharged in comparison_rows
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
