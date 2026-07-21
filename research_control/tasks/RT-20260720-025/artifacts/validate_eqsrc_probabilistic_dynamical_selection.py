#!/usr/bin/env python3
"""Validate the exact finite P3-T04 probability and dynamics controls."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


HERE = Path(__file__).resolve().parent
SPEC_PATH = HERE / "eqsrc_probabilistic_dynamical_selection_spec_v1.yaml"
CONTROLS_PATH = HERE / "eqsrc_probabilistic_dynamical_selection_finite_controls_v1.json"
MATH_CHILD_PATH = HERE / "child_phys_math_eqsrc_probabilistic_dynamical_selection.yaml"
PHIL_CHILD_PATH = HERE / "child_phys_phil_eqsrc_probabilistic_dynamical_selection.yaml"
CONFLICT_PATH = HERE / "parent_conflict_review_eqsrc_probabilistic_dynamical_selection.yaml"
FUSION_PATH = HERE / "parent_fusion_notes_eqsrc_probabilistic_dynamical_selection.md"
THEOREM_PATH = HERE / "eqsrc_probabilistic_dynamical_selection_theorem_v1.tex"
REPORT_PATH = HERE / "eqsrc_probabilistic_dynamical_selection_validation.json"

EXPECTED_CASE_IDS = [
    "C1_C2_TRANSITIVE_SWAP",
    "C2_C3_REGULAR_CYCLE",
    "C3_C2_SWAP_PLUS_FIXED_POINT",
    "C4_C2_TWO_DISJOINT_SWAPS",
    "C5_TRIVIAL_ACTION_THREE_POINTS",
    "C6_EQUIVARIANT_TWO_BASIN_DYNAMICS",
    "C7_EQUIVARIANT_ERGODIC_MARKOV_CHAIN",
    "C8_ASYMMETRIC_DYNAMICS_SELECTS_A",
]

EXPECTED_THEOREM_IDS = {
    "PM1_ORBIT_SIMPLEX_CLASSIFICATION",
    "PM2_INVARIANT_DIRAC_FIXED_POINT",
    "PM3_NO_FREE_MEASURE_DECODER",
    "DM1_EQUIVARIANT_MARKOV_SYMMETRY_PRESERVATION",
    "DM2_UNIQUE_STATIONARY_LAW_GUARD",
    "DM3_GLOBAL_ATTRACTOR_FIXED_POINT",
    "DM4_SAMPLE_HISTORY_PROVENANCE",
}


def fraction(value: Any) -> Fraction:
    return Fraction(str(value))


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain a mapping")
    return data


def distribution(states: list[str], raw: dict[str, Any]) -> dict[str, Fraction]:
    if set(raw) != set(states):
        raise ValueError("distribution support does not equal the declared state set")
    result = {state: fraction(raw[state]) for state in states}
    if any(value < 0 for value in result.values()):
        raise ValueError("distribution contains a negative weight")
    if sum(result.values(), Fraction(0)) != 1:
        raise ValueError("distribution is not normalized")
    return result


def pushforward(
    states: list[str], law: dict[str, Fraction], permutation: dict[str, str]
) -> dict[str, Fraction]:
    result = {state: Fraction(0) for state in states}
    for state in states:
        result[permutation[state]] += law[state]
    return result


def is_invariant(
    states: list[str], law: dict[str, Fraction], permutations: list[dict[str, str]]
) -> bool:
    return all(pushforward(states, law, permutation) == law for permutation in permutations)


def normalize_partition(states: list[str], parts: list[list[str]]) -> list[list[str]]:
    order = {state: index for index, state in enumerate(states)}
    normalized = [sorted(part, key=order.__getitem__) for part in parts]
    return sorted(normalized, key=lambda part: order[part[0]])


def compute_orbits(states: list[str], permutations: list[dict[str, str]]) -> list[list[str]]:
    remaining = set(states)
    parts: list[list[str]] = []
    while remaining:
        seed = next(state for state in states if state in remaining)
        orbit = {permutation[seed] for permutation in permutations}
        parts.append(list(orbit))
        remaining -= orbit
    return normalize_partition(states, parts)


def check_group(states: list[str], permutations: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    state_set = set(states)
    encoded: set[tuple[str, ...]] = set()
    for index, permutation in enumerate(permutations):
        if set(permutation) != state_set or set(permutation.values()) != state_set:
            errors.append(f"group element {index} is not a permutation of the carrier")
        encoded.add(tuple(permutation.get(state, "") for state in states))
    identity = tuple(states)
    if identity not in encoded:
        errors.append("group action omits the identity permutation")
    for left in permutations:
        for right in permutations:
            composed = tuple(left[right[state]] for state in states)
            if composed not in encoded:
                errors.append("listed action permutations are not closed under composition")
                return errors
    return errors


def transition_matrix(
    states: list[str], dynamics: dict[str, Any]
) -> tuple[dict[str, dict[str, Fraction]], dict[str, str] | None]:
    if dynamics["kind"] == "deterministic":
        mapping = dynamics["map"]
        if set(mapping) != set(states) or not set(mapping.values()) <= set(states):
            raise ValueError("deterministic dynamics is not an endomap")
        matrix = {
            source: {
                target: Fraction(int(mapping[source] == target)) for target in states
            }
            for source in states
        }
        return matrix, mapping
    if dynamics["kind"] != "markov":
        raise ValueError("unknown dynamics kind")
    raw_matrix = dynamics["matrix"]
    if set(raw_matrix) != set(states):
        raise ValueError("Markov matrix row support is incomplete")
    matrix: dict[str, dict[str, Fraction]] = {}
    for source in states:
        if set(raw_matrix[source]) != set(states):
            raise ValueError("Markov matrix column support is incomplete")
        row = {target: fraction(raw_matrix[source][target]) for target in states}
        if any(value < 0 for value in row.values()) or sum(row.values(), Fraction(0)) != 1:
            raise ValueError("Markov matrix row is not stochastic")
        matrix[source] = row
    return matrix, None


def matrix_equivariant(
    states: list[str],
    matrix: dict[str, dict[str, Fraction]],
    permutations: list[dict[str, str]],
) -> bool:
    for permutation in permutations:
        for source in states:
            for target in states:
                if matrix[permutation[source]][permutation[target]] != matrix[source][target]:
                    return False
    return True


def evolve(
    states: list[str],
    law: dict[str, Fraction],
    matrix: dict[str, dict[str, Fraction]],
) -> dict[str, Fraction]:
    return {
        target: sum(
            (law[source] * matrix[source][target] for source in states), Fraction(0)
        )
        for target in states
    }


def closed_communicating_classes(
    states: list[str], matrix: dict[str, dict[str, Fraction]]
) -> list[list[str]]:
    reach: dict[str, set[str]] = {
        source: {target for target in states if matrix[source][target] > 0}
        for source in states
    }
    for state in states:
        reach[state].add(state)
    changed = True
    while changed:
        changed = False
        for source in states:
            expanded = set(reach[source])
            for middle in list(reach[source]):
                expanded |= reach[middle]
            if expanded != reach[source]:
                reach[source] = expanded
                changed = True
    remaining = set(states)
    classes: list[list[str]] = []
    while remaining:
        seed = next(state for state in states if state in remaining)
        component = {state for state in states if state in reach[seed] and seed in reach[state]}
        remaining -= component
        classes.append([state for state in states if state in component])
    return [
        component
        for component in classes
        if all(
            matrix[source][target] == 0
            for source in component
            for target in states
            if target not in component
        )
    ]


def unique_global_point_attractor(states: list[str], mapping: dict[str, str]) -> str | None:
    fixed = [state for state in states if mapping[state] == state]
    global_attractors: list[str] = []
    for candidate in fixed:
        attracts_all = True
        for start in states:
            current = start
            for _ in range(len(states) + 1):
                if current == candidate:
                    break
                current = mapping[current]
            else:
                attracts_all = False
            if current != candidate:
                attracts_all = False
        if attracts_all:
            global_attractors.append(candidate)
    return global_attractors[0] if len(global_attractors) == 1 else None


def verify_case(case: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    states = case["states"]
    permutations = [element["permutation"] for element in case["group"]]
    errors.extend(check_group(states, permutations))

    orbits = compute_orbits(states, permutations)
    expected_orbits = normalize_partition(states, case["expected_orbits"])
    if orbits != expected_orbits:
        errors.append(f"orbit mismatch: computed {orbits} expected {expected_orbits}")

    fixed_points = [
        state for state in states if all(permutation[state] == state for permutation in permutations)
    ]
    if fixed_points != case["expected_fixed_points"]:
        errors.append("fixed-locus mismatch")

    dimension = len(orbits) - 1
    if dimension != case["expected_invariant_simplex_dimension"]:
        errors.append("invariant-simplex dimension mismatch")
    unique_invariant = len(orbits) == 1
    if unique_invariant != case["expected_unique_invariant_measure"]:
        errors.append("unique invariant-law classification mismatch")

    expected_extremes = [distribution(states, raw) for raw in case["expected_orbit_uniform_extremes"]]
    computed_extremes = []
    for orbit in orbits:
        computed_extremes.append(
            {
                state: Fraction(1, len(orbit)) if state in orbit else Fraction(0)
                for state in states
            }
        )
    if computed_extremes != expected_extremes:
        errors.append("orbit-uniform extreme point mismatch")
    if not all(is_invariant(states, law, permutations) for law in computed_extremes):
        errors.append("computed orbit-uniform law is not invariant")

    dynamics = case["dynamics"]
    matrix, mapping = transition_matrix(states, dynamics)
    equivariant = matrix_equivariant(states, matrix, permutations)
    if equivariant != dynamics["expected_equivariant"]:
        errors.append("dynamics equivariance mismatch")

    closed_classes = closed_communicating_classes(states, matrix)
    if len(closed_classes) != dynamics["expected_closed_class_count"]:
        errors.append("closed communicating-class count mismatch")
    unique_stationary = len(closed_classes) == 1
    if unique_stationary != dynamics["expected_unique_stationary_law"]:
        errors.append("unique stationary-law classification mismatch")

    for raw_stationary in dynamics.get("stationary_laws", []):
        law = distribution(states, raw_stationary)
        if evolve(states, law, matrix) != law:
            errors.append("declared stationary law is not stationary")

    attractor = None
    if mapping is not None:
        attractor = unique_global_point_attractor(states, mapping)
        if attractor != dynamics["expected_unique_global_point_attractor"]:
            errors.append("unique global point-attractor mismatch")
        if equivariant and attractor is not None and attractor not in fixed_points:
            errors.append("equivariant unique global attractor is not structurally fixed")

    initial = case["initial_law"]
    initial_law = distribution(states, initial["weights"])
    initial_invariant = is_invariant(states, initial_law, permutations)
    if initial_invariant != initial["expected_invariant"]:
        errors.append("initial-law invariance mismatch")
    next_law = evolve(states, initial_law, matrix)
    expected_next = distribution(states, initial["expected_next"])
    if next_law != expected_next:
        errors.append("one-step law mismatch")
    if equivariant and initial_invariant and not is_invariant(states, next_law, permutations):
        errors.append("equivariant dynamics failed to preserve an invariant law")

    summary = {
        "case_id": case["case_id"],
        "state_count": len(states),
        "group_element_count": len(permutations),
        "orbit_count": len(orbits),
        "fixed_point_count": len(fixed_points),
        "invariant_simplex_dimension": dimension,
        "unique_invariant_measure": unique_invariant,
        "dynamics_equivariant": equivariant,
        "closed_class_count": len(closed_classes),
        "unique_stationary_law": unique_stationary,
        "unique_global_point_attractor": attractor,
        "initial_law_invariant": initial_invariant,
    }
    return summary, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, detail: Any) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    spec = load_yaml(SPEC_PATH)
    controls = json.loads(CONTROLS_PATH.read_text(encoding="utf-8"))
    math_child = load_yaml(MATH_CHILD_PATH)
    phil_child = load_yaml(PHIL_CHILD_PATH)
    conflict = load_yaml(CONFLICT_PATH)
    theorem_text = THEOREM_PATH.read_text(encoding="utf-8")
    fusion_text = FUSION_PATH.read_text(encoding="utf-8")

    add_check("spec_status", spec.get("status") == "draft/control" and spec.get("adoption_status") == "proposal-only", spec.get("status"))
    theorem_ids = {entry["theorem_id"] for entry in spec.get("theorem_contracts", [])}
    add_check("theorem_contract_inventory", theorem_ids == EXPECTED_THEOREM_IDS, sorted(theorem_ids))
    flags = spec.get("authority_flags", {})
    add_check("spec_authority_flags", bool(flags) and all(value is False for value in flags.values()), flags)
    add_check(
        "child_outputs",
        math_child.get("status") == "completed"
        and math_child.get("execution_unit_id") == "child_phys_math"
        and phil_child.get("status") == "completed"
        and phil_child.get("execution_unit_id") == "child_phys_phil",
        [math_child.get("execution_unit_id"), phil_child.get("execution_unit_id")],
    )
    add_check(
        "parent_conflict_resolution",
        conflict.get("status") == "resolved"
        and conflict.get("resolved_conflict_count") == 8
        and conflict.get("unresolved_conflicts") == [],
        {"resolved": conflict.get("resolved_conflict_count"), "unresolved": conflict.get("unresolved_conflicts")},
    )
    add_check(
        "parent_fusion",
        all(token in fusion_text for token in ["orbit-simplex", "provenance ledger", "P3-T05 may become", "not executed"]),
        "shared consensus and unique contributions preserved",
    )

    cases = controls.get("cases", [])
    case_ids = [case.get("case_id") for case in cases]
    add_check("finite_control_inventory", case_ids == EXPECTED_CASE_IDS, case_ids)
    case_summaries: list[dict[str, Any]] = []
    for case in cases:
        try:
            summary, errors = verify_case(case)
        except Exception as exc:  # precise case failure is retained in the report
            summary = {"case_id": case.get("case_id")}
            errors = [f"{type(exc).__name__}: {exc}"]
        case_summaries.append(summary)
        add_check(f"finite_control_{case.get('case_id')}", not errors, errors or summary)

    controls_flags = controls.get("authority_flags", {})
    add_check("controls_authority_flags", bool(controls_flags) and all(value is False for value in controls_flags.values()), controls_flags)
    add_check(
        "no_free_measure_positive_controls",
        case_summaries[0].get("unique_invariant_measure") is True
        and case_summaries[0].get("fixed_point_count") == 0
        and case_summaries[1].get("unique_stationary_law") is True
        and case_summaries[1].get("fixed_point_count") == 0,
        "C1 and C2 separate law uniqueness from point selection",
    )
    add_check(
        "fixed_attractor_guard",
        case_summaries[2].get("unique_global_point_attractor") == "c"
        and case_summaries[2].get("fixed_point_count") == 1,
        "C3 selects only the already-fixed point c",
    )
    add_check(
        "symmetric_dynamics_guard",
        case_summaries[5].get("dynamics_equivariant") is True
        and case_summaries[5].get("initial_law_invariant") is True
        and case_summaries[5].get("unique_global_point_attractor") is None,
        "C6 preserves a symmetric branch mixture",
    )
    add_check(
        "asymmetric_dynamics_provenance",
        case_summaries[7].get("dynamics_equivariant") is False
        and case_summaries[7].get("unique_global_point_attractor") == "a",
        "C8 selection is purchased by a non-equivariant law",
    )

    required_theorem_tokens = [
        "Orbit-simplex classification",
        "No-free-measure decoder",
        "Equivariant Markov preservation",
        "Unique stationary-law guard",
        "Unique global point attractor",
        "blocked while continuation is open",
        "P3-T05 is not",
    ]
    add_check("theorem_text_contract", all(token in theorem_text for token in required_theorem_tokens), required_theorem_tokens)
    forbidden_overreads = [
        "source law is adopted",
        "general EqSrc is discharged",
        "physical gauge is established",
        "completed derivation",
    ]
    add_check("forbidden_overread_absence", not any(token in theorem_text for token in forbidden_overreads), forbidden_overreads)

    failed = [check for check in checks if check["status"] != "PASS"]
    report = {
        "schema_id": "eqsrc_probabilistic_dynamical_selection_validation_v1",
        "task_id": "RT-20260720-025",
        "job_id": "AJ-RT-20260720-025-001",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "validation_status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "finite_case_count": len(cases),
        "case_summaries": case_summaries,
        "checks": checks,
        "authority_summary": {
            "source_law_adopted": False,
            "canonical_point_selected": False,
            "effective_gr_dynamics_used_as_substrate_law": False,
            "general_eqsrc_discharged": False,
            "distance_to_gr_delta_changed": False,
            "physics_promotion_authorized": False,
        },
    }
    if args.write_report:
        REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['validation_status']}: {len(checks)} checks; {len(failed)} failed")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
