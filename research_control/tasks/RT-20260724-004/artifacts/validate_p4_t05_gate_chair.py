#!/usr/bin/env python3
"""Validate the bounded P4-T05 Gate Chair packet without mutating files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260724-004"
ART = TASK / "artifacts"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    approval = yaml.safe_load(
        (ROOT / "research_control/approvals/approval-20260724-001.yaml").read_text()
    )
    authorization = yaml.safe_load(
        (ART / "human_authorization_p4_t05_continuum_first_v1.yaml").read_text()
    )
    route = yaml.safe_load(
        (ART / "canonical_next_route_authorization_v1.yaml").read_text()
    )
    math_child = yaml.safe_load(
        (ART / "child_phys_math_ontology_regime_gate_chair_review.yaml").read_text()
    )
    phil_child = yaml.safe_load(
        (ART / "child_phys_phil_ontology_regime_gate_chair_review.yaml").read_text()
    )
    conflict = yaml.safe_load(
        (ART / "parent_conflict_review_ontology_regime_gate_chair_review.yaml").read_text()
    )
    receipt = json.loads((ART / "p4_t05_gate_chair_compact_receipt_v1.json").read_text())
    decision_text = (ART / "ontology_regime_gate_chair_decision_v1.tex").read_text()

    expected_auth = "HUMAN-P4-T05-20260722-CONTINUUM-FIRST-01"
    expected_decision = "SELECT_CONTINUUM_FIRST_WITH_NARROW_PREMETRIC_BOUNDARY"
    assert approval["human_authorization_id"] == expected_auth
    assert approval["decision_code"] == expected_decision
    assert approval["status"] == "consumed"
    assert approval["consumed_by"] == "AJ-RT-20260724-004-001"
    assert authorization["human_authorization_id"] == expected_auth
    assert authorization["decision_code"] == expected_decision
    assert route["selected_next_plan_task_id"] == "P4-T06"
    assert route["selected_next_worker_skill"] == "continue-research"
    assert math_child["mathematical_assessment"]["derived_result_count"] == 0
    assert phil_child["ontological_assessment"]["truth_status"] == (
        "not established as fundamental physical ontology"
    )
    assert conflict["blocking_conflicts"] == []
    assert receipt["canonical_ontology_files_changed"] == 0
    assert receipt["adopted_physical_structure_count"] == 0
    assert receipt["physics_promotion_authorized"] is False
    assert "not identified with physical spacetime by fiat" in decision_text
    assert "No canonical ontology source is edited in P4-T05" not in decision_text
    assert "P4-T05 selects and delimits the research architecture" in decision_text
    assert "P4-T06" in decision_text

    expected_inputs = {
        ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
            "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
        ROOT / "research_control/tasks/RT-20260720-031/artifacts/continuum_first_premetric_ontology_option_v1.tex":
            "7d408e527015f4e7c09df90277282c284f299fb705cbd4917a22e62ab3e0d1f8",
        ROOT / "research_control/tasks/RT-20260720-032/artifacts/emergence_first_process_order_ontology_option_v1.tex":
            "121e86bd8609863ca79fd21d1cf9b5ee855057bc5a0804927946911f1222d6f5",
        ROOT / "research_control/tasks/RT-20260721-002/artifacts/ontology_regime_comparison_report_v1.md":
            "5dd5526ebdce949ff121f4aa2785e665e006b5e9fec5f8b1d72877d7da26b7ae",
    }
    for path, expected in expected_inputs.items():
        assert sha256(path) == expected, path

    print(
        json.dumps(
            {
                "status": "PASS",
                "task_id": "RT-20260724-004",
                "approval_id": approval["approval_id"],
                "decision_code": expected_decision,
                "next_plan_task_id": route["selected_next_plan_task_id"],
                "physical_structure_adoption_count": 0,
                "canonical_ontology_files_changed": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
