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
    AUTHORITY_LIMITS,
    CHECKPOINT_RECOVERY_SCHEMA_ID,
    DEFAULT_PLAN_ID,
    PLAN_REAUDIT_ACTIVATION_SCHEMA_ID,
    POLICY_ID,
    PROTECTED_HUMAN_OVERRIDE_SCHEMA_ID,
    REQUIRED_AFTER,
    THRESHOLD,
    completed_plan_task_identities,
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

    def test_v22_handoff_resolves_colliding_p1_t01_in_selected_plan(self) -> None:
        v22_plan_id = "recommendations_implementation_plan_continue_task-v22"
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            backlog_root = repo_root / "research_control/design"
            backlog_root.mkdir(parents=True)
            (backlog_root / "v22_recommendation_backlog.yaml").write_text(
                "source_plan:\n"
                f"  plan_id: {v22_plan_id}\n"
                "items:\n"
                "  - plan_task_id: P1-T01\n"
                "    task_class: project_system\n"
                "    worker_skill: improve-project-system\n"
                "    requires_human_gate: false\n"
                "    depends_on: [P0-T03]\n",
                encoding="utf-8",
            )
            record = {
                "schema_id": ordinary_route_guard.EVALUATION_SCHEMA_ID,
                "policy_id": POLICY_ID,
                "ordinary_handoff_id": "handoff-9900",
                "threshold": THRESHOLD,
                "consecutive_project_system_tasks_before_selection": 4,
                "selected_plan_id": v22_plan_id,
                "selected_plan_task_id": "P1-T01",
                "selected_route_class": "project_system",
                "selected_worker_skill": "improve-project-system",
                "ready_science_plan_task_ids": [],
                "ready_science_plan_task_refs": [],
                "outcome": "all_ready_science_blocked_exception",
                "ordinary_research_handoff_authoritative": True,
                "project_system_sidecar_supersedes": False,
                "exception_receipt": {
                    "active": True,
                    "schema_id": ordinary_route_guard.EXCEPTION_SCHEMA_ID,
                    "exception_class": "all_ready_science_blocked",
                    "ordinary_handoff_id": "handoff-9900",
                    "ready_science_plan_task_ids": [],
                    "ready_science_plan_task_refs": [],
                    "blocked_routes": [],
                    "authority_limits": dict(AUTHORITY_LIMITS),
                },
                "authority_limits": dict(AUTHORITY_LIMITS),
            }
            handoff = {
                "created_at": "2026-08-08T23:00:00Z",
                "handoff_id": "handoff-9900",
                "selected_next_route": {
                    "plan_id": v22_plan_id,
                    "plan_task_id": "P1-T01",
                },
                "ordinary_route_guard": record,
            }
            with mock.patch.object(
                ordinary_route_guard,
                "discover_ready_science_routes",
                return_value=[],
            ), mock.patch.object(
                ordinary_route_guard,
                "derive_consecutive_project_system_tasks",
                return_value=4,
            ):
                result = evaluate_research_handoff_guard(handoff, repo_root)

            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["selected_plan_id"], v22_plan_id)
            self.assertEqual(result["selected_plan_task_id"], "P1-T01")

    def test_legacy_v22_intake_handoffs_retain_v21_guard_interpretation(self) -> None:
        for handoff_id in ("handoff-0967", "handoff-0968"):
            path = ROOT / f"research_control/handoffs/{handoff_id}.yaml"
            handoff = yaml.safe_load(path.read_text(encoding="utf-8"))
            result = evaluate_research_handoff_guard(handoff, ROOT)
            self.assertIn(result["status"], {"PASS", "WARN"}, result)
            self.assertEqual(result["errors"], [], result)
            self.assertEqual(result["selected_plan_id"], DEFAULT_PLAN_ID)

    def test_completed_work_item_identity_does_not_cross_plan_namespace(self) -> None:
        v22_plan_id = "recommendations_implementation_plan_continue_task-v22"
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            backlog_root = repo_root / "research_control/design"
            backlog_root.mkdir(parents=True)
            for version, plan_id in (("v21", DEFAULT_PLAN_ID), ("v22", v22_plan_id)):
                (backlog_root / f"{version}_recommendation_backlog.yaml").write_text(
                    "source_plan:\n"
                    f"  plan_id: {plan_id}\n"
                    "items:\n"
                    "  - plan_task_id: P0-T03\n"
                    "    depends_on: []\n"
                    "  - plan_task_id: P1-T01\n"
                    "    depends_on: [P0-T03]\n",
                    encoding="utf-8",
                )

            task_root = repo_root / "research_control/tasks"
            v21_task = task_root / "RT-V21"
            v21_task.mkdir(parents=True)
            (v21_task / "00_TASK.yaml").write_text(
                "task_id: RT-V21\n"
                "closure_status: qualifying_complete\n"
                "implementation_plan:\n"
                f"  plan_id: {DEFAULT_PLAN_ID}\n"
                "  plan_task_id: P1-T01\n",
                encoding="utf-8",
            )
            v22_task = task_root / "RT-V22"
            v22_task.mkdir(parents=True)
            (v22_task / "00_TASK.yaml").write_text(
                "task_id: RT-V22\n"
                "closure_status: qualifying_complete\n"
                "implementation_plan:\n"
                f"  plan_id: {v22_plan_id}\n"
                "  plan_task_id: P0-T03\n",
                encoding="utf-8",
            )
            rows = [
                {
                    "task_id": "RT-V21",
                    "task_path": "research_control/tasks/RT-V21",
                    "status": "completed",
                    "closed_at": "2026-08-08T22:00:00Z",
                },
                {
                    "task_id": "RT-V22",
                    "task_path": "research_control/tasks/RT-V22",
                    "status": "completed",
                    "closed_at": "2026-08-08T22:00:01Z",
                },
            ]
            with mock.patch.object(ordinary_route_guard, "_read_csv", return_value=rows):
                identities = completed_plan_task_identities(
                    repo_root,
                    "2026-08-08T23:00:00Z",
                )

            self.assertIn((DEFAULT_PLAN_ID, "P1-T01"), identities)
            self.assertIn((v22_plan_id, "P0-T03"), identities)
            self.assertNotIn((v22_plan_id, "P1-T01"), identities)

    def test_untracked_handoff_requires_exact_atomic_checkpoint_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            handoff_path = repo_root / "research_control/handoffs/handoff-9901.yaml"
            blocker_path = repo_root / "research_control/tasks/RT-OLD/artifacts/blocker.yaml"
            completion_path = (
                repo_root
                / "research_control/tasks/RT-OLD/jobs/completions/AJC-AJ-OLD.yaml"
            )
            for path in (handoff_path, blocker_path, completion_path):
                path.parent.mkdir(parents=True, exist_ok=True)
            handoff_path.write_text(
                "handoff_id: handoff-9901\n"
                "task_id: RT-OLD\n"
                "job_id: AJ-OLD\n"
                "selected_next_route:\n"
                f"  plan_id: {DEFAULT_PLAN_ID}\n"
                "  plan_task_id: P12-T04\n"
                "ordinary_route_guard:\n"
                "  outcome: all_ready_science_blocked_exception\n",
                encoding="utf-8",
            )
            blocker_path.write_text(
                "status: active_blocking\njob_id: AJ-OLD\n",
                encoding="utf-8",
            )
            completion_path.write_text(
                "job_id: AJ-OLD\ncheckpoint_commit:\n  status: PENDING\n",
                encoding="utf-8",
            )
            registry_path = repo_root / ordinary_route_guard.JOB_REGISTRY_PATH
            registry_path.parent.mkdir(parents=True, exist_ok=True)
            registry_path.write_text(
                "job_id,status,completion_path\n"
                "AJ-OLD,completed,research_control/tasks/RT-OLD/jobs/completions/AJC-AJ-OLD.yaml\n",
                encoding="utf-8",
            )
            source_path = handoff_path.relative_to(repo_root).as_posix()
            source_hash = ordinary_route_guard._sha256(handoff_path)
            blocker_rel = blocker_path.relative_to(repo_root).as_posix()
            completion_rel = completion_path.relative_to(repo_root).as_posix()
            job = {
                "plan_id": DEFAULT_PLAN_ID,
                "plan_task_id": "P12-T04",
                "allowed_write_paths": [source_path, blocker_rel, completion_rel],
                "ordinary_route_guard_admission": {
                    "schema_id": ordinary_route_guard.ADMISSION_SCHEMA_ID,
                    "policy_id": POLICY_ID,
                    "source_handoff_id": "handoff-9901",
                    "source_handoff_path": source_path,
                    "source_handoff_sha256": source_hash,
                    "selected_plan_id": DEFAULT_PLAN_ID,
                    "selected_plan_task_id": "P12-T04",
                    "selected_plan_task_ref": f"{DEFAULT_PLAN_ID}:P12-T04",
                    "guard_outcome": "all_ready_science_blocked_exception",
                    "authority_limits": dict(AUTHORITY_LIMITS),
                },
                "checkpoint_recovery": {
                    "schema_id": CHECKPOINT_RECOVERY_SCHEMA_ID,
                    "status": "active",
                    "atomic_checkpoint_required": True,
                    "source_handoff_id": "handoff-9901",
                    "source_handoff_path": source_path,
                    "source_handoff_sha256": source_hash,
                    "prior_job_id": "AJ-OLD",
                    "prior_task_id": "RT-OLD",
                    "blocker_path": blocker_rel,
                    "blocker_sha256": ordinary_route_guard._sha256(blocker_path),
                },
            }
            candidates = {source_path, blocker_rel, completion_rel}
            with mock.patch.object(
                ordinary_route_guard,
                "_tracked_paths",
                return_value=set(),
            ), mock.patch.object(
                ordinary_route_guard,
                "_repository_candidate_paths",
                return_value=candidates,
            ), mock.patch.object(
                ordinary_route_guard,
                "evaluate_research_handoff_guard",
                return_value={"status": "PASS", "errors": [], "warnings": []},
            ):
                result = evaluate_agent_job_route_admission(
                    job,
                    created_at="2026-08-08T23:00:00Z",
                    repo_root=repo_root,
                )
                missing_recovery = copy.deepcopy(job)
                missing_recovery.pop("checkpoint_recovery")
                rejected = evaluate_agent_job_route_admission(
                    missing_recovery,
                    created_at="2026-08-08T23:00:00Z",
                    repo_root=repo_root,
                )

            self.assertEqual(result["status"], "PASS")
            self.assertIn("source_handoff_not_tracked", rejected["errors"])

    def test_hash_bound_reaudit_activation_is_prospective_and_resolvable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            task_root = repo_root / "research_control/tasks"
            source_completion = (
                task_root
                / "RT-20260803-008/jobs/completions/AJC-AJ-RT-20260803-008-001.yaml"
            )
            source_completion.parent.mkdir(parents=True)
            source_completion.write_text(
                "task_id: RT-20260803-008\n"
                "selected_next_route:\n"
                "  plan_task_id: P16-T02\n",
                encoding="utf-8",
            )
            source_hash = ordinary_route_guard._sha256(source_completion)

            audit_path = task_root / "RT-20260803-003"
            audit_path.mkdir(parents=True)
            (audit_path / "00_TASK.yaml").write_text(
                "task_id: RT-20260803-003\n"
                "task_type: v21_p16_t02_gate_authority_consistency_audit\n"
                "closure_status: repair_required_status_layer_drift\n"
                "task_taxonomy:\n"
                "  scope: scientific\n"
                "implementation_plan:\n"
                "  plan_id: recommendations_implementation_plan_continue_task-v21\n"
                "  plan_task_id: P16-T02\n",
                encoding="utf-8",
            )
            activation_path = task_root / "RT-20260803-009"
            activation_path.mkdir(parents=True)
            (activation_path / "00_TASK.yaml").write_text(
                "task_id: RT-20260803-009\n"
                "task_type: project_system_p16_t02_control_spine_reconciliation\n"
                "task_taxonomy:\n"
                "  scope: project_system\n"
                "implementation_plan:\n"
                "  plan_id: recommendations_implementation_plan_continue_task-v21\n"
                "  plan_task_id: P16-T02\n"
                "ordinary_route_guard_plan_reaudit_activation:\n"
                f"  schema_id: {PLAN_REAUDIT_ACTIVATION_SCHEMA_ID}\n"
                "  status: required\n"
                "  plan_task_id: P16-T02\n"
                "  activated_by_task_id: RT-20260803-009\n"
                "  source_task_id: RT-20260803-008\n"
                "  source_completion_path: research_control/tasks/RT-20260803-008/jobs/completions/AJC-AJ-RT-20260803-008-001.yaml\n"
                f"  source_completion_sha256: {source_hash}\n",
                encoding="utf-8",
            )

            rows = [
                {
                    "task_id": "RT-20260803-003",
                    "task_path": "research_control/tasks/RT-20260803-003",
                    "status": "completed",
                    "closed_at": "2026-08-03T05:08:32Z",
                },
                {
                    "task_id": "RT-20260803-009",
                    "task_path": "research_control/tasks/RT-20260803-009",
                    "status": "completed",
                    "closed_at": "2026-08-03T14:42:26Z",
                },
            ]
            with mock.patch.object(
                ordinary_route_guard,
                "_read_csv",
                return_value=rows,
            ), mock.patch.object(
                ordinary_route_guard,
                "_load_backlog",
                return_value=[
                    {
                        "plan_task_id": "P16-T02",
                        "task_class": "science",
                        "depends_on": [],
                    }
                ],
            ):
                before = ordinary_route_guard.completed_plan_task_ids(
                    repo_root, "2026-08-03T14:42:25Z"
                )
                reopened = ordinary_route_guard.completed_plan_task_ids(
                    repo_root, "2026-08-03T14:42:26Z"
                )
            self.assertIn("P16-T02", before)
            self.assertNotIn("P16-T02", reopened)

            resolved_path = task_root / "RT-20260803-010"
            resolved_path.mkdir(parents=True)
            (resolved_path / "00_TASK.yaml").write_text(
                "task_id: RT-20260803-010\n"
                "task_type: v21_p16_t02_gate_authority_consistency_reaudit\n"
                "closure_status: qualifying_finalized_gate_alignment\n"
                "task_taxonomy:\n"
                "  scope: scientific\n"
                "implementation_plan:\n"
                "  plan_id: recommendations_implementation_plan_continue_task-v21\n"
                "  plan_task_id: P16-T02\n",
                encoding="utf-8",
            )
            rows.append(
                {
                    "task_id": "RT-20260803-010",
                    "task_path": "research_control/tasks/RT-20260803-010",
                    "status": "completed",
                    "closed_at": "2026-08-03T15:00:00Z",
                }
            )
            with mock.patch.object(
                ordinary_route_guard,
                "_read_csv",
                return_value=rows,
            ), mock.patch.object(
                ordinary_route_guard,
                "_load_backlog",
                return_value=[
                    {
                        "plan_task_id": "P16-T02",
                        "task_class": "science",
                        "depends_on": [],
                    }
                ],
            ):
                resolved = ordinary_route_guard.completed_plan_task_ids(
                    repo_root, "2026-08-03T15:00:00Z"
                )
            self.assertIn("P16-T02", resolved)


if __name__ == "__main__":
    unittest.main()
