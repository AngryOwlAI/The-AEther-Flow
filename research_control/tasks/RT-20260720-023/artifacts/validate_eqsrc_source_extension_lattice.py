#!/usr/bin/env python3
"""Validate the bounded v21 P3-T02 source-extension lattice packet.

PASS establishes finite task-local consistency only. It is not ontology,
physical-gauge, physical-admissibility, EqSrc, or promotion authority.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


ARTIFACTS = Path(__file__).resolve().parent
ROOT = ARTIFACTS.parents[3]
LATTICE_ID = "EQSRC-SOURCE-EXTENSION-LATTICE-V1"
REPORT = ARTIFACTS / "eqsrc_source_extension_lattice_validation.json"
ATOMS = ("R", "O", "Q", "G", "M", "I", "B", "D")
COST_AXES = (
    "source_signature_delta",
    "selector_readout_delta",
    "state_boundary_delta",
    "dynamics_delta",
    "probability_delta",
    "variation_class_delta",
    "functoriality_burden",
    "empirical_calibration_delta",
    "target_import_risk",
    "human_authority_required",
)
FAMILY_PACKAGES = {
    "EQSRC-CANONICAL-CHOICE-INTRINSIC-DISCRIMINATOR": ("Q",),
    "EQSRC-CANONICAL-CHOICE-CYCLE-BOUNDARY-LINE": ("O",),
    "EQSRC-CANONICAL-CHOICE-ORIENTATION-TORSOR": ("R", "O"),
    "EQSRC-CANONICAL-CHOICE-ROOTED-PARTITION": ("R", "D"),
    "EQSRC-CANONICAL-CHOICE-GRADED-ORBIT-ROOT": ("G", "D"),
}
EXPECTED_SOURCES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/design/gr_derivation_burden_map.md": "6d1df3488be163b72296cf34ee07b979e29b061d508e6a4c271ac3305373aa1f",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61",
    "research_control/tasks/RT-20260720-010/artifacts/eqsrc_canonical_choice_family_inventory.json": "5a823d46054fa75ee7f5f7814aa76ff52ea3e8d8868547229d5b0b2a26e0685e",
    "research_control/tasks/RT-20260720-011/artifacts/eqsrc_canonical_choice_family_freeze_manifest.yaml": "fc0d36a7ea96b6aaaafced309c73c6bb2e71d969ee679d5c286afc2753a95b43",
    "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex": "d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae",
    "research_control/tasks/RT-20260720-017/artifacts/eqsrc_finite_countermodel_atlas_fixtures.json": "e8ced96541fa941e5a3b4ceaa8d7b48204acf7ca8ec342ac6b23dbbf5c470a73",
    "research_control/tasks/RT-20260720-022/artifacts/eqsrc_selector_resolution_taxonomy_v1.tex": "4af38c29cc97729cbd4278e5174b4ff3cc76d7921dbf148f953e92c9a3f03d30",
    "ontology/tex/aether_flow_foundations.tex": "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2",
}


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


Permutation = tuple[int, ...]


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def generated_group(size: int, generators: list[list[int]]) -> tuple[Permutation, ...]:
    identity = tuple(range(size))
    normalized = [tuple(generator) for generator in generators]
    if any(sorted(generator) != list(range(size)) for generator in normalized):
        raise ValueError("Every generator must be a permutation of the choice indices.")
    group = {identity, *normalized}
    changed = True
    while changed:
        changed = False
        for left in tuple(group):
            for right in tuple(group):
                product = compose(left, right)
                if product not in group:
                    group.add(product)
                    changed = True
    return tuple(sorted(group))


def fixed_indices(size: int, group: tuple[Permutation, ...]) -> list[int]:
    return [
        index
        for index in range(size)
        if all(permutation[index] == index for permutation in group)
    ]


def enumerate_lattice() -> tuple[list[frozenset[str]], list[tuple[frozenset[str], frozenset[str]]]]:
    nodes = [
        frozenset(combination)
        for rank in range(len(ATOMS) + 1)
        for combination in itertools.combinations(ATOMS, rank)
    ]
    covers = [
        (node, node | {atom})
        for node in nodes
        for atom in ATOMS
        if atom not in node
    ]
    return nodes, covers


def validate_lattice(spec: dict[str, Any], checks: list[dict[str, str]]) -> None:
    nodes, covers = enumerate_lattice()
    ranks = Counter(map(len, nodes))
    expected_ranks = [math.comb(len(ATOMS), rank) for rank in range(len(ATOMS) + 1)]
    order = spec.get("order", {})
    add_check(
        len(nodes) == order.get("node_count") == 256
        and len(covers) == order.get("cover_count") == 1024
        and [ranks[rank] for rank in range(9)] == order.get("rank_counts") == expected_ranks,
        "boolean_declaration_envelope_exactness",
        "Exhaustive B8 enumeration has 256 nodes, 1024 covers, and exact binomial ranks.",
        checks,
    )

    universe = frozenset(ATOMS)
    lattice_laws = all(
        (left & right).issubset(left)
        and (left & right).issubset(right)
        and left.issubset(left | right)
        and right.issubset(left | right)
        and (left & (left | right)) == left
        and (left | (left & right)) == left
        and (left & (universe - left)) == frozenset()
        and (left | (universe - left)) == universe
        for left in nodes
        for right in nodes
    )
    add_check(
        lattice_laws,
        "lattice_laws_exhaustive",
        "Meet, join, absorption, and complement laws hold for every ordered node pair.",
        checks,
    )

    atom_codes = tuple(row.get("code") for row in spec.get("atoms", []))
    typing = spec.get("typing_and_reduct_guard", {})
    add_check(
        atom_codes == ATOMS
        and typing.get("full_boolean_physical_realizability_claimed") is False
        and typing.get("admissible_subposet_must_be_a_lattice") is False
        and "reduct" in typing.get("scientific_extension_order", "").lower()
        and order.get("false_total_order_forbidden") is True
        and order.get("scientific_preference_encoded") is False,
        "typing_and_reduct_guard",
        "Eight distinct atom types are exact and B8 is explicitly only a declaration envelope.",
        checks,
    )

    incomparable = spec.get("required_incomparabilities", [])
    exact_incomparability = all(
        not set(row["left"]).issubset(row["right"])
        and not set(row["right"]).issubset(row["left"])
        for row in incomparable
    )
    add_check(
        len(incomparable) == 5
        and exact_incomparability
        and any(row["left"] == ["Q"] and row["right"] == ["G"] for row in incomparable),
        "declared_incomparabilities",
        "Five exact inclusion-incomparable pairs include the differential-versus-grading guard.",
        checks,
    )


def validate_costs(checks: list[dict[str, str]]) -> None:
    path = ARTIFACTS / "eqsrc_source_extension_assumption_costs_v1.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    codes = tuple(row["atom_code"] for row in rows)
    numeric_ok = all(
        0 <= int(row[axis]) <= 3
        for row in rows
        for axis in COST_AXES
    )
    no_scalar = not any(
        token in field.lower()
        for field in fieldnames
        for token in ("total", "score", "weight", "rank")
    )
    add_check(
        codes == ATOMS
        and all(axis in fieldnames for axis in COST_AXES)
        and numeric_ok
        and no_scalar
        and all(int(row["human_authority_required"]) == 3 for row in rows),
        "multidimensional_cost_contract",
        "All eight atoms have ten bounded burden components, no scalarization field, and a protected-adoption burden.",
        checks,
    )

    vectors = {
        row["atom_code"]: tuple(int(row[axis]) for axis in COST_AXES)
        for row in rows
    }
    m_le_d = all(left <= right for left, right in zip(vectors["M"], vectors["D"]))
    d_le_m = all(left <= right for left, right in zip(vectors["D"], vectors["M"]))
    add_check(
        not m_le_d and not d_le_m,
        "cost_vector_incomparability_control",
        "Measure and dynamics atoms remain incomparable under the declared componentwise burden order.",
        checks,
    )


def validate_witnesses(
    witnesses: dict[str, Any],
    checks: list[dict[str, str]],
) -> None:
    rows = witnesses.get("point_witnesses", [])
    computed: dict[str, dict[str, Any]] = {}
    compatible_stable = True
    authority_false = True
    probability_ok = True
    for row in rows:
        size = len(row["choice_labels"])
        group = generated_group(size, row["group_generators"])
        stabilizer = generated_group(size, row["stabilizer_generators"])
        compatible = set(row["compatible_choice_indices"])
        compatible_stable = compatible_stable and set(stabilizer).issubset(group)
        compatible_stable = compatible_stable and all(
            {permutation[index] for index in compatible} == compatible
            for permutation in stabilizer
        )
        base_fixed = fixed_indices(size, group)
        compatible_fixed = [
            index
            for index in sorted(compatible)
            if all(permutation[index] == index for permutation in stabilizer)
        ]
        computed[row["witness_id"]] = {
            "base_group_order": len(group),
            "stabilizer_order": len(stabilizer),
            "base_fixed_indices": base_fixed,
            "compatible_fixed_indices": compatible_fixed,
            "deterministic_selector_count": len(compatible_fixed),
        }
        expectation = row["expected"]
        probability_count = expectation.get("invariant_probability_selector_count")
        if "probability_weights" in row:
            weights = [Fraction(value) for value in row["probability_weights"]]
            invariant = all(
                all(weights[index] == weights[permutation[index]] for index in range(size))
                for permutation in group
            )
            probability_ok = (
                probability_ok
                and sum(weights) == 1
                and invariant
                and probability_count == 1
            )
        authority_false = (
            authority_false
            and row.get("source_provenance_established") is False
            and row.get("physical_admissibility_established") is False
        )

    exact_values = all(
        all(row["expected"].get(key) == value for key, value in computed[row["witness_id"]].items())
        for row in rows
    )
    add_check(
        len(rows) == 8 and exact_values and compatible_stable,
        "finite_stabilizer_and_fixed_locus_witnesses",
        "Eight finite group-action witnesses reproduce every group, stabilizer, fixed-locus, and compatibility count.",
        checks,
    )
    add_check(
        probability_ok
        and computed["W4-C3-UNIFORM-MEASURE"]["deterministic_selector_count"] == 0
        and computed["W5-C2-EQUIVARIANT-DYNAMICS-ONLY"]["deterministic_selector_count"] == 0
        and computed["W6-C2-INITIAL-STATE-WITH-DYNAMICS"]["deterministic_selector_count"] == 1,
        "target_type_and_dynamics_controls",
        "Uniform probability, dynamics-only failure, and linked-state-plus-dynamics selection stay distinct.",
        checks,
    )
    arbitrary = next(row for row in rows if row["witness_id"] == "W7-C3-ARBITRARY-MARK-CONTROL")
    add_check(
        authority_false
        and arbitrary.get("counts_as_lawful_source_extension_witness") is False
        and computed[arbitrary["witness_id"]]["deterministic_selector_count"] == 1,
        "provenance_and_physical_admissibility_guard",
        "Formal uniqueness is explicitly separated from source provenance and physical admissibility.",
        checks,
    )


def validate_historical(
    placements: dict[str, Any],
    checks: list[dict[str, str]],
) -> None:
    rows = placements.get("families", [])
    observed = {
        row["family_id"]: tuple(row["candidate_package"])
        for row in rows
    }
    add_check(
        observed == FAMILY_PACKAGES
        and len(set(observed.values())) == 5
        and all(set(package).issubset(ATOMS) for package in observed.values())
        and all(row.get("family_freeze_preserved") is True for row in rows)
        and all(row.get("additional_unmet_obligations") for row in rows),
        "historical_family_placements",
        "Five frozen families occupy five exact candidate nodes and retain explicit unmet obligations.",
        checks,
    )
    boundary = placements.get("authority_boundary", {})
    add_check(
        "not a universal theorem" in placements.get("minimality_scope", "")
        and all(value is False for value in boundary.values()),
        "historical_minimality_and_authority",
        "Minimality is finite-witness-local and every reopening, adoption, ranking, ledger, EqSrc, and no-go authority remains false.",
        checks,
    )


def validate_children(checks: list[dict[str, str]]) -> None:
    math_child = load_yaml("child_phys_math_eqsrc_source_extension_lattice.yaml")
    phil_child = load_yaml("child_phys_phil_eqsrc_source_extension_lattice.yaml")
    conflict = load_yaml("parent_conflict_review_eqsrc_source_extension_lattice.yaml")
    fusion = (ARTIFACTS / "parent_fusion_notes_eqsrc_source_extension_lattice.md").read_text(encoding="utf-8")
    add_check(
        math_child.get("status") == "completed"
        and phil_child.get("status") == "completed"
        and math_child.get("authority", "").startswith("analysis-only")
        and phil_child.get("authority", "").startswith("analysis-only"),
        "parallel_child_outputs",
        "Both bounded internal perspectives completed without independent AgentJob authority.",
        checks,
    )
    conflicts = conflict.get("conflicts", [])
    add_check(
        conflict.get("status") == "completed"
        and conflict.get("resolution_rounds_used") == 1
        and conflict.get("resolved_conflict_count") == len(conflicts) == 6
        and conflict.get("unresolved_conflict_count") == 0
        and all(row.get("status") == "resolved" for row in conflicts)
        and "256 nodes and 1024 directed" in fusion
        and "need not be closed" in fusion,
        "parent_conflict_review_and_fusion",
        "Six child conflicts resolve in one round and the fused typing guard is explicit.",
        checks,
    )


def validate_tex(checks: list[dict[str, str]]) -> None:
    tex = (ARTIFACTS / "eqsrc_source_extension_lattice_v1.tex").read_text(encoding="utf-8")
    normalized = " ".join(tex.split())
    required = (
        "EQSRC-SOURCE-EXTENSION-LATTICE-V1",
        "draft/control, proposal-only, source-extension data",
        "256 nodes",
        "1024 directed cover edges",
        "WellTyped",
        "compatible stabilizer-fixed locus",
        "current ontology does not derive",
        "Distance-to-GR delta",
        "blocked\\_adoption\\_open\\_continuation",
        "P3-T03 is the next dependency-ready theorem packet",
    )
    add_check(
        tex.count("{") == tex.count("}")
        and "\\begin{document}" in tex
        and "\\end{document}" in tex
        and all(term in normalized for term in required),
        "tex_structure_claim_boundary_and_decisiveness",
        "The TeX construction is structurally complete and reports payload, bridge, obstruction, freeze, and authority boundaries.",
        checks,
    )


def validate_sources_and_receipt(checks: list[dict[str, str]]) -> None:
    observed_sources = {
        path: digest(ROOT / path)
        for path in EXPECTED_SOURCES
    }
    add_check(
        observed_sources == EXPECTED_SOURCES,
        "source_hash_parity",
        "Nine fixed plan, ontology, theorem, family, fixture, taxonomy, burden, and ledger sources retain exact hashes.",
        checks,
    )

    receipt = load_json("eqsrc_source_extension_compact_receipt.json")
    receipt_sources = {
        row["path"]: row["sha256"]
        for row in receipt.get("source_hashes", [])
    }
    artifact_hashes = receipt.get("artifact_hashes", [])
    artifact_parity = all(
        digest(ROOT / row["path"]) == row["sha256"]
        for row in artifact_hashes
    )
    boundary = receipt.get("claim_boundary_summary", {})
    add_check(
        receipt.get("lattice_id") == LATTICE_ID
        and receipt.get("task_id") == "RT-20260720-023"
        and receipt.get("generation") == 23
        and receipt_sources == EXPECTED_SOURCES
        and artifact_parity
        and receipt.get("finding_counts", {}).get("declaration_node_count") == 256
        and receipt.get("finding_counts", {}).get("finite_witness_count") == 8
        and boundary.get("source_extension_adoption_authorized") is False
        and boundary.get("distance_to_gr_delta") is False
        and boundary.get("next_dependency_ready_item") == "P3-T03",
        "compact_receipt_parity",
        "Compact receipt identities, hashes, counts, authority flags, and next dependency are exact.",
        checks,
    )


def validate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    required_paths = (
        "eqsrc_source_extension_lattice_v1.tex",
        "eqsrc_source_extension_lattice_v1.yaml",
        "eqsrc_source_extension_assumption_costs_v1.csv",
        "eqsrc_source_extension_finite_witnesses_v1.json",
        "eqsrc_source_extension_historical_placements_v1.yaml",
        "child_phys_math_eqsrc_source_extension_lattice.yaml",
        "child_phys_phil_eqsrc_source_extension_lattice.yaml",
        "parent_conflict_review_eqsrc_source_extension_lattice.yaml",
        "parent_fusion_notes_eqsrc_source_extension_lattice.md",
        "eqsrc_source_extension_compact_receipt.json",
    )
    add_check(
        all((ARTIFACTS / name).is_file() for name in required_paths),
        "artifact_set",
        "All ten fused, machine, child, review, and compact-receipt artifacts exist.",
        checks,
    )

    spec = load_yaml("eqsrc_source_extension_lattice_v1.yaml")
    witnesses = load_json("eqsrc_source_extension_finite_witnesses_v1.json")
    placements = load_yaml("eqsrc_source_extension_historical_placements_v1.yaml")
    add_check(
        spec.get("lattice_id") == LATTICE_ID
        and witnesses.get("lattice_id") == LATTICE_ID
        and placements.get("lattice_id") == LATTICE_ID
        and spec.get("status") == "draft/control"
        and spec.get("adoption_status") == "proposal-only",
        "packet_identity_and_status",
        "Machine artifacts share the exact lattice identity and proposal-only status.",
        checks,
    )

    validate_lattice(spec, checks)
    validate_costs(checks)
    validate_witnesses(witnesses, checks)
    validate_historical(placements, checks)
    validate_children(checks)
    validate_tex(checks)

    authority = spec.get("authority_boundary", {})
    add_check(
        all(value is False for key, value in authority.items() if key != "classification")
        and authority.get("classification") == "blocked_adoption_open_continuation"
        and spec.get("downstream_boundaries", {}).get("execution_of_downstream_items") is False,
        "global_authority_boundary",
        "Ontology, adoption, physical, empirical, EqSrc, ledger, promotion, no-go, and downstream-execution flags remain false.",
        checks,
    )
    validate_sources_and_receipt(checks)

    status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    return {
        "schema_id": "v21_p3_t02_eqsrc_source_extension_lattice_validation_v1",
        "lattice_id": LATTICE_ID,
        "task_id": "RT-20260720-023",
        "job_id": "AJ-RT-20260720-023-001",
        "status": status,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "fail_count": sum(row["status"] == "FAIL" for row in checks),
        "checks": checks,
        "authority_note": "PASS is finite task-local consistency evidence only and creates no protected scientific authority.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
