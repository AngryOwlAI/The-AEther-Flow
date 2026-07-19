from __future__ import annotations

import ast
import contextlib
from concurrent.futures import ThreadPoolExecutor
import copy
import datetime as dt
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".codex/skills/continue-research-goal/scripts/goal_state.py"
SPEC = importlib.util.spec_from_file_location("continue_research_goal_state", MODULE_PATH)
assert SPEC and SPEC.loader
goal_state = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(goal_state)


BASE_TIME = "2026-07-10T12:00:00Z"


def binding() -> dict:
    return {
        "execution_profile": "acceptance_test",
        "root": "/tmp/aether-flow-goal-test",
        "branch": "codex/continue-research-goal-test",
        "environment_mode": "local",
        "git_common_dir": "/tmp/aether-flow/.git",
        "starting_head": "a" * 40,
    }


def production_binding(*, branch: str = "codex/v19-remaining-relay") -> dict:
    return {
        "execution_profile": "production_profile",
        "root": "/Volumes/P-SSD/AngryOwl/The-AEther-Flow",
        "branch": branch,
        "environment_mode": "local",
        "git_common_dir": "/Volumes/P-SSD/AngryOwl/The-AEther-Flow/.git",
        "starting_head": "b" * 40,
    }


def contract(label: str = "complete the bounded goal") -> dict:
    return {
        "interpretation": label,
        "required_evidence": ["tracked repository transition", "required validators pass"],
        "user_confirmed_when_ambiguous": False,
    }


def scope_contract() -> dict:
    return {
        "mode": "single_objective",
        "included_work_items": [
            {
                "work_item_id": "objective-1",
                "objective": "complete the bounded goal",
                "depends_on": [],
            }
        ],
        "dependency_source": None,
        "exclusions": ["all work outside the exact user goal"],
        "source_hashes": {"goal-source.md": "c" * 64},
        "allow_scope_expansion": False,
    }


def multi_scope_contract() -> dict:
    return {
        "mode": "multi_step",
        "included_work_items": [
            {"work_item_id": "task-a", "objective": "complete task A", "depends_on": []},
            {"work_item_id": "task-b", "objective": "complete task B", "depends_on": ["task-a"]},
            {"work_item_id": "task-c", "objective": "complete independent task C", "depends_on": []},
        ],
        "dependency_source": {"path": "plan.yaml", "sha256": "e" * 64},
        "exclusions": ["task-d and every unlisted task"],
        "source_hashes": {"plan.yaml": "e" * 64},
        "allow_scope_expansion": False,
    }


def work_result(
    *,
    work_item_id: str = "objective-1",
    status: str = "completed",
    progress: str = "one bounded frame completed",
    agent_job: bool = True,
    outside: list[str] | None = None,
) -> dict:
    return {
        "work_item_id": work_item_id,
        "work_item_status": status,
        "task_id": "RT-TEST-001" if agent_job else None,
        "agent_job_id": "AJ-TEST-001" if agent_job else None,
        "completion_path": "research_control/tasks/RT-TEST-001/completion.yaml" if agent_job else None,
        "completion_sha256": "d" * 64 if agent_job else None,
        "checkpoint_commit": "b" * 40 if agent_job else None,
        "validator_results": ["validate_research_control=PASS"],
        "progress_summary": progress,
        "zero_job_reason": None if agent_job else "no worker AgentJob was required",
        "out_of_scope_remaining_work": outside or [],
    }


def human_intervention(*attempted_strategy_ids: str) -> dict:
    return {
        "required_action": "Choose extension or cancellation after reviewing canonical evidence.",
        "reason": "No safe authorized autonomous route remains.",
        "blocking_evidence_hashes": ["f" * 64],
        "safe_authorized_strategies_exhausted": True,
        "attempted_strategy_ids": list(attempted_strategy_ids),
        "remaining_safe_authorized_strategy_ids": [],
    }


def dirty_manifest(*, changed_hash: str = "1" * 64) -> dict:
    return {
        "owning_task_id": "RT-TEST-001",
        "owning_agent_job_id": "AJ-TEST-001",
        "head": "b" * 40,
        "porcelain": " M generated.txt",
        "changed_paths": [{"path": "generated.txt", "sha256": changed_hash}],
        "failed_gates": [
            {
                "gate_id": "generated_derivative",
                "status": "FAIL",
                "evidence_sha256": "2" * 64,
            }
        ],
    }


def fingerprint(label: str) -> str:
    return goal_state.canonical_fingerprint(
        {
            "branch": "codex/continue-research-goal-test",
            "head": label,
            "program_state_sha256": label * 4,
            "status": "",
            "validators": ["PASS"],
        }
    )


class GoalStateTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.goals = Path(self.temp.name) / "goals"
        self.store = goal_state.GoalStore(self.goals)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def initialize(
        self,
        *,
        goal: str = "Perform two bounded passes.",
        passes: int = 3,
        goal_id: str | None = None,
        reasoning_effort: str = "max",
    ):
        return self.store.initialize(
            goal_text=goal,
            completion_contract=contract(),
            scope_contract=scope_contract(),
            reasoning_effort=reasoning_effort,
            max_continue_passes=passes,
            max_elapsed_minutes=60,
            repository_binding=binding(),
            initial_fingerprint=fingerprint("A"),
            goal_id=goal_id,
            timestamp=BASE_TIME,
            launcher_token="launcher-token",
        )

    def reserve_and_record(self, path: Path, record: dict, generation: int = 1, successor: str = "thread-1"):
        record = self.store.reserve_successor(
            path,
            expected_revision=record["state"]["revision"],
            predecessor_thread_id="launcher" if generation == 1 else f"thread-{generation - 1}",
            handoff_token=f"handoff-token-{generation}",
            timestamp=BASE_TIME,
        )
        record = self.store.record_successor(
            path,
            expected_revision=record["state"]["revision"],
            generation=generation,
            handoff_token=f"handoff-token-{generation}",
            successor_thread_id=successor,
            timestamp=BASE_TIME,
        )
        return record

    def claim(self, path: Path, record: dict, generation: int = 1, token: str = "claim-token"):
        return self.store.claim_generation(
            path,
            expected_revision=record["state"]["revision"],
            generation=generation,
            handoff_token=f"handoff-token-{generation}",
            idempotency_key=f"{record['goal_id']}:{generation}",
            claim_token=token,
            timestamp=BASE_TIME,
        )

    def returned_step(
        self,
        path: Path,
        record: dict,
        generation: int,
        claim_token: str,
        after: str,
        evaluation: str,
        *,
        worker_skill: str = "continue-research",
        work_item_id: str = "objective-1",
        work_item_status: str | None = None,
        observed_dirty_state_manifest: dict | None = None,
        agent_job: bool = True,
    ):
        record = self.store.consume_invocation(
            path,
            expected_revision=record["state"]["revision"],
            generation=generation,
            claim_token=claim_token,
            worker_skill=worker_skill,
            observed_dirty_state_manifest=observed_dirty_state_manifest,
            timestamp=BASE_TIME,
        )
        record = self.store.record_invocation_returned(
            path,
            expected_revision=record["state"]["revision"],
            generation=generation,
            claim_token=claim_token,
            worker_skill=worker_skill,
            execution_evidence={"skill": worker_skill, "returned": True},
            observed_dirty_state_manifest=observed_dirty_state_manifest,
            timestamp=BASE_TIME,
        )
        record = self.store.verify_step(
            path,
            expected_revision=record["state"]["revision"],
            generation=generation,
            claim_token=claim_token,
            after_fingerprint=after,
            goal_evaluation=evaluation,
            evidence={
                "after_head": "b" * 40,
                "active_task_id": "RT-TEST-001",
                "latest_handoff_id": "handoff-test",
                "agent_job_id": "AJ-TEST-001",
                "checkpoint_commit": "b" * 40,
                "validator_results": ["validate_research_control=PASS"],
                "progress_summary": "one bounded pass completed",
                "remaining_work": "one pass remains" if evaluation == "unmet" else "none",
                "work_result": work_result(
                    work_item_id=work_item_id,
                    status=work_item_status
                    or ("completed" if evaluation == "met" else "in_progress"),
                    progress="one bounded pass completed",
                    agent_job=agent_job,
                ),
            },
            timestamp=BASE_TIME,
        )
        return record


