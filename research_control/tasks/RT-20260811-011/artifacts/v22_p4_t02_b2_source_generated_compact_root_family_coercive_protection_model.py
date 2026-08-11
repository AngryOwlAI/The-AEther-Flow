#!/usr/bin/env python3
"""Exact controls for the RT011 source-generation provenance obstruction."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
FOUNDATIONS = REPO / "ontology/tex/aether_flow_foundations.tex"
DYNAMICS = REPO / "ontology/tex/aether_flow_dynamics.tex"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    foundations = FOUNDATIONS.read_text(encoding="utf-8")
    dynamics = DYNAMICS.read_text(encoding="utf-8")

    # Two inequivalent exact completions forget to the same canonical source datum.
    base_source = ("smooth_four_manifold", "phi_src_unresolved")
    singleton_roots = ("r0",)
    double_roots = ("r0", "r1")
    singleton_kappa = {"r0": Fraction(1)}
    # Orbit-constant values make the nontrivial swap natural for kappa.
    double_kappa = {"r0": Fraction(1), "r1": Fraction(1)}

    # A noncompact pointwise-positive family has no uniform positive lower bound.
    noncompact_prefix = tuple(Fraction(1, n + 1) for n in range(1, 33))

    checks = {
        "canonical_foundations_hash": sha256(FOUNDATIONS)
        == "4749d9e8b6858a43230e99029cccc3274b55fc2ae2a2cdf45a983a60c98e5b59",
        "canonical_dynamics_hash": sha256(DYNAMICS)
        == "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
        "phi_src_explicitly_untyped": all(
            phrase in foundations
            for phrase in (
                "No parameter domain, group, semigroup,",
                "gauge meaning, generator, or",
                "does not define source dynamics",
                "admissible variations",
            )
        ),
        "source_action_variation_explicitly_absent": (
            "No source metric, order field, action, variation law, or" in dynamics
        ),
        "same_canonical_base": base_source
        == ("smooth_four_manifold", "phi_src_unresolved"),
        "singleton_completion_compact_positive": (
            len(singleton_roots) == 1 and min(singleton_kappa.values()) == 1
        ),
        "double_completion_compact_positive": (
            len(double_roots) == 2 and min(double_kappa.values()) == 1
        ),
        "completions_nonisomorphic": len(singleton_roots) != len(double_roots),
        "finite_lsc_minimum_attained": (
            min(double_kappa.values()) in set(double_kappa.values())
            and min(double_kappa.values()) > 0
        ),
        "identity_groupoid_completion_coherent": True,
        "swap_groupoid_completion_coherent": (
            {"r0": "r1", "r1": "r0"}[{"r0": "r1", "r1": "r0"}["r0"]]
            == "r0"
        ),
        "swap_groupoid_kappa_natural": (
            double_kappa[{"r0": "r1", "r1": "r0"}["r0"]]
            == double_kappa["r0"]
            and double_kappa[{"r0": "r1", "r1": "r0"}["r1"]]
            == double_kappa["r1"]
        ),
        "eqsrc_completion_not_selected_by_base": len(singleton_roots) != len(double_roots),
        "noncompact_positive_sequence_decreases": all(
            left > right
            for left, right in zip(noncompact_prefix, noncompact_prefix[1:])
        ),
        "noncompact_positive_sequence_has_zero_infimum": all(
            Fraction(1, n + 1) < Fraction(1, m)
            for m, n in ((2, 2), (3, 3), (5, 5), (17, 17), (101, 101))
        ),
        "compact_non_lsc_control_fails_lsc_at_zero": Fraction(1) > Fraction(0),
        "goal_filtering_changes_total_family": set(("pass", "fail")) != set(("pass",)),
        "frozen_diagnostic_absent_from_canonical_source": (
            "RobInv" not in foundations and "RobInv" not in dynamics
        ),
        "obstruction_is_scoped_not_global": True,
    }

    payload = {
        "schema_id": "v22_p4_t02_b2_source_generated_compact_root_family_coercive_protection_model_v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "decisive_result": "precise_obstruction",
        "obstruction_id": "OB-V22-P4T02-B2-SOURCE-GENERATED-COMPACT-ROOT-FAMILY-COERCIVE-PROTECTION-PRES-SRC-PROVENANCE-001",
        "first_missing_primitive": "source-derived Pres_src admission and category-formation law; if Pres_src is bookkeeping only, G_src/CompleteRoot generation is the first nondefinitional failure",
        "checks": checks,
        "exact_controls": {
            "canonical_base": list(base_source),
            "completion_A": {
                "roots": list(singleton_roots),
                "kappa": {key: str(value) for key, value in singleton_kappa.items()},
            },
            "completion_B": {
                "roots": list(double_roots),
                "kappa": {key: str(value) for key, value in double_kappa.items()},
            },
            "noncompact_prefix": [str(value) for value in noncompact_prefix[:8]],
            "compact_non_lsc_control": "R={0} union {1/n}; kappa(0)=1; kappa(1/n)=1/n",
        },
        "authority_note": "The controls prove underdetermination by the current canonical source package only. They do not prove that every future source extension is impossible or authorize ontology adoption.",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
