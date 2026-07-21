#!/usr/bin/env python3
"""Validate the bounded v21 P3-T07 EqSrc freeze/inventory integration."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260720-028"
ARTIFACT_DIR = TASK_DIR / "artifacts"
REPORT_PATH = ARTIFACT_DIR / "eqsrc_family_freeze_inventory_validation.json"
INVENTORY_PATH = ROOT / "research_control/design/frontier_theorem_inventory.md"

EXPECTED_FAMILIES = {
    "EQSRC-CANONICAL-CHOICE-INTRINSIC-DISCRIMINATOR": {
        "EQSRC-IDISC-V1", "EQSRC-IDISC-V2", "EQSRC-IDISC-V3"
    },
    "EQSRC-CANONICAL-CHOICE-CYCLE-BOUNDARY-LINE": {
        "EQSRC-CYCLE-BOUNDARY-V1"
    },
    "EQSRC-CANONICAL-CHOICE-ORIENTATION-TORSOR": {
        "EQSRC-ORIENTATION-TORSOR-V1"
    },
    "EQSRC-CANONICAL-CHOICE-ROOTED-PARTITION": {
        "EQSRC-ROOTED-PARTITION-V1"
    },
    "EQSRC-CANONICAL-CHOICE-GRADED-ORBIT-ROOT": {
        "EQSRC-GRADED-ORBIT-ROOT-V1"
    },
}
EXPECTED_REOPENING_CRITERIA = {
    "REOPEN-EQSRC-CURRENT-ONTOLOGY-DERIVATION-001",
    "REOPEN-EQSRC-GENERAL-SELECTOR-THEOREM-002",
    "REOPEN-EQSRC-PHYSICAL-IRRELEVANCE-003",
    "REOPEN-EQSRC-MATERIAL-LEDGER-DELTA-004",
    "REOPEN-EQSRC-PROTECTED-ONTOLOGY-AUTHORITY-005",
}
EXPECTED_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md": "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/handoffs/handoff-0797.yaml": "3c99c4cf52834c2ba72c1aaf006e4049861645912a76b846ed10ca5970260fc8",
    "research_control/tasks/RT-20260720-010/artifacts/eqsrc_canonical_choice_family_inventory.json": "5a823d46054fa75ee7f5f7814aa76ff52ea3e8d8868547229d5b0b2a26e0685e",
    "research_control/tasks/RT-20260720-011/artifacts/eqsrc_canonical_choice_family_freeze_manifest.yaml": "fc0d36a7ea96b6aaaafced309c73c6bb2e71d969ee679d5c286afc2753a95b43",
    "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex": "d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae",
    "research_control/tasks/RT-20260720-019/artifacts/eqsrc_selector_theorem_smuggling_audit_v1.tex": "d093d7b0afbe322cf537644de54f17156ea2427fcc0988f4fc8fb305e93a0f76",
    "research_control/tasks/RT-20260720-020/artifacts/eqsrc_selector_theorem_stress_cases.json": "4b7bc68f625b119060b5abf09066c99a55235fa2676aaa4d01b293ae43eb3bf5",
    "research_control/tasks/RT-20260720-023/artifacts/eqsrc_source_extension_historical_placements_v1.yaml": "b0d5a6f5df55799ab49f85cd1a002728a938fd643cc4c8cb8dbe1483d37d35b2",
    "research_control/tasks/RT-20260720-024/artifacts/eqsrc_representative_irrelevance_theorem_v1.tex": "1a08e02c462d4401a3ad75219d7903c598f996d4011105baab31f07ba1dab0d1",
    "research_control/tasks/RT-20260720-025/artifacts/eqsrc_probabilistic_dynamical_selection_theorem_v1.tex": "c71673f1a79f62b7afce6cd55663594419a234ac16c5a737128bb88b9e4e39a4",
    "research_control/tasks/RT-20260720-026/artifacts/eqsrc_invariant_functor_quotient_relation_candidate_v1.tex": "badc60c72ff16f84fe88568b825ff738a8f160a225f011715f027c1da2cfa1c3",
    "research_control/tasks/RT-20260720-027/artifacts/eqsrc_invariant_functor_quotient_smuggling_audit_v1.tex": "0e3991d70dd7754149821d132808062dd5bf153c810086629686e45593c78c1c",
    "research_control/tasks/RT-20260720-027/artifacts/eqsrc_invariant_functor_quotient_stress_cases_v1.json": "0f307c3bb437d260ccf123e28d5fbd3144052bb8e6a0a7a910b72d3ae6b5ac08",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"expected mapping in {path}")
    return data


def add(checks: list[dict], check_id: str, passed: bool, detail: str) -> None:
    checks.append({
        "check_id": check_id,
        "status": "PASS" if passed else "FAIL",
        "detail": detail,
    })


def family_map(rows: list[dict], id_key: str, members_key: str) -> dict[str, set[str]]:
    return {
        str(row[id_key]): {str(value) for value in row[members_key]}
        for row in rows
    }


def validate() -> dict:
    checks: list[dict] = []

    for relative, expected in EXPECTED_HASHES.items():
        path = ROOT / relative
        observed = sha256(path) if path.is_file() else "missing"
        add(
            checks,
            f"hash:{relative}",
            observed == expected,
            f"expected={expected} observed={observed}",
        )

    historical = json.loads(
        (ROOT / "research_control/tasks/RT-20260720-010/artifacts/eqsrc_canonical_choice_family_inventory.json")
        .read_text(encoding="utf-8")
    )
    prior_freeze = load_yaml(
        ROOT / "research_control/tasks/RT-20260720-011/artifacts/eqsrc_canonical_choice_family_freeze_manifest.yaml"
    )
    ledger = load_yaml(ARTIFACT_DIR / "eqsrc_historical_family_freeze_ledger_v1.yaml")
    decision = load_yaml(ARTIFACT_DIR / "eqsrc_next_frontier_decision_v1.yaml")
    math_child = load_yaml(ARTIFACT_DIR / "child_phys_math_eqsrc_family_freeze_inventory.yaml")
    phil_child = load_yaml(ARTIFACT_DIR / "child_phys_phil_eqsrc_family_freeze_inventory.yaml")
    conflict = load_yaml(ARTIFACT_DIR / "parent_conflict_review_eqsrc_family_freeze_inventory.yaml")

    historical_map = family_map(
        historical["families"], "family_id", "member_candidate_ids"
    )
    ledger_map = family_map(ledger["families"], "family_id", "member_candidate_ids")
    add(checks, "historical_family_identity", historical_map == EXPECTED_FAMILIES,
        f"family_count={len(historical_map)} candidate_count={sum(map(len, historical_map.values()))}")
    add(checks, "ledger_family_identity", ledger_map == EXPECTED_FAMILIES,
        f"family_count={len(ledger_map)} candidate_count={sum(map(len, ledger_map.values()))}")
    add(checks, "ledger_summary_counts",
        ledger["family_count"] == 5 and ledger["candidate_count"] == 7
        and ledger["locally_frozen_family_count"] == 5
        and ledger["reopened_family_count"] == 0,
        "expected 5 families 7 candidates 5 frozen 0 reopened")

    prior_dispositions = {
        row["family_id"]: row["final_disposition"] for row in prior_freeze["families"]
    }
    add(checks, "prior_freezes_all_local",
        set(prior_dispositions) == set(EXPECTED_FAMILIES)
        and set(prior_dispositions.values()) == {"family_locally_frozen"},
        f"dispositions={sorted(set(prior_dispositions.values()))}")
    ledger_dispositions = {row["final_disposition"] for row in ledger["families"]}
    add(checks, "ledger_freezes_preserved",
        ledger_dispositions == {"family_locally_frozen"}
        and all(row["reopened"] is False and row["global_no_go"] is False for row in ledger["families"]),
        f"dispositions={sorted(ledger_dispositions)}")
    add(checks, "theorem_subsumption_scoped",
        all(str(row["theorem_subsumption_status"]).startswith("shared_selector_coordinate_subsumed") for row in ledger["families"]),
        "all five rows classify only the shared selector coordinate")

    prior_criteria = {row["criterion_id"] for row in prior_freeze["reopening_criteria"]}
    ledger_criteria = {row["criterion_id"] for row in ledger["reopening_criteria"]}
    add(checks, "reopening_criteria_preserved",
        prior_criteria == ledger_criteria == EXPECTED_REOPENING_CRITERIA,
        f"criteria={sorted(ledger_criteria)}")
    add(checks, "general_theorem_not_automatic_reopening",
        "not automatic family adoption" in ledger["reopening_criteria"][1]["opens"]
        and ledger["reopening_criteria"][1].get("current_evaluation", "").startswith("satisfied only"),
        "general theorem opens analysis only")

    quotient = ledger["quotient_route"]
    add(checks, "quotient_identity",
        quotient["candidate_id"] == "EQSRC-INVARIANT-FUNCTOR-QUOTIENT-RELATION-CANDIDATE-V1"
        and quotient["candidate_sha256"] == EXPECTED_HASHES["research_control/tasks/RT-20260720-026/artifacts/eqsrc_invariant_functor_quotient_relation_candidate_v1.tex"],
        f"candidate={quotient['candidate_id']}")
    add(checks, "quotient_validity_vs_adequacy",
        quotient["conditional_theorem_status"].startswith("valid_under")
        and "obstructed" in quotient["adequacy_status"]
        and quotient["final_disposition"] == "exact_candidate_locally_frozen",
        "conditional theorem retained and adequacy route locally frozen")
    add(checks, "quotient_boundaries",
        quotient["physical_observational_equivalence_established"] is False
        and quotient["general_eqsrc_discharged"] is False
        and quotient["global_no_go"] is False
        and len(quotient["reopening_criteria"]) == 4,
        "physical EqSrc global no-go and reopening boundaries")

    ledger_authority = ledger["authority_boundary"]
    protected_true = [
        key for key, value in ledger_authority.items()
        if key not in {"classification"} and value is True
    ]
    add(checks, "ledger_authority_boundary", not protected_true,
        f"unexpected_true={protected_true}")

    route = decision["theoretical_decision_output"]
    add(checks, "single_next_route",
        route["selected_next_packet_type"] == "ontology_law_research_packet"
        and route["selected_route"] == "ontology-law-research-packet"
        and route["selected_next_plan_task"] == "P4-T01"
        and route["next_execution_role_family"] == "ontology-formalizer@0.2.0",
        f"selected={route['selected_next_plan_task']}")
    selected_alternatives = [row for row in decision["alternatives"] if row["disposition"] == "selected"]
    add(checks, "exactly_one_selected_alternative",
        len(selected_alternatives) == 1 and selected_alternatives[0]["route"] == "P4-T01",
        f"selected_count={len(selected_alternatives)}")
    add(checks, "p4_not_executed",
        decision["authority_boundary"]["P4_T01_executed"] is False
        and route["selected_next_packet_requires_human_gate"] is False,
        "P4-T01 selected but not executed")

    math_map = family_map(math_child["family_classifications"], "family_id", "immutable_member_candidate_ids")
    phil_map = family_map(phil_child["historical_family_classifications"], "family_id", "member_candidate_ids")
    add(checks, "child_family_identity", math_map == phil_map == EXPECTED_FAMILIES,
        "children independently enumerate the same five families and seven candidates")
    add(checks, "child_freeze_consensus",
        all(row["reopened"] is False and row["current_scoped_disposition"] == "family_locally_frozen" for row in math_child["family_classifications"])
        and all(row["exact_family_reopened"] is False and row["exact_family_disposition"] == "family_locally_frozen" for row in phil_child["historical_family_classifications"]),
        "both child reviews preserve every exact family freeze")
    add(checks, "child_next_route_consensus",
        math_child["recommended_next_plan_task"]["plan_task_id"] == "P4-T01"
        and phil_child["theoretical_decision_output"]["selected_next_plan_task"] == "P4-T01",
        "both children select P4-T01")
    add(checks, "child_authority_consensus",
        math_child["general_eqsrc_status"]["discharged"] is False
        and phil_child["authority_flags"]["general_eqsrc_discharged"] is False
        and phil_child["gate_chair_assessment"]["gate_chair_decision_justified"] is False,
        "general EqSrc and Gate Chair boundaries agree")

    add(checks, "parent_conflict_resolved",
        conflict["status"] == "resolved" and conflict["resolution_rounds"] == 0
        and conflict["unresolved_conflicts"] == []
        and conflict["blocking_conflict_present"] is False,
        "no unresolved parent-child conflict")

    inventory_text = INVENTORY_PATH.read_text(encoding="utf-8")
    item_two = inventory_text.split("### Item 2: source_equivalence_eqsrc", 1)[1].split("### Item 3: retain_h", 1)[0]
    required_inventory_phrases = [
        "theorem;obstruction;frozen_negative_route;missing_theorem",
        "All five families remain locally frozen",
        "every finite partition can be a prospective functor kernel",
        "internal AI red-team review, not independent external human review",
        "General `EqSrc` remains undischarged",
        "`P4-T01` comprehensive source-assumption ledger",
        "no_global_theory_rejection",
        "no_future_source_extension_impossibility",
    ]
    add(checks, "inventory_item_two_updated",
        all(phrase in item_two for phrase in required_inventory_phrases),
        "selector theorem family freezes quotient obstruction and P4-T01 are present")
    add(checks, "inventory_registered_source_paths_exist",
        all((ROOT / relative).is_file() for relative in [
            "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex",
            "research_control/tasks/RT-20260720-019/artifacts/eqsrc_selector_theorem_smuggling_audit_v1.tex",
            "research_control/tasks/RT-20260720-020/artifacts/eqsrc_selector_theorem_refuter_stress_v1.tex",
            "research_control/tasks/RT-20260720-024/artifacts/eqsrc_representative_irrelevance_theorem_v1.tex",
            "research_control/tasks/RT-20260720-025/artifacts/eqsrc_probabilistic_dynamical_selection_theorem_v1.tex",
            "research_control/tasks/RT-20260720-026/artifacts/eqsrc_invariant_functor_quotient_relation_candidate_v1.tex",
            "research_control/tasks/RT-20260720-027/artifacts/eqsrc_invariant_functor_quotient_smuggling_audit_v1.tex",
        ]),
        "all Item 2 registered TeX evidence paths exist")

    final_paths = [
        TASK_DIR / "00_TASK.yaml",
        TASK_DIR / "DDR-20260720-028.md",
        TASK_DIR / "documentation_impact.yaml",
        TASK_DIR / "jobs/AJ-RT-20260720-028-001.yaml",
        TASK_DIR / "jobs/completions/AJC-AJ-RT-20260720-028-001.yaml",
        TASK_DIR / "roles/theoretical-continuation-selector@0.1.0--RT-20260720-028.yaml",
        ARTIFACT_DIR / "parent_fusion_notes_eqsrc_family_freeze_inventory.md",
        ARTIFACT_DIR / "eqsrc_family_freeze_and_frontier_decision_receipt.md",
        ARTIFACT_DIR / "eqsrc_family_freeze_inventory_compact_receipt_v1.json",
        ROOT / "research_control/handoffs/handoff-0798.yaml",
        ROOT / "research_control/handoffs/handoff-0798.md",
    ]
    add(checks, "required_final_outputs_present",
        all(path.is_file() for path in final_paths),
        f"present={sum(path.is_file() for path in final_paths)}/{len(final_paths)}")

    failures = [row for row in checks if row["status"] != "PASS"]
    return {
        "schema_id": "v21-p3-t07-eqsrc-family-freeze-inventory-validation.v1",
        "task_id": "RT-20260720-028",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failures),
        "failed_check_count": len(failures),
        "source_hash_count": len(EXPECTED_HASHES),
        "family_count": 5,
        "candidate_count": 7,
        "locally_frozen_family_count": 5,
        "reopened_family_count": 0,
        "quotient_candidate_locally_frozen": True,
        "selected_next_plan_task": "P4-T01",
        "general_eqsrc_discharged": False,
        "physics_promotion_authorized": False,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']} {report['passed_check_count']}/{report['check_count']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