class SerializationAndSchemaTests(GoalStateTestCase):
    def test_v4_default_effort_contract_and_omitted_scheduling_guards(self):
        path, record = self.store.initialize(
            goal_text="unbounded scheduling horizon",
            completion_contract=contract(),
            scope_contract=scope_contract(),
            reasoning_effort="max",
            repository_binding=binding(),
            initial_fingerprint=fingerprint("A"),
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["schema_version"], "continue-research-goal.v4")
        self.assertEqual(record["discussion_contract"]["reasoning_effort"], "max")
        self.assertEqual(
            record["discussion_contract"]["accepted_goal_sha256"],
            record["goal_sha256"],
        )
        self.assertEqual(
            record["discussion_contract"]["confirmation_marker"],
            goal_state.DISCUSSION_CONFIRMATION_MARKER,
        )
        self.assertEqual(
            record["discussion_contract_sha256"],
            goal_state.sha256_json(record["discussion_contract"]),
        )
        initialized = record["journal"][0]["payload"]
        self.assertEqual(
            initialized["discussion_contract_sha256"],
            record["discussion_contract_sha256"],
        )
        self.assertIsNone(record["guards"]["max_continue_passes"])
        self.assertIsNone(record["deadline_at"])
        self.assertIsNone(goal_state.effective_guards(record)["max_continue_passes"])
        self.assertIsNone(goal_state.effective_guards(record)["deadline_at"])
        self.assertEqual(self.store.read(path), record)

    def test_pass_and_absolute_deadline_overrides_are_independent(self):
        path, record = self.store.initialize(
            goal_text="pass-only guard",
            completion_contract=contract(),
            scope_contract=scope_contract(),
            reasoning_effort="max",
            max_continue_passes=4,
            repository_binding=binding(),
            initial_fingerprint=fingerprint("A"),
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["guards"]["max_continue_passes"], 4)
        self.assertIsNone(record["deadline_at"])
        terminal = self.store.reserve_successor(
            path,
            expected_revision=record["state"]["revision"],
            predecessor_thread_id="launcher",
            handoff_token="handoff-token-1",
            timestamp=BASE_TIME,
        )
        self.store.dispatch_failure(
            path,
            expected_revision=terminal["state"]["revision"],
            generation=1,
            handoff_token="handoff-token-1",
            outcome="definitive",
            diagnostic={"fixture": "release lease"},
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )

        _, record = self.store.initialize(
            goal_text="deadline-only guard",
            completion_contract=contract(),
            scope_contract=scope_contract(),
            reasoning_effort="max",
            deadline_at="2026-07-10T15:30:00+02:00",
            repository_binding=binding(),
            initial_fingerprint=fingerprint("B"),
            timestamp=BASE_TIME,
        )
        self.assertIsNone(record["guards"]["max_continue_passes"])
        self.assertEqual(record["deadline_at"], "2026-07-10T13:30:00Z")

    def test_deadline_validation_rejects_invalid_naive_and_nonfuture_values(self):
        for index, deadline in enumerate(
            ("invalid", "2026-07-10T13:00:00", BASE_TIME, "2026-07-10T11:59:59Z")
        ):
            with self.subTest(deadline=deadline):
                with self.assertRaises(goal_state.ValidationError):
                    self.store.initialize(
                        goal_text=f"invalid deadline {index}",
                        completion_contract=contract(),
                        scope_contract=scope_contract(),
                        reasoning_effort="max",
                        deadline_at=deadline,
                        repository_binding=binding(),
                        initial_fingerprint=fingerprint("A"),
                        timestamp=BASE_TIME,
                    )

    def test_finite_scheduling_overrides_require_positive_integers(self):
        for kwargs in (
            {"max_continue_passes": 0},
            {"max_continue_passes": True},
            {"max_elapsed_minutes": 0},
            {"max_elapsed_minutes": True},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(goal_state.ValidationError):
                    self.store.initialize(
                        goal_text="invalid finite scheduling guard",
                        completion_contract=contract(),
                        scope_contract=scope_contract(),
                        reasoning_effort="max",
                        repository_binding=binding(),
                        initial_fingerprint=fingerprint("A"),
                        timestamp=BASE_TIME,
                        **kwargs,
                    )

    def test_legacy_elapsed_alias_derives_deadline_and_conflicts_with_absolute_deadline(self):
        with self.assertRaises(goal_state.ValidationError):
            self.store.initialize(
                goal_text="conflicting deadline inputs",
                completion_contract=contract(),
                scope_contract=scope_contract(),
                reasoning_effort="max",
                deadline_at="2026-07-10T13:00:00Z",
                max_elapsed_minutes=30,
                repository_binding=binding(),
                initial_fingerprint=fingerprint("A"),
                timestamp=BASE_TIME,
            )
        _, record = self.store.initialize(
            goal_text="legacy elapsed alias",
            completion_contract=contract(),
            scope_contract=scope_contract(),
            reasoning_effort="max",
            max_elapsed_minutes=30,
            repository_binding=binding(),
            initial_fingerprint=fingerprint("A"),
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["schema_version"], "continue-research-goal.v4")
        self.assertEqual(record["deadline_at"], "2026-07-10T12:30:00Z")

    def test_cli_deadline_arguments_are_optional_and_mutually_exclusive(self):
        common = [
            "--goals-dir",
            str(self.goals),
            "initialize",
            "--goal-text",
            "CLI fixture",
            "--completion-contract-json",
            json.dumps(contract()),
            "--scope-contract-json",
            json.dumps(scope_contract()),
            "--reasoning-effort",
            "max",
            "--repository-binding-json",
            json.dumps(binding()),
            "--initial-fingerprint",
            fingerprint("A"),
        ]
        args = goal_state.build_parser().parse_args(common)
        self.assertIsNone(args.max_continue_passes)
        self.assertIsNone(args.deadline_at)
        self.assertIsNone(args.max_elapsed_minutes)
        self.assertEqual(args.reasoning_effort, "max")
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                goal_state.build_parser().parse_args(
                    common
                    + [
                        "--deadline-at",
                        "2026-07-10T13:00:00Z",
                        "--max-elapsed-minutes",
                        "60",
                    ]
                )

        missing_effort = common.copy()
        effort_index = missing_effort.index("--reasoning-effort")
        del missing_effort[effort_index : effort_index + 2]
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                goal_state.build_parser().parse_args(missing_effort)

    def test_alternate_reasoning_effort_serializes_and_summarizes(self):
        path, record = self.initialize(reasoning_effort="high")
        summary = self.store.summarize(path)
        self.assertEqual(record["discussion_contract"]["reasoning_effort"], "high")
        self.assertEqual(summary["reasoning_effort"], "high")
        self.assertEqual(
            summary["discussion_contract_sha256"],
            record["discussion_contract_sha256"],
        )

    def test_unsupported_reasoning_effort_is_rejected_without_state(self):
        with self.assertRaises(goal_state.ValidationError):
            self.store.initialize(
                goal_text="unsupported reasoning fixture",
                completion_contract=contract(),
                scope_contract=scope_contract(),
                reasoning_effort="extreme",
                repository_binding=binding(),
                initial_fingerprint=fingerprint("A"),
                timestamp=BASE_TIME,
            )
        self.assertEqual(list(self.goals.glob("goal-*.md")), [])

    def _retained_record(self, record: dict, schema_version: str) -> dict:
        retained = copy.deepcopy(record)
        retained["schema_version"] = schema_version
        for key in (
            "discussion_contract",
            "discussion_contract_sha256",
            "scope_contract",
            "scope_contract_sha256",
            "recovery_ledger",
            "completion_summary",
            "completion_summary_sha256",
            "human_intervention_summary",
            "human_intervention_summary_sha256",
        ):
            retained.pop(key)
        for key in ("approved_route", "approved_route_sha256", "human_intervention"):
            retained["state"].pop(key)
        for key in (
            "stop_on_human_gate",
            "stop_on_validation_failure",
            "stop_on_checkpoint_failure",
            "stop_on_unexpected_dirty_state",
            "stop_on_no_progress",
            "stop_on_repeated_state",
            "stop_on_capability_loss",
            "stop_on_branch_or_repository_mismatch",
        ):
            retained["guards"].pop(key)
        return retained

    def test_v1_finite_record_validates_and_round_trips_without_mutation(self):
        path, record = self.initialize()
        legacy = self._retained_record(record, goal_state.LEGACY_SCHEMA_VERSION)
        path.write_text(goal_state.render_goal(legacy), encoding="utf-8")
        before = path.read_bytes()
        loaded = self.store.read(path)
        self.assertEqual(loaded["schema_version"], "continue-research-goal.v1")
        self.assertIsInstance(loaded["guards"]["max_continue_passes"], int)
        self.assertIsInstance(loaded["deadline_at"], str)
        self.assertEqual(goal_state.render_goal(loaded).encode("utf-8"), before)
        self.assertEqual(path.read_bytes(), before)

    def test_v2_record_validates_byte_for_byte_but_cannot_resume(self):
        path, record = self.initialize()
        retained = self._retained_record(record, goal_state.RETAINED_SCHEMA_VERSION)
        path.write_text(goal_state.render_goal(retained), encoding="utf-8")
        before = path.read_bytes()
        loaded = self.store.read(path)
        self.assertEqual(loaded["schema_version"], "continue-research-goal.v2")
        self.assertEqual(path.read_bytes(), before)
        with self.assertRaises(goal_state.StateConflict):
            self.store.reserve_successor(
                path,
                expected_revision=loaded["state"]["revision"],
                predecessor_thread_id="launcher",
            )
        self.assertEqual(path.read_bytes(), before)

    def test_v3_record_is_validation_and_summary_only_without_migration(self):
        path, record = self.initialize()
        retained = copy.deepcopy(record)
        retained["schema_version"] = goal_state.AUTONOMOUS_SCHEMA_VERSION
        retained.pop("discussion_contract")
        retained.pop("discussion_contract_sha256")
        path.write_text(goal_state.render_goal(retained), encoding="utf-8")
        before = path.read_bytes()
        loaded = self.store.read(path)
        summary = self.store.summarize(path)
        self.assertEqual(loaded["schema_version"], "continue-research-goal.v3")
        self.assertEqual(summary["reasoning_effort"], None)
        self.assertIn("validation and summary only", summary["reader_report"])
        with self.assertRaises(goal_state.StateConflict):
            self.store.reserve_successor(
                path,
                expected_revision=loaded["state"]["revision"],
                predecessor_thread_id="launcher",
            )
        self.assertEqual(path.read_bytes(), before)

    def test_exact_goal_serialization_hash_and_round_trip(self):
        exact = "  α goal\r\nline two\r\n"
        path, record = self.initialize(goal=exact)
        expected = "  α goal\nline two\n"
        self.assertEqual(record["goal_text"], expected)
        self.assertEqual(record["goal_sha256"], goal_state.sha256_bytes(expected.encode("utf-8")))
        self.assertEqual(self.store.read(path), record)
        self.assertNotIn(expected, path.read_text(encoding="utf-8").split("# Goal relay record", 1)[1])

    def test_secret_goal_and_acceptance_main_binding_are_rejected(self):
        with self.assertRaises(goal_state.ValidationError):
            self.initialize(goal="use api_key=super-secret-value")
        bad = binding()
        bad["branch"] = "main"
        with self.assertRaises(goal_state.ValidationError):
            self.store.initialize(
                goal_text="safe goal",
                completion_contract=contract(),
                scope_contract=scope_contract(),
                reasoning_effort="max",
                max_continue_passes=1,
                max_elapsed_minutes=1,
                repository_binding=bad,
                initial_fingerprint=fingerprint("A"),
                timestamp=BASE_TIME,
            )

    def test_v4_production_profile_main_round_trips(self):
        path, record = self.store.initialize(
            goal_text="safe production goal on main",
            completion_contract=contract(),
            scope_contract=scope_contract(),
            reasoning_effort="max",
            max_continue_passes=2,
            max_elapsed_minutes=30,
            repository_binding=production_binding(branch="main"),
            initial_fingerprint=fingerprint("A"),
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["schema_version"], goal_state.SCHEMA_VERSION)
        self.assertEqual(record["repository_binding"]["execution_profile"], "production_profile")
        self.assertEqual(record["repository_binding"]["branch"], "main")
        self.assertEqual(self.store.read(path), record)

    def test_retained_v1_v3_records_bound_to_main_remain_rejected(self):
        path, record = self.store.initialize(
            goal_text="safe production goal on main",
            completion_contract=contract(),
            scope_contract=scope_contract(),
            reasoning_effort="max",
            max_continue_passes=2,
            max_elapsed_minutes=30,
            repository_binding=production_binding(branch="main"),
            initial_fingerprint=fingerprint("A"),
            timestamp=BASE_TIME,
        )
        for schema_version in (
            goal_state.LEGACY_SCHEMA_VERSION,
            goal_state.RETAINED_SCHEMA_VERSION,
            goal_state.AUTONOMOUS_SCHEMA_VERSION,
        ):
            retained = self._retained_record(record, schema_version)
            path.write_text(goal_state.render_goal(retained), encoding="utf-8")
            with self.subTest(schema_version=schema_version):
                with self.assertRaises(goal_state.ValidationError):
                    self.store.read(path)

    def test_production_profile_round_trips_and_unknown_profile_fails_closed(self):
        bad = production_binding()
        bad["execution_profile"] = "unregistered_profile"
        with self.assertRaises(goal_state.ValidationError):
            self.store.initialize(
                goal_text="safe goal",
                completion_contract=contract(),
                scope_contract=scope_contract(),
                reasoning_effort="max",
                max_continue_passes=1,
                max_elapsed_minutes=1,
                repository_binding=bad,
                initial_fingerprint=fingerprint("A"),
                timestamp=BASE_TIME,
            )

        path, record = self.store.initialize(
            goal_text="safe production goal",
            completion_contract=contract(),
            scope_contract=scope_contract(),
            reasoning_effort="max",
            max_continue_passes=2,
            max_elapsed_minutes=30,
            repository_binding=production_binding(),
            initial_fingerprint=fingerprint("A"),
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["repository_binding"]["execution_profile"], "production_profile")
        self.assertEqual(self.store.read(path), record)

    def test_contract_and_guard_amendments_are_append_only_and_hash_validated(self):
        path, record = self.initialize()
        original_contract = copy.deepcopy(record["completion_contract"])
        original_guards = copy.deepcopy(record["guards"])
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.store.pre_execution_stop(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            stop_reason="human_gate",
            evidence={
                "zero_agent_job_reason": "protected human decision",
                "progress_summary": "protected human gate detected before worker execution",
                "out_of_scope_remaining_work": [],
            },
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )
        record = self.store.begin_recovery(
            path,
            expected_revision=record["state"]["revision"],
            user_authorization="user approves contract clarification",
            canonical_reconciliation={"prior_holder_terminal": True},
            timestamp=BASE_TIME,
        )
        new_contract = contract("complete after two distinct checkpoint commits")
        record = self.store.amend_completion_contract(
            path,
            expected_revision=record["state"]["revision"],
            user_authorization="user confirms the evidence interpretation",
            new_contract=new_contract,
            timestamp=BASE_TIME,
        )
        later = (goal_state.parse_utc(record["deadline_at"]) + dt.timedelta(hours=2)).isoformat().replace("+00:00", "Z")
        record = self.store.amend_guards(
            path,
            expected_revision=record["state"]["revision"],
            user_authorization="user extends the pass and time guards",
            new_guards={"max_continue_passes": 5, "deadline_at": later},
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["completion_contract"], original_contract)
        self.assertEqual(record["guards"], original_guards)
        self.assertEqual(goal_state.effective_completion_contract(record), new_contract)
        self.assertEqual(goal_state.effective_guards(record)["max_continue_passes"], 5)
        self.store.read(path)

    def test_v2_guard_amendments_allow_finite_to_unlimited_but_never_tighten_unlimited(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.store.pre_execution_stop(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            stop_reason="human_gate",
            evidence={
                "zero_agent_job_reason": "guard amendment fixture",
                "progress_summary": "guard amendment is required before worker execution",
                "out_of_scope_remaining_work": [],
            },
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )
        record = self.store.begin_recovery(
            path,
            expected_revision=record["state"]["revision"],
            user_authorization="user authorizes scheduling-horizon extension",
            canonical_reconciliation={"prior_holder_terminal": True},
            timestamp=BASE_TIME,
        )
        record = self.store.amend_guards(
            path,
            expected_revision=record["state"]["revision"],
            user_authorization="user makes both finite scheduling guards unlimited",
            new_guards={"max_continue_passes": None, "deadline_at": None},
            timestamp=BASE_TIME,
        )
        effective = goal_state.effective_guards(record)
        self.assertIsNone(effective["max_continue_passes"])
        self.assertIsNone(effective["deadline_at"])
        revision = record["state"]["revision"]
        for tightening in (
            {"max_continue_passes": 100},
            {"deadline_at": "2026-07-11T12:00:00Z"},
            {"max_continue_passes": None},
            {"deadline_at": None},
        ):
            with self.subTest(tightening=tightening):
                with self.assertRaises(goal_state.ValidationError):
                    self.store.amend_guards(
                        path,
                        expected_revision=revision,
                        user_authorization="attempted tightening",
                        new_guards=tightening,
                        timestamp=BASE_TIME,
                    )
                self.assertEqual(self.store.read(path)["state"]["revision"], revision)

    def test_corrupted_schema_hash_journal_body_and_filename_fail_closed(self):
        path, record = self.initialize()
        variants = []
        for mutate in (
            lambda item: item.__setitem__("schema_version", "wrong"),
            lambda item: item.__setitem__("goal_sha256", "0" * 64),
            lambda item: item["discussion_contract"].__setitem__(
                "reasoning_effort",
                "high",
            ),
            lambda item: item["journal"][0].__setitem__("entry_hash", "0" * 64),
        ):
            candidate = copy.deepcopy(record)
            mutate(candidate)
            variants.append(candidate)
        for candidate in variants:
            path.write_text(goal_state.render_goal(candidate), encoding="utf-8")
            with self.assertRaises(goal_state.ValidationError):
                self.store.read(path)
            path.write_text(goal_state.render_goal(record), encoding="utf-8")
        path.write_text(goal_state.render_goal(record) + "tamper\n", encoding="utf-8")
        with self.assertRaises(goal_state.ValidationError):
            self.store.read(path)
        path.write_text(goal_state.render_goal(record), encoding="utf-8")
        wrong = path.with_name("goal-crg-20260710T120000Z-deadbeef.md")
        path.rename(wrong)
        with self.assertRaises(goal_state.ValidationError):
            self.store.read(wrong)

    def test_rehashed_discussion_tamper_is_rejected_by_initialization_evidence(self):
        path, record = self.initialize()
        tampered = copy.deepcopy(record)
        tampered["discussion_contract"]["reasoning_effort"] = "high"
        tampered["discussion_contract_sha256"] = goal_state.sha256_json(
            tampered["discussion_contract"]
        )
        path.write_text(goal_state.render_goal(tampered), encoding="utf-8")
        with self.assertRaisesRegex(
            goal_state.ValidationError,
            "initialization evidence does not bind discussion contract",
        ):
            self.store.read(path)

    def test_path_traversal_symlink_and_hardlink_are_rejected(self):
        path, _ = self.initialize()
        outside = Path(self.temp.name) / path.name
        outside.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        with self.assertRaises(goal_state.ValidationError):
            self.store.read(outside)
        link = self.goals / "goal-crg-20260710T120000Z-bbbbbbbb.md"
        link.symlink_to(path)
        with self.assertRaises(goal_state.ValidationError):
            self.store.read(link)
        hard = self.goals / "goal-crg-20260710T120000Z-cccccccc.md"
        hard.hardlink_to(path)
        with self.assertRaises(goal_state.ValidationError):
            self.store.read(path)


class AtomicityAndConcurrencyTests(GoalStateTestCase):
    def test_exclusive_collision_safe_creation(self):
        fixed = "crg-20260710T120000Z-aaaaaaaa"
        path, record = self.initialize(goal_id=fixed)
        self.assertTrue(path.exists())
        with self.assertRaises(goal_state.ActiveRelayError):
            self.initialize(goal_id="crg-20260710T120000Z-bbbbbbbb")
        terminal = self.store.reserve_successor(
            path,
            expected_revision=record["state"]["revision"],
            predecessor_thread_id="launcher",
            handoff_token="handoff-token-1",
            timestamp=BASE_TIME,
        )
        terminal = self.store.dispatch_failure(
            path,
            expected_revision=terminal["state"]["revision"],
            generation=1,
            handoff_token="handoff-token-1",
            outcome="definitive",
            diagnostic={"created": False},
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )
        with self.assertRaises(goal_state.StateConflict):
            self.initialize(goal_id=fixed)

    def test_two_simultaneous_launchers_have_one_global_lease_winner(self):
        barrier = threading.Barrier(2)

        def launch(suffix: str):
            store = goal_state.GoalStore(self.goals)
            barrier.wait()
            try:
                path, _ = store.initialize(
                    goal_text=f"goal {suffix}",
                    completion_contract=contract(),
                    scope_contract=scope_contract(),
                    reasoning_effort="max",
                    max_continue_passes=2,
                    max_elapsed_minutes=30,
                    repository_binding=binding(),
                    initial_fingerprint=fingerprint("A"),
                    goal_id=f"crg-20260710T120000Z-{suffix * 8}",
                    timestamp=BASE_TIME,
                )
                return ("won", path.name)
            except goal_state.ActiveRelayError:
                return ("lost", suffix)

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(launch, ("a", "b")))
        self.assertEqual([status for status, _ in results].count("won"), 1)
        self.assertEqual(len(list(self.goals.glob("goal-*.md"))), 1)

    def test_stale_revision_is_rejected_and_atomic_temp_files_do_not_remain(self):
        path, record = self.initialize()
        updated = self.store.reserve_successor(
            path,
            expected_revision=record["state"]["revision"],
            predecessor_thread_id="launcher",
            handoff_token="handoff-token-1",
            timestamp=BASE_TIME,
        )
        with self.assertRaises(goal_state.StateConflict):
            self.store.record_successor(
                path,
                expected_revision=record["state"]["revision"],
                generation=1,
                handoff_token="handoff-token-1",
                successor_thread_id="thread-1",
                timestamp=BASE_TIME,
            )
        self.assertEqual(self.store.read(path), updated)
        self.assertEqual(list(self.goals.glob("*.tmp")), [])

    def test_two_simultaneous_claims_have_exactly_one_winner(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        revision = record["state"]["revision"]
        barrier = threading.Barrier(2)

        def claim(token: str):
            store = goal_state.GoalStore(self.goals)
            barrier.wait()
            try:
                store.claim_generation(
                    path,
                    expected_revision=revision,
                    generation=1,
                    handoff_token="handoff-token-1",
                    idempotency_key=f"{record['goal_id']}:1",
                    claim_token=token,
                    timestamp=BASE_TIME,
                )
                return "won"
            except goal_state.StateConflict:
                return "lost"

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(claim, ("claim-a", "claim-b")))
        self.assertEqual(results.count("won"), 1)
        self.assertEqual(self.store.read(path, require_lease_parity=True)["state"]["phase"], "step_active")

    def test_cross_file_transaction_mismatch_blocks_writers(self):
        path, record = self.initialize()
        lease = json.loads(self.store.global_lease_path.read_text(encoding="utf-8"))
        lease["transaction_id"] = "corrupt"
        self.store.global_lease_path.write_text(json.dumps(lease), encoding="utf-8")
        with self.assertRaises(goal_state.ValidationError):
            self.store.reserve_successor(
                path,
                expected_revision=record["state"]["revision"],
                predecessor_thread_id="launcher",
            )
        with self.assertRaises(goal_state.ActiveRelayError):
            self.initialize(goal_id="crg-20260710T120000Z-dddddddd")


class StateMachineTests(GoalStateTestCase):
    def test_normal_recursive_edge_finalizes_one_receipt_and_one_successor(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.returned_step(path, record, 1, "claim-token", fingerprint("B"), "unmet")
        record = self.store.decide_step(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            decision="continuation_required",
            timestamp=BASE_TIME,
        )
        record = self.store.reserve_successor(
            path,
            expected_revision=record["state"]["revision"],
            predecessor_thread_id="thread-1",
            handoff_token="handoff-token-2",
            timestamp=BASE_TIME,
        )
        with self.assertRaises(goal_state.StateConflict):
            self.store.reserve_successor(
                path,
                expected_revision=record["state"]["revision"],
                predecessor_thread_id="thread-1",
            )
        record = self.store.record_successor(
            path,
            expected_revision=record["state"]["revision"],
            generation=2,
            handoff_token="handoff-token-2",
            successor_thread_id="thread-2",
            timestamp=BASE_TIME,
        )
        idempotent = self.store.record_successor(
            path,
            expected_revision=record["state"]["revision"] - 1,
            generation=2,
            handoff_token="handoff-token-2",
            successor_thread_id="thread-2",
            timestamp=BASE_TIME,
        )
        self.assertEqual(idempotent["state"]["revision"], record["state"]["revision"])
        receipts = [item for item in record["journal"] if item["kind"] == "step_receipt"]
        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]["payload"]["successor_thread_id"], "thread-2")
        self.assertEqual(record["generations"]["1"]["finalized_receipt_hash"], receipts[0]["entry_hash"])

    def test_success_base_case_releases_leases_and_has_no_successor(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.returned_step(path, record, 1, "claim-token", fingerprint("B"), "met")
        record = self.store.decide_step(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            decision="terminal_complete",
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["state"]["phase"], "terminal_complete")
        self.assertIsNone(record["state"]["active_lease"])
        self.assertFalse(self.store.global_lease_path.exists())
        self.assertEqual(record["generations"]["1"]["successor_thread_id"], "thread-1")
        self.assertNotIn("2", record["generations"])
        with self.assertRaises(goal_state.StateConflict):
            self.store.begin_recovery(
                path,
                expected_revision=record["state"]["revision"],
                user_authorization="resume",
                canonical_reconciliation={"terminal": True},
            )

    def test_pre_execution_stop_consumes_zero_and_finalizes_once(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.store.pre_execution_stop(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            stop_reason="validation",
            evidence={
                "zero_agent_job_reason": "validator failed before research",
                "progress_summary": "validator failure prevented worker execution",
                "out_of_scope_remaining_work": [],
            },
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )
        receipt = next(item for item in record["journal"] if item["kind"] == "step_receipt")
        self.assertEqual(receipt["payload"]["continue_research_invocation_count"], 0)
        self.assertEqual(record["state"]["passes_consumed"], 0)
        with self.assertRaises(goal_state.StateConflict):
            self.store.pre_execution_stop(
                path,
                expected_revision=record["state"]["revision"],
                generation=1,
                claim_token="claim-token",
                stop_reason="validation",
                human_intervention=human_intervention(),
            )

    def test_consumption_replay_is_blocked_and_pass_count_increments_once(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        before_revision = record["state"]["revision"]
        record = self.store.consume_invocation(
            path,
            expected_revision=before_revision,
            generation=1,
            claim_token="claim-token",
            worker_skill="continue-research",
            timestamp=BASE_TIME,
        )
        with self.assertRaises(goal_state.StateConflict):
            self.store.consume_invocation(
                path,
                expected_revision=record["state"]["revision"],
                generation=1,
                claim_token="claim-token",
                worker_skill="continue-research",
                timestamp=BASE_TIME,
            )
        self.assertEqual(self.store.read(path)["state"]["passes_consumed"], 1)

    def test_uncertain_crash_gap_keeps_both_leases_quarantined_then_records_unknown(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.store.consume_invocation(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            worker_skill="continue-research",
            timestamp=BASE_TIME,
        )
        record = self.store.record_invocation_uncertain(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            worker_skill="continue-research",
            diagnostic={"crash_window": "consumption_before_research_return"},
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )
        self.assertTrue(record["state"]["active_lease"]["quarantined"])
        self.assertTrue(json.loads(self.store.global_lease_path.read_text())["quarantined"])
        self.assertIsNone(record["generations"]["1"]["finalized_receipt_hash"])
        record = self.store.begin_recovery(
            path,
            expected_revision=record["state"]["revision"],
            user_authorization="user authorizes reconciliation only",
            canonical_reconciliation={"prior_holder_terminal": True, "state_stable": True},
            timestamp=BASE_TIME,
        )
        record = self.store.reconcile_consumed(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            returned_proven=False,
            terminal_holder_proof={"thread_state": "completed"},
            canonical_evidence={
                "after_head": "unknown",
                "goal_evaluation": "indeterminate",
                "work_result": work_result(
                    status="blocked",
                    progress="worker outcome remains unknown",
                    agent_job=False,
                ),
            },
            decision="terminal_awaiting_human",
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )
        receipt = next(item for item in record["journal"] if item["kind"] == "step_receipt")
        self.assertEqual(receipt["payload"]["continue_research_invocation_count"], "unknown")
        self.assertFalse(self.store.global_lease_path.exists())

    def test_abandoned_unconsumed_generation_gets_zero_receipt(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.store.abandon_unconsumed(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            user_authorization="user authorizes abandoned claim recovery",
            terminal_holder_proof={"thread_state": "failed"},
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )
        receipt = next(item for item in record["journal"] if item["kind"] == "step_receipt")
        self.assertEqual(receipt["payload"]["continue_research_invocation_count"], 0)
        self.assertEqual(record["state"]["passes_consumed"], 0)

    def test_dispatch_terminal_mappings(self):
        expected = {
            "definitive": "terminal_failed",
            "ambiguous": "terminal_handoff_ambiguous",
            "duplicate": "terminal_duplicate_detected",
            "timeout": "terminal_handoff_timeout",
        }
        for index, (outcome, phase) in enumerate(expected.items()):
            with self.subTest(outcome=outcome):
                with tempfile.TemporaryDirectory() as temp:
                    store = goal_state.GoalStore(Path(temp) / "goals")
                    path, record = store.initialize(
                        goal_text="dispatch fixture",
                        completion_contract=contract(),
                        scope_contract=scope_contract(),
                        reasoning_effort="max",
                        max_continue_passes=2,
                        max_elapsed_minutes=20,
                        repository_binding=binding(),
                        initial_fingerprint=fingerprint("A"),
                        goal_id=f"crg-20260710T120000Z-{index + 1:08x}",
                        timestamp=BASE_TIME,
                    )
                    record = store.reserve_successor(
                        path,
                        expected_revision=record["state"]["revision"],
                        predecessor_thread_id="launcher",
                        handoff_token="token",
                        timestamp=BASE_TIME,
                    )
                    record = store.dispatch_failure(
                        path,
                        expected_revision=record["state"]["revision"],
                        generation=1,
                        handoff_token="token",
                        outcome=outcome,
                        diagnostic={"fixture": outcome},
                        human_intervention=human_intervention(),
                        timestamp=BASE_TIME,
                    )
                    self.assertEqual(record["state"]["phase"], phase)
                    if outcome == "ambiguous":
                        self.assertTrue(store.global_lease_path.exists())
                    else:
                        self.assertFalse(store.global_lease_path.exists())

    def test_handoff_wait_is_read_only_until_created(self):
        path, record = self.initialize()
        record = self.store.reserve_successor(
            path,
            expected_revision=record["state"]["revision"],
            predecessor_thread_id="launcher",
            handoff_token="handoff-token-1",
            timestamp=BASE_TIME,
        )
        revision = record["state"]["revision"]
        self.assertFalse(
            self.store.handoff_ready(
                path,
                generation=1,
                handoff_token="handoff-token-1",
                idempotency_key=f"{record['goal_id']}:1",
            )
        )
        self.assertEqual(self.store.read(path)["state"]["revision"], revision)

    def test_illegal_edges_are_rejected_without_mutation(self):
        path, record = self.initialize()
        with self.assertRaises(goal_state.StateConflict):
            self.store.claim_generation(
                path,
                expected_revision=record["state"]["revision"],
                generation=1,
                handoff_token="missing",
                idempotency_key=f"{record['goal_id']}:1",
            )
        self.assertEqual(self.store.read(path), record)
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        with self.assertRaises(goal_state.StateConflict):
            self.store.decide_step(
                path,
                expected_revision=record["state"]["revision"],
                generation=1,
                claim_token="claim-token",
                decision="terminal_complete",
            )
        self.assertEqual(self.store.read(path), record)

    def test_guard_deadline_and_pass_limit_stop_before_second_consumption(self):
        path, record = self.initialize(passes=1)
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        late = "2026-07-10T14:00:00Z"
        with self.assertRaises(goal_state.GuardStop):
            self.store.consume_invocation(
                path,
                expected_revision=record["state"]["revision"],
                generation=1,
                claim_token="claim-token",
                worker_skill="continue-research",
                timestamp=late,
            )
        unchanged = self.store.read(path)
        self.assertFalse(unchanged["generations"]["1"]["invocation_consumed"])
        self.assertEqual(unchanged["state"]["passes_consumed"], 0)

    def test_unlimited_scheduling_guards_do_not_stop_at_former_limits(self):
        path, record = self.store.initialize(
            goal_text="unlimited guard fixture",
            completion_contract=contract(),
            scope_contract=scope_contract(),
            reasoning_effort="max",
            repository_binding=binding(),
            initial_fingerprint=fingerprint("A"),
            timestamp=BASE_TIME,
        )
        record["state"]["passes_consumed"] = 10001
        self.assertEqual(
            self.store.check_guards(record, timestamp="2099-07-10T14:00:00Z"),
            [],
        )
        self.store._write_record(path, record)
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.store.consume_invocation(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            worker_skill="continue-research",
            timestamp="2099-07-10T14:00:00Z",
        )
        self.assertEqual(record["state"]["passes_consumed"], 10002)

    def test_finite_pass_and_deadline_guards_stop_independently(self):
        _, record = self.initialize(passes=1)
        record["state"]["passes_consumed"] = 1
        self.assertEqual(self.store.check_guards(record, timestamp=BASE_TIME), ["pass_limit"])
        record["state"]["passes_consumed"] = 0
        self.assertEqual(
            self.store.check_guards(record, timestamp="2026-07-10T13:00:00Z"),
            ["elapsed_limit"],
        )


class V4AutonomousRoutingTests(GoalStateTestCase):
    def initialize_multi(self):
        return self.store.initialize(
            goal_text="Complete task A and then task B; preserve independent task C.",
            completion_contract=contract("complete the explicitly included plan tasks"),
            scope_contract=multi_scope_contract(),
            reasoning_effort="max",
            max_continue_passes=8,
            max_elapsed_minutes=120,
            repository_binding=binding(),
            initial_fingerprint=fingerprint("A"),
            timestamp=BASE_TIME,
            launcher_token="launcher-token",
        )

    def recovery_plan(
        self,
        record: dict,
        *,
        strategy_id: str,
        worker_skill: str = "continue-research",
        work_item_id: str | None = None,
        manifest: dict | None = None,
    ) -> dict:
        generation = record["state"]["current_generation"]
        entry = record["generations"][str(generation)]
        return {
            "worker_skill": worker_skill,
            "reason_id": f"recover_with_{strategy_id}",
            "strategy_id": strategy_id,
            "work_item_id": work_item_id or entry["route"]["work_item_id"],
            "blocker_fingerprint": entry.get("after_fingerprint")
            or record["state"]["last_canonical_fingerprint"],
            "evidence_hashes": ["3" * 64],
            "dirty_state_manifest": manifest,
            "work_result": copy.deepcopy(entry["pending_step_result"]["work_result"]),
        }

    def test_explicit_multi_step_scope_crosses_included_task_boundary_and_summarizes(self):
        path, record = self.initialize_multi()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.returned_step(
            path,
            record,
            1,
            "claim-token",
            fingerprint("B"),
            "unmet",
            work_item_id="task-a",
            work_item_status="completed",
        )
        record = self.store.decide_step(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            decision="continuation_required",
            next_work_item_id="task-b",
            timestamp=BASE_TIME,
        )
        record = self.reserve_and_record(path, record, generation=2, successor="thread-2")
        self.assertEqual(record["generations"]["2"]["route"]["work_item_id"], "task-b")
        record = self.claim(path, record, generation=2, token="claim-token-2")
        record = self.returned_step(
            path,
            record,
            2,
            "claim-token-2",
            fingerprint("C"),
            "met",
            work_item_id="task-b",
            work_item_status="completed",
        )
        record = self.store.decide_step(
            path,
            expected_revision=record["state"]["revision"],
            generation=2,
            claim_token="claim-token-2",
            decision="terminal_complete",
            timestamp=BASE_TIME,
        )
        summary = self.store.summarize(path)
        self.assertEqual(summary["finalized_receipt_count"], 2)
        self.assertEqual(summary["phase"], "terminal_complete")
        self.assertTrue(summary["reader_report"].startswith("Goal reached.\n"))
        self.assertIn(json.dumps(record["goal_text"], ensure_ascii=False), summary["reader_report"])
        self.assertTrue(summary["reader_report"].endswith("That goal was reached."))
        self.assertEqual(record["completion_summary_sha256"], goal_state.sha256_json(record["completion_summary"]))

    def test_single_objective_scope_rejects_unlisted_next_task(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.returned_step(
            path,
            record,
            1,
            "claim-token",
            fingerprint("B"),
            "unmet",
            work_item_status="completed",
        )
        revision = record["state"]["revision"]
        with self.assertRaises(goal_state.StateConflict):
            self.store.decide_step(
                path,
                expected_revision=revision,
                generation=1,
                claim_token="claim-token",
                decision="continuation_required",
                next_work_item_id="task-b",
                timestamp=BASE_TIME,
            )
        self.assertEqual(self.store.read(path)["state"]["revision"], revision)

    def test_research_to_project_system_repair_to_resumed_research_counts_every_frame(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.returned_step(
            path,
            record,
            1,
            "claim-token",
            fingerprint("B"),
            "unmet",
            work_item_status="in_progress",
        )
        manifest = dirty_manifest()
        plan = self.recovery_plan(
            record,
            strategy_id="repair_generated_derivative",
            worker_skill="improve-project-system",
            manifest=manifest,
        )
        record = self.store.record_recovery_required(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            recovery_plan=plan,
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["state"]["phase"], "recovery_required")
        self.assertEqual(len(record["recovery_ledger"]), 1)
        record = self.reserve_and_record(path, record, generation=2, successor="thread-2")
        self.assertEqual(
            record["generations"]["2"]["route"]["worker_skill"],
            "improve-project-system",
        )
        record = self.claim(path, record, generation=2, token="repair-claim")
        revision = record["state"]["revision"]
        with self.assertRaises(goal_state.StateConflict):
            self.store.consume_invocation(
                path,
                expected_revision=revision,
                generation=2,
                claim_token="repair-claim",
                worker_skill="continue-research",
                timestamp=BASE_TIME,
            )
        with self.assertRaises(goal_state.StateConflict):
            self.store.consume_invocation(
                path,
                expected_revision=revision,
                generation=2,
                claim_token="repair-claim",
                worker_skill="improve-project-system",
                observed_dirty_state_manifest=dirty_manifest(changed_hash="4" * 64),
                timestamp=BASE_TIME,
            )
        self.assertEqual(self.store.read(path)["state"]["revision"], revision)
        record = self.returned_step(
            path,
            record,
            2,
            "repair-claim",
            fingerprint("C"),
            "unmet",
            worker_skill="improve-project-system",
            work_item_status="repair_completed",
            observed_dirty_state_manifest=manifest,
        )
        self.assertEqual(record["state"]["passes_consumed"], 2)
        record = self.store.decide_step(
            path,
            expected_revision=record["state"]["revision"],
            generation=2,
            claim_token="repair-claim",
            decision="continuation_required",
            timestamp=BASE_TIME,
        )
        record = self.store.reserve_successor(
            path,
            expected_revision=record["state"]["revision"],
            predecessor_thread_id="thread-2",
            handoff_token="handoff-token-3",
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["generations"]["3"]["route"]["worker_skill"], "continue-research")
        self.assertEqual(
            record["generations"]["3"]["route"]["reason_id"],
            "resume_research_after_project_system_repair",
        )

    def test_human_gated_item_is_deferred_while_independent_scope_continues(self):
        path, record = self.initialize_multi()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.returned_step(
            path,
            record,
            1,
            "claim-token",
            fingerprint("B"),
            "unmet",
            work_item_id="task-a",
            work_item_status="deferred_human_gate",
        )
        record = self.store.decide_step(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            decision="continuation_required",
            next_work_item_id="task-c",
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["state"]["phase"], "continuation_required")
        self.assertEqual(record["state"]["approved_route"]["work_item_id"], "task-c")
        self.assertIsNone(record["state"]["human_intervention"])

    def test_repeated_fingerprint_switches_distinct_strategies_then_stops_with_exact_human_action(self):
        path, record = self.initialize(passes=6)
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.returned_step(
            path,
            record,
            1,
            "claim-token",
            fingerprint("A"),
            "unmet",
            work_item_status="in_progress",
        )
        record = self.store.record_recovery_required(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            claim_token="claim-token",
            recovery_plan=self.recovery_plan(record, strategy_id="source_acquisition"),
            timestamp=BASE_TIME,
        )
        record = self.reserve_and_record(path, record, generation=2, successor="thread-2")
        record = self.claim(path, record, generation=2, token="claim-2")
        record = self.returned_step(
            path,
            record,
            2,
            "claim-2",
            fingerprint("A"),
            "unmet",
            work_item_status="in_progress",
        )
        duplicate_plan = self.recovery_plan(record, strategy_id="source_acquisition")
        revision = record["state"]["revision"]
        with self.assertRaises(goal_state.StateConflict):
            self.store.record_recovery_required(
                path,
                expected_revision=revision,
                generation=2,
                claim_token="claim-2",
                recovery_plan=duplicate_plan,
                timestamp=BASE_TIME,
            )
        record = self.store.record_recovery_required(
            path,
            expected_revision=revision,
            generation=2,
            claim_token="claim-2",
            recovery_plan=self.recovery_plan(record, strategy_id="bounded_calculation"),
            timestamp=BASE_TIME,
        )
        record = self.reserve_and_record(path, record, generation=3, successor="thread-3")
        record = self.claim(path, record, generation=3, token="claim-3")
        record = self.returned_step(
            path,
            record,
            3,
            "claim-3",
            fingerprint("A"),
            "unmet",
            work_item_status="blocked",
        )
        record = self.store.decide_step(
            path,
            expected_revision=record["state"]["revision"],
            generation=3,
            claim_token="claim-3",
            decision="terminal_no_progress",
            human_intervention=human_intervention(
                "source_acquisition",
                "bounded_calculation",
            ),
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["state"]["passes_consumed"], 3)
        self.assertEqual(record["state"]["phase"], "terminal_no_progress")
        self.assertTrue(
            record["human_intervention_summary"]["reader_report"].startswith(
                "Goal not reached — human action required"
            )
        )

    def test_dispatch_reconciliation_retries_only_after_zero_children_or_adopts_one(self):
        path, record = self.initialize()
        record = self.store.reserve_successor(
            path,
            expected_revision=record["state"]["revision"],
            predecessor_thread_id="launcher",
            handoff_token="handoff-token-1",
            timestamp=BASE_TIME,
        )
        record = self.store.reconcile_dispatch(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            handoff_token="handoff-token-1",
            recovery_evidence={
                "prior_holder_terminal": True,
                "matching_unclaimed_successor_ids": [],
                "capability_available": True,
                "inspection_evidence_hashes": ["5" * 64],
            },
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["state"]["phase"], "recovery_required")
        record = self.store.reserve_successor(
            path,
            expected_revision=record["state"]["revision"],
            predecessor_thread_id="launcher",
            handoff_token="handoff-token-2",
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["state"]["current_generation"], 2)

        with tempfile.TemporaryDirectory() as temp:
            store = goal_state.GoalStore(Path(temp) / "goals")
            path, record = store.initialize(
                goal_text="dispatch adoption fixture",
                completion_contract=contract(),
                scope_contract=scope_contract(),
                reasoning_effort="max",
                max_continue_passes=2,
                max_elapsed_minutes=30,
                repository_binding=binding(),
                initial_fingerprint=fingerprint("A"),
                timestamp=BASE_TIME,
            )
            record = store.reserve_successor(
                path,
                expected_revision=record["state"]["revision"],
                predecessor_thread_id="launcher",
                handoff_token="token",
                timestamp=BASE_TIME,
            )
            revision = record["state"]["revision"]
            with self.assertRaises(goal_state.StateConflict):
                store.reconcile_dispatch(
                    path,
                    expected_revision=revision,
                    generation=1,
                    handoff_token="token",
                    recovery_evidence={
                        "prior_holder_terminal": True,
                        "matching_unclaimed_successor_ids": ["thread-a", "thread-b"],
                        "capability_available": True,
                        "inspection_evidence_hashes": ["6" * 64],
                    },
                    timestamp=BASE_TIME,
                )
            self.assertEqual(store.read(path)["state"]["revision"], revision)
            record = store.reconcile_dispatch(
                path,
                expected_revision=revision,
                generation=1,
                handoff_token="token",
                recovery_evidence={
                    "prior_holder_terminal": True,
                    "matching_unclaimed_successor_ids": ["thread-only"],
                    "capability_available": True,
                    "inspection_evidence_hashes": ["7" * 64],
                },
                timestamp=BASE_TIME,
            )
            self.assertEqual(record["state"]["phase"], "successor_created")
            self.assertEqual(record["handoff"]["successor_thread_id"], "thread-only")

    def test_scope_contract_hash_and_route_hash_fail_closed(self):
        path, record = self.initialize()
        tampered = copy.deepcopy(record)
        tampered["scope_contract"]["exclusions"].append("silently added exclusion")
        path.write_text(goal_state.render_goal(tampered), encoding="utf-8")
        with self.assertRaises(goal_state.ValidationError):
            self.store.read(path)
        path.write_text(goal_state.render_goal(record), encoding="utf-8")
        record = self.reserve_and_record(path, record)
        tampered = copy.deepcopy(record)
        tampered["generations"]["1"]["route"]["strategy_id"] = "rewritten"
        path.write_text(goal_state.render_goal(tampered), encoding="utf-8")
        with self.assertRaises(goal_state.ValidationError):
            self.store.read(path)


class FingerprintAndReceiptTests(GoalStateTestCase):
    def test_canonical_fingerprint_is_deterministic_and_detects_cycle(self):
        one = {"z": [2, 1], "a": {"y": 2, "x": 1}}
        two = {"a": {"x": 1, "y": 2}, "z": [2, 1]}
        self.assertEqual(goal_state.canonical_fingerprint(one), goal_state.canonical_fingerprint(two))
        a = fingerprint("A")
        b = fingerprint("B")
        self.assertEqual(goal_state.fingerprint_status([a], a), "unchanged")
        self.assertEqual(goal_state.fingerprint_status([a], b), "new")
        self.assertEqual(goal_state.fingerprint_status([a, b], a), "repeated")

    def test_unchanged_and_a_b_a_fingerprints_cannot_recurse(self):
        for after in (fingerprint("A"), fingerprint("A")):
            with tempfile.TemporaryDirectory() as temp:
                store = goal_state.GoalStore(Path(temp) / "goals")
                path, record = store.initialize(
                    goal_text="fingerprint fixture",
                    completion_contract=contract(),
                    scope_contract=scope_contract(),
                    reasoning_effort="max",
                    max_continue_passes=3,
                    max_elapsed_minutes=30,
                    repository_binding=binding(),
                    initial_fingerprint=fingerprint("A"),
                    timestamp=BASE_TIME,
                )
                record = store.reserve_successor(path, expected_revision=record["state"]["revision"], predecessor_thread_id="launcher", handoff_token="handoff-token-1", timestamp=BASE_TIME)
                record = store.record_successor(path, expected_revision=record["state"]["revision"], generation=1, handoff_token="handoff-token-1", successor_thread_id="thread-1", timestamp=BASE_TIME)
                record = store.claim_generation(path, expected_revision=record["state"]["revision"], generation=1, handoff_token="handoff-token-1", idempotency_key=f"{record['goal_id']}:1", claim_token="claim", timestamp=BASE_TIME)
                record = store.consume_invocation(path, expected_revision=record["state"]["revision"], generation=1, claim_token="claim", worker_skill="continue-research", timestamp=BASE_TIME)
                record = store.record_invocation_returned(path, expected_revision=record["state"]["revision"], generation=1, claim_token="claim", worker_skill="continue-research", execution_evidence={"returned": True}, timestamp=BASE_TIME)
                record = store.verify_step(path, expected_revision=record["state"]["revision"], generation=1, claim_token="claim", after_fingerprint=after, goal_evaluation="unmet", evidence={"progress_summary": "none", "work_result": work_result(status="in_progress", progress="no canonical progress")}, timestamp=BASE_TIME)
                with self.assertRaises(goal_state.StateConflict):
                    store.decide_step(path, expected_revision=record["state"]["revision"], generation=1, claim_token="claim", decision="continuation_required", timestamp=BASE_TIME)

        history = [fingerprint("A"), fingerprint("B")]
        self.assertEqual(goal_state.fingerprint_status(history, fingerprint("A")), "repeated")

    def test_finalized_receipt_cannot_be_replayed_or_mutated(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.returned_step(path, record, 1, "claim-token", fingerprint("B"), "met")
        record = self.store.decide_step(path, expected_revision=record["state"]["revision"], generation=1, claim_token="claim-token", decision="terminal_complete", timestamp=BASE_TIME)
        receipts = [entry for entry in record["journal"] if entry["kind"] == "step_receipt"]
        self.assertEqual(len(receipts), 1)
        with self.assertRaises(goal_state.StateConflict):
            self.store.decide_step(path, expected_revision=record["state"]["revision"], generation=1, claim_token="claim-token", decision="terminal_complete", timestamp=BASE_TIME)
        tampered = copy.deepcopy(record)
        next(item for item in tampered["journal"] if item["kind"] == "step_receipt")["payload"]["progress_summary"] = "rewritten"
        path.write_text(goal_state.render_goal(tampered), encoding="utf-8")
        with self.assertRaises(goal_state.ValidationError):
            self.store.read(path)

    def test_all_stop_mappings_and_representative_forbidden_reason(self):
        for reason, phase in goal_state.STOP_PHASES.items():
            self.assertEqual(goal_state.map_stop(reason), phase)
        with self.assertRaises(goal_state.ValidationError):
            goal_state.map_stop("invented_success")


class CrashWindowTests(GoalStateTestCase):
    def test_intent_before_create_and_create_before_id_record_are_recoverable(self):
        path, record = self.initialize()
        record = self.store.reserve_successor(path, expected_revision=record["state"]["revision"], predecessor_thread_id="launcher", handoff_token="handoff-token-1", timestamp=BASE_TIME)
        self.assertEqual(record["state"]["phase"], "successor_intent")
        self.assertFalse(self.store.handoff_ready(path, generation=1, handoff_token="handoff-token-1", idempotency_key=f"{record['goal_id']}:1"))
        recorded = self.store.record_successor(path, expected_revision=record["state"]["revision"], generation=1, handoff_token="handoff-token-1", successor_thread_id="thread-returned-before-record", timestamp=BASE_TIME)
        again = self.store.record_successor(path, expected_revision=record["state"]["revision"], generation=1, handoff_token="handoff-token-1", successor_thread_id="thread-returned-before-record", timestamp=BASE_TIME)
        self.assertEqual(recorded, again)

    def test_concrete_id_record_failure_writes_only_ignored_recovery_sidecar(self):
        path, record = self.initialize()
        record = self.store.reserve_successor(path, expected_revision=record["state"]["revision"], predecessor_thread_id="launcher", handoff_token="handoff-token-1", timestamp=BASE_TIME)
        sidecar = self.store.write_dispatch_recovery_sidecar(
            path,
            generation=1,
            handoff_token="handoff-token-1",
            idempotency_key=f"{record['goal_id']}:1",
            returned_thread_id="thread-created",
            expected_revision=record["state"]["revision"],
            error="record-only persistence failed",
            timestamp=BASE_TIME,
        )
        payload = json.loads(sidecar.read_text(encoding="utf-8"))
        self.assertEqual(payload["returned_thread_id"], "thread-created")
        self.assertEqual(self.store.read(path)["state"]["phase"], "successor_intent")

    def test_recovery_can_adopt_one_uniquely_proven_live_unclaimed_successor(self):
        path, record = self.initialize()
        record = self.store.reserve_successor(path, expected_revision=record["state"]["revision"], predecessor_thread_id="launcher", handoff_token="handoff-token-1", timestamp=BASE_TIME)
        record = self.store.dispatch_failure(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            handoff_token="handoff-token-1",
            outcome="ambiguous",
            diagnostic={"create_result": "unknown"},
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )
        record = self.store.begin_recovery(
            path,
            expected_revision=record["state"]["revision"],
            user_authorization="adopt the uniquely proven child",
            canonical_reconciliation={"prior_holder_terminal": True},
            timestamp=BASE_TIME,
        )
        record = self.store.adopt_successor(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            successor_thread_id="thread-unique-live",
            unique_live_successor_proof={"matching_threads": ["thread-unique-live"], "state": "running"},
            timestamp=BASE_TIME,
        )
        self.assertEqual(record["state"]["phase"], "successor_created")
        self.assertEqual(record["handoff"]["successor_thread_id"], "thread-unique-live")
        self.assertTrue(self.store.handoff_ready(path, generation=1, handoff_token="handoff-token-1", idempotency_key=f"{record['goal_id']}:1"))

    def test_id_record_before_predecessor_exit_allows_only_one_claim(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        claimed = self.claim(path, record)
        with self.assertRaises(goal_state.StateConflict):
            self.store.claim_generation(path, expected_revision=claimed["state"]["revision"], generation=1, handoff_token="handoff-token-1", idempotency_key=f"{record['goal_id']}:1", claim_token="other", timestamp=BASE_TIME)

    def test_return_before_receipt_can_be_completed_without_second_consumption(self):
        path, record = self.initialize()
        record = self.reserve_and_record(path, record)
        record = self.claim(path, record)
        record = self.store.consume_invocation(path, expected_revision=record["state"]["revision"], generation=1, claim_token="claim-token", worker_skill="continue-research", timestamp=BASE_TIME)
        record = self.store.record_invocation_uncertain(path, expected_revision=record["state"]["revision"], generation=1, claim_token="claim-token", worker_skill="continue-research", diagnostic={"crash": "return-before-receipt"}, human_intervention=human_intervention(), timestamp=BASE_TIME)
        record = self.store.begin_recovery(path, expected_revision=record["state"]["revision"], user_authorization="reconcile returned pass", canonical_reconciliation={"holder_terminal": True}, timestamp=BASE_TIME)
        record = self.store.reconcile_consumed(
            path,
            expected_revision=record["state"]["revision"],
            generation=1,
            returned_proven=True,
            terminal_holder_proof={"thread_state": "completed"},
            canonical_evidence={"after_head": "b" * 40, "goal_evaluation": "unmet", "progress_summary": "pass returned", "work_result": work_result(status="in_progress", progress="pass returned")},
            decision="terminal_awaiting_human",
            human_intervention=human_intervention(),
            timestamp=BASE_TIME,
        )
        receipt = next(item for item in record["journal"] if item["kind"] == "step_receipt")
        self.assertEqual(receipt["payload"]["continue_research_invocation_count"], 1)
        self.assertEqual(record["state"]["passes_consumed"], 1)


class RepositoryContractTests(unittest.TestCase):
    def test_skill_frontmatter_names_are_unique_and_discoverable_once(self):
        paths = {
            "continue-research-goal": ROOT / ".codex/skills/continue-research-goal/SKILL.md",
            "continue-research-continue-goal": ROOT / ".codex/skills/continue-research-continue-goal/SKILL.md",
        }
        found = {}
        for path in ROOT.glob(".codex/skills/**/SKILL.md"):
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---\n"):
                continue
            front = text[4:].split("\n---\n", 1)[0]
            for line in front.splitlines():
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip()
                    found.setdefault(name, []).append(path)
        for name, path in paths.items():
            self.assertEqual(found.get(name), [path])

    def test_launcher_has_zero_research_execution_and_recursive_contract_has_one(self):
        launcher = (ROOT / ".codex/skills/continue-research-goal/SKILL.md").read_text(encoding="utf-8")
        recursive = (ROOT / ".codex/skills/continue-research-continue-goal/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("invokes `continue-research` zero times", launcher)
        self.assertIn("invoke `$continue-research` exactly once", recursive)
        self.assertIn("creates zero or one successor", recursive)

    def test_main_branch_policy_is_production_v4_only(self):
        launcher = (ROOT / ".codex/skills/continue-research-goal/SKILL.md").read_text(
            encoding="utf-8"
        )
        recursive = (
            ROOT / ".codex/skills/continue-research-continue-goal/SKILL.md"
        ).read_text(encoding="utf-8")
        schema = (
            ROOT / ".codex/skills/continue-research-goal/references/goal-file-schema.md"
        ).read_text(encoding="utf-8")
        self.assertIn("accept either `main` or a\nbranch under `codex/*`", launcher)
        self.assertIn("acceptance\nprofile, reject a different root or branch and continue to reject `main`", launcher)
        self.assertIn("A v4 `production_profile` branch may be `main`", recursive)
        self.assertIn("an `acceptance_test` branch", recursive)
        self.assertIn("For new v4 records, `main` is valid only with `production_profile`", schema)
        self.assertIn("Retained v1-v3 records bound to `main`\nremain invalid", schema)

    def test_launcher_acceptance_loop_covers_defaults_edits_and_ambiguous_approval(self):
        launcher = (ROOT / ".codex/skills/continue-research-goal/SKILL.md").read_text(
            encoding="utf-8"
        )
        for token in (
            'reasoning_effort: "<value>"',
            "Omission of `reasoning_effort` selects `max`",
            "edits only the goal, preserve the previously selected",
            "edits only the effort, preserve the goal",
            "edits both simultaneously, replace both candidates",
            "restart the loop",
            "ambiguous approval",
            "create no state",
        ):
            self.assertIn(token, launcher)

    def test_launcher_metadata_mismatch_stops_before_initialization(self):
        launcher = (ROOT / ".codex/skills/continue-research-goal/SKILL.md").read_text(
            encoding="utf-8"
        )
        metadata = 'nodeRepl.requestMeta["x-codex-turn-metadata"]'
        self.assertIn(metadata, launcher)
        self.assertIn("active metadata model", launcher)
        self.assertIn("current-task `reasoning_effort` exactly equals", launcher)
        self.assertIn("stops before goal initialization", launcher)
        self.assertIn("change the Codex UI reasoning setting", launcher)
        self.assertLess(launcher.index(metadata), launcher.index("call helper `initialize` exactly once"))

    def test_both_relay_skills_pin_thinking_and_omit_model(self):
        launcher = (ROOT / ".codex/skills/continue-research-goal/SKILL.md").read_text(
            encoding="utf-8"
        )
        recursive = (
            ROOT / ".codex/skills/continue-research-continue-goal/SKILL.md"
        ).read_text(encoding="utf-8")
        pinned_call = (
            "create_thread(..., thinking=<persisted discussion_contract reasoning_effort>)"
        )
        for text in (launcher, recursive):
            self.assertIn(pinned_call, text)
            self.assertIn("omit the `model` argument", text)
            self.assertIn("silently downgrade", text)
        self.assertIn("rely on default inheritance", launcher)
        self.assertIn("inherit a default reasoning effort", recursive)

    def test_recursive_effort_checks_precede_claim_and_successor_reservation(self):
        recursive = (
            ROOT / ".codex/skills/continue-research-continue-goal/SKILL.md"
        ).read_text(encoding="utf-8")
        metadata = 'nodeRepl.requestMeta["x-codex-turn-metadata"]'
        self.assertIn(metadata, recursive)
        self.assertIn("stops before generation claim", recursive)
        self.assertLess(recursive.index(metadata), recursive.index("Call helper `claim` exactly once"))
        rediscover = (
            "rediscover the exact saved project and current `create_thread` contract\n"
            "   before successor reservation"
        )
        self.assertIn(rediscover, recursive)
        self.assertLess(
            recursive.index(rediscover),
            recursive.index("call helper `reserve-successor` once"),
        )

    def test_native_goal_operations_appear_only_in_forbidden_sections(self):
        banned = ("create_goal", "get_goal", "update_goal", "thread/goal/", "`/goal`")
        for relative in (
            ".codex/skills/continue-research-goal/SKILL.md",
            ".codex/skills/continue-research-continue-goal/SKILL.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            executable, forbidden = text.split("## Forbidden Actions", 1)
            for token in banned:
                self.assertNotIn(token, executable)
                self.assertIn(token, forbidden)
        helper = MODULE_PATH.read_text(encoding="utf-8")
        for token in banned:
            self.assertNotIn(token, helper)

    def test_helper_has_no_task_research_network_or_git_mutation_api(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imports = {node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)}
        self.assertFalse(imports & {"subprocess", "socket", "requests", "urllib"})
        source = MODULE_PATH.read_text(encoding="utf-8")
        for token in ("create_thread", "list_projects", "continue_research.py", "git commit", "git push"):
            self.assertNotIn(token, source)

    def test_nested_ignore_covers_all_runtime_files_and_only_ignore_is_tracked(self):
        runtime = [
            ".codex/skills/continue-research-goal/goals/goal-fixture.md",
            ".codex/skills/continue-research-goal/goals/goal-fixture.lock",
            ".codex/skills/continue-research-goal/goals/goal-fixture.tmp",
            ".codex/skills/continue-research-goal/goals/goal-fixture.dispatch-recovery.json",
            ".codex/skills/continue-research-goal/goals/.relay-lease.json",
            ".codex/skills/continue-research-goal/goals/.relay-lease.lock",
        ]
        for path in runtime:
            result = subprocess.run(["git", "check-ignore", "-q", "--no-index", path], cwd=ROOT)
            self.assertEqual(result.returncode, 0, path)
        visible = subprocess.check_output(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                ".codex/skills/continue-research-goal/goals",
            ],
            cwd=ROOT,
            text=True,
        ).splitlines()
        self.assertEqual(visible, [".codex/skills/continue-research-goal/goals/.gitignore"])

    def test_runtime_goal_instances_are_absent_from_registries_and_generated_outputs(self):
        registries = ROOT / "registries"
        for path in registries.glob("*.csv"):
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    fields = line.rstrip("\n").split(",")
                    self.assertFalse(any("/goals/goal-" in field for field in fields), path)
        tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
        self.assertFalse(any("/goals/goal-" in path for path in tracked))

    def test_primary_main_worktree_is_clean_or_contains_one_governed_transaction(self):
        lines = subprocess.check_output(["git", "worktree", "list", "--porcelain"], cwd=ROOT, text=True).splitlines()
        main_path = None
        current_path = None
        for line in lines:
            if line.startswith("worktree "):
                current_path = Path(line.split(" ", 1)[1])
            elif line == "branch refs/heads/main":
                main_path = current_path
        if main_path is None:
            self.skipTest("no primary main worktree is present")
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=main_path, text=True)
        if status:
            governed = subprocess.run(
                [
                    ".venv/bin/python",
                    "scripts/research_control/validate_research_control.py",
                    "--check-diff",
                ],
                cwd=main_path,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            self.assertEqual(governed.returncode, 0, governed.stdout)


if __name__ == "__main__":
    unittest.main()
