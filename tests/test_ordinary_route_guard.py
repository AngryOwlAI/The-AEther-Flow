from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from scripts.research_control.ordinary_route_guard import (
    POLICY_ID,
    REQUIRED_AFTER,
    THRESHOLD,
    derive_consecutive_project_system_tasks,
    discover_ready_science_routes,
    evaluate_agent_job_route_admission,
    evaluate_research_handoff_guard,
    ordinary_route_guard_policy,
    policy_active,
)


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    ROOT
    / "research_control/tasks/RT-20260722-015/artifacts/validate_ordinary_route_guard.py"
)


def load_fixture_validator():
    spec = importlib.util.spec_from_file_location("validate_ordinary_route_guard", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load ordinary-route fixture validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OrdinaryRouteGuardTests(unittest.TestCase):
    def test_policy_contract(self) -> None:
        policy = ordinary_route_guard_policy()
        self.assertEqual(policy["policy_id"], POLICY_ID)
        self.assertEqual(policy["threshold"], THRESHOLD)
        self.assertEqual(policy["warning_at"], THRESHOLD - 1)
        self.assertEqual(policy["enforcement"], "prospective_hard_failure")
        self.assertFalse(policy["authority_limits"]["physics_promotion_authorized"])

    def test_activation_boundary_is_strictly_after_implementation_job(self) -> None:
        self.assertFalse(policy_active(REQUIRED_AFTER))
        self.assertTrue(policy_active("2026-07-22T19:00:54Z"))

    def test_fixture_suite(self) -> None:
        report = load_fixture_validator().build_validation_report()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["fixture_case_count"], 12)
        self.assertEqual(report["fixture_pass_count"], 12)
        self.assertEqual(report["fixture_failure_count"], 0)

    def test_historical_handoff_without_guard_is_readable(self) -> None:
        result = evaluate_research_handoff_guard(
            {"created_at": REQUIRED_AFTER, "handoff_id": "handoff-0000"},
            ROOT,
        )
        self.assertEqual(result["status"], "LEGACY_READABLE")
        self.assertFalse(result["policy_required"])

    def test_implementation_job_does_not_require_its_own_admission(self) -> None:
        result = evaluate_agent_job_route_admission(
            {"plan_task_id": "P12-T04"},
            created_at=REQUIRED_AFTER,
            repo_root=ROOT,
        )
        self.assertEqual(result["status"], "LEGACY_READABLE")

    def test_later_job_requires_admission(self) -> None:
        result = evaluate_agent_job_route_admission(
            {"plan_task_id": "P14-T01"},
            created_at="2026-07-22T19:00:54Z",
            repo_root=ROOT,
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("ordinary_route_guard_admission_missing_or_not_mapping", result["errors"])

    def test_current_precompletion_run_is_four(self) -> None:
        self.assertEqual(
            derive_consecutive_project_system_tasks(ROOT, REQUIRED_AFTER),
            4,
        )

    def test_current_ready_science_routes_are_exact(self) -> None:
        routes = discover_ready_science_routes(ROOT, REQUIRED_AFTER)
        self.assertEqual(
            [route["plan_task_id"] for route in routes],
            ["P4-T05", "P14-T01"],
        )
        self.assertTrue(routes[0]["requires_human_gate"])
        self.assertFalse(routes[1]["requires_human_gate"])


if __name__ == "__main__":
    unittest.main()
