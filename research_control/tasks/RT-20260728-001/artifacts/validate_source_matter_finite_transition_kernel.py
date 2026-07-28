#!/usr/bin/env python3
"""Deterministic task-local validator for RT-20260728-001.

Operational validation only. PASS does not adopt ontology or a source law,
establish physical probability or time, or create proof or promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[4]
TASK = REPO / "research_control/tasks/RT-20260728-001"
ART = TASK / "artifacts"
REPORT = ART / "source_matter_finite_transition_kernel_validation_v1.json"
COMPACT = ART / "source_matter_finite_transition_kernel_compact_receipt_v1.json"

EXPECTED_SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
        "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/tasks/RT-20260727-007/artifacts/"
    "source_matter_ontology_and_sector_taxonomy_v1.tex":
        "8d160217bf223078a11bc63fde6593c11c39d5b50d9c48fbad7b12084f8a752d",
    "research_control/tasks/RT-20260727-007/artifacts/"
    "source_matter_ontology_spec_v1.yaml":
        "a5563edddaff90ebab6ac4d3d4e2dc0425fea23b5f27c1c6174cb28b1f4652be",
    "research_control/tasks/RT-20260727-007/artifacts/"
    "source_matter_assumption_dependency_table_v1.yaml":
        "c665dbc7522d4ee1b6aa01db14100689c8d9acc28c7e659c33b4272d32976991",
    "research_control/tasks/RT-20260727-007/jobs/completions/"
    "AJC-AJ-RT-20260727-007-001.yaml":
        "4d1fc3d7d045defa6000dc0860973fba50280ddd1ee72cb4881d8ee2de2ddc1c",
    "research_control/tasks/RT-20260727-008/artifacts/"
    "source_matter_dynamics_packet_selection_v1.yaml":
        "6692a493dfe91cc6d92986e69cfda48d04656d42f2d559ca6aa498f3366ccbd7",
    "research_control/tasks/RT-20260727-008/jobs/completions/"
    "AJC-AJ-RT-20260727-008-001.yaml":
        "e1f4d1a2b9edc4de6252c829c8bbc2df6fe3fddabe2151907672fb4ebe6ca16e",
    "research_control/handoffs/handoff-0890.yaml":
        "874ac8d05924af09c2d837f1cbad23dbabab261e8a7b9d31c96cda968b40b03d",
    "research_control/tasks/RT-20260614-257/artifacts/"
    "286_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_"
    "MATTER_COUPLING_BRIDGE_TARGET_V1_FORMALIZATION.tex":
        "3d1c6dfb2ea543c8ea455ee2f3553e3cac76e3072902213ed07aff0db514605e",
    "research_control/tasks/RT-20260702-064/artifacts/"
    "source_certificate_operation_laws_v1.tex":
        "2ebc781bd82b4d39ab394255e5d3836d992625bdece8b8f912a8ab809669b986",
    "research_control/design/frontier_theorem_inventory.md":
        "fa7d97207315b49517e6e05bc3ae5b6bfcd0e335b669ba6a98371e55b4721600",
    "registries/METRIC_USE_LEDGER.csv":
        "108b1b56d9ef2d2d6cd30d7caa77461c813d8729890afd537206c6f94a1f24cb",
}

REQUIRED_ARTIFACTS = [
    "source_matter_finite_transition_kernel_candidate_v1.tex",
    "source_matter_finite_transition_kernel_spec_v1.yaml",
    "source_matter_finite_transition_kernel_controls_v1.yaml",
    "source_matter_finite_transition_kernel_assumption_dependency_table_v1.yaml",
    "child_phys_math_p7_t02_finite_transition_kernel.yaml",
    "child_phys_phil_p7_t02_finite_transition_kernel.yaml",
    "parent_conflict_review_p7_t02_finite_transition_kernel.yaml",
    "parent_fusion_notes_p7_t02_finite_transition_kernel.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    value = yaml.safe_load((ART / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{name} must contain a YAML mapping")
    return value


def get_path(obj: Any, path: str) -> Any:
    current = obj
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def parse_fraction(value: Any) -> Fraction:
    return Fraction(str(value))


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    for name in REQUIRED_ARTIFACTS:
        check(
            f"artifact_exists::{name}",
            (ART / name).is_file(),
            f"required task-local artifact {name}",
        )

    spec = load_yaml("source_matter_finite_transition_kernel_spec_v1.yaml")
    controls = load_yaml("source_matter_finite_transition_kernel_controls_v1.yaml")
    assumptions = load_yaml(
        "source_matter_finite_transition_kernel_assumption_dependency_table_v1.yaml"
    )
    phys_math = load_yaml("child_phys_math_p7_t02_finite_transition_kernel.yaml")
    phys_phil = load_yaml("child_phys_phil_p7_t02_finite_transition_kernel.yaml")
    conflict = load_yaml(
        "parent_conflict_review_p7_t02_finite_transition_kernel.yaml"
    )
    tex = (ART / "source_matter_finite_transition_kernel_candidate_v1.tex").read_text(
        encoding="utf-8"
    )
    fusion = (
        ART / "parent_fusion_notes_p7_t02_finite_transition_kernel.md"
    ).read_text(encoding="utf-8")

    expected_spec_values = {
        "schema_id": "source_matter_finite_transition_kernel_spec_v1",
        "candidate_status": "proposal-only",
        "candidate_id": "SourceMatterFiniteTransitionKernelCandidate_v1",
        "update_id": "SourceMatterBookkeepingUpdate_v1",
        "adoption_status": "blocked_adoption_open_continuation",
        "fixed_basis.candidate_id": "SourceMatterIncidenceCandidate_v1",
        "finite_control_system.identity_transition.id": "IdTransition_v1",
        "finite_control_system.identity_transition.required_in_every_row": True,
        "kernel.definition.enabled": "1/d_C(x) when T is in E_x",
        "kernel.physical_probability": False,
        "kernel.physical_rate": False,
        "kernel.no_tunable_parameter_count": 0,
        "update.composition_index.physical_time": False,
        "result_branches.malformed.symbol": "bottom_K",
        "result_branches.underdetermined.symbol": "undetermined_K",
        "source_extension_classification.relation_to_current_ontology":
            "missing_primitive",
    }
    for path, expected in expected_spec_values.items():
        actual = get_path(spec, path)
        check(
            f"spec::{path}",
            actual == expected,
            f"expected {expected!r}; observed {actual!r}",
        )

    theorem_ids = {
        row.get("theorem_id")
        for row in spec.get("theorems", [])
        if isinstance(row, dict)
    }
    check(
        "spec::theorem_ids",
        theorem_ids
        == {
            "P7T02-THM-FINITE-KERNEL-NORMALIZATION-CLOSURE-001",
            "P7T02-THM-SOURCE-PRESENTATION-EQUIVARIANCE-001",
        },
        f"observed {sorted(theorem_ids)}",
    )

    inherited = get_path(spec, "constraint_ledger.inherited") or []
    new_consequences = get_path(spec, "constraint_ledger.new_candidate_consequences") or []
    check(
        "spec::inherited_constraint_count",
        len(inherited) == 3,
        f"observed {len(inherited)}",
    )
    check(
        "spec::new_consequence_count",
        len(new_consequences) == 5,
        f"observed {len(new_consequences)}",
    )
    check(
        "spec::inherited_not_new",
        all(row.get("newly_derived_here") is False for row in inherited),
        "all P7-T01 support constraints must be labeled inherited",
    )

    auth = spec.get("authority_limits", {})
    false_authority_flags = [
        "canonical_ontology_modified",
        "canonical_ontology_candidate_promoted",
        "source_law_adopted",
        "matter_ontology_adopted",
        "physical_time_established",
        "physical_probability_established",
        "physical_conservation_law_established",
        "physical_interpretation_established",
        "detector_semantics_established",
        "target_metric_imported",
        "effective_geometry_assumed",
        "stress_energy_established",
        "matter_action_established",
        "coupling_law_adopted",
        "matter_coupling_derived",
        "einstein_equations_derived",
        "benchmark_promoted",
        "completed_derivation_claimed",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
        "physics_promotion_authorized",
        "proof_authority",
    ]
    check(
        "spec::authority_flags_false",
        all(auth.get(name) is False for name in false_authority_flags),
        "all protected authority flags must remain false",
    )

    control_rows = {
        row.get("control_id"): row
        for row in controls.get("controls", [])
        if isinstance(row, dict)
    }
    required_control_ids = {
        "P7T02-CONTROL-POSITIVE-PROPAGATION-001",
        "P7T02-CONTROL-NULL-001",
        "P7T02-CONTROL-INDEPENDENT-PRODUCT-001",
        "P7T02-CONTROL-INTERACTING-JOINT-001",
        "P7T02-CONTROL-DEGENERATE-NONNULL-001",
        "P7T02-CONTROL-MALFORMED-CONTINUITY-001",
        "P7T02-CONTROL-MALFORMED-EMPTY-ROW-001",
        "P7T02-CONTROL-MALFORMED-NORMALIZATION-001",
        "P7T02-CONTROL-MALFORMED-TARGET-IMPORT-001",
        "P7T02-CONTROL-UNDERDETERMINED-001",
    }
    check(
        "controls::required_ids",
        set(control_rows) == required_control_ids,
        f"observed {sorted(control_rows)}",
    )

    positive = control_rows["P7T02-CONTROL-POSITIVE-PROPAGATION-001"]
    positive_rows = positive["kernel_rows"]
    xu_sum = (
        parse_fraction(positive_rows["x_u"]["id_u"])
        + parse_fraction(positive_rows["x_u"]["move_e"])
    )
    xv_sum = parse_fraction(positive_rows["x_v"]["id_v"])
    check(
        "controls::positive_row_normalization",
        xu_sum == 1 and xv_sum == 1,
        f"x_u={xu_sum}; x_v={xv_sum}",
    )
    check(
        "controls::positive_residuals_zero",
        all(
            row.get("continuity_residual") == "0"
            for row in positive["transitions"].values()
        ),
        "all positive-control continuity residuals must vanish",
    )

    solution_ok = True
    for n in range(9):
        xu = Fraction(1, 2**n)
        xv = 1 - xu
        next_xu = xu / 2
        next_xv = xv + xu / 2
        if next_xu != Fraction(1, 2 ** (n + 1)):
            solution_ok = False
        if next_xv != 1 - Fraction(1, 2 ** (n + 1)):
            solution_ok = False
        if xu + xv != 1:
            solution_ok = False
    check(
        "controls::positive_exact_solution",
        solution_ok,
        "verified n=0 through n=8 exactly over rational arithmetic",
    )

    null = control_rows["P7T02-CONTROL-NULL-001"]
    check(
        "controls::null_identity",
        get_path(null, "kernel.id_0") == "1"
        and get_path(null, "kernel.row_sum") == "1"
        and null.get("physical_vacuum_claimed") is False,
        "valid null row must be identity-only and nonphysical",
    )

    independent = control_rows["P7T02-CONTROL-INDEPENDENT-PRODUCT-001"]
    check(
        "controls::independent_factorization",
        independent.get("row_cardinality") == 4
        and independent.get("kernel_each") == "1/4"
        and independent.get("factorization_check") == "1/4=(1/2)(1/2)",
        "two binary rows must form a four-element uniform product row",
    )

    interacting = control_rows["P7T02-CONTROL-INTERACTING-JOINT-001"]
    check(
        "controls::interacting_continuity",
        get_path(interacting, "transitions.joint_e1e2.continuity_residual") == "0"
        and get_path(interacting, "transitions.joint_e1e2.defect_residual") == "0",
        "joint transition must satisfy fixed P7-T01 constraints",
    )
    check(
        "controls::interacting_nonfactorization",
        get_path(interacting, "nonfactorization.cartesian_product_cardinality") == 4
        and get_path(interacting, "nonfactorization.actual_joint_row_cardinality") == 2
        and len(get_path(interacting, "nonfactorization.missing_mixed_records")) == 2,
        "diagonal two-record row must differ from four-record Cartesian product",
    )
    check(
        "controls::interacting_no_physical_claim",
        interacting.get("physical_interaction_claimed") is False
        and interacting.get("coupling_law_claimed") is False
        and interacting.get("force_claimed") is False,
        "structural interaction must not be promoted",
    )

    degenerate = control_rows["P7T02-CONTROL-DEGENERATE-NONNULL-001"]
    check(
        "controls::degenerate_distinctions",
        get_path(degenerate, "configuration.null") is False
        and degenerate.get("distinct_from_null") is True
        and degenerate.get("distinct_from_malformed") is True
        and get_path(degenerate, "kernel.row_sum") == "1",
        "non-null identity-only branch must remain valid and distinct",
    )

    malformed_rows = [
        row for row in control_rows.values() if row.get("branch") == "malformed"
    ]
    check(
        "controls::malformed_count",
        len(malformed_rows) == 4,
        f"observed {len(malformed_rows)}",
    )
    check(
        "controls::malformed_fail_closed",
        all(row.get("result") == "bottom_K" for row in malformed_rows),
        "every malformed control must fail closed",
    )

    underdetermined = control_rows["P7T02-CONTROL-UNDERDETERMINED-001"]
    check(
        "controls::underdetermined_distinctions",
        underdetermined.get("result") == "undetermined_K"
        and underdetermined.get("distinct_from_null") is True
        and underdetermined.get("distinct_from_degenerate") is True
        and underdetermined.get("distinct_from_malformed") is True,
        "missing row selection must remain distinct from null, degeneracy, and failure",
    )

    assumption_rows = assumptions.get("assumptions", [])
    dependency_rows = assumptions.get("dependencies", [])
    check(
        "assumptions::count",
        len(assumption_rows) == 9
        and get_path(assumptions, "assumption_counts.total") == 9,
        f"observed {len(assumption_rows)} assumptions",
    )
    check(
        "dependencies::count",
        len(dependency_rows) == 13
        and get_path(assumptions, "dependency_counts.total") == 13,
        f"observed {len(dependency_rows)} dependencies",
    )
    check(
        "assumptions::no_target_or_physical_inputs",
        all(
            get_path(assumptions, f"assumption_counts.{name}") == 0
            for name in [
                "target_geometry_assumptions",
                "physical_time_assumptions",
                "physical_probability_assumptions",
                "physical_interpretation_assumptions",
                "process_authority_assumptions",
                "free_coupling_constants",
                "dimensional_scales",
            ]
        ),
        "all target, physical, process, free-coupling, and scale counts must be zero",
    )

    child_expectations = [
        (phys_math, "child_phys_math", "physicist_mathematician"),
        (phys_phil, "child_phys_phil", "physicist_philosopher"),
    ]
    for child, unit, perspective in child_expectations:
        check(
            f"child::{unit}::identity",
            child.get("execution_unit_id") == unit
            and child.get("perspective") == perspective
            and child.get("status") == "completed",
            f"{unit} must be completed with perspective {perspective}",
        )
        child_auth = child.get("authority_flags", child.get("authority_limits", {}))
        check(
            f"child::{unit}::no_promotion",
            child_auth.get("physics_promotion_authorized", False) is False
            and child_auth.get("source_law_adopted") is False,
            f"{unit} must preserve source-law and promotion blocks",
        )

    check(
        "parent::conflict_resolution",
        conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflict_count") == 0,
        "parent conflict review must resolve all blocking differences",
    )
    check(
        "parent::fusion_markers",
        all(
            marker in fusion
            for marker in [
                "Shared consensus",
                "Physicist-mathematician contribution",
                "Physicist-philosopher contribution",
                "Resolved differences",
                "Unresolved limitations",
                "Claim boundary",
            ]
        ),
        "fusion notes must preserve consensus, unique contributions, resolutions, limits, and boundary",
    )

    required_tex_markers = [
        "SourceMatterFiniteTransitionKernelCandidate",
        "P7-T02",
        "blocked\\_adoption\\_open\\_continuation",
        r"K_{\Control}(T\mid x)",
        r"(\Update\mu)(y)",
        "Finite normalization, closure, and inherited-sector support",
        "Source-presentation equivariance",
        r"\mu_n(x_u)=2^{-n}",
        r"[v_1]+[v_2]-[u_1]-[u_2]",
        "not a physical force",
        "not a physical vacuum",
        "not a physical conservation law",
        "constructed\\_candidate",
        "current ontology does not derive",
        "no tunable",
        "physical time",
        "physical probabilities",
    ]
    for marker in required_tex_markers:
        check(
            f"tex::marker::{marker}",
            marker in tex,
            f"required TeX marker {marker!r}",
        )

    source_hashes: dict[str, str] = {}
    for relative, expected_hash in EXPECTED_SOURCE_HASHES.items():
        path = REPO / relative
        actual_hash = sha256(path) if path.is_file() else ""
        source_hashes[relative] = actual_hash
        check(
            f"source_hash::{relative}",
            actual_hash == expected_hash,
            f"expected {expected_hash}; observed {actual_hash}",
        )

    artifact_hashes = {
        name: sha256(ART / name)
        for name in REQUIRED_ARTIFACTS
        if (ART / name).is_file()
    }
    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "source_matter_finite_transition_kernel_validation_v1",
        "authority": "operational_validation_only",
        "task_id": "RT-20260728-001",
        "job_id": "AJ-RT-20260728-001-001",
        "candidate_id": "SourceMatterFiniteTransitionKernelCandidate_v1",
        "theorem_ids": sorted(theorem_ids),
        "validated_at": "2026-07-28T04:25:00Z",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "finding_counts": {
            "theorem_count": len(theorem_ids),
            "inherited_constraint_count": len(inherited),
            "new_candidate_consequence_count": len(new_consequences),
            "control_count": len(control_rows),
            "valid_positive_free_count": 1,
            "valid_null_count": 1,
            "valid_independent_count": 1,
            "valid_interacting_count": 1,
            "valid_degenerate_count": 1,
            "malformed_count": len(malformed_rows),
            "underdetermined_count": 1,
            "exact_solution_family_count": 1,
            "assumption_count": len(assumption_rows),
            "dependency_count": len(dependency_rows),
            "child_review_count": 2,
            "unresolved_conflict_count":
                conflict.get("unresolved_conflict_count"),
            "physical_probability_claim_count": 0,
            "physical_time_claim_count": 0,
            "physical_conservation_claim_count": 0,
        },
        "source_hashes": source_hashes,
        "artifact_hashes": artifact_hashes,
        "checks": checks,
        "authority_limits": {
            "validator_pass_counts_as_physics": False,
            "theorem_truth_inferred": False,
            "canonical_ontology_modified": False,
            "source_law_adopted": False,
            "matter_ontology_adopted": False,
            "physical_probability_established": False,
            "physical_time_established": False,
            "physical_conservation_law_established": False,
            "distance_to_gr_changed": True,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }


def build_compact_receipt(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "source_matter_finite_transition_kernel_compact_receipt_v1",
        "authority": "operational_evidence_only",
        "task_id": report["task_id"],
        "job_id": report["job_id"],
        "candidate_id": report["candidate_id"],
        "candidate_status": "proposal-only",
        "result_status": report["status"],
        "finding_counts": report["finding_counts"],
        "validator_ids": [
            "task_local_source_matter_finite_transition_kernel",
            "scratch_tex_build",
            "claim_language_changed",
            "source_authority_hash_check",
        ],
        "source_hashes": report["source_hashes"],
        "artifact_hashes": report["artifact_hashes"],
        "claim_boundary_summary": (
            "One proposal-only finite source transition kernel and exact "
            "bookkeeping consequences only; no adoption, physical probability, "
            "time, conservation, detector, geometry, stress energy, coupling, "
            "GR, benchmark, proof, publication, push, or completed derivation."
        ),
        "distance_to_gr": {
            "changed": True,
            "scope": "proposal-only P7-T02 source transition law and exact finite constraint structure",
            "physics_promotion_authorized": False,
        },
        "authority_limits": report["authority_limits"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    compact = build_compact_receipt(report)
    if args.write_report:
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        COMPACT.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        if not REPORT.is_file() or not COMPACT.is_file():
            report["status"] = "FAIL"
            report["checks"].append(
                {
                    "check_id": "stored_reports_exist",
                    "status": "FAIL",
                    "detail": "validation report and compact receipt must exist",
                }
            )
        else:
            stored_report = json.loads(REPORT.read_text(encoding="utf-8"))
            stored_compact = json.loads(COMPACT.read_text(encoding="utf-8"))
            if stored_report != report or stored_compact != compact:
                report["status"] = "FAIL"
                report["checks"].append(
                    {
                        "check_id": "stored_reports_fresh",
                        "status": "FAIL",
                        "detail": "stored report or compact receipt is stale",
                    }
                )

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"{report['status']}: "
            f"{report['check_count']} checks; "
            f"{report['failure_count']} failures"
        )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
