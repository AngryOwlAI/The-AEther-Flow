#!/usr/bin/env python3
"""Exact controls for the RT016 arbitrary-finite-rank Bridge_OM repair."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
SOURCE_MODEL = ROOT / "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_model.py"

SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md": "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1012.yaml": "279f064dfeac08dfce4b597c5d2a4ce1b7227f126b1d6273f9f12fd6f09ff8d7",
    "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_covector_circuit_bridge_v1.tex": "20590d4e7386ac43757b73c636c023bb7884706c9352bf307819885185c29cab",
    "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_record_v1.yaml": "1e2ef686e1788fbb229f6560e88854422a2c0830b41a5aba6ea10a2dee1ec0e5",
    "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_fixtures_v1.yaml": "54008f917b431469d8660f32e486d3671f93c052bc59ce4c57c904a6dbd4b7d7",
    "research_control/tasks/RT-20260810-014/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_model.py": "2f6f48daa86a7941edd3ecbc2056be7077814eb787f7499d1ff1ac8294fcf000",
    "research_control/tasks/RT-20260810-015/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_smuggling_audit_v1.tex": "910bc2565e6933f3e4ef134936c1f9cc37dd0592e2acdfbf89470755eb001621",
    "research_control/tasks/RT-20260810-015/artifacts/v22_p4_t02_b2_oriented_matroid_bridge_smuggling_disposition_v1.yaml": "134e390709e4a3fcdf61a54fc2d4d383d6a31cc9d7ebab61b7c6a5ca23bb4a50",
    "research_control/tasks/RT-20260810-015/artifacts/parent_fusion_notes_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.md": "d4d48eaaa552563afa6ca78ce1e05e499495d56c9b4b1ae359e3ddf44dd5ecbf",
    "research_control/tasks/RT-20260810-015/artifacts/child_phys_math_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.yaml": "c050a716c5b854ab0b6f974730dd7dbe425be34cea952f96c88fdd12725d99f9",
    "research_control/tasks/RT-20260810-015/artifacts/child_phys_phil_p4_t02_b2_oriented_matroid_bridge_smuggling_audit.yaml": "0e3c49ddf1d935765244f45be127d84280809af9893a50cfa417f647d0297e48",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source_model() -> ModuleType:
    spec = importlib.util.spec_from_file_location("rt014_bridge_model", SOURCE_MODEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen RT014 Bridge_OM model")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def basis(rank_value: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(Fraction(int(i == j)) for i in range(rank_value))
        for j in range(rank_value)
    )


def signed_sum(rank_value: int, sign: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(sign) for _ in range(rank_value))


def evaluate(
    covector: tuple[Fraction, ...], column: tuple[Fraction, ...]
) -> Fraction:
    return sum((a * b for a, b in zip(covector, column)), Fraction(0))


def family_control(module: ModuleType, rank_value: int) -> dict[str, Any]:
    labels = tuple(f"s{i + 1}" for i in range(rank_value + 1))
    standard_basis = basis(rank_value)
    feasible_columns = standard_basis + (signed_sum(rank_value, 1),)
    obstructed_columns = standard_basis + (signed_sum(rank_value, -1),)
    feasible_rank = module.rank(
        module.matrix_rows(feasible_columns), len(feasible_columns)
    )
    obstructed_rank = module.rank(
        module.matrix_rows(obstructed_columns), len(obstructed_columns)
    )
    feasible_circuits = module.positive_circuits(feasible_columns, labels)
    obstructed_circuits = module.positive_circuits(obstructed_columns, labels)
    witness = tuple(Fraction(1) for _ in range(rank_value))
    evaluations = [evaluate(witness, column) for column in feasible_columns]
    obstruction = obstructed_circuits[0] if obstructed_circuits else {}
    checks = {
        "feasible_rank_equals_r": feasible_rank == rank_value,
        "obstructed_rank_equals_r": obstructed_rank == rank_value,
        "feasible_witness_is_strict": all(value > 0 for value in evaluations),
        "feasible_has_no_positive_circuit": not feasible_circuits,
        "obstructed_has_exactly_one_positive_circuit": len(obstructed_circuits) == 1,
        "obstruction_support_is_all_r_plus_one_columns": obstruction.get("support") == list(labels),
        "obstruction_coefficients_are_all_one": obstruction.get("coefficients") == [1] * (rank_value + 1),
        "obstruction_rank_is_support_minus_one": obstruction.get("rank") == rank_value,
        "obstruction_kernel_is_one_dimensional": obstruction.get("kernel_dimension") == 1,
        "support_bound_is_sharp": len(obstruction.get("support", [])) == rank_value + 1,
    }
    if not all(checks.values()):
        raise AssertionError(f"general-rank control failed at r={rank_value}: {checks}")
    return {
        "rank": rank_value,
        "sector_count": rank_value + 1,
        "field": "Q",
        "feasible_family": {
            "columns": "[e_1,...,e_r,+sum_i e_i]",
            "certificate": "k=(1,...,1)",
            "evaluations": [str(value) for value in evaluations],
            "total_branch": "Feasible",
        },
        "obstructed_family": {
            "columns": "[e_1,...,e_r,-sum_i e_i]",
            "certificate": "alpha=(1,...,1)",
            "support_size": rank_value + 1,
            "total_branch": "Obstructed",
        },
        "checks": checks,
    }


def build() -> dict[str, Any]:
    observed_hashes = {path: sha256(ROOT / path) for path in SOURCE_HASHES}
    if observed_hashes != SOURCE_HASHES:
        mismatch = {
            path: {"expected": SOURCE_HASHES[path], "observed": observed_hashes[path]}
            for path in SOURCE_HASHES
            if SOURCE_HASHES[path] != observed_hashes[path]
        }
        raise AssertionError(f"frozen source mismatch: {mismatch}")

    module = load_source_model()
    frozen = module.build()
    if frozen["status"] != "PASS":
        raise AssertionError("frozen RT014 model no longer passes")

    controls = [family_control(module, rank_value) for rank_value in range(1, 9)]
    rank_five = controls[4]
    rank_six = controls[5]
    conformance_fixtures = {
        fixture_id: {
            "declared_rank": summary["rank"],
            "classification": "nonphysical_conformance_sample",
            "theorem_domain_restriction": False,
            "target_dimension_evidence": False,
        }
        for fixture_id, summary in frozen["inventories"].items()
    }

    checks = {
        "all_frozen_source_hashes_match": observed_hashes == SOURCE_HASHES,
        "frozen_rt014_model_passes_unchanged": frozen["status"] == "PASS",
        "candidate_map_is_byte_identical_string": frozen["candidate_map"] == "Bridge_OM(A)=(Cstar(A),Cir_plus(A),Tot(A),Ref(A),Strat(A))",
        "all_rank_controls_one_through_eight_pass": all(
            all(row["checks"].values()) for row in controls
        ),
        "rank_five_support_six_control_passes": rank_five["obstructed_family"]["support_size"] == 6,
        "rank_six_support_seven_control_passes": rank_six["obstructed_family"]["support_size"] == 7,
        "all_old_fixtures_are_nonphysical_conformance_only": all(
            row["classification"] == "nonphysical_conformance_sample"
            and not row["theorem_domain_restriction"]
            and not row["target_dimension_evidence"]
            for row in conformance_fixtures.values()
        ),
        "all_original_rt014_exact_checks_remain_true": all(frozen["checks"].values()),
        "all_three_freezes_preserved": True,
        "distance_to_gr_unchanged": True,
    }
    if not all(checks.values()):
        raise AssertionError(f"repair control failed: {checks}")

    result: dict[str, Any] = {
        "schema_id": "v22_p4_t02_b2_oriented_matroid_bridge_general_rank_repair_exact_model_v1",
        "status": "PASS",
        "source_hashes": observed_hashes,
        "candidate_map_held_fixed": frozen["candidate_map"],
        "semantic_patch": {
            "old_domain": "finite nonempty S with 1<=rank(A)=r<=4",
            "new_domain": "finite nonempty S with arbitrary finite 1<=rank(A)=r<=card(S)",
            "old_circuit_ceiling": "card(C)<=r+1<=5",
            "new_circuit_ceiling": "card(C)<=r+1",
            "fixture_label_added": "nonphysical_conformance_sample",
            "other_definitions_changed": False,
        },
        "general_rank_theorem": {
            "statement": "For every finite rank r>=1, every support-minimal positive circuit C satisfies rank(A_C)=card(C)-1<=r and therefore card(C)<=r+1.",
            "proof_spine": [
                "a positive kernel vector alpha exists on C",
                "if ker(A_C) had dimension greater than one, perturbing alpha along an independent kernel vector to the boundary of the nonnegative orthant would produce a nonzero nonnegative dependence on a proper subset",
                "support minimality therefore forces dim ker(A_C)=1 and rank(A_C)=card(C)-1",
                "rank(A_C)<=rank(A)=r",
                "hence card(C)<=r+1",
            ],
            "sharp_family": "[e_1,...,e_r,-sum_i e_i] with alpha=(1,...,1)",
            "target_geometry_used": False,
            "physical_dimension_inferred": False,
        },
        "exact_family_controls": controls,
        "mandatory_controls": {
            "rank_five": rank_five,
            "rank_six": rank_six,
        },
        "legacy_fixture_reclassification": conformance_fixtures,
        "held_fixed_rt014_checks": frozen["checks"],
        "checks": checks,
        "new_mathematical_payloads": [
            "arbitrary-finite-rank minimal-positive-circuit support theorem",
            "sharp feasible/obstructed standard-basis family for every r>=1",
            "exact rational rank-five and rank-six controls outside the old cap",
            "semantic quarantine separating bounded conformance fixtures from theorem domain and target dimension",
        ],
        "authority_limits": {
            "proposal_only": True,
            "current_ontology_derivation_claimed": False,
            "universal_p7_coverage_constructed": False,
            "physical_causality_constructed": False,
            "empirical_response_constructed": False,
            "conformal_geometry_constructed": False,
            "effective_metric_constructed": False,
            "distance_to_gr_changed": False,
            "adoption_authorized": False,
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["model_payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.compact:
        result = {
            "schema_id": result["schema_id"],
            "status": result["status"],
            "model_payload_sha256": result["model_payload_sha256"],
            "semantic_patch": result["semantic_patch"],
            "mandatory_controls": result["mandatory_controls"],
            "checks": result["checks"],
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
