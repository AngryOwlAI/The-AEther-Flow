#!/usr/bin/env python3
"""Focused validation for RT-20260809-023."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

import yaml


REPO = pathlib.Path(__file__).resolve().parents[4]
ARTIFACTS = REPO / "research_control/tasks/RT-20260809-023/artifacts"
REPORT = ARTIFACTS / "v22_p4_t02_b2_descriptor_construction_validation.json"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((ARTIFACTS / name).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, evidence: Any) -> None:
        checks.append({"check_id": check_id, "passed": bool(condition), "evidence": evidence})

    required_files = [
        "v22_p4_t02_b2_equipped_chain_descriptor_attempt_v1.tex",
        "v22_p4_t02_b2_equipped_chain_descriptor_population_v1.yaml",
        "v22_p4_t02_b2_atomic_obligation_construction_matrix_v1.yaml",
        "v22_p4_t02_b2_source_factorization_provenance_v1.yaml",
        "v22_p4_t02_b2_explicit_unit_cocycle_v1.yaml",
        "v22_p4_t02_b2_d7_separation_obstruction_v1.yaml",
        "v22_p4_t02_b2_descriptor_construction_model.py",
        "child_phys_math_p4_t02_b2_descriptor_construction.yaml",
        "child_phys_phil_p4_t02_b2_descriptor_construction.yaml",
        "parent_conflict_review_p4_t02_b2_descriptor_construction.yaml",
        "parent_fusion_notes_p4_t02_b2_descriptor_construction.md",
    ]
    for name in required_files:
        check(f"file_exists:{name}", (ARTIFACTS / name).is_file(), name)

    population = load_yaml("v22_p4_t02_b2_equipped_chain_descriptor_population_v1.yaml")
    obligations = load_yaml("v22_p4_t02_b2_atomic_obligation_construction_matrix_v1.yaml")
    provenance = load_yaml("v22_p4_t02_b2_source_factorization_provenance_v1.yaml")
    cocycle = load_yaml("v22_p4_t02_b2_explicit_unit_cocycle_v1.yaml")
    obstruction = load_yaml("v22_p4_t02_b2_d7_separation_obstruction_v1.yaml")

    expected_population = {
        "descriptor_component_count": 10,
        "populated_component_slot_count": 10,
        "fully_evidenced_component_count": 9,
        "populated_but_blocked_component_count": 1,
        "atomic_obligation_count": 35,
        "discharged_obligation_count": 33,
        "blocked_obligation_count": 2,
    }
    for field, expected in expected_population.items():
        actual = population["population_summary"].get(field)
        check(f"population:{field}", actual == expected, {"expected": expected, "actual": actual})
    check(
        "population:result_type",
        population["decisive_result"]["result_type"] == "precise_obstruction",
        population["decisive_result"]["result_type"],
    )
    check(
        "population:blocked_ids",
        population["population_summary"]["descriptor_instance_failure_obligations"] == ["D7-O2", "D7-O4"],
        population["population_summary"]["descriptor_instance_failure_obligations"],
    )
    check("population:not_complete", population["population_summary"]["descriptor_instance_complete"] is False, False)
    check("population:no_adequacy", population["population_summary"]["adequacy_reevaluated"] is False, False)
    check("population:no_activation", population["population_summary"]["b2_activated"] is False, False)
    check("population:p4_t03_locked", population["population_summary"]["p4_t03_unlocked"] is False, False)

    components = population["formal_descriptor"]["ordered_components"]
    component_ids = [row["component_id"] for row in components]
    expected_component_ids = [
        "D0_SECTOR_SET",
        "D1_CONTINUUM_FIELDS",
        "D2_FINITE_TO_CONTINUUM_LIFT",
        "D3_SOURCE_QUOTIENT",
        "D3_OUTPUT_QUOTIENT",
        "D4_SECTOR_EQUATIONS",
        "D5_COMPATIBILITY_RELATION",
        "D5_COMMON_PRINCIPAL_TARGET",
        "D6_OPERATIONAL_NO_TARGET_RECEIPT",
        "D7_ADEQUACY_PROCEDURE",
    ]
    check("population:component_order", component_ids == expected_component_ids, component_ids)

    flat_obligations = [
        row
        for family in obligations["families"]
        for row in family["obligations"]
    ]
    obligation_ids = [row["obligation_id"] for row in flat_obligations]
    blocked_ids = [
        row["obligation_id"]
        for row in flat_obligations
        if row["status"] == "blocked_by_active_claim_boundary"
    ]
    discharged_ids = [
        row["obligation_id"]
        for row in flat_obligations
        if row["status"] == "discharged_proposal_only"
    ]
    check("obligations:unique_35", len(obligation_ids) == 35 and len(set(obligation_ids)) == 35, len(obligation_ids))
    check("obligations:discharged_33", len(discharged_ids) == 33, len(discharged_ids))
    check("obligations:blocked_2", blocked_ids == ["D7-O2", "D7-O4"], blocked_ids)
    check("obligations:matrix_counts", obligations["discharged_count"] == 33 and obligations["blocked_count"] == 2, {"discharged": obligations["discharged_count"], "blocked": obligations["blocked_count"]})

    witnesses = provenance["component_witnesses"]
    check("provenance:component_count", len(witnesses) == 10, len(witnesses))
    check("provenance:target_invariance", all(row["target_invariant"] for row in witnesses), witnesses)
    check("provenance:authority_invariance", all(row["authority_invariant"] for row in witnesses), witnesses)
    check("provenance:no_target_import", provenance["explicit_target_import_count"] == 0, provenance["explicit_target_import_count"])
    check("provenance:no_authority_import", provenance["explicit_authority_import_count"] == 0, provenance["explicit_authority_import_count"])

    for source in provenance["sources"]:
        path = REPO / source["path"]
        actual_hash = sha256(path)
        check(
            f"source_hash:{source['object_id']}",
            actual_hash == source["sha256"],
            {"expected": source["sha256"], "actual": actual_hash},
        )

    check("cocycle:locally_principal", cocycle["global_generator"]["locally_principal"] is True, True)
    check("cocycle:units_6", cocycle["nowhere_zero_unit_count"] == 6, cocycle["nowhere_zero_unit_count"])
    check("cocycle:inverse_6", cocycle["inverse_identity_count"] == 6, cocycle["inverse_identity_count"])
    check("cocycle:triples_2", cocycle["triple_cocycle_count"] == 2, cocycle["triple_cocycle_count"])
    check("cocycle:no_zero_set_inference", cocycle["uniqueness_guard"]["real_zero_set_equality_used"] is False, False)

    record = obstruction["obstruction_record"]
    check("obstruction:present", record["present"] is True, record["present"])
    check("obstruction:id", record["obstruction_id"] == "OBST-V22-P4T02-B2-D7-SEPARATION-001", record["obstruction_id"])
    check("obstruction:failed_ids", record["failed_obligations"] == ["D7-O2", "D7-O4"], record["failed_obligations"])
    check("obstruction:scoped", record["scope"] == "source_extension_candidate", record["scope"])
    check("obstruction:repair_allowed", record["source_extension_implication"] == "repair_allowed", record["source_extension_implication"])
    check("obstruction:not_frozen", obstruction["freeze_criteria"]["freeze_decision"] == "not_frozen", obstruction["freeze_criteria"]["freeze_decision"])
    check("obstruction:next_auditor", obstruction["selected_repair_route"]["immediate_next_role"] == "smuggling-auditor@0.2.0", obstruction["selected_repair_route"]["immediate_next_role"])

    model_path = ARTIFACTS / "v22_p4_t02_b2_descriptor_construction_model.py"
    model_run = subprocess.run(
        [sys.executable, str(model_path), "--json"],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    check("model:exit_zero", model_run.returncode == 0, model_run.returncode)
    try:
        model = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model = {"status": "INVALID_JSON", "failure_count": -1, "check_count": 0}
    check("model:status", model.get("status") == "PASS", model.get("status"))
    check("model:failure_count", model.get("failure_count") == 0, model.get("failure_count"))
    check("model:check_count", model.get("check_count") == 12, model.get("check_count"))

    tex = (ARTIFACTS / "v22_p4_t02_b2_equipped_chain_descriptor_attempt_v1.tex").read_text(encoding="utf-8")
    required_tex_markers = [
        "precise\\_obstruction",
        "OBST-V22-P4T02-B2-D7-SEPARATION-001",
        "M_{\\Bthree}",
        "L_{s,n}(r_s)(x)=r_s",
        "E_s[r_s](u)",
        "\\bar\\sigma_s(x,k)=k(\\tau_x)I_3",
        "\\sqrt{\\langle\\det\\bar\\sigma_s\\rangle}",
        "g_{ij}=1",
        "g_{ij}g_{jk}g_{ki}=1",
        "Source-fiber factorization",
        "Thirty-three",
        "D7-O2",
        "D7-O4",
        "B2 is inactive",
        "P4-T03 is",
    ]
    for marker in required_tex_markers:
        check(f"tex_marker:{marker}", marker in tex, marker)
    forbidden_positive_claims = [
        "descriptor instance is complete",
        "B2 is activated",
        "P4-T03 is unlocked",
        "we derive g_{\\mathrm{eff}}",
        "global no-go theorem is proved",
    ]
    for phrase in forbidden_positive_claims:
        check(f"tex_forbidden:{phrase}", phrase not in tex, phrase)

    failed = [row for row in checks if not row["passed"]]
    report = {
        "schema_id": "v22_p4_t02_b2_descriptor_construction_validation_v1",
        "task_id": "RT-20260809-023",
        "job_id": "AJ-RT-20260809-023-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "warning_count": 0,
        "failed_check_ids": [row["check_id"] for row in failed],
        "checks": checks,
        "model_summary": {
            "status": model.get("status"),
            "check_count": model.get("check_count"),
            "failure_count": model.get("failure_count"),
        },
        "authority_limits": {
            "validator_is_physics_evidence": False,
            "descriptor_instance_complete": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "distance_to_gr_changed": False,
        },
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
