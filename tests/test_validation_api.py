from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.project_control.classify_project_changes import classify_paths
from scripts.validation import api
from scripts.validation.executor import ExecutionOutcome
from scripts.validation.plan import build_plan, load_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidationApiTests(unittest.TestCase):
    def test_plan_api_matches_direct_planner(self) -> None:
        request = api.ValidationPlanRequest(
            profile="affected",
            paths=("scripts/validation/api.py",),
            scopes=("working",),
            role_obligations=("documentation_impact",),
        )
        actual = api.plan_validation(request)
        expected = build_plan(
            load_manifest(api.DEFAULT_MANIFEST),
            classify_paths(request.paths),
            profile=request.profile,
            scopes=request.scopes,
            role_obligations=request.role_obligations,
        )
        self.assertEqual(actual.canonical_json(), expected.canonical_json())
        self.assertEqual(api.plan_exit_code(actual), 0)
        self.assertFalse(actual.to_dict()["authority"]["physics_claim_authority"])

    def test_invalid_profile_has_blocked_configuration_semantics(self) -> None:
        with self.assertRaises(api.ValidationApiError) as raised:
            api.plan_validation(api.ValidationPlanRequest(profile="unsupported"))
        self.assertEqual(raised.exception.status, "BLOCKED_CONFIGURATION")
        self.assertEqual(raised.exception.exit_code, 2)

    def test_request_rejects_blank_values(self) -> None:
        with self.assertRaises(api.ValidationApiError):
            api.ValidationPlanRequest(profile="affected", paths=("",))

    def test_blocked_plan_maps_to_exit_two(self) -> None:
        plan = api.plan_validation(
            api.ValidationPlanRequest(
                profile="affected",
                paths=("wiki/markdown/direct-generated-edit.md",),
            )
        )
        self.assertEqual(plan.status, "BLOCKED_CONFIGURATION")
        self.assertEqual(api.plan_exit_code(plan), 2)

    def test_execution_adapter_returns_executor_outcome(self) -> None:
        plan = api.plan_validation(
            api.ValidationPlanRequest(
                profile="fast",
                paths=("scripts/validation/api.py",),
            )
        )
        expected = ExecutionOutcome(
            status="PASS",
            exit_code=0,
            receipt={"counts": {"gate_count": 0}},
            receipt_path=None,
        )
        with tempfile.TemporaryDirectory() as temporary:
            request = api.ValidationExecutionRequest(
                receipt_root=Path(temporary),
                run_id="RUN-api-contract-test",
            )
            with (
                mock.patch.object(api, "load_adapters", return_value={}),
                mock.patch.object(api, "execute_plan", return_value=expected) as execute,
            ):
                actual = api.execute_validation(plan, request)
        self.assertIs(actual, expected)
        self.assertEqual(execute.call_args.kwargs["run_id"], "RUN-api-contract-test")
        self.assertEqual(execute.call_args.kwargs["max_workers"], 4)

    def test_api_contract_document_contains_executable_example(self) -> None:
        contract = (
            REPO_ROOT
            / "research_control/tasks/RT-20260723-020/artifacts/validator_api_contract_v1.md"
        ).read_text(encoding="utf-8")
        self.assertIn("ValidationPlanRequest(", contract)
        self.assertIn("plan_validation(request)", contract)
        self.assertIn("0", contract)
        self.assertIn("1", contract)
        self.assertIn("2", contract)


if __name__ == "__main__":
    unittest.main()
