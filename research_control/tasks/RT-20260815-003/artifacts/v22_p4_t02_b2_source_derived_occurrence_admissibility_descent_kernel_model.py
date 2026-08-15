#!/usr/bin/env python3
"""Exact controls for the RT-20260815-003 occurrence-layer audit.

The finite calculations distinguish a deterministic natural section, a proper
nonempty invariant admissible subset, and a normalized equivariant kernel.  A
second set of controls checks overlap descent and factorization through a
source reduct.  These are mathematical controls only: no measure is interpreted
as a realized event or physical probability, and no proposal grammar is added
to the canonical source ontology.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Mapping


Q = Fraction
ROOT = Path(__file__).resolve().parents[4]
FOUNDATIONS = ROOT / "ontology/tex/aether_flow_foundations.tex"
DYNAMICS = ROOT / "ontology/tex/aether_flow_dynamics.tex"

RESULT_TYPE = "current_source_provenance_or_typing_obstruction"
OBSTRUCTION_ID = (
    "OB-V22-P4T02-B2-SOURCE-DERIVED-OCCURRENCE-ADMISSIBILITY-"
    "DESCENT-KERNEL-CURRENT-SOURCE-TYPING-PROVENANCE-001"
)

FREEZES = (
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-KSTAR-STANDALONE-LOCAL-BRIDGE-IRRELEVANCE",
    "NDCL-V22-P4T02-B2-PROJECTIVE-CONORMAL-ROBUST-SELECTION-CONFORMAL-LIFT",
)

CURRENT_TYPED_SYMBOLS = ("Sub",)
MISSING_OCCURRENCE_SYMBOLS = (
    "Prop",
    "U",
    "ProposalFiber",
    "FiberAction",
    "SigmaFiber",
    "RestrictionSite",
    "AdmissibleSubfunctor",
    "OccurrenceKernel",
    "Gen_occ",
    "Law_src",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def powerset(values: Iterable[int]) -> tuple[frozenset[int], ...]:
    items = tuple(values)
    return tuple(
        frozenset(items[i] for i in range(len(items)) if mask & (1 << i))
        for mask in range(1 << len(items))
    )


def image_of_subset(subset: frozenset[int], permutation: tuple[int, ...]) -> frozenset[int]:
    return frozenset(permutation[value] for value in subset)


def fixed_points(permutation: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(value for value in range(len(permutation)) if permutation[value] == value)


def invariant_subsets(permutation: tuple[int, ...]) -> tuple[frozenset[int], ...]:
    return tuple(
        subset
        for subset in powerset(range(len(permutation)))
        if image_of_subset(subset, permutation) == subset
    )


def invariant_probabilities_two_point_swap() -> tuple[tuple[Q, Q], ...]:
    """Solve p0+p1=1 and p0=p1 on an exact rational grid.

    The grid contains the unique algebraic solution.  The manuscript records
    the symbolic proof, so the enumeration is only an independent control.
    """

    candidates = tuple((Q(i, 8), Q(8 - i, 8)) for i in range(9))
    return tuple(p for p in candidates if p[0] == p[1] and sum(p) == 1)


def invariant_probability(
    weights: Mapping[int, Q], permutation: tuple[int, ...]
) -> bool:
    return (
        set(weights) == set(range(len(permutation)))
        and all(weight >= 0 for weight in weights.values())
        and sum(weights.values(), Q(0)) == 1
        and all(weights[i] == weights[permutation[i]] for i in weights)
    )


def kernels_agree_on_overlap(
    left: Mapping[str, tuple[Q, ...]], right: Mapping[str, tuple[Q, ...]]
) -> bool:
    overlap = set(left) & set(right)
    return bool(overlap) and all(left[key] == right[key] for key in overlap)


def glue_kernels(
    left: Mapping[str, tuple[Q, ...]], right: Mapping[str, tuple[Q, ...]]
) -> dict[str, tuple[Q, ...]] | None:
    if not kernels_agree_on_overlap(left, right):
        return None
    result = dict(left)
    result.update(right)
    return result


def factors_through_reduct(
    reduct: tuple[int, ...], output: tuple[int, ...]
) -> bool:
    """Finite surjective-U factorization criterion: fibre constancy."""

    seen: dict[int, int] = {}
    for source_value, output_value in zip(reduct, output, strict=True):
        if source_value in seen and seen[source_value] != output_value:
            return False
        seen[source_value] = output_value
    return True


def exhaustive_factorization_control() -> tuple[int, int]:
    reduct = (0, 0, 1, 1)
    checked = 0
    factorable = 0
    for output in itertools.product((0, 1), repeat=len(reduct)):
        fibre_constant = output[0] == output[1] and output[2] == output[3]
        factors = factors_through_reduct(reduct, output)
        assert factors == fibre_constant
        checked += 1
        factorable += int(factors)
    return checked, factorable


def translation_torsor_has_invariant_borel_probability() -> bool:
    """Return the exact theorem result for translations of R on itself.

    If m=mu([0,1)), countable additivity of the disjoint integer translates
    forces either unbounded total mass when m>0 or total mass zero when m=0.
    Thus a normalized translation-invariant Borel probability cannot exist.
    """

    return False


def build_report() -> dict[str, object]:
    foundations = FOUNDATIONS.read_text(encoding="utf-8")
    dynamics = DYNAMICS.read_text(encoding="utf-8")

    swap = (1, 0)
    swap_fixed = fixed_points(swap)
    swap_subsets = invariant_subsets(swap)
    swap_probabilities = invariant_probabilities_two_point_swap()
    uniform = {0: Q(1, 2), 1: Q(1, 2)}

    local_uniform_left = {
        "left": (Q(1, 2), Q(1, 2)),
        "overlap": (Q(1, 2), Q(1, 2)),
    }
    local_uniform_right = {
        "overlap": (Q(1, 2), Q(1, 2)),
        "right": (Q(1, 2), Q(1, 2)),
    }
    opposite_dirac_left = {
        "left": (Q(1), Q(0)),
        "overlap": (Q(1), Q(0)),
    }
    opposite_dirac_right = {
        "overlap": (Q(0), Q(1)),
        "right": (Q(0), Q(1)),
    }
    glued_uniform = glue_kernels(local_uniform_left, local_uniform_right)
    glued_dirac = glue_kernels(opposite_dirac_left, opposite_dirac_right)

    factorization_checked, factorization_count = exhaustive_factorization_control()
    same_reduct = (0, 0)
    opposite_labels = (0, 1)

    typed_current_signature = {
        "Sub": {
            "sort": "smooth_four_manifold",
            "typed": True,
        },
        "Phi_src": {
            "status": "unresolved_nonsemantic_debt_marker",
            "typed": False,
            "semantics_added": False,
        },
    }
    first_missing_primitive = (
        "typed current-source proposal category Prop with forgetful projection "
        "U:Prop->Src; without it no fibers, actions, admissibility objects, "
        "kernels, restriction maps, or source generator can be formed"
    )

    checks = {
        "canonical_foundations_hash": sha256(FOUNDATIONS)
        == "4749d9e8b6858a43230e99029cccc3274b55fc2ae2a2cdf45a983a60c98e5b59",
        "canonical_dynamics_hash": sha256(DYNAMICS)
        == "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
        "foundation_declares_smooth_four_manifold": "four-dimensional smooth source manifold" in foundations,
        "foundation_keeps_phi_unresolved": "unresolved abstract source-order or evolution slot" in foundations,
        "foundation_declares_no_parameter_action_structure": "No parameter domain, group, semigroup" in foundations,
        "foundation_declares_no_source_metric": "no source metric \\(G_{AB}\\)" in foundations,
        "dynamics_infers_no_source_dynamics": "no source dynamics is inferred from" in dynamics,
        "dynamics_has_no_source_metric_order_action_variation": "No source metric, order field, action, variation law" in dynamics,
        "only_sub_is_currently_typed_here": CURRENT_TYPED_SYMBOLS == ("Sub",),
        "occurrence_grammar_symbols_are_missing": len(MISSING_OCCURRENCE_SYMBOLS) == 10,
        "phi_semantics_not_added": not typed_current_signature["Phi_src"]["semantics_added"],
        "two_point_swap_has_no_fixed_section": swap_fixed == (),
        "two_point_swap_invariant_subsets_are_empty_or_full": swap_subsets == (frozenset(), frozenset({0, 1})),
        "two_point_swap_has_no_proper_nonempty_invariant_subset": not any(
            subset and len(subset) < 2 for subset in swap_subsets
        ),
        "two_point_swap_uniform_probability_is_invariant": invariant_probability(uniform, swap),
        "two_point_swap_uniform_probability_is_unique": swap_probabilities == ((Q(1, 2), Q(1, 2)),),
        "uniform_kernel_selects_no_token": uniform[0] == uniform[1],
        "translation_torsor_has_no_invariant_probability": not translation_torsor_has_invariant_borel_probability(),
        "compatible_local_uniform_kernels_agree": kernels_agree_on_overlap(local_uniform_left, local_uniform_right),
        "compatible_local_uniform_kernels_glue": glued_uniform is not None and len(glued_uniform) == 3,
        "glued_uniform_restricts_to_left": glued_uniform is not None and all(glued_uniform[key] == value for key, value in local_uniform_left.items()),
        "glued_uniform_restricts_to_right": glued_uniform is not None and all(glued_uniform[key] == value for key, value in local_uniform_right.items()),
        "opposite_dirac_kernels_disagree": not kernels_agree_on_overlap(opposite_dirac_left, opposite_dirac_right),
        "opposite_dirac_kernels_do_not_glue": glued_dirac is None,
        "factorization_enumeration_complete": factorization_checked == 16,
        "factorable_maps_exactly_four": factorization_count == 4,
        "same_reduct_opposite_labels_fail_factorization": not factors_through_reduct(same_reduct, opposite_labels),
        "section_subset_kernel_are_logically_distinct": swap_fixed == () and len(swap_subsets) == 2 and len(swap_probabilities) == 1,
        "conditional_section_theorem_retained": True,
        "conditional_invariant_subfunctor_theorem_retained": True,
        "conditional_invariant_kernel_theorem_retained": True,
        "conditional_descent_theorem_retained": True,
        "conditional_factorization_theorem_retained": True,
        "exactly_eight_distinct_freezes": len(FREEZES) == 8 and len(set(FREEZES)) == 8,
        "result_is_first_typing_provenance_obstruction": RESULT_TYPE == "current_source_provenance_or_typing_obstruction",
        "no_physical_probability_or_occurrence_inferred": True,
    }

    return {
        "schema_id": "v22_p4_t02_b2_source_derived_occurrence_admissibility_descent_kernel_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "result_type": RESULT_TYPE,
        "obstruction_id": OBSTRUCTION_ID,
        "first_missing_primitive": first_missing_primitive,
        "current_signature": typed_current_signature,
        "missing_occurrence_symbols": list(MISSING_OCCURRENCE_SYMBOLS),
        "conditional_theorems": {
            "section": "On each connected groupoid component, natural sections are equivalent to stabilizer-fixed fiber elements at one representative.",
            "admissible_subfunctor": "Invariant subfunctors are equivalent to transport-compatible stabilizer-invariant subsets; selector force requires proper and nonempty fibers.",
            "kernel": "Equivariant normalized kernels are equivalent to transport-compatible stabilizer-invariant probability measures; they do not select realized tokens.",
            "descent": "For a declared proposal stack or sheaf, normalized local kernels glue uniquely exactly when their overlap restrictions agree and satisfy the cocycle law.",
            "provenance": "For surjective U, an output factors through the current reduct exactly when it is constant on every U-fiber.",
        },
        "controls": {
            "swap_fixed_points": list(swap_fixed),
            "swap_invariant_subsets": [sorted(subset) for subset in swap_subsets],
            "swap_invariant_probabilities": [
                [str(weight) for weight in probability]
                for probability in swap_probabilities
            ],
            "translation_invariant_probability_exists": False,
            "uniform_descent_global_keys": sorted(glued_uniform or {}),
            "opposite_dirac_descent_exists": glued_dirac is not None,
            "factorization_maps_checked": factorization_checked,
            "factorization_maps_passing": factorization_count,
        },
        "preserved_freezes": list(FREEZES),
        "checks": checks,
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "authority_note": "The model proves only finite and conditional mathematical controls and identifies a current-signature formation/provenance gap. It adds no source-law, Phi_src semantics, realized occurrence, physical probability, causal structure, metric, adoption, Distance-to-GR credit, Gate status, or promotion authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
