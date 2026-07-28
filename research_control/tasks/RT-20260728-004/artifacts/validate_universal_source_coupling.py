#!/usr/bin/env python3
"""Deterministic source-only validation for the P7-T05 draft/control packet."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
ARTIFACTS = Path(__file__).resolve().parent
SPEC_PATH = ARTIFACTS / "universal_source_coupling_map_spec_v1.yaml"
CONTROLS_PATH = ARTIFACTS / "universal_source_coupling_controls_v1.yaml"
ASSUMPTIONS_PATH = ARTIFACTS / "universal_source_coupling_assumption_dependency_table_v1.yaml"
TEX_PATH = ARTIFACTS / "universal_source_coupling_map_candidate_v1.tex"
CHILD_MATH_PATH = ARTIFACTS / "child_phys_math_p7_t05_source_coupling.yaml"
CHILD_PHIL_PATH = ARTIFACTS / "child_phys_phil_p7_t05_source_coupling.yaml"
CONFLICT_PATH = ARTIFACTS / "parent_conflict_review_p7_t05_source_coupling.yaml"
FUSION_PATH = ARTIFACTS / "parent_fusion_notes_p7_t05_source_coupling.md"
REPORT_PATH = ARTIFACTS / "universal_source_coupling_validation_v1.json"
COMPACT_PATH = ARTIFACTS / "universal_source_coupling_compact_receipt_v1.json"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_matrix(value: Any) -> list[list[Fraction]]:
    if not isinstance(value, list):
        return []
    result: list[list[Fraction]] = []
    for row in value:
        if not isinstance(row, list):
            return []
        result.append([Fraction(str(item)) for item in row])
    return result


def square(matrix: list[list[Fraction]]) -> bool:
    return bool(matrix) and all(len(row) == len(matrix) for row in matrix)


def column_sums(matrix: list[list[Fraction]]) -> list[Fraction]:
    if not square(matrix):
        return []
    return [sum(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix))]


def support(matrix: list[list[Fraction]]) -> list[list[int]]:
    return [[int(entry > 0) for entry in row] for row in matrix]


def edge_count(matrix: list[list[int]]) -> int:
    return sum(sum(row) for row in matrix)


def reduced_edge_count(matrix: list[list[int]]) -> int:
    return sum(
        entry
        for row_index, row in enumerate(matrix)
        for column_index, entry in enumerate(row)
        if row_index != column_index
    )


def permutation_equivalent(left: list[list[int]], right: list[list[int]]) -> bool:
    if len(left) != len(right) or any(len(row) != len(left) for row in left + right):
        return False
    size = len(left)
    for permutation in itertools.permutations(range(size)):
        transported = [
            [left[permutation[row]][permutation[column]] for column in range(size)]
            for row in range(size)
        ]
        if transported == right:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    required_paths = [
        SPEC_PATH,
        CONTROLS_PATH,
        ASSUMPTIONS_PATH,
        TEX_PATH,
        CHILD_MATH_PATH,
        CHILD_PHIL_PATH,
        CONFLICT_PATH,
        FUSION_PATH,
    ]
    for path in required_paths:
        check(f"exists:{path.name}", path.is_file(), str(path.relative_to(ROOT)))

    spec = load_yaml(SPEC_PATH)
    controls = load_yaml(CONTROLS_PATH)
    assumptions = load_yaml(ASSUMPTIONS_PATH)
    tex = TEX_PATH.read_text(encoding="utf-8")

    check(
        "spec_schema",
        spec.get("schema_id") == "v21_p7_t05_universal_source_coupling_map_spec_v1",
        "spec schema",
    )
    check("task_id", spec.get("task_id") == "RT-20260728-004", "task identity")
    check("job_id", spec.get("job_id") == "AJ-RT-20260728-004-001", "job identity")
    check("plan_task_id", spec.get("plan_task_id") == "P7-T05", "plan identity")
    check("proposal_only", spec.get("candidate_status") == "proposal-only", "candidate status")
    check(
        "adoption_blocked",
        spec.get("adoption_status") == "blocked_adoption_open_continuation",
        "adoption status",
    )
    check(
        "result_kind",
        spec.get("result_kind") == "precise_obstruction_with_constructive_restricted_domain",
        "decisive result classification",
    )

    fixed_sources = spec.get("fixed_source_basis", [])
    fixed_hashes = {
        str(item.get("object_id", item.get("path", ""))): str(item.get("sha256", ""))
        for item in fixed_sources
        if isinstance(item, dict)
    }
    expected_hashes = {
        "TEX-V21-P7-T01-SOURCE-MATTER-ONTOLOGY-SECTOR-TAXONOMY-V1":
            "8d160217bf223078a11bc63fde6593c11c39d5b50d9c48fbad7b12084f8a752d",
        "TEX-V21-P7-T02-SOURCE-MATTER-FINITE-TRANSITION-KERNEL-V1":
            "65ac095f5cdf4c2e319365c8b0e024d031b19d9fc2b8102e59997afa1e8f9129",
        "TEX-V21-P7-T03-SOURCE-OPERATIONAL-DEVICE-SUITE-V1":
            "d6c818ee29f1a7e659e2f454aec21431d680b3d2d4df048fcf36f4aba87ba22a",
        "TEX-V21-P7-T04-COMMON-SOURCE-PROPAGATION-PROFILE-V1":
            "87014253023cdb8945ed67f606355d762486884ce3a6de4fa2d32e2af32e2b43",
    }
    for object_id, expected_hash in expected_hashes.items():
        check(
            f"fixed_hash:{object_id}",
            fixed_hashes.get(object_id) == expected_hash,
            expected_hash,
        )

    carrier = controls.get("common_three_address_carrier", {})
    carrier_matrix = fraction_matrix(carrier.get("update_matrix_rows_target_columns_source"))
    expected_carrier = [
        [Fraction(1, 2), Fraction(0), Fraction(0)],
        [Fraction(1, 2), Fraction(1, 2), Fraction(0)],
        [Fraction(0), Fraction(1, 2), Fraction(1)],
    ]
    check("carrier_matrix_square", square(carrier_matrix), "three by three matrix")
    check("carrier_matrix_exact", carrier_matrix == expected_carrier, "fixed B3 update")
    check(
        "carrier_column_normalization",
        column_sums(carrier_matrix) == [Fraction(1), Fraction(1), Fraction(1)],
        str(column_sums(carrier_matrix)),
    )
    carrier_support = support(carrier_matrix)
    check("carrier_full_edge_count", edge_count(carrier_support) == 5, "three loops and two forward edges")
    check("carrier_reduced_edge_count", reduced_edge_count(carrier_support) == 2, "two forward edges")
    check("carrier_not_physical_geometry", carrier.get("physical_geometry_claimed") is False, "source carrier only")

    equipped = controls.get("equipped_control_type", {})
    predicates = equipped.get("predicates", [])
    check("equipment_type_id", equipped.get("type_id") == "ExplicitlyEquippedSectorControl_v1", "type identity")
    check("equipment_predicate_count", isinstance(predicates, list) and len(predicates) >= 5, "explicit equipment predicates")
    check("no_global_sector_selection", equipped.get("global_sector_selection_claimed") is False, "restricted domain")

    instances = controls.get("constructive_instances", [])
    check("constructive_instance_count", isinstance(instances, list) and len(instances) == 3, "Rod Signal Detector")
    expected_state_prefixes = {
        "P7T05-EQUIPPED-ROD-CHAIN-001": "r_",
        "P7T05-EQUIPPED-SIGNAL-CHAIN-001": "s_",
        "P7T05-EQUIPPED-DETECTOR-CHAIN-001": "q_",
    }
    for instance in instances if isinstance(instances, list) else []:
        instance_id = str(instance.get("instance_id", ""))
        states = instance.get("states", [])
        kappa = instance.get("kappa", {})
        prefix = expected_state_prefixes.get(instance_id, "")
        check(f"instance_known:{instance_id}", bool(prefix), instance_id)
        check(
            f"instance_states:{instance_id}",
            states == [f"{prefix}0", f"{prefix}1", f"{prefix}2"],
            str(states),
        )
        check(
            f"instance_kappa_bijective:{instance_id}",
            isinstance(kappa, dict) and sorted(kappa.values()) == ["b_0", "b_1", "b_2"],
            str(kappa),
        )
        check(
            f"instance_intertwining:{instance_id}",
            instance.get("exact_update_intertwining") is True,
            "declared exact source update transport",
        )

    countermodel = controls.get("same_sector_countermodel", {})
    identity_control = countermodel.get("identity_only_control", {})
    forward_control = countermodel.get("forward_control", {})
    identity_matrix = fraction_matrix(identity_control.get("update_matrix_rows_target_columns_source"))
    forward_matrix = fraction_matrix(forward_control.get("update_matrix_rows_target_columns_source"))
    expected_identity = [
        [Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1)],
    ]
    expected_forward = [
        [Fraction(1, 2), Fraction(0)],
        [Fraction(1, 2), Fraction(1)],
    ]
    check("countermodel_identity_matrix", identity_matrix == expected_identity, "identity-only update")
    check("countermodel_forward_matrix", forward_matrix == expected_forward, "identity-plus-forward update")
    check(
        "countermodel_normalized",
        column_sums(identity_matrix) == [Fraction(1), Fraction(1)]
        and column_sums(forward_matrix) == [Fraction(1), Fraction(1)],
        "both finite updates are normalized",
    )
    identity_support = support(identity_matrix)
    forward_support = support(forward_matrix)
    check("countermodel_equal_cardinality", len(identity_support) == len(forward_support) == 2, "two states each")
    check("countermodel_edge_counts", edge_count(identity_support) == 2 and edge_count(forward_support) == 3, "2 versus 3")
    check("countermodel_reduced_edges", reduced_edge_count(identity_support) == 0 and reduced_edge_count(forward_support) == 1, "0 versus 1")
    check(
        "countermodel_nonisomorphic",
        not permutation_equivalent(identity_support, forward_support),
        "no support-preserving bijection",
    )
    fixed_sector = countermodel.get("fixed_sector", {})
    check("countermodel_same_sector", fixed_sector.get("sector_value") == "(1,[0])", "sigma_0 held fixed")
    check("countermodel_not_p7t04_repeat", countermodel.get("p7_t04_obstruction_repeated") is False, "distinct branch")
    check("countermodel_no_global_no_go", countermodel.get("global_no_go_claimed") is False, "scope guard")

    theorem_records = spec.get("theorems", [])
    theorem_ids = {
        str(item.get("theorem_id", ""))
        for item in theorem_records
        if isinstance(item, dict)
    }
    for theorem_id in [
        "P7T05-THM-THREE-ADDRESS-COUPLING-NATURALITY-001",
        "P7T05-THM-SECTOR-DATA-NONSELECTION-001",
    ]:
        check(f"theorem:{theorem_id}", theorem_id in theorem_ids, theorem_id)

    obstruction = spec.get("obstruction_record", {})
    check(
        "obstruction_id",
        obstruction.get("obstruction_id")
        == "OBST-P7T05-SECTOR-COUPLING-FUNCTOR-NONSELECTION-001",
        "precise obstruction identity",
    )
    check("obstruction_present", obstruction.get("present") is True, "obstruction record")
    check("obstruction_result_type", obstruction.get("result_type") == "precise_obstruction", "hard result type")
    check("obstruction_no_fog", obstruction.get("no_fog") is True, "no-fog requirement")
    check("obstruction_repair_open", obstruction.get("source_extension_implication") == "repair_allowed", "open continuation")
    failed_components = obstruction.get("failed_components", [])
    check(
        "obstruction_failed_components",
        isinstance(failed_components, list) and len(failed_components) >= 3,
        "explicit failed components",
    )

    obligations = spec.get("missing_source_extension_obligations", [])
    obligation_ids = {
        str(item.get("obligation_id", ""))
        for item in obligations
        if isinstance(item, dict)
    }
    for obligation_id in [
        "P7T05-OBL-SECTOR-CONTROL-SELECTOR-001",
        "P7T05-OBL-NATURAL-COMPARISON-FAMILY-001",
        "P7T05-OBL-COMMON-CARRIER-JUSTIFICATION-001",
        "P7T05-OBL-MODEL-TO-WORLD-COUPLING-001",
        "P7T05-OBL-VARIATIONAL-OBJECT-001",
    ]:
        check(f"obligation:{obligation_id}", obligation_id in obligation_ids, obligation_id)

    fail_closed = controls.get("fail_closed_controls", [])
    fail_ids = {
        str(item.get("control_id", ""))
        for item in fail_closed
        if isinstance(item, dict)
    }
    for control_id in [
        "P7T05-CTRL-VALID-EQUIPPED-001",
        "P7T05-CTRL-MISSING-KAPPA-001",
        "P7T05-CTRL-NONBIJECTIVE-KAPPA-001",
        "P7T05-CTRL-NONINTERTWINING-KAPPA-001",
        "P7T05-CTRL-SECTOR-FIBER-NOT-B3-001",
        "P7T05-CTRL-TARGET-IMPORT-001",
        "P7T05-CTRL-PHYSICAL-OVERREAD-001",
    ]:
        check(f"fail_closed:{control_id}", control_id in fail_ids, control_id)

    assumption_rows = assumptions.get("assumptions", [])
    assumption_ids = {
        str(item.get("assumption_id", ""))
        for item in assumption_rows
        if isinstance(item, dict)
    }
    for assumption_id in [
        "P7T05-A01-P7T01-FIXED",
        "P7T05-A02-P7T02-FIXED",
        "P7T05-A03-P7T03-CHAINS",
        "P7T05-A04-P7T04-CARRIER",
        "P7T05-A05-EXPLICIT-EQUIPMENT",
        "P7T05-A06-NO-TARGET-IMPORT",
    ]:
        check(f"assumption:{assumption_id}", assumption_id in assumption_ids, assumption_id)

    status_matrix = assumptions.get("status_matrix", {})
    for key in [
        "every_current_p7_t01_sector_covered",
        "sector_only_selector_derived",
        "common_physical_geometry_preserved",
        "physical_matter_coupling_derived",
        "matter_action_derived",
        "stress_energy_derived",
        "conservation_law_derived",
        "equivalence_principle_behavior_derived",
        "einstein_equations_derived",
        "ontology_or_source_law_adopted",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
        "physics_promotion_authorized",
    ]:
        check(f"status_false:{key}", status_matrix.get(key) is False, key)

    required_tex_tokens = [
        "SourceUniversalCouplingMapCandidate",
        "P7T05-THM-THREE-ADDRESS-COUPLING-NATURALITY-001",
        "P7T05-THM-SECTOR-DATA-NONSELECTION-001",
        "OBST-P7T05-SECTOR-COUPLING-FUNCTOR-NONSELECTION-001",
        "blocked\\_adoption\\_open\\_continuation",
        "Same-sector nonselection theorem",
        "Distinctness from P7-T04",
        "Fail-closed branches and reopening obligations",
        "future source-extension impossibility",
    ]
    for token in required_tex_tokens:
        check(f"tex_token:{token[:36]}", token in tex, token)

    authority = spec.get("authority_limits", {})
    for key in [
        "canonical_ontology_modified",
        "source_law_adopted",
        "candidate_adopted",
        "physical_matter_coupling_derived",
        "physical_universality_established",
        "covariant_derivative_derived",
        "matter_action_derived",
        "stress_energy_derived",
        "physical_conservation_law_derived",
        "principal_symbol_derived",
        "characteristic_cone_derived",
        "effective_metric_derived",
        "equivalence_principle_behavior_derived",
        "detector_semantics_established",
        "einstein_equations_derived",
        "exact_gr_recovered",
        "benchmark_promotion_authorized",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
        "physics_promotion_authorized",
    ]:
        check(f"authority_false:{key}", authority.get(key) is False, key)

    if CHILD_MATH_PATH.is_file():
        child_math = load_yaml(CHILD_MATH_PATH)
        check(
            "child_math_identity",
            child_math.get("execution_unit_id") == "child_phys_math",
            "physicist-mathematician child",
        )
        check("child_math_completed", child_math.get("status") == "completed", "child status")
    if CHILD_PHIL_PATH.is_file():
        child_phil = load_yaml(CHILD_PHIL_PATH)
        check(
            "child_phil_identity",
            child_phil.get("execution_unit_id") == "child_phys_phil",
            "physicist-philosopher child",
        )
        check("child_phil_completed", child_phil.get("status") == "completed", "child status")
    if CONFLICT_PATH.is_file():
        conflict = load_yaml(CONFLICT_PATH)
        check(
            "conflict_resolved",
            conflict.get("verdict") in {"resolved", "no_conflict"},
            "parent conflict verdict",
        )
        check(
            "no_unresolved_conflicts",
            conflict.get("unresolved_conflicts") in ([], None),
            "no unresolved conflicts",
        )

    failed = [item for item in checks if item["status"] != "PASS"]
    source_paths = [SPEC_PATH, CONTROLS_PATH, ASSUMPTIONS_PATH, TEX_PATH]
    for optional in [CHILD_MATH_PATH, CHILD_PHIL_PATH, CONFLICT_PATH, FUSION_PATH]:
        if optional.is_file():
            source_paths.append(optional)
    source_hashes = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in source_paths
    }
    report = {
        "schema_id": "universal_source_coupling_validation_v1",
        "artifact_id": "P7T05-UNIVERSAL-SOURCE-COUPLING-VALIDATION-V1",
        "task_id": "RT-20260728-004",
        "job_id": "AJ-RT-20260728-004-001",
        "plan_task_id": "P7-T05",
        "status": "PASS" if not failed else "FAIL",
        "result_status": "PRECISE_OBSTRUCTION_WITH_CONSTRUCTIVE_RESTRICTED_DOMAIN",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
        "source_hashes": source_hashes,
        "claim_boundary_summary": (
            "Explicitly equipped finite source reindexing and same-sector "
            "selection obstruction only; no physical coupling action stress "
            "energy cone metric equivalence principle GR proof or promotion."
        ),
        "proof_authority": False,
        "physics_promotion_authorized": False,
    }
    compact = {
        "schema_id": "universal_source_coupling_compact_receipt_v1",
        "artifact_id": "P7T05-UNIVERSAL-SOURCE-COUPLING-COMPACT-RECEIPT-V1",
        "task_id": "RT-20260728-004",
        "job_id": "AJ-RT-20260728-004-001",
        "status": report["status"],
        "result_status": report["result_status"],
        "candidate_id": "SourceUniversalCouplingMapCandidate_v1",
        "comparison_id": "ThreeAddressSupportCouplingMap_v1",
        "obstruction_id": "OBST-P7T05-SECTOR-COUPLING-FUNCTOR-NONSELECTION-001",
        "check_count": report["check_count"],
        "failed_check_count": report["failed_check_count"],
        "constructive_instance_count": len(instances) if isinstance(instances, list) else 0,
        "countermodel_state_count_each": 2,
        "countermodel_full_edge_counts": [2, 3],
        "no_fog": obstruction.get("no_fog") is True,
        "physical_matter_coupling_derived": False,
        "effective_geometry_derived": False,
        "global_no_go_claimed": False,
        "source_hashes": source_hashes,
        "claim_boundary_summary": report["claim_boundary_summary"],
    }

    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        COMPACT_PATH.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    output = compact if args.check else report
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(
            f"{report['status']} checks={report['check_count']} "
            f"failed={report['failed_check_count']}"
        )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
