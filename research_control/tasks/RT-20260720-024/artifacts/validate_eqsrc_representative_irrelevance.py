#!/usr/bin/env python3
"""Validate the bounded v21 P3-T03 representative-irrelevance packet.

PASS establishes task-local finite orbit calculations and internal contract
consistency only. It is not ontology, physical-gauge, general EqSrc,
operational-observable, promotion, or publication authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ARTIFACTS = Path(__file__).resolve().parent
ROOT = ARTIFACTS.parents[3]
REPORT = ARTIFACTS / "eqsrc_representative_irrelevance_validation.json"
ARTIFACT_ID = "EQSRC-REPRESENTATIVE-IRRELEVANCE-THEOREM-V1"
EXPECTED_CASE_IDS = (
    "RI-C1-ORIENTATION-TORSOR",
    "RI-C2-CYCLE-ROOT",
    "RI-C3-THREE-LINE",
    "RI-C4-ORDERED-PARTITION",
    "RI-C5-GRADED-ORBIT-PHASE",
    "RI-C6-MULTI-ORBIT-REPRESENTATIVE",
)
EXPECTED_SOURCES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/design/gr_derivation_burden_map.md": "6d1df3488be163b72296cf34ee07b979e29b061d508e6a4c271ac3305373aa1f",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61",
    "ontology/tex/aether_flow_foundations.tex": "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2",
    "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex": "d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae",
    "research_control/tasks/RT-20260720-022/artifacts/eqsrc_selector_resolution_taxonomy_v1.tex": "4af38c29cc97729cbd4278e5174b4ff3cc76d7921dbf148f953e92c9a3f03d30",
    "research_control/tasks/RT-20260720-023/artifacts/eqsrc_source_extension_lattice_v1.tex": "b0f539b7a1d53f9cafb93151f6420cbd12077c317e2bba8176442607c0319a85",
}


Permutation = tuple[int, ...]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((ARTIFACTS / name).read_text(encoding="utf-8"))


def load_json(name: str) -> dict[str, Any]:
    return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))


def add_check(
    condition: bool,
    check_id: str,
    detail: str,
    checks: list[dict[str, str]],
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "detail": detail,
            "status": "PASS" if condition else "FAIL",
        }
    )


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def validate_group(actions: list[list[int]], size: int) -> tuple[Permutation, ...]:
    group = tuple(tuple(action) for action in actions)
    expected_indices = list(range(size))
    if not group or any(sorted(action) != expected_indices for action in group):
        raise ValueError("Every declared action must be a permutation.")
    if len(set(group)) != len(group):
        raise ValueError("Group action list contains duplicates.")
    identity = tuple(expected_indices)
    if identity not in group:
        raise ValueError("Group action list omits the identity.")
    group_set = set(group)
    for left in group:
        for right in group:
            if compose(left, right) not in group_set:
                raise ValueError("Group action list is not closed under composition.")
    for action in group:
        if not any(
            compose(action, candidate) == identity
            and compose(candidate, action) == identity
            for candidate in group
        ):
            raise ValueError("Group action list omits an inverse.")
    return group


def enumerate_orbits(group: tuple[Permutation, ...], size: int) -> list[list[int]]:
    unseen = set(range(size))
    orbits: list[list[int]] = []
    while unseen:
        seed = min(unseen)
        orbit = sorted({action[seed] for action in group})
        orbits.append(orbit)
        unseen.difference_update(orbit)
    return orbits


def orbit_invariant(values: list[Any], group: tuple[Permutation, ...]) -> bool:
    return all(
        values[action[index]] == values[index]
        for action in group
        for index in range(len(values))
    )


def all_choice_equal(values: list[Any]) -> bool:
    return bool(values) and all(value == values[0] for value in values)


def joint_all_choice_equal(observables: list[dict[str, Any]]) -> bool:
    if not observables:
        return False
    size = len(observables[0]["values"])
    signatures = [
        tuple(json.dumps(row["values"][index], sort_keys=True) for row in observables)
        for index in range(size)
    ]
    return bool(signatures) and all(signature == signatures[0] for signature in signatures)


def validate_definition(spec: dict[str, Any], checks: list[dict[str, str]]) -> None:
    add_check(
        spec.get("artifact_id") == ARTIFACT_ID
        and spec.get("status") == "draft/control"
        and spec.get("adoption_status") == "proposal-only"
        and spec.get("plan_task_id") == "P3-T03"
        and spec.get("target_derivation_milestone") == "source_equivalence_eqsrc",
        "artifact_identity_and_status",
        "The machine definition is bound to P3-T03 and proposal-only source-equivalence work.",
        checks,
    )

    fixed = spec.get("fixed_input_contract", {})
    add_check(
        "nonempty" in fixed.get("representative_domain", "").lower()
        and "before evaluation" in fixed.get("observable_family", "").lower()
        and "D_X/G_X" in fixed.get("orbit_quotient", "")
        and len(fixed.get("target_exclusions", [])) >= 6,
        "fixed_source_only_input_contract",
        "Representative domain, action, observable family, and exclusions are fixed before evaluation.",
        checks,
    )

    criteria = spec.get("criteria", {})
    add_check(
        "iff" in criteria.get("orbit_factorization", {}).get("statement", "")
        and criteria.get("all_choice_equality", {}).get("nonempty_guard_required") is True
        and "not equality" in criteria.get("equivariance_guard", {}).get("statement", "")
        and "does not imply" in criteria.get("multiple_orbit_guard", {}).get("statement", ""),
        "factorization_and_guard_contract",
        "Orbit factorization, nonempty all-choice equality, equivariance, and multi-orbit guards are explicit.",
        checks,
    )

    algebra = spec.get("real_valued_invariant_algebra", {})
    add_check(
        algebra.get("carrier") == "Fun(D_X,R)^{G_X}"
        and "|G_X|^{-1}" in algebra.get("reynolds_projection", "")
        and "finite" in algebra.get("exact_scope", "").lower()
        and "real-valued" in algebra.get("exact_scope", "").lower()
        and "arbitrary" in algebra.get("does_not_apply_to", "").lower(),
        "finite_reynolds_scope_guard",
        "The invariant-algebra projection is limited to finite groups and real-valued readouts.",
        checks,
    )

    source_hashes = spec.get("source_hashes", {})
    add_check(
        source_hashes == EXPECTED_SOURCES
        and all(digest(ROOT / path) == expected for path, expected in EXPECTED_SOURCES.items()),
        "canonical_source_hashes",
        "All canonical source paths remain byte-equal to the inspected pre-execution inputs.",
        checks,
    )


def validate_cases(data: dict[str, Any], checks: list[dict[str, str]]) -> dict[str, int]:
    rows = data.get("cases", [])
    add_check(
        tuple(row.get("case_id") for row in rows) == EXPECTED_CASE_IDS,
        "bounded_case_identity",
        "The exact six required orientation, root, line, partition, grade, and multi-orbit controls are present.",
        checks,
    )

    group_exact = True
    orbit_exact = True
    classification_exact = True
    invariant_factorization_count = 0
    invariant_all_choice_count = 0
    raw_all_choice_count = 0
    countermodel_count = 0
    transitive_count = 0
    multi_orbit_count = 0
    sensitive_witnesses = 0

    for row in rows:
        choices = row.get("choices", [])
        observables = row.get("observables", [])
        try:
            group = validate_group(row.get("group_actions", []), len(choices))
        except ValueError:
            group_exact = False
            group = (tuple(range(len(choices))),)
        orbits = enumerate_orbits(group, len(choices))
        orbit_exact = orbit_exact and orbits == row.get("expected_orbits")
        if len(orbits) == 1:
            transitive_count += 1
        else:
            multi_orbit_count += 1

        invariant_rows: list[dict[str, Any]] = []
        sensitive_rows: list[dict[str, Any]] = []
        for observable in observables:
            values = observable.get("values", [])
            actual = orbit_invariant(values, group) if len(values) == len(choices) else False
            expected = observable.get("expected_class") == "orbit_invariant"
            classification_exact = classification_exact and actual == expected
            if actual:
                invariant_rows.append(observable)
            else:
                sensitive_rows.append(observable)

        invariant_factorization_count += int(bool(invariant_rows) and all(
            orbit_invariant(observable["values"], group) for observable in invariant_rows
        ))
        invariant_all_choice = joint_all_choice_equal(invariant_rows)
        raw_all_choice = joint_all_choice_equal(observables)
        invariant_all_choice_count += int(invariant_all_choice)
        raw_all_choice_count += int(raw_all_choice)
        countermodel_count += int(not raw_all_choice)
        sensitive_witnesses += len(sensitive_rows)
        classification_exact = classification_exact and (
            invariant_all_choice == row.get("expected_invariant_subfamily_all_choice_equal")
            and raw_all_choice == row.get("expected_raw_interface_all_choice_equal")
            and bool(sensitive_rows)
        )

    add_check(
        group_exact,
        "group_action_exactness",
        "Every declared finite action list is a duplicate-free group containing identity, closure, and inverses.",
        checks,
    )
    add_check(
        orbit_exact and transitive_count == 5 and multi_orbit_count == 1,
        "orbit_enumeration_complete",
        "Complete enumeration yields five transitive controls and one exact two-orbit control.",
        checks,
    )
    add_check(
        classification_exact and sensitive_witnesses >= 6,
        "observable_classification_exact",
        "Every readout is correctly classified by exhaustive action evaluation, with at least one sensitive witness per raw interface.",
        checks,
    )
    add_check(
        invariant_factorization_count == 6
        and invariant_all_choice_count == 5
        and raw_all_choice_count == 0
        and countermodel_count == 6,
        "factorization_and_countermodel_counts",
        "All invariant subfamilies factor; five are globally constant, while all six raw interfaces are countermodels to full irrelevance.",
        checks,
    )

    computed = {
        "case_count": len(rows),
        "transitive_case_count": transitive_count,
        "multi_orbit_case_count": multi_orbit_count,
        "invariant_subfamily_factorization_pass_count": invariant_factorization_count,
        "invariant_subfamily_all_choice_equal_count": invariant_all_choice_count,
        "raw_interface_all_choice_equal_count": raw_all_choice_count,
        "raw_interface_countermodel_count": countermodel_count,
    }
    add_check(
        computed == data.get("expected_summary"),
        "summary_reproduction",
        "The stored summary is exactly reproduced from the finite action and readout tables.",
        checks,
    )

    boundary = data.get("authority_boundary", {})
    add_check(
        boundary.get("finite_source_controls_only") is True
        and boundary.get("operational_physical_observable_established") is False
        and boundary.get("physical_gauge_established") is False
        and boundary.get("source_law_adopted") is False
        and boundary.get("general_eqsrc_discharged") is False
        and boundary.get("distance_to_gr_delta_changed") is False
        and boundary.get("global_no_go_authorized") is False,
        "finite_authority_boundary",
        "Finite calculations carry no ontology, gauge, general EqSrc, ledger, or global no-go authority.",
        checks,
    )
    return computed


def validate_narrative(checks: list[dict[str, str]]) -> None:
    tex = (ARTIFACTS / "eqsrc_representative_irrelevance_theorem_v1.tex").read_text(
        encoding="utf-8"
    )
    required_tokens = (
        "Orbit-factorization criterion",
        "All-choice equality criterion",
        "Equivariance is not equality",
        "Maximal invariant real-readout algebra",
        "Multiple-orbit guard",
        "scoped raw-interface obstruction",
        r"blocked\_adoption\_open\_continuation",
        "Structural automorphisms are not thereby physical gauge transformations",
        "general \\EqSrc{} remains open",
    )
    add_check(
        all(token in tex for token in required_tokens),
        "theorem_and_boundary_narrative",
        "The theorem source contains every decisive statement and authority boundary.",
        checks,
    )

    child_paths = (
        "child_phys_math_eqsrc_representative_irrelevance.yaml",
        "child_phys_phil_eqsrc_representative_irrelevance.yaml",
    )
    child_records = [load_yaml(path) for path in child_paths]
    review = load_yaml("parent_conflict_review_eqsrc_representative_irrelevance.yaml")
    add_check(
        all(record.get("status") == "completed" for record in child_records)
        and all(record.get("agent_job_id") == "AJ-RT-20260720-024-001" for record in child_records)
        and review.get("status") == "resolved"
        and review.get("unresolved_blocking_conflicts") == [],
        "parent_child_synthesis",
        "Both internal perspectives completed under one outer AgentJob and the parent resolved all blocking conflicts.",
        checks,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, str]] = []
    spec = load_yaml("eqsrc_observable_invariance_definition_v1.yaml")
    data = load_json("eqsrc_representative_irrelevance_orbit_examples_v1.json")
    validate_definition(spec, checks)
    computed = validate_cases(data, checks)
    validate_narrative(checks)

    failures = [check for check in checks if check["status"] != "PASS"]
    report = {
        "schema_id": "v21_p3_t03_eqsrc_representative_irrelevance_validation_v1",
        "artifact_id": ARTIFACT_ID,
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failures),
        "computed_summary": computed,
        "checks": checks,
        "authority_note": "PASS is bounded support evidence only and creates no ontology, physical-gauge, operational-observable, general EqSrc, promotion, publication, or global no-go authority.",
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
