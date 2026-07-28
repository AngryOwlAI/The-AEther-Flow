#!/usr/bin/env python3
"""Deterministic task-local validator for RT-20260728-002.

Operational validation only. PASS does not adopt ontology, source laws, or
operational semantics and does not establish physical clocks, rods, signals,
detectors, free fall, geometry, coupling, proof, or promotion authority.
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
TASK = REPO / "research_control/tasks/RT-20260728-002"
ART = TASK / "artifacts"
REPORT = ART / "source_operational_device_validation_v1.json"
COMPACT = ART / "source_operational_device_compact_receipt_v1.json"

EXPECTED_SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
        "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/tasks/RT-20260727-007/artifacts/"
    "source_matter_ontology_and_sector_taxonomy_v1.tex":
        "8d160217bf223078a11bc63fde6593c11c39d5b50d9c48fbad7b12084f8a752d",
    "research_control/tasks/RT-20260727-007/artifacts/"
    "source_matter_ontology_spec_v1.yaml":
        "a5563edddaff90ebab6ac4d3d4e2dc0425fea23b5f27c1c6174cb28b1f4652be",
    "research_control/tasks/RT-20260728-001/artifacts/"
    "source_matter_finite_transition_kernel_candidate_v1.tex":
        "65ac095f5cdf4c2e319365c8b0e024d031b19d9fc2b8102e59997afa1e8f9129",
    "research_control/tasks/RT-20260728-001/artifacts/"
    "source_matter_finite_transition_kernel_spec_v1.yaml":
        "936d2aa6dfea3d263675468ff581190240efde84c1241ad971a8c1383a065a97",
    "research_control/tasks/RT-20260728-001/artifacts/"
    "source_matter_finite_transition_kernel_controls_v1.yaml":
        "af7fc976590b4ca82fca5c34c6f30091f6599428b8005cf3932ce03f92f7d779",
    "research_control/tasks/RT-20260728-001/jobs/completions/"
    "AJC-AJ-RT-20260728-001-001.yaml":
        "0355c30c700cd5a8a7c35e81bd2d0b3f833efa8be99be00946734988dd570c3d",
    "research_control/handoffs/handoff-0891.yaml":
        "690197127ce9df4c2eaf9f706646a34212a2421df25e49c35cc374badd31353b",
    "research_control/design/frontier_theorem_inventory.md":
        "fa7d97207315b49517e6e05bc3ae5b6bfcd0e335b669ba6a98371e55b4721600",
    "registries/METRIC_USE_LEDGER.csv":
        "108b1b56d9ef2d2d6cd30d7caa77461c813d8729890afd537206c6f94a1f24cb",
    "research_control/tasks/RT-20260614-257/artifacts/"
    "286_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_"
    "MATTER_COUPLING_BRIDGE_TARGET_V1_FORMALIZATION.tex":
        "3d1c6dfb2ea543c8ea455ee2f3553e3cac76e3072902213ed07aff0db514605e",
    "research_control/tasks/RT-20260702-064/artifacts/"
    "source_certificate_operation_laws_v1.tex":
        "2ebc781bd82b4d39ab394255e5d3836d992625bdece8b8f912a8ab809669b986",
}

REQUIRED_ARTIFACTS = [
    "source_operational_device_suite_candidate_v1.tex",
    "source_operational_device_suite_spec_v1.yaml",
    "source_operational_device_controls_v1.yaml",
    "source_operational_device_assumption_dependency_table_v1.yaml",
    "child_phys_math_p7_t03_operational_devices.yaml",
    "child_phys_phil_p7_t03_operational_devices.yaml",
    "parent_conflict_review_p7_t03_operational_devices.yaml",
    "parent_fusion_notes_p7_t03_operational_devices.md",
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
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def fraction(value: Any) -> Fraction:
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

    spec = load_yaml("source_operational_device_suite_spec_v1.yaml")
    controls = load_yaml("source_operational_device_controls_v1.yaml")
    assumptions = load_yaml(
        "source_operational_device_assumption_dependency_table_v1.yaml"
    )
    phys_math = load_yaml("child_phys_math_p7_t03_operational_devices.yaml")
    phys_phil = load_yaml("child_phys_phil_p7_t03_operational_devices.yaml")
    conflict = load_yaml("parent_conflict_review_p7_t03_operational_devices.yaml")
    tex = (ART / "source_operational_device_suite_candidate_v1.tex").read_text(
        encoding="utf-8"
    )
    fusion = (
        ART / "parent_fusion_notes_p7_t03_operational_devices.md"
    ).read_text(encoding="utf-8")

    expected_spec_values = {
        "schema_id": "source_operational_device_suite_spec_v1",
        "candidate_status": "proposal-only",
        "candidate_id": "SourceOperationalDeviceSuiteCandidate_v1",
        "response_id": "SourceOperationalResponseTrace_v1",
        "adoption_status": "blocked_adoption_open_continuation",
        "fixed_basis.source_matter_candidate_id": "SourceMatterIncidenceCandidate_v1",
        "fixed_basis.transition_kernel_candidate_id":
            "SourceMatterFiniteTransitionKernelCandidate_v1",
        "protocol_type.name": "finite source operational protocol",
        "protocol_type.fields.r.target_observable_input": False,
        "formal_histories.response.codomain": "Q_nonnegative",
        "result_branches.malformed.symbol": "bottom_D",
        "result_branches.underdetermined.symbol": "undetermined_D",
        "result_branches.cross_device_inconsistent.symbol": "inconsistent_D",
        "source_extension_classification.relation_to_current_ontology":
            "not_derived",
    }
    for path, expected in expected_spec_values.items():
        actual = get_path(spec, path)
        check(
            f"spec::{path}",
            actual == expected,
            f"expected {expected!r}; observed {actual!r}",
        )

    device_roles = spec.get("device_roles", {})
    required_roles = {
        "Clock_src",
        "Rod_src",
        "Signal_src",
        "Detector_src",
        "FreeFall_src",
    }
    check(
        "spec::five_device_roles",
        set(device_roles) == required_roles,
        f"observed {sorted(device_roles)}",
    )
    for role in sorted(required_roles):
        record = device_roles.get(role, {})
        check(
            f"spec::device::{role}::complete",
            all(record.get(field) for field in ["source_subsystem", "preparation",
                                                 "evolution", "readout", "success",
                                                 "failure", "comparison"])
            and len(record.get("prohibited_meanings", [])) >= 4,
            f"{role} must declare all protocol fields and guarded meanings",
        )

    theorem_ids = {
        row.get("theorem_id")
        for row in spec.get("theorems", [])
        if isinstance(row, dict)
    }
    required_theorems = {
        "P7T03-THM-FINITE-TOKEN-RESPONSE-CLOSURE-001",
        "P7T03-THM-SOURCE-PRESENTATION-NATURALITY-001",
    }
    check(
        "spec::theorem_ids",
        theorem_ids == required_theorems,
        f"observed {sorted(theorem_ids)}",
    )
    check(
        "spec::independent_systems",
        get_path(spec, "independent_systems.first.device_role") == "Clock_src"
        and get_path(spec, "independent_systems.second.device_role") == "Signal_src"
        and get_path(spec, "independent_systems.empirical_independence_claimed")
        is False,
        "Clock_src and Signal_src must be declared independent source systems",
    )
    check(
        "spec::cross_device_contracts",
        len(spec.get("cross_device_contracts", [])) == 3,
        "three explicit cross-device contracts are required",
    )

    auth = spec.get("authority_limits", {})
    false_authority_flags = [
        "canonical_ontology_modified",
        "canonical_ontology_candidate_promoted",
        "source_law_adopted",
        "matter_ontology_adopted",
        "operational_semantics_adopted",
        "physical_clock_established",
        "physical_rod_established",
        "physical_signal_established",
        "physical_detector_established",
        "physical_free_fall_established",
        "physical_time_established",
        "physical_length_established",
        "physical_causality_established",
        "physical_probability_established",
        "physical_conservation_law_established",
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

    rows = {
        row.get("control_id"): row
        for row in controls.get("controls", [])
        if isinstance(row, dict)
    }
    required_control_ids = {
        "P7T03-CONTROL-CLOCK-TWO-STATE-001",
        "P7T03-CONTROL-ROD-ADDRESS-CHAIN-001",
        "P7T03-CONTROL-SIGNAL-CHAIN-001",
        "P7T03-CONTROL-DETECTOR-TRANSDUCER-001",
        "P7T03-CONTROL-FREEFALL-BASELINE-INTERVENTION-001",
        "P7T03-CONTROL-INDEPENDENT-CLOCK-SIGNAL-001",
        "P7T03-CONTROL-NULL-NO-EVENT-001",
        "P7T03-CONTROL-MALFORMED-PARTIAL-READOUT-001",
        "P7T03-CONTROL-MALFORMED-TOKEN-OUTSIDE-ALPHABET-001",
        "P7T03-CONTROL-MALFORMED-TARGET-IMPORT-001",
        "P7T03-CONTROL-UNDERDETERMINED-READOUT-001",
        "P7T03-CONTROL-CROSS-DEVICE-INCONSISTENT-001",
    }
    check(
        "controls::required_ids",
        set(rows) == required_control_ids,
        f"observed {sorted(rows)}",
    )

    clock = rows["P7T03-CONTROL-CLOCK-TWO-STATE-001"]
    check(
        "controls::clock_response",
        fraction(get_path(clock, "exact_response.tick_1")) == Fraction(1, 4)
        and fraction(get_path(clock, "exact_response.idle_2")) == Fraction(3, 4)
        and fraction(get_path(clock, "exact_response.sum")) == 1,
        "clock token response must be exactly 1/4 plus 3/4",
    )
    for control_id, success_path, failure_path in [
        ("P7T03-CONTROL-ROD-ADDRESS-CHAIN-001",
         "exact_response.endpoint_2", "exact_response.not_endpoint_2"),
        ("P7T03-CONTROL-SIGNAL-CHAIN-001",
         "exact_response.arrived_2", "exact_response.not_arrived_2"),
        ("P7T03-CONTROL-DETECTOR-TRANSDUCER-001",
         "exact_response.triggered_2", "exact_response.ready_2"),
    ]:
        row = rows[control_id]
        check(
            f"controls::{control_id}::response",
            fraction(get_path(row, success_path)) == Fraction(1, 4)
            and fraction(get_path(row, failure_path)) == Fraction(3, 4)
            and fraction(get_path(row, "exact_response.sum")) == 1,
            f"{control_id} response must be exactly 1/4 plus 3/4",
        )

    detector = rows["P7T03-CONTROL-DETECTOR-TRANSDUCER-001"]
    check(
        "controls::signal_detector_agreement",
        detector.get("cross_device_result")
        == "R_signal(arrived_2)=R_detector(triggered_2)=1/4",
        "paired source-history responses must agree exactly",
    )

    freefall = rows["P7T03-CONTROL-FREEFALL-BASELINE-INTERVENTION-001"]
    differences = get_path(
        freefall, "exact_response.difference_i_minus_baseline"
    )
    check(
        "controls::intervention_difference",
        fraction(differences["address_f0"]) == Fraction(1, 2)
        and fraction(differences["address_f1"]) == Fraction(-1, 2)
        and fraction(differences["sum"]) == 0,
        "formal intervention difference must be +1/2 and -1/2",
    )

    independent = rows["P7T03-CONTROL-INDEPENDENT-CLOCK-SIGNAL-001"]
    check(
        "controls::independent_factorization",
        fraction(get_path(independent, "marginal_responses.tick_1"))
        == Fraction(1, 4)
        and fraction(get_path(independent, "marginal_responses.arrived_2"))
        == Fraction(1, 4)
        and fraction(get_path(independent, "joint_response.value"))
        == Fraction(1, 16)
        and independent.get("physical_independence_claimed") is False,
        "joint response must be exact formal product 1/16",
    )

    no_event = rows["P7T03-CONTROL-NULL-NO-EVENT-001"]
    check(
        "controls::valid_no_event",
        fraction(get_path(no_event, "exact_response.no_event_3")) == 1
        and no_event.get("physical_vacuum_claimed") is False
        and no_event.get("physical_stasis_claimed") is False,
        "identity-only no-event branch must remain valid and nonphysical",
    )

    malformed = [row for row in rows.values() if row.get("branch") == "malformed"]
    check(
        "controls::malformed_count",
        len(malformed) == 3,
        f"observed {len(malformed)}",
    )
    check(
        "controls::malformed_fail_closed",
        all(row.get("result") == "bottom_D" for row in malformed),
        "every malformed protocol must fail closed",
    )

    underdetermined = rows["P7T03-CONTROL-UNDERDETERMINED-READOUT-001"]
    check(
        "controls::underdetermined_distinctions",
        underdetermined.get("result") == "undetermined_D"
        and underdetermined.get("distinct_from_no_event") is True
        and underdetermined.get("distinct_from_malformed") is True,
        "missing readout data must remain distinct from no-event and malformed",
    )

    inconsistent = rows["P7T03-CONTROL-CROSS-DEVICE-INCONSISTENT-001"]
    check(
        "controls::cross_device_inconsistent",
        fraction(inconsistent.get("signal_arrival_response")) == Fraction(1, 4)
        and fraction(inconsistent.get("attempted_detector_trigger_response"))
        == Fraction(3, 4)
        and inconsistent.get("result") == "inconsistent_D"
        and inconsistent.get("physical_falsification_claimed") is False,
        "paired 1/4 and 3/4 responses must fail only the formal contract",
    )

    assumption_rows = assumptions.get("assumptions", [])
    dependency_rows = assumptions.get("dependencies", [])
    check(
        "assumptions::count",
        len(assumption_rows) == 9
        and get_path(assumptions, "assumption_counts.total") == 9,
        f"observed {len(assumption_rows)}",
    )
    check(
        "dependencies::count",
        len(dependency_rows) == 14
        and get_path(assumptions, "dependency_counts.total") == 14,
        f"observed {len(dependency_rows)}",
    )
    zero_assumption_fields = [
        "target_geometry_assumptions",
        "proper_time_assumptions",
        "physical_length_assumptions",
        "physical_causality_assumptions",
        "physical_probability_assumptions",
        "empirical_detector_assumptions",
        "physical_free_fall_assumptions",
        "process_authority_assumptions",
        "free_coupling_constants",
        "dimensional_scales",
    ]
    check(
        "assumptions::no_target_or_physical_inputs",
        all(
            get_path(assumptions, f"assumption_counts.{name}") == 0
            for name in zero_assumption_fields
        ),
        "all target empirical physical process free-coupling and scale counts must be zero",
    )
    check(
        "assumptions::new_consequence_count",
        len(assumptions.get("new_candidate_consequences", [])) == 6,
        "six materially new candidate-level consequences are required",
    )

    for child, unit, perspective in [
        (phys_math, "child_phys_math", "physicist_mathematician"),
        (phys_phil, "child_phys_phil", "physicist_philosopher"),
    ]:
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
            and child_auth.get("source_law_adopted", False) is False,
            f"{unit} must preserve source-law and promotion blocks",
        )

    check(
        "parent::conflict_resolution",
        conflict.get("status") == "resolved"
        and conflict.get("unresolved_conflict_count") == 0,
        "parent conflict review must resolve every blocking difference",
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
        "fusion notes must preserve consensus contributions resolutions limits and boundary",
    )

    required_tex_markers = [
        "SourceOperationalDeviceSuiteCandidate",
        "P7-T03",
        "blocked\\_adoption\\_open\\_continuation",
        r"\Device=(\Control,P,I,\Tokens,r,S,F)",
        r"\Response_{\Device,p,i,n}(a)",
        "Finite token-response closure and partition",
        "Source-presentation naturality",
        r"R(\mathsf{tick}_1)=\frac14",
        r"R_{\mathrm{joint}}",
        r"\frac1{16}",
        "not proper",
        "not physical length",
        "not a causal signal",
        "not empirical detection",
        "not gravitational free fall",
        "constructed\\_candidate",
        "current ontology does not derive",
        "physical probabilities",
        "common physical propagation",
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
        "schema_id": "source_operational_device_validation_v1",
        "authority": "operational_validation_only",
        "task_id": "RT-20260728-002",
        "job_id": "AJ-RT-20260728-002-001",
        "candidate_id": "SourceOperationalDeviceSuiteCandidate_v1",
        "theorem_ids": sorted(theorem_ids),
        "validated_at": "2026-07-28T05:45:00Z",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "finding_counts": {
            "theorem_count": len(theorem_ids),
            "device_role_count": len(device_roles),
            "control_count": len(rows),
            "valid_positive_count": 5,
            "valid_independent_count": 1,
            "valid_no_event_count": 1,
            "malformed_count": len(malformed),
            "underdetermined_count": 1,
            "cross_device_inconsistent_count": 1,
            "independent_operational_system_count": 2,
            "cross_device_contract_count":
                len(spec.get("cross_device_contracts", [])),
            "assumption_count": len(assumption_rows),
            "dependency_count": len(dependency_rows),
            "child_review_count": 2,
            "unresolved_conflict_count":
                conflict.get("unresolved_conflict_count"),
            "physical_interpretation_claim_count": 0,
        },
        "source_hashes": source_hashes,
        "artifact_hashes": artifact_hashes,
        "checks": checks,
        "authority_limits": {
            "validator_pass_counts_as_physics": False,
            "theorem_truth_inferred": False,
            "canonical_ontology_modified": False,
            "source_law_adopted": False,
            "operational_semantics_adopted": False,
            "physical_time_established": False,
            "physical_length_established": False,
            "physical_causality_established": False,
            "physical_probability_established": False,
            "physical_detector_established": False,
            "physical_free_fall_established": False,
            "distance_to_gr_changed": True,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }


def build_compact_receipt(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "source_operational_device_compact_receipt_v1",
        "authority": "operational_evidence_only",
        "task_id": report["task_id"],
        "job_id": report["job_id"],
        "candidate_id": report["candidate_id"],
        "candidate_status": "proposal-only",
        "result_status": report["status"],
        "finding_counts": report["finding_counts"],
        "validator_ids": [
            "task_local_source_operational_device_suite",
            "scratch_tex_build",
            "claim_language_changed",
            "source_authority_hash_check",
        ],
        "source_hashes": report["source_hashes"],
        "artifact_hashes": report["artifact_hashes"],
        "claim_boundary_summary": (
            "One proposal-only finite source operational-device suite and exact "
            "formal token consequences only; no adoption, physical clock, rod, "
            "signal, detector, free fall, time, length, causality, probability, "
            "geometry, coupling, GR, benchmark, proof, publication, push, or "
            "completed derivation."
        ),
        "distance_to_gr": {
            "changed": True,
            "scope": "proposal-only P7-T03 source operational-device and formal response sub-burden",
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
