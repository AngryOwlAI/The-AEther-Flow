from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

import scripts.research_control.ordinary_route_guard as ordinary_route_guard
from scripts.research_control.ordinary_route_guard import (
    POLICY_ID,
    PROTECTED_HUMAN_OVERRIDE_SCHEMA_ID,
    REQUIRED_AFTER,
    THRESHOLD,
    derive_consecutive_project_system_tasks,
    discover_ready_science_routes,
    evaluate_agent_job_route_admission,
    evaluate_research_handoff_guard,
    ordinary_route_guard_policy,
    policy_active,
    route_guard_read_cache,
)


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    ROOT
    / "research_control/tasks/RT-20260722-015/artifacts/validate_ordinary_route_guard.py"
)
P4_T05_JOB_PATH = (
    ROOT
    / "research_control/tasks/RT-20260724-004/jobs/AJ-RT-20260724-004-001.yaml"
)
P4_T05_OVERRIDE_RECEIPT_NAME = (
    "protected_human_route_override_admission_v1.yaml"
)
P4_T05_RECOVERY_JOB_PATH = (
    ROOT
    / "research_control/tasks/RT-20260724-005/jobs/AJ-RT-20260724-005-001.yaml"
)


def load_fixture_validator():
    spec = importlib.util.spec_from_file_location("validate_ordinary_route_guard", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load ordinary-route fixture validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OrdinaryRouteGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository_candidate_paths = (
            ordinary_route_guard._repository_candidate_paths(ROOT)
        )
        cls.approval_job_uses = ordinary_route_guard._approval_job_uses(
            ROOT,
            "approval-20260724-001",
        )

    def p4_t05_job(self) -> dict:
        value = yaml.safe_load(P4_T05_JOB_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(value, dict)
        return value

    def evaluate_p4_t05(self, job: dict | None = None) -> dict:
        selected = job if job is not None else self.p4_t05_job()
        return evaluate_agent_job_route_admission(
            selected,
            created_at=str(selected["created_at"]),
            repo_root=ROOT,
        )

    def evaluate_p4_t05_fast(self, job: dict | None = None) -> dict:
        with mock.patch.object(
            ordinary_route_guard,
            "evaluate_research_handoff_guard",
            return_value={"status": "PASS", "errors": [], "warnings": []},
        ), mock.patch.object(
            ordinary_route_guard,
            "_repository_candidate_paths",
            return_value=self.repository_candidate_paths,
        ), mock.patch.object(
            ordinary_route_guard,
            "_approval_job_uses",
            return_value=self.approval_job_uses,
        ):
            return self.evaluate_p4_t05(job)

    def evaluate_with_mapping_mutation(self, mutate) -> dict:
        original_load = ordinary_route_guard._load_mapping

        def patched(path: Path):
            value = original_load(path)
            if path.name == P4_T05_OVERRIDE_RECEIPT_NAME:
                value = copy.deepcopy(value)
                mutate(value)
            return value

        with mock.patch.object(
            ordinary_route_guard,
            "_load_mapping",
            side_effect=patched,
        ), mock.patch.object(
            ordinary_route_guard,
            "evaluate_research_handoff_guard",
            return_value={"status": "PASS", "errors": [], "warnings": []},
        ), mock.patch.object(
            ordinary_route_guard,
            "_repository_candidate_paths",
            return_value=self.repository_candidate_paths,
        ), mock.patch.object(
            ordinary_route_guard,
            "_approval_job_uses",
            return_value=self.approval_job_uses,
        ):
            return self.evaluate_p4_t05()

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

    def test_read_cache_is_bounded_and_invalidates_changed_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "record.yaml"
            path.write_text("value: 1\n", encoding="utf-8")
            real_safe_load = ordinary_route_guard.yaml.safe_load
            with mock.patch.object(
                ordinary_route_guard.yaml,
                "safe_load",
                wraps=real_safe_load,
            ) as safe_load:
                with route_guard_read_cache():
                    first = ordinary_route_guard._load_mapping(path)
                    second = ordinary_route_guard._load_mapping(path)
                    self.assertIs(first, second)
                    self.assertEqual(safe_load.call_count, 1)

                    path.write_text("value: 200\n", encoding="utf-8")
                    changed = ordinary_route_guard._load_mapping(path)
                    self.assertEqual(changed, {"value": 200})
                    self.assertEqual(safe_load.call_count, 2)

                outside = ordinary_route_guard._load_mapping(path)
                self.assertEqual(outside, {"value": 200})
                self.assertEqual(safe_load.call_count, 3)

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

    def test_exact_protected_human_override_is_admitted(self) -> None:
        result = self.evaluate_p4_t05()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["errors"], [])

    def test_exact_checkpoint_recovery_override_is_admitted(self) -> None:
        job = yaml.safe_load(P4_T05_RECOVERY_JOB_PATH.read_text(encoding="utf-8"))
        result = evaluate_agent_job_route_admission(
            job,
            created_at=str(job["created_at"]),
            repo_root=ROOT,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["errors"], [])

    def test_ordinary_equality_rule_remains_without_override(self) -> None:
        job = self.p4_t05_job()
        job["ordinary_route_guard_admission"].pop("override_authority")
        result = self.evaluate_p4_t05_fast(job)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("job_plan_task_id_not_selected_by_handoff", result["errors"])

    def test_future_override_requires_exact_receipt_hash(self) -> None:
        job = self.p4_t05_job()
        job["created_at"] = "2026-07-24T16:00:01Z"
        override = job["ordinary_route_guard_admission"]["override_authority"]
        override["schema_id"] = PROTECTED_HUMAN_OVERRIDE_SCHEMA_ID
        override["receipt_path"] = (
            "research_control/tasks/RT-20260724-004/artifacts/"
            + P4_T05_OVERRIDE_RECEIPT_NAME
        )
        override["receipt_sha256"] = "0" * 64
        result = self.evaluate_p4_t05_fast(job)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("protected_override_receipt_hash_mismatch", result["errors"])

    def test_override_rejects_stale_approval_hash(self) -> None:
        result = self.evaluate_with_mapping_mutation(
            lambda receipt: receipt["approval"].update({"sha256": "0" * 64})
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("protected_override_approval_hash_mismatch", result["errors"])

    def test_override_rejects_unconsumed_approval(self) -> None:
        original_load = ordinary_route_guard._load_mapping

        def patched(path: Path):
            value = original_load(path)
            if path.name == "approval-20260724-001.yaml":
                value = copy.deepcopy(value)
                value["status"] = "active"
            return value

        with mock.patch.object(
            ordinary_route_guard,
            "_load_mapping",
            side_effect=patched,
        ), mock.patch.object(
            ordinary_route_guard,
            "evaluate_research_handoff_guard",
            return_value={"status": "PASS", "errors": [], "warnings": []},
        ), mock.patch.object(
            ordinary_route_guard,
            "_repository_candidate_paths",
            return_value=self.repository_candidate_paths,
        ), mock.patch.object(
            ordinary_route_guard,
            "_approval_job_uses",
            return_value=self.approval_job_uses,
        ):
            result = self.evaluate_p4_t05()
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("protected_override_approval_status_mismatch", result["errors"])

    def test_override_rejects_approval_reuse(self) -> None:
        with mock.patch.object(
            ordinary_route_guard,
            "_approval_job_uses",
            return_value=[
                "AJ-RT-20260724-004-001",
                "AJ-RT-20260724-999-001",
            ],
        ), mock.patch.object(
            ordinary_route_guard,
            "evaluate_research_handoff_guard",
            return_value={"status": "PASS", "errors": [], "warnings": []},
        ), mock.patch.object(
            ordinary_route_guard,
            "_repository_candidate_paths",
            return_value=self.repository_candidate_paths,
        ):
            result = self.evaluate_p4_t05()
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "protected_override_approval_reused_or_ambiguous",
            result["errors"],
        )

    def test_override_rejects_goal_generation_mismatch(self) -> None:
        def mutate(receipt: dict) -> None:
            receipt["admitted_route"]["generation"] = 98
            receipt["admitted_route"]["idempotency_key"] = (
                "crg-20260720T161354Z-96bc2664ce31bfe0:98"
            )

        result = self.evaluate_with_mapping_mutation(mutate)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "protected_override_admitted_route_generation_mismatch",
            result["errors"],
        )

    def test_override_rejects_director_decision_mismatch(self) -> None:
        result = self.evaluate_with_mapping_mutation(
            lambda receipt: receipt["protected_job"].update(
                {"decision_id": "DDR-20260724-999"}
            )
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "protected_override_protected_job_decision_id_mismatch",
            result["errors"],
        )

    def test_override_rejects_source_handoff_mismatch(self) -> None:
        result = self.evaluate_with_mapping_mutation(
            lambda receipt: receipt["source_handoff"].update(
                {"handoff_id": "handoff-9999"}
            )
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "protected_override_source_handoff_handoff_id_mismatch",
            result["errors"],
        )

    def test_override_rejects_broadened_approval(self) -> None:
        original_load = ordinary_route_guard._load_mapping

        def patched(path: Path):
            value = original_load(path)
            if path.name == "approval-20260724-001.yaml":
                value = copy.deepcopy(value)
                value["protected_scope"]["must_not_authorize"] = []
            return value

        with mock.patch.object(
            ordinary_route_guard,
            "_load_mapping",
            side_effect=patched,
        ), mock.patch.object(
            ordinary_route_guard,
            "evaluate_research_handoff_guard",
            return_value={"status": "PASS", "errors": [], "warnings": []},
        ), mock.patch.object(
            ordinary_route_guard,
            "_repository_candidate_paths",
            return_value=self.repository_candidate_paths,
        ), mock.patch.object(
            ordinary_route_guard,
            "_approval_job_uses",
            return_value=self.approval_job_uses,
        ):
            result = self.evaluate_p4_t05()
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "protected_override_approval_non_authorizations_missing",
            result["errors"],
        )

    def test_override_preserves_noninference_limits(self) -> None:
        result = self.evaluate_with_mapping_mutation(
            lambda receipt: receipt["authority_limits"].update(
                {"physics_promotion_authorized": True}
            )
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "authority_limits_physics_promotion_authorized_must_be_false",
            result["errors"],
        )

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
