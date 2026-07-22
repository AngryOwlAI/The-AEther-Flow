from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

from scripts.research_control.family_freeze_admission import (
    ACTIVE_AFTER,
    POLICY_ID,
    family_freeze_policy,
    evaluate_family_freeze_admission,
)
from scripts.research_control.physics_payload_admission import (
    evaluate_agent_job_admission,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = REPO_ROOT / "research_control" / "tasks" / "RT-20260722-013" / "artifacts"
VALIDATOR_PATH = ARTIFACT_DIR / "validate_family_freeze_policy.py"
FIXTURE_PATH = ARTIFACT_DIR / "fixtures" / "family_freeze_route_cases.json"


def _load_validator_module():
    spec = importlib.util.spec_from_file_location("p12_t02_validator", VALIDATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FamilyFreezeAdmissionTests(unittest.TestCase):
    def test_fixture_matrix_blocks_repeats_and_allows_evidenced_routes(self) -> None:
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        module = _load_validator_module()
        observed = {}
        for case in fixture["cases"]:
            job = module._merge(fixture["base_job"], case.get("job_patch", {}))
            result = evaluate_family_freeze_admission(
                job,
                expected_admission_path="physics",
                created_at=fixture["created_at"],
                evidence_verifier=module._fixture_evidence_verifier,
            )
            observed[case["case_id"]] = result
            self.assertEqual(result["status"], case["expected_status"], case["case_id"])
            self.assertFalse(result["theorem_truth_evaluated"])

        self.assertEqual(observed["frozen_family_repeat_blocked"]["status"], "rejected")
        self.assertEqual(observed["renamed_same_assumption_blocked"]["match_reasons"], ["assumption_sha256"])
        self.assertEqual(observed["new_theorem_reopening_admitted"]["status"], "admitted_reopened")
        self.assertEqual(observed["distinct_theorem_branch_admitted_without_reopening"]["status"], "admitted_distinct_branch")
        self.assertEqual(observed["unfrozen_family_admitted"]["status"], "admitted_unfrozen")

    def test_policy_preserves_local_freeze_without_global_no_go(self) -> None:
        policy = family_freeze_policy()
        self.assertEqual(policy["policy_id"], POLICY_ID)
        self.assertEqual(policy["active_after"], ACTIVE_AFTER)
        self.assertEqual(policy["frozen_family_count"], 5)
        self.assertFalse(policy["renamed_or_repackaged_route_admitted"])
        self.assertFalse(policy["distinct_theorem_or_ontology_branch_blocked"])
        self.assertFalse(policy["local_freeze_is_global_no_go"])
        self.assertFalse(policy["theorem_truth_evaluated"])
        self.assertFalse(policy["physics_promotion_authorized"])

    def test_project_system_path_is_separate(self) -> None:
        result = evaluate_family_freeze_admission(
            {"created_at": "2026-07-22T17:25:52Z"},
            expected_admission_path="project_system",
        )
        self.assertEqual(result["status"], "not_applicable")
        self.assertFalse(result["required"])

    def test_physics_payload_gate_enforces_the_family_freeze_result(self) -> None:
        job = {
            "created_at": "2026-07-22T17:25:52Z",
            "role_id": "candidate-constructor",
            "requires_human_gate": False,
            "physics_payload_admission": {
                "schema_id": "physics_payload_admission_v1",
                "policy_id": "physics_payload_admission_policy_v1",
                "admission_path": "physics",
                "payload_type": "candidate_construction",
                "candidate_family": "EQSRC-CANONICAL-CHOICE-INTRINSIC-DISCRIMINATOR",
                "assumption_delta": ["No material delta from the frozen v3 assumption basis."],
                "materiality_basis": "Fixture exercises integrated admission only.",
                "source_basis": ["FIXTURE-SOURCE"],
                "expected_artifact_paths": ["research_control/tasks/FIXTURE/artifact.tex"],
                "process_receipts_excluded_from_payload": [
                    "validator_pass",
                    "checkpoint_pass",
                    "documentation_receipt",
                    "role_or_route_selection",
                ],
                "authority_limits": {
                    "theorem_truth_inferred": False,
                    "scientific_status_changed": False,
                    "ontology_or_source_law_adopted": False,
                    "distance_to_gr_changed": False,
                    "physics_promotion_authorized": False,
                },
            },
        }
        task = {"task_taxonomy": {"scope": "scientific"}}
        missing = evaluate_agent_job_admission(job, task)
        self.assertEqual(missing["status"], "rejected")
        self.assertTrue(
            any("missing family_freeze_admission" in item for item in missing["errors"])
        )

        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        module = _load_validator_module()
        unfrozen_case = next(
            item for item in fixture["cases"] if item["case_id"] == "unfrozen_family_admitted"
        )
        admitted_job = module._merge(job, fixture["base_job"])
        admitted_job = module._merge(admitted_job, unfrozen_case["job_patch"])
        admitted = evaluate_agent_job_admission(admitted_job, task)
        self.assertEqual(admitted["status"], "admitted")
        self.assertEqual(
            admitted["family_freeze_admission"]["status"], "admitted_unfrozen"
        )

    def test_task_local_report_is_deterministic_and_current(self) -> None:
        result = subprocess.run(
            [
                str(REPO_ROOT / ".venv" / "bin" / "python"),
                str(VALIDATOR_PATH),
                "--check",
                "--json",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["failed_case_count"], 0)
        self.assertTrue(report["historical_sources_unchanged"])


if __name__ == "__main__":
    unittest.main()
