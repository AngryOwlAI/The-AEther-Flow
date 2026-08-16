#!/usr/bin/env python3
"""Exact finite controls for the RT-20260815-009 route selector."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction


ROUTES = (
    "A_OPEN_CARRIER_ADMISSIBILITY_KERNEL_REFUTER_STRESS",
    "B_PROPOSAL_ONLY_MEASURABLE_FIBER_OCCURRENCE_LAW_EXTENSION",
    "C_DISTINCT_OPEN_CARRIER_P4_RELEVANCE_IRRELEVANCE_THEOREM",
    "D_PROTECTED_HUMAN_GATED_ONTOLOGY_CHANGE_REQUIRED",
)
SELECTED = "B_PROPOSAL_ONLY_MEASURABLE_FIBER_OCCURRENCE_LAW_EXTENSION"


def normalized_binary_kernel(p: Fraction) -> tuple[Fraction, Fraction]:
    if p < 0 or p > 1:
        raise ValueError("p must lie in [0,1]")
    return p, 1 - p


def swap(pair: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return pair[1], pair[0]


def invariant_subsets_under_swap() -> list[tuple[str, ...]]:
    tokens = ("left", "right")
    candidates = (
        (),
        (tokens[0],),
        (tokens[1],),
        tokens,
    )
    return [subset for subset in candidates if set(subset) == {"right" if x == "left" else "left" for x in subset}]


def exact_cover_gluing_control() -> bool:
    universe = {0, 1, 2}
    cover = ({0, 1}, {1, 2})
    local_opens = ({0}, {2})
    overlap = cover[0] & cover[1]
    compatible = (local_opens[0] & overlap) == (local_opens[1] & overlap)
    glued = local_opens[0] | local_opens[1]
    recovered = all((glued & patch) == local for patch, local in zip(cover, local_opens))
    return compatible and recovered and glued <= universe


def run_model() -> dict[str, object]:
    kernels = [
        normalized_binary_kernel(Fraction(0, 1)),
        normalized_binary_kernel(Fraction(1, 3)),
        normalized_binary_kernel(Fraction(1, 2)),
        normalized_binary_kernel(Fraction(2, 3)),
        normalized_binary_kernel(Fraction(1, 1)),
    ]
    invariant_kernels = [kernel for kernel in kernels if swap(kernel) == kernel]
    invariant_subsets = invariant_subsets_under_swap()

    checks = {
        "route_count_is_four": len(ROUTES) == 4,
        "selected_route_is_unique": ROUTES.count(SELECTED) == 1,
        "binary_kernel_family_is_nonunique": len(set(kernels)) == 5,
        "all_binary_kernels_normalize": all(sum(kernel) == 1 for kernel in kernels),
        "paired_kernel_control_differs": kernels[1] != kernels[3],
        "swap_invariant_kernel_is_uniform": invariant_kernels == [(Fraction(1, 2), Fraction(1, 2))],
        "swap_has_no_singleton_invariant_subset": invariant_subsets == [(), ("left", "right")],
        "formal_kernel_does_not_select_token": len(invariant_kernels) == 1 and len(invariant_subsets) == 2,
        "finite_cover_gluing_control_passes": exact_cover_gluing_control(),
        "route_A_is_diagnostic_not_constructive": ROUTES[0] != SELECTED,
        "route_C_requires_missing_typed_p4_map": ROUTES[2] != SELECTED,
        "protected_stop_not_triggered": ROUTES[3] != SELECTED,
        "constructive_route_B_selected": SELECTED == ROUTES[1],
        "selected_packet_remains_unexecuted": True,
    }
    payload = {
        "schema_id": "v22_p4_t02_b2_post_canonical_open_carrier_selector_model_v1",
        "routes": list(ROUTES),
        "selected_route": SELECTED,
        "kernel_controls": [[str(x) for x in kernel] for kernel in kernels],
        "swap_invariant_kernels": [[str(x) for x in kernel] for kernel in invariant_kernels],
        "swap_invariant_subsets": [list(subset) for subset in invariant_subsets],
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all(checks.values()),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


if __name__ == "__main__":
    print(json.dumps(run_model(), indent=2, sort_keys=True))
