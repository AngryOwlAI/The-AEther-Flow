from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

from scripts.research_control.dual_budget_policy import (
    ACTIVE_AFTER,
    POLICY_ID,
    dual_budget_policy,
    evaluate_dual_budget_allocation,
    evaluate_dual_budget_completion,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = REPO_ROOT / "research_control" / "tasks" / "RT-20260722-014" / "artifacts"
VALIDATOR_PATH = ARTIFACT_DIR / "validate_dual_budget_policy.py"
FIXTURE_PATH = ARTIFACT_DIR / "fixtures" / "dual_budget_cases.json"


def _load_validator_module():
    spec = importlib.util.spec_from_file_location("p12_t03_validator", VALIDATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DualBudgetPolicyTests(unittest.TestCase):
    def test_fixture_matrix_covers_categories_and_hard_failures(self) -> None:
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        module = _load_validator_module()
        observed = {}
        for case in fixture["cases"]:
            job = module._merge(fixture["base_job"], case.get("job_patch", {}))
            result = evaluate_dual_budget_allocation(
                job,
                created_at=fixture["created_at"],
                evidence_verifier=module._fixture_evidence_verifier,
            )
            observed[case["case_id"]] = result
            self.assertEqual(result["status"], case["expected_status"], case["case_id"])
            self.assertFalse(result["theorem_truth_evaluated"])

        self.assertIn(
            "exactly one total credit",
            " ".join(observed["double_task_credit_rejected"]["errors"]),
        )
        self.assertIn(
            "must be disjoint",
            " ".join(observed["mixed_shared_output_rejected"]["errors"]),
        )
        self.assertIn(
            "not_measured value must be null",
            " ".join(observed["missing_compute_coerced_to_zero_rejected"]["errors"]),
        )

    def test_policy_reserves_route_guard_and_denies_science_credit(self) -> None:
        policy = dual_budget_policy()
        self.assertEqual(policy["policy_id"], POLICY_ID)
        self.assertEqual(policy["active_after"], ACTIVE_AFTER)
        self.assertEqual(policy["ordinary_route_guard_owner"], "P12-T04")
        self.assertEqual(policy["existing_three_task_threshold"], "advisory_in_p12_t03")
        self.assertFalse(policy["system_success_counts_as_physics"])
        self.assertFalse(policy["system_success_counts_as_distance_to_gr"])

    def test_legacy_job_without_allocation_remains_readable(self) -> None:
        result = evaluate_dual_budget_allocation(
            {"created_at": "2026-07-22T18:10:43Z"}
        )
        self.assertEqual(result["status"], "legacy_readable")
        self.assertFalse(result["required"])

    def test_completion_cannot_transfer_system_acceptance_to_physics(self) -> None:
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        job = fixture["base_job"]
        allocation = job["dual_budget_allocation"]
        completion = {
            "distance_to_gr_delta": {"changed": False},
            "dual_budget_result": {
                "schema_id": "dual_budget_result_v1",
                "policy_id": "dual_budget_policy_v1",
                "category": allocation["category"],
                "primary_budget": allocation["primary_budget"],
                "task_count_credit": allocation["task_count_credit"],
                "observed_durable_outputs": allocation["expected_durable_outputs"],
                "accepted_criteria": allocation["acceptance_criteria"],
                "resource_measurement": allocation["resource_measurement"],
                "authority_limits": allocation["authority_limits"],
            },
        }
        accepted = evaluate_dual_budget_completion(job, completion)
        self.assertEqual(accepted["status"], "accepted")

        completion["dual_budget_result"]["accepted_criteria"]["physics"] = [
            "validator passed therefore physics advanced"
        ]
        rejected = evaluate_dual_budget_completion(job, completion)
        self.assertEqual(rejected["status"], "rejected")
        self.assertTrue(
            any("may not claim physics lane success" in item for item in rejected["errors"])
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
        self.assertTrue(report["category_coverage_complete"])
        self.assertFalse(report["p12_t04_route_guard_implemented"])


if __name__ == "__main__":
    unittest.main()
