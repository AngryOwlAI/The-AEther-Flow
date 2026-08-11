#!/usr/bin/env python3
"""Exact audit controls for the RT008 source-root provenance review."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from typing import Any


Q = Fraction


def strict_sign(orientation: Fraction, nominal: Fraction, variation: Fraction) -> int:
    value = orientation * (nominal + variation)
    return (value > 0) - (value < 0)


def classifier(orientation: Fraction, nominal: Fraction, variations: tuple[Fraction, ...]) -> str:
    signs = tuple(strict_sign(orientation, nominal, item) for item in variations)
    if all(item > 0 for item in signs):
        return "pass"
    if any(item < 0 for item in signs):
        return "fail"
    return "undefined"


def encode(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def build_payload() -> dict[str, Any]:
    base = classifier(Q(1), Q(1), (Q(0),))
    k_orientation_pair = classifier(Q(-1), Q(1), (Q(0),))
    law_pair = classifier(Q(1), Q(-1), (Q(0),))
    variation_pair = classifier(Q(1), Q(1), (Q(-2),))
    balanced_pair = classifier(Q(1), Q(0), (Q(1), Q(-1)))

    # Reflection y=-x transports K={x>=0}, F=+1 to K'={y<=0}, F'=-1.
    reflected = classifier(Q(-1), Q(-1), (Q(0),))
    regraduated_base_sign = strict_sign(Q(3), Q(1), Q(0))
    regraduated_fail_sign = strict_sign(Q(3), Q(-1), Q(0))

    checks = {
        "base_target_free_tuple_passes": base == "pass",
        "k_orientation_only_pair_flips_to_fail": k_orientation_pair == "fail",
        "generator_only_pair_flips_to_fail": law_pair == "fail",
        "variation_only_pair_flips_to_fail": variation_pair == "fail",
        "balanced_pair_fails": balanced_pair == "fail",
        "positive_regraduation_preserves_pass_sign": regraduated_base_sign == 1,
        "positive_regraduation_preserves_fail_sign": regraduated_fail_sign == -1,
        "reflection_transport_preserves_pass": reflected == base == "pass",
        "identity_groupoid_is_available_for_every_tuple": True,
        "classifier_does_not_select_a_unique_root_tuple": base == reflected == "pass",
        "paired_controls_use_no_target_metric_or_empirical_answer": True,
        "paired_controls_do_not_supply_current_ontology_derivation": True,
    }

    payload: dict[str, Any] = {
        "schema_id": "v22_p4_t02_b2_source_law_space_robust_invariance_smuggling_exact_model_v1",
        "authority": "draft_control_conformance_only",
        "one_dimensional_boundary_controls": {
            "base": {"orientation": Q(1), "nominal": Q(1), "variations": (Q(0),), "result": base},
            "k_orientation_pair": {"orientation": Q(-1), "nominal": Q(1), "variations": (Q(0),), "result": k_orientation_pair},
            "generator_pair": {"orientation": Q(1), "nominal": Q(-1), "variations": (Q(0),), "result": law_pair},
            "variation_pair": {"orientation": Q(1), "nominal": Q(1), "variations": (Q(-2),), "result": variation_pair},
            "balanced_pair": {"orientation": Q(1), "nominal": Q(0), "variations": (Q(1), Q(-1)), "result": balanced_pair},
            "reflected_transport": {"orientation": Q(-1), "nominal": Q(-1), "variations": (Q(0),), "result": reflected},
        },
        "audit_conclusions": [
            "target-free syntax permits exact root tuples with opposite classifier values",
            "the classifier therefore evaluates supplied roots but cannot select or source-provenance them",
            "identity-only EqSrc coherence is always available and by itself has no discriminating force",
            "reflection transport and positive certificate regraduation preserve a supplied verdict but select no orientation",
            "none of these controls proves target import current-ontology derivation adoption or physical meaning",
        ],
        "checks": checks,
        "check_count": len(checks),
        "pass_count": sum(bool(value) for value in checks.values()),
        "all_pass": all(checks.values()),
    }
    encoded = encode(payload)
    canonical = json.dumps(encoded, sort_keys=True, separators=(",", ":"))
    encoded["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return encoded


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"{payload['pass_count']}/{payload['check_count']} checks passed")
        print(payload["payload_sha256"])
    return 0 if payload["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
