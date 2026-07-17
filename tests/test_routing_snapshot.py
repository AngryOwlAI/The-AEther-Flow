"""Focused tests for the narrow active-state routing validator."""

from __future__ import annotations

import csv
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from scripts.research_control import continue_research
from scripts.research_control import validate_research_control
from scripts.research_control import validate_routing_snapshot as routing


class RoutingFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.allowed_write_paths = ["output/result.json", "research_control/tasks/RT-TEST/**"]
        self._build()

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def write_csv(
        self,
        relative: str,
        fieldnames: list[str],
        rows: list[dict[str, str]],
    ) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _build(self) -> None:
        allowlist = ";".join(self.allowed_write_paths)
        self.write_csv(
            "registries/RESEARCH_TASK_REGISTRY.csv",
            [
                "task_id",
                "task_path",
                "task_type",
                "status",
                "current_decision_id",
                "current_job_id",
                "parent_task_id",
                "created_at",
                "updated_at",
                "closed_at",
                "closure_status",
                "requires_human_gate",
                "notes",
            ],
            [
                {
                    "task_id": "RT-TEST",
                    "task_path": "research_control/tasks/RT-TEST",
                    "task_type": "fixture",
                    "status": "completed",
                    "current_decision_id": "DDR-TEST",
                    "current_job_id": "AJ-TEST",
                    "parent_task_id": "",
                    "created_at": "2026-01-01T00:00:00Z",
                    "updated_at": "2026-01-01T00:00:00Z",
                    "closed_at": "2026-01-01T00:00:00Z",
                    "closure_status": "fixture_complete",
                    "requires_human_gate": "false",
                    "notes": "fixture",
                }
            ],
        )
        self.write_csv(
            "registries/DIRECTOR_DECISION_REGISTRY.csv",
            [
                "decision_id",
                "task_id",
                "decision_path",
                "director_version",
                "decision_type",
                "selected_role_id",
                "selected_role_version",
                "agent_job_id",
                "status",
                "supersedes_decision_id",
                "requires_human_gate",
                "created_at",
                "activated_at",
                "completed_at",
                "validation_status",
                "notes",
            ],
            [
                {
                    "decision_id": "DDR-TEST",
                    "task_id": "RT-TEST",
                    "decision_path": "research_control/tasks/RT-TEST/DDR-TEST.md",
                    "director_version": "project-system-director@0.2.0",
                    "decision_type": "task_overlay",
                    "selected_role_id": "validator-engineer",
                    "selected_role_version": "0.2.0",
                    "agent_job_id": "AJ-TEST",
                    "status": "completed",
                    "supersedes_decision_id": "",
                    "requires_human_gate": "false",
                    "created_at": "2026-01-01T00:00:00Z",
                    "activated_at": "2026-01-01T00:00:00Z",
                    "completed_at": "2026-01-01T00:00:00Z",
                    "validation_status": "PASS",
                    "notes": "fixture",
                }
            ],
        )
        self.write_csv(
            "registries/AGENT_JOB_REGISTRY.csv",
            [
                "job_id",
                "task_id",
                "decision_id",
                "role_id",
                "role_version",
                "job_path",
                "completion_path",
                "status",
                "allowed_write_paths",
                "output_paths",
                "validation_status",
                "created_at",
                "started_at",
                "completed_at",
                "requires_human_gate",
                "notes",
            ],
            [
                {
                    "job_id": "AJ-TEST",
                    "task_id": "RT-TEST",
                    "decision_id": "DDR-TEST",
                    "role_id": "validator-engineer",
                    "role_version": "0.2.0",
                    "job_path": "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
                    "completion_path": (
                        "research_control/tasks/RT-TEST/jobs/completions/"
                        "AJC-AJ-TEST.yaml"
                    ),
                    "status": "completed",
                    "allowed_write_paths": allowlist,
                    "output_paths": "output/result.json",
                    "validation_status": "PASS",
                    "created_at": "2026-01-01T00:00:00Z",
                    "started_at": "2026-01-01T00:00:00Z",
                    "completed_at": "2026-01-01T00:00:00Z",
                    "requires_human_gate": "false",
                    "notes": "fixture",
                }
            ],
        )
        self.write_csv(
            "registries/ROLE_EXECUTION_REGISTRY.csv",
            [
                "execution_role_ref",
                "role_execution_kind",
                "task_id",
                "agent_job_id",
                "record_path",
                "base_role_id",
                "base_role_version",
                "provisional_role_name",
                "authority_delta_summary",
                "added_constraints",
                "removed_permissions",
                "expanded_permissions",
                "allowed_write_paths",
                "requires_human_gate",
                "expires_after",
                "justification",
                "non_reusable_until_registered",
                "validation_status",
                "created_at",
                "updated_at",
                "notes",
            ],
            [
                {
                    "execution_role_ref": "validator-engineer@0.2.0--RT-TEST",
                    "role_execution_kind": "task_overlay",
                    "task_id": "RT-TEST",
                    "agent_job_id": "AJ-TEST",
                    "record_path": (
                        "research_control/tasks/RT-TEST/roles/"
                        "validator-engineer@0.2.0--RT-TEST.yaml"
                    ),
                    "base_role_id": "validator-engineer",
                    "base_role_version": "0.2.0",
                    "provisional_role_name": "Fixture validator",
                    "authority_delta_summary": "Fixture-only authority",
                    "added_constraints": "fixture only",
                    "removed_permissions": "physics authority",
                    "expanded_permissions": "fixture validation",
                    "allowed_write_paths": allowlist,
                    "requires_human_gate": "false",
                    "expires_after": "AJ-TEST",
                    "justification": "fixture",
                    "non_reusable_until_registered": "false",
                    "validation_status": "PASS",
                    "created_at": "2026-01-01T00:00:00Z",
                    "updated_at": "2026-01-01T00:00:00Z",
                    "notes": "fixture",
                }
            ],
        )
        self.write_csv(
            "registries/AGENT_ROLE_REGISTRY.csv",
            [
                "role_id",
                "version",
                "role_name",
                "role_kind",
                "role_contract_path",
                "authority_level",
                "status",
                "requires_human_gate",
            ],
            [
                {
                    "role_id": "validator-engineer",
                    "version": "0.2.0",
                    "role_name": "Validator Engineer",
                    "role_kind": "process_control",
                    "role_contract_path": (
                        ".agents/roles/research_ops/"
                        "validator-engineer.v0.2.0.md"
                    ),
                    "authority_level": "process_control",
                    "status": "active",
                    "requires_human_gate": "false",
                }
            ],
        )
        self.write(
            ".agents/roles/research_ops/validator-engineer.v0.2.0.md",
            """---
role_id: "validator-engineer"
version: "0.2.0"
role_kind: "process_control"
authority_level: "process_control"
status: "active"
requires_human_gate: false
---

# Fixture Validator
""",
        )
        self.write(
            "research_control/tasks/RT-TEST/00_TASK.yaml",
            """task_id: "RT-TEST"
task_type: "fixture"
status: "completed"
current_decision_id: "DDR-TEST"
current_job_id: "AJ-TEST"
requires_human_gate: false
""",
        )
        self.write(
            "research_control/tasks/RT-TEST/DDR-TEST.md",
            """---
decision_id: "DDR-TEST"
task_id: "RT-TEST"
selected_role_id: "validator-engineer"
selected_role_version: "0.2.0"
agent_job_id: "AJ-TEST"
status: "completed"
requires_human_gate: false
---

# Fixture Decision
""",
        )
        self.write(
            "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
            """job_id: "AJ-TEST"
task_id: "RT-TEST"
decision_id: "DDR-TEST"
role_id: "validator-engineer"
role_version: "0.2.0"
execution_role_ref: "validator-engineer@0.2.0--RT-TEST"
status: "completed"
requires_human_gate: false
allowed_write_paths:
  - "output/result.json"
  - "research_control/tasks/RT-TEST/**"
""",
        )
        self.write(
            "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml",
            'completion_id: "AJC-AJ-TEST"\nvalidation_status: "PASS"\n',
        )
        self.write(
            (
                "research_control/tasks/RT-TEST/roles/"
                "validator-engineer@0.2.0--RT-TEST.yaml"
            ),
            """execution_role_ref: "validator-engineer@0.2.0--RT-TEST"
role_execution_kind: "task_overlay"
task_id: "RT-TEST"
agent_job_id: "AJ-TEST"
base_role_id: "validator-engineer"
base_role_version: "0.2.0"
requires_human_gate: false
allowed_write_paths:
  - "output/result.json"
  - "research_control/tasks/RT-TEST/**"
""",
        )
        self.write(
            "research_control/program_state.yaml",
            """mode: "director_led_research_control"
active_task_id: "RT-TEST"
latest_handoff_id: "handoff-0001"
current_status: "fixture_complete"
next_recommended_action: "Run fixture route."
""",
        )
        self.write(
            "research_control/handoffs/handoff-0001.yaml",
            """handoff_id: "handoff-0001"
handoff_number: 1
task_id: "RT-TEST"
job_id: "AJ-TEST"
completion_path: "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml"
next_action: "Run fixture route."
active_state_bifurcation:
  latest_research_task_id: "RT-TEST"
  latest_research_handoff_id: "handoff-0001"
  latest_research_next_action: "Run fixture route."
  latest_project_system_task_id: "none"
  latest_project_system_status: "none"
  latest_project_system_sidecar_task_id: "none"
  latest_project_system_sidecar_status: "none"
  sidecar_supersedes_research_handoff: false
  next_research_route_source: "latest_research_handoff"
""",
        )
        self.write(
            "research_control/handoffs/handoff-0001.md",
            "# handoff-0001\n\nRun fixture route.\n",
        )
        self.write(
            "research_control/current_frontier.md",
            """# Current Research Frontier

## Active Research State

| Field | Value |
| --- | --- |
| Active task ID | `RT-TEST` |
| Latest handoff ID | `handoff-0001` |
| Current status | `fixture_complete` |
| Next recommended action | Primary route: Run fixture route. |

## Active-State Bifurcation

| Field | Value |
| --- | --- |
| Latest research task ID | `RT-TEST` |
| Latest research handoff ID | `handoff-0001` |
| Latest research next action | Run fixture route. |
| Latest project-system task ID | `none` |
| Latest project-system status | `none` |
| Latest project-system sidecar task ID | `none` |
| Latest project-system sidecar status | `none` |
| Sidecar supersedes research handoff | false |
| Next research route source | `latest_research_handoff` |
""",
        )


class NarrowRoutingSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.fixture = RoutingFixture(self.root)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def assert_gate_failed(
        self, evaluation: routing.RoutingEvaluation, gate_id: str
    ) -> None:
        self.assertTrue(
            any(error.startswith(f"[{gate_id}]") for error in evaluation.report.errors),
            evaluation.report.errors,
        )

    def test_valid_snapshot_is_deterministic_and_excludes_heavy_surfaces(self) -> None:
        first = routing.evaluate(self.root)
        second = routing.evaluate(self.root)

        self.assertEqual(first.report.errors, [])
        self.assertEqual(
            first.payload["routing_snapshot_fingerprint"],
            second.payload["routing_snapshot_fingerprint"],
        )
        self.assertEqual(
            first.payload["source_fingerprint"],
            second.payload["source_fingerprint"],
        )
        self.assertTrue(first.payload["full_acceptance_validator_required"])
        self.assertFalse(
            first.payload["authority_boundary"]["physics_claim_authority"]
        )
        self.assertIn("memory derivatives", first.payload["exclusions"])
        source_paths = {
            row["path"] for row in first.payload["source_manifest"]
        }
        self.assertNotIn("output/research_dependency_graph.json", source_paths)

    def test_stale_handoff_fails_closed(self) -> None:
        self.fixture.write(
            "research_control/handoffs/handoff-0002.yaml",
            """handoff_id: "handoff-0002"
handoff_number: 2
task_id: "RT-TEST"
job_id: "AJ-TEST"
completion_path: "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-TEST.yaml"
next_action: "Run fixture route."
""",
        )
        self.fixture.write(
            "research_control/handoffs/handoff-0002.md", "# handoff-0002\n"
        )

        evaluation = routing.evaluate(self.root)

        self.assert_gate_failed(evaluation, "latest_handoff")
        with self.assertRaisesRegex(ValueError, "latest_handoff"):
            routing.build_routing_snapshot(self.root)

    def test_mismatched_current_job_fails_closed(self) -> None:
        task_path = self.root / "research_control/tasks/RT-TEST/00_TASK.yaml"
        task_path.write_text(
            task_path.read_text(encoding="utf-8").replace(
                'current_job_id: "AJ-TEST"', 'current_job_id: "AJ-WRONG"'
            ),
            encoding="utf-8",
        )

        evaluation = routing.evaluate(self.root)

        self.assert_gate_failed(evaluation, "active_task")

    def test_missing_execution_role_fails_closed(self) -> None:
        path = self.root / "registries/ROLE_EXECUTION_REGISTRY.csv"
        header = path.read_text(encoding="utf-8").splitlines()[0]
        path.write_text(header + "\n", encoding="utf-8")

        evaluation = routing.evaluate(self.root)

        self.assert_gate_failed(evaluation, "execution_role")

    def test_conflicting_pending_jobs_fail_closed(self) -> None:
        path = self.root / "registries/AGENT_JOB_REGISTRY.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
            fieldnames = list(rows[0])
        first = dict(rows[0])
        first["status"] = "active"
        second = dict(first)
        second["job_id"] = "AJ-CONFLICT"
        second["job_path"] = (
            "research_control/tasks/RT-TEST/jobs/AJ-CONFLICT.yaml"
        )
        self.fixture.write_csv(
            "registries/AGENT_JOB_REGISTRY.csv", fieldnames, [first, second]
        )

        evaluation = routing.evaluate(self.root)

        self.assert_gate_failed(evaluation, "pending_job_uniqueness")

    def test_human_gate_is_preserved_as_a_routing_boundary(self) -> None:
        task_registry = self.root / "registries/RESEARCH_TASK_REGISTRY.csv"
        registry_text = task_registry.read_text(encoding="utf-8")
        task_registry.write_text(
            registry_text.replace(",false,fixture", ",true,fixture"),
            encoding="utf-8",
        )
        task_path = self.root / "research_control/tasks/RT-TEST/00_TASK.yaml"
        task_path.write_text(
            task_path.read_text(encoding="utf-8").replace(
                "requires_human_gate: false", "requires_human_gate: true"
            ),
            encoding="utf-8",
        )

        evaluation = routing.evaluate(self.root)
        compatible_report = continue_research.ValidationReport(
            errors=list(evaluation.report.errors),
            warnings=list(evaluation.report.warnings),
        )
        status = continue_research.continuation_status(
            validation_result=continue_research.make_validation_receipt(
                compatible_report
            ),
            routing_snapshot=continue_research.make_routing_snapshot(
                evaluation.payload
            ),
        )

        self.assertEqual(evaluation.report.errors, [])
        self.assertTrue(evaluation.payload["protected_gate"]["requires_human_gate"])
        self.assertEqual(status["boundary"], "human_gate_required")

    def test_allowlist_drift_fails_closed(self) -> None:
        job_path = self.root / "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml"
        job_path.write_text(
            job_path.read_text(encoding="utf-8").replace(
                '  - "output/result.json"\n', ""
            ),
            encoding="utf-8",
        )

        evaluation = routing.evaluate(self.root)

        self.assert_gate_failed(evaluation, "allowlist")

    def test_live_default_does_not_compute_advisory_metrics(self) -> None:
        with mock.patch.object(
            continue_research,
            "build_physics_progress_report",
            side_effect=AssertionError("default routing computed advisory metrics"),
        ):
            status = continue_research.continuation_status()

        self.assertEqual(status["status"], "ready")
        self.assertEqual(
            status["route_orbit_diagnostics"]["status"],
            "excluded_from_narrow_snapshot",
        )

    def test_live_narrow_and_full_validation_agree_on_current_state(self) -> None:
        narrow = routing.validate_all()
        full = validate_research_control.validate_all()

        self.assertEqual(narrow.errors, [])
        self.assertEqual(full.errors, [])

    def test_live_narrow_snapshot_has_subsecond_python_runtime(self) -> None:
        started = time.perf_counter()
        evaluation = routing.evaluate()
        elapsed = time.perf_counter() - started

        self.assertEqual(evaluation.report.errors, [])
        self.assertLess(elapsed, 1.0)


if __name__ == "__main__":
    unittest.main()
