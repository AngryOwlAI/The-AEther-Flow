from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path

from scripts.research_control.physics_payload_admission import (
    ACTIVE_AFTER,
    POLICY_ID,
    admission_policy,
    evaluate_agent_job_admission,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = REPO_ROOT / "research_control" / "tasks" / "RT-20260722-012" / "artifacts"
FIXTURE_PATH = ARTIFACT_DIR / "fixtures" / "physics_payload_admission_cases.json"
VALIDATOR_PATH = ARTIFACT_DIR / "validate_physics_payload_admission.py"


class PhysicsPayloadAdmissionTests(unittest.TestCase):
    def test_fixture_matrix_matches_expected_status(self) -> None:
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        observed = {}
        for case in fixture["cases"]:
            result = evaluate_agent_job_admission(
                case["job"],
                case["task"],
                created_at=case["created_at"],
                role_id=case["role_id"],
            )
            observed[case["case_id"]] = result
            self.assertEqual(result["status"], case["expected_status"], case["case_id"])
            self.assertFalse(result["theorem_truth_evaluated"])

        self.assertEqual(observed["legacy_missing_block"]["status"], "legacy_readable")
        self.assertEqual(observed["source_acquisition_admitted"]["status"], "admitted")
        self.assertEqual(observed["precise_obstruction_admitted"]["status"], "admitted")
        self.assertEqual(observed["selector_only_rejected"]["status"], "rejected")
        self.assertEqual(observed["project_system_admitted_separately"]["expected_admission_path"], "project_system")

    def test_policy_context_is_explicitly_non_promotional(self) -> None:
        policy = admission_policy()
        self.assertEqual(policy["policy_id"], POLICY_ID)
        self.assertEqual(policy["active_after"], ACTIVE_AFTER)
        self.assertEqual(policy["enforcement"], "hard_failure")
        self.assertEqual(policy["historical_jobs_without_block"], "legacy_readable")
        self.assertTrue(policy["source_acquisition_allowed"])
        self.assertTrue(policy["precise_obstruction_allowed"])
        self.assertFalse(policy["theorem_truth_evaluated"])
        self.assertFalse(policy["physics_promotion_authorized"])

    def test_task_local_report_is_deterministic_and_current(self) -> None:
        result = subprocess.run(
            [str(REPO_ROOT / ".venv" / "bin" / "python"), str(VALIDATOR_PATH), "--check", "--json"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["failed_case_count"], 0)


if __name__ == "__main__":
    unittest.main()
