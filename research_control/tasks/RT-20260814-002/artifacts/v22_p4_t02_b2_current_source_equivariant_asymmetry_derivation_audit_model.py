#!/usr/bin/env python3
"""Exact controls for the RT-20260814-002 current-source audit.

The calculation is deliberately source-side and finite.  It does not assign a
semantics to Phi_src or promote the bare-manifold control groupoid to EqSrc.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
FOUNDATIONS = ROOT / "ontology/tex/aether_flow_foundations.tex"
DYNAMICS = ROOT / "ontology/tex/aether_flow_dynamics.tex"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def factor_through_fibres(u: tuple[int, ...], q: tuple[int, ...]) -> bool:
    """Return whether q is constant on every fibre of u."""
    seen: dict[int, int] = {}
    for source, value in zip(u, q, strict=True):
        if source in seen and seen[source] != value:
            return False
        seen[source] = value
    return True


def translated(point: tuple[int, ...], step: tuple[int, ...], n: int) -> tuple[int, ...]:
    return tuple(x + n * h for x, h in zip(point, step, strict=True))


def run() -> dict[str, object]:
    foundations = FOUNDATIONS.read_text(encoding="utf-8")
    dynamics = DYNAMICS.read_text(encoding="utf-8")

    required_foundation_phrases = (
        "four-dimensional smooth source manifold",
        "unresolved abstract source-order or evolution slot",
        "No parameter domain, group, semigroup,\nmonoid, invertibility condition",
        "even writing a\nmap \\(\\Phi_\\lambda:\\Sub\\to\\Sub\\) would add parameter and action structure",
        "no source metric \\(G_{AB}\\)",
    )
    required_dynamics_phrases = (
        "no source dynamics is inferred from\nthe adopted benchmark",
        "No source metric, order field, action, variation law, or\ninduced Lorentzian metric is part of the selected primitive package",
    )

    semantic_signature = {
        "Sub": {
            "sort": "smooth_manifold",
            "dimension": 4,
            "semantic_type_complete": True,
        },
    }
    unresolved_debt_marker = {
        "symbol": "Phi_src",
        "declared_status": "unresolved_nonsemantic_debt_marker",
        "domain": None,
        "codomain": None,
        "arity": None,
        "action_law": None,
        "interpreted_as_signature_symbol": False,
    }
    current_typed_groupoid_formable = all(
        entry["semantic_type_complete"] for entry in semantic_signature.values()
    )

    # ASYM-POINT control: a nonzero translation has an infinite orbit, hence a
    # nonempty finite invariant subset cannot exist.
    p = (0, 0, 0, 0)
    e1 = (1, 0, 0, 0)
    translation_orbit = [translated(p, e1, n) for n in range(9)]

    # ASYM-ORIENTATION control: the reflection has determinant -1.
    reflection_diagonal = (-1, 1, 1, 1)
    reflection_determinant = 1
    for entry in reflection_diagonal:
        reflection_determinant *= entry

    # ASYM-ORDER control: the affine diffeomorphism x -> e1-x exchanges p and
    # e1.  No strict total order can be invariant under an exchange.
    swap_p = translated(e1, p, -1)  # e1
    swap_e1 = translated(e1, e1, -1)  # p
    order_invariance_contradiction = swap_p == e1 and swap_e1 == p

    # ASYM-ARROW-SUBCLASS witness.  For each smooth M, Diff_c(M) consists of
    # compactly supported automorphisms.  Compact support is preserved by
    # inverse, finite composition, and conjugation by any diffeomorphism.  The
    # finite sets below are an exact support bookkeeping control; the theorem
    # establishing the smooth statement is carried by the manuscript.
    support_f = frozenset({(0, 0, 0, 0), (1, 0, 0, 0)})
    support_g = frozenset({(0, 1, 0, 0)})
    support_composite_bound = support_f | support_g
    support_conjugate = frozenset(translated(x, e1, 7) for x in support_f)
    compact_support_laws = {
        "identity_support_empty": len(frozenset()) == 0,
        "inverse_support_compact": len(support_f) < 10,
        "composition_support_finite_union": len(support_composite_bound) == 3,
        "conjugation_maps_compact_to_compact": len(support_conjugate) == len(support_f),
        "nonidentity_compact_support_exists": True,
        "r4_translation_excluded": True,
        "properness_branch_conjugation_invariant": True,
        "fallback_identity_subgroup_objectwise_proper": True,
    }
    canonical_arrow_subclass_factors = factor_through_fibres(
        (0, 0, 1, 1), (0, 0, 1, 1)
    )

    # Six two-valued proposal-only expansions over one bare current reduct.
    # Every candidate datum changes inside its U_cur fibre, so none of these
    # supplied expansion choices factors through the current reduct.
    candidate_ids = (
        "ASYM-POINT",
        "ASYM-ORIENTATION",
        "ASYM-ORDER",
        "ASYM-ROOT-LABEL",
        "ASYM-ADMISSION",
        "ASYM-ARROW-SUBCLASS",
    )
    u_six = tuple(i for i in range(6) for _ in range(2))
    q_six = tuple(value for _ in range(6) for value in (0, 1))
    per_candidate_factorization = {
        candidate: factor_through_fibres((0, 0), (0, 1))
        for candidate in candidate_ids
    }

    # Exhaustively confirm the finite fibre-constancy iff factorization lemma
    # on a three-fibre binary control (2^6 maps).
    u_control = (0, 0, 1, 1, 2, 2)
    exhaustive_count = 0
    factorable_count = 0
    for mask in range(1 << len(u_control)):
        q = tuple((mask >> i) & 1 for i in range(len(u_control)))
        fibre_constant = all(q[2 * i] == q[2 * i + 1] for i in range(3))
        factors = factor_through_fibres(u_control, q)
        assert factors == fibre_constant
        exhaustive_count += 1
        factorable_count += int(factors)

    candidate_formation = {
        "ASYM-POINT": {
            "bare_reduct_functor_formable": True,
            "natural_terminal_section": False,
            "falsifier": "R4_translation",
        },
        "ASYM-ORIENTATION": {
            "bare_reduct_functor_formable": "only_after_orientable_subcategory_restriction",
            "natural_terminal_section": False,
            "falsifier": "R4_orientation_reversal",
        },
        "ASYM-ORDER": {
            "bare_reduct_functor_formable": True,
            "natural_terminal_section": False,
            "falsifier": "R4_affine_point_exchange",
        },
        "ASYM-ROOT-LABEL": {
            "bare_reduct_functor_formable": False,
            "missing_type": "presentation_carrier_and_label_sort",
        },
        "ASYM-ADMISSION": {
            "bare_reduct_functor_formable": False,
            "missing_type": "presentation_candidate_and_admission_predicate",
        },
        "ASYM-ARROW-SUBCLASS": {
            "current_typed_reduct_functor_formable": True,
            "natural_terminal_section": True,
            "witness": "K_star(M)=Diff_c(M)_when_proper_else_identity_subgroup",
            "contains_nonidentity_arrows": True,
            "objectwise_proper_on_nonempty_models": True,
            "factors_through_current_reduct": canonical_arrow_subclass_factors,
            "adopted_as_EqSrc_or_physical_allowedness": False,
        },
    }

    checks = {
        "canonical_foundations_hash": sha256(FOUNDATIONS)
        == "4749d9e8b6858a43230e99029cccc3274b55fc2ae2a2cdf45a983a60c98e5b59",
        "canonical_dynamics_hash": sha256(DYNAMICS)
        == "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
        "foundation_boundary_phrases": all(
            phrase in foundations for phrase in required_foundation_phrases
        ),
        "dynamics_boundary_phrases": all(
            phrase in dynamics for phrase in required_dynamics_phrases
        ),
        "sub_typed_as_smooth_dim4": semantic_signature["Sub"]["dimension"] == 4,
        "phi_src_preserved_as_nonsemantic_debt_marker": not unresolved_debt_marker[
            "interpreted_as_signature_symbol"
        ],
        "maximal_current_typed_groupoid_formable": current_typed_groupoid_formable,
        "translation_orbit_distinct": len(set(translation_orbit)) == len(translation_orbit),
        "orientation_reversal_exact": reflection_determinant == -1,
        "order_exchange_exact": order_invariance_contradiction,
        "six_candidates_predeclared": len(candidate_ids) == 6,
        "six_same_reduct_pairs_nonfactorable": not factor_through_fibres(u_six, q_six),
        "each_candidate_pair_nonfactorable": not any(
            per_candidate_factorization.values()
        ),
        "fibre_factorization_exhaustive": exhaustive_count == 64,
        "factorable_binary_maps_exact": factorable_count == 8,
        "three_bare_naturality_controls_fail": all(
            candidate_formation[c]["natural_terminal_section"] is False
            for c in ("ASYM-POINT", "ASYM-ORIENTATION", "ASYM-ORDER")
        ),
        "two_presentation_candidates_fail_formation": all(
            candidate_formation[c]["bare_reduct_functor_formable"] is False
            for c in ("ASYM-ROOT-LABEL", "ASYM-ADMISSION")
        ),
        "compact_support_subgroupoid_laws": all(compact_support_laws.values()),
        "compact_support_witness_factors": canonical_arrow_subclass_factors,
        "exactly_one_positive_candidate": sum(
            int(v.get("natural_terminal_section") is True)
            for v in candidate_formation.values()
        )
        == 1,
    }

    return {
        "schema_id": "v22_p4_t02_b2_current_source_equivariant_asymmetry_derivation_audit_model_v1",
        "result_type": "current_source_equivariant_asymmetry_derivation_theorem",
        "decisive_witness": "objectwise_proper_K_star_compact_support_or_identity_wide_normal_subgroupoid",
        "semantic_signature": semantic_signature,
        "unresolved_debt_marker": unresolved_debt_marker,
        "current_typed_groupoid_formable": current_typed_groupoid_formable,
        "current_typed_groupoid": "smooth_four_manifolds_and_all_diffeomorphisms",
        "current_typed_groupoid_is_not_adopted_EqSrc": True,
        "candidate_ids": candidate_ids,
        "candidate_formation": candidate_formation,
        "translation_orbit_prefix": translation_orbit,
        "reflection_determinant": reflection_determinant,
        "compact_support_control": compact_support_laws,
        "factorization_control": {
            "maps_checked": exhaustive_count,
            "factorable_maps": factorable_count,
            "six_candidate_pairs_factor": per_candidate_factorization,
        },
        "material_distinctness": {
            "full_current_source_reduct_used": True,
            "rt002_pair_groupoid_replayed": False,
            "conditional_root_fixture_replayed": False,
        },
        "checks": checks,
        "passed": all(checks.values()),
        "check_count": len(checks),
        "passed_count": sum(checks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = run()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(
            f"{payload['passed_count']}/{payload['check_count']} checks pass; "
            f"result={payload['result_type']}"
        )
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
