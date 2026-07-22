from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class PhysicsProgressMetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        load_module("report_scientific_payload_density", "report_scientific_payload_density.py")
        cls.reporter = load_module(
            "report_physics_progress_metrics",
            "report_physics_progress_metrics.py",
        )

    def write_csv(self, path: Path, rows: list[dict[str, str]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    def write_task(
        self,
        repo: Path,
        task_id: str,
        task_type: str,
        role_id: str,
        role_version: str,
        completion_body: str,
        index: int,
    ) -> None:
        timestamp = f"2026-07-08T00:0{index}:00Z"
        task_dir = repo / "research_control" / "tasks" / task_id
        completion_dir = task_dir / "jobs" / "completions"
        completion_dir.mkdir(parents=True, exist_ok=True)
        (task_dir / "00_TASK.yaml").write_text(
            f'task_id: "{task_id}"\n'
            f'task_type: "{task_type}"\n'
            'implementation_plan:\n'
            '  plan_phase_id: "P8"\n',
            encoding="utf-8",
        )
        (task_dir / "jobs" / f"AJ-{task_id}.yaml").write_text(
            f'job_id: "AJ-{task_id}"\n'
            f'task_id: "{task_id}"\n'
            f'role_id: "{role_id}"\n'
            f'role_version: "{role_version}"\n'
            'target_derivation_milestone: "none"\n'
            "support_only: true\n",
            encoding="utf-8",
        )
        (completion_dir / f"AJC-AJ-{task_id}.yaml").write_text(
            f'completion_id: "AJC-AJ-{task_id}"\n'
            f'job_id: "AJ-{task_id}"\n'
            f'task_id: "{task_id}"\n'
            'validation_status: "PASS"\n'
            f"completed_at: \"{timestamp}\"\n"
            f"{completion_body}",
            encoding="utf-8",
        )

    def make_repo(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name)

        self.write_csv(
            repo / "registries" / "AGENT_ROLE_REGISTRY.csv",
            [
                {
                    "role_id": "candidate-constructor",
                    "version": "0.2.0",
                    "role_name": "Candidate Constructor",
                    "role_kind": "scientific_candidate_construction",
                    "role_contract_path": "",
                    "authority_level": "science_draft",
                    "status": "active",
                    "may_execute_autonomously": "true",
                    "may_create_outputs": "true",
                    "may_modify_sources": "true",
                    "may_promote_claims": "false",
                    "requires_human_gate": "false",
                    "default_output_format": "yaml",
                    "default_validators": "",
                    "created_at": "2026-07-08T00:00:00Z",
                    "updated_at": "2026-07-08T00:00:00Z",
                    "notes": "",
                },
                {
                    "role_id": "validator-engineer",
                    "version": "0.2.0",
                    "role_name": "Validator Engineer",
                    "role_kind": "project_system_validation",
                    "role_contract_path": "",
                    "authority_level": "project_control",
                    "status": "active",
                    "may_execute_autonomously": "true",
                    "may_create_outputs": "true",
                    "may_modify_sources": "true",
                    "may_promote_claims": "false",
                    "requires_human_gate": "false",
                    "default_output_format": "py",
                    "default_validators": "",
                    "created_at": "2026-07-08T00:00:00Z",
                    "updated_at": "2026-07-08T00:00:00Z",
                    "notes": "",
                },
            ],
        )
        self.write_csv(
            repo / "registries" / "CLAIM_BOUNDARY_REGISTRY.csv",
            [
                {
                    "boundary_id": "CB-FIXTURE",
                    "boundary_type": "task",
                    "scope_path": "research_control/tasks",
                    "allowed_claims": "fixture metrics only",
                    "forbidden_claims": "physics proof",
                    "protected_authority": "proof authority",
                    "evidence_path": "",
                    "status": "active",
                    "created_at": "2026-07-08T00:00:00Z",
                    "updated_at": "2026-07-08T00:00:00Z",
                    "notes": "",
                }
            ],
        )
        self.write_csv(
            repo / "registries" / "RESEARCH_TASK_REGISTRY.csv",
            [
                {
                    "task_id": "RT-PHYS",
                    "task_path": "research_control/tasks/RT-PHYS",
                    "task_type": "candidate_construction_fixture",
                    "status": "completed",
                    "current_decision_id": "DDR-PHYS",
                    "current_job_id": "AJ-RT-PHYS",
                    "parent_task_id": "",
                    "created_at": "2026-07-08T00:00:00Z",
                    "updated_at": "2026-07-08T00:00:00Z",
                    "closed_at": "2026-07-08T00:00:00Z",
                    "closure_status": "done",
                    "requires_human_gate": "false",
                    "notes": "",
                },
                {
                    "task_id": "RT-PS1",
                    "task_path": "research_control/tasks/RT-PS1",
                    "task_type": "physics_payload_ratio_policy",
                    "status": "completed",
                    "current_decision_id": "DDR-PS1",
                    "current_job_id": "AJ-RT-PS1",
                    "parent_task_id": "",
                    "created_at": "2026-07-08T00:01:00Z",
                    "updated_at": "2026-07-08T00:01:00Z",
                    "closed_at": "2026-07-08T00:01:00Z",
                    "closure_status": "done",
                    "requires_human_gate": "false",
                    "notes": "",
                },
                {
                    "task_id": "RT-PS2",
                    "task_path": "research_control/tasks/RT-PS2",
                    "task_type": "route_history_payload_ratio_metrics",
                    "status": "completed",
                    "current_decision_id": "DDR-PS2",
                    "current_job_id": "AJ-RT-PS2",
                    "parent_task_id": "",
                    "created_at": "2026-07-08T00:02:00Z",
                    "updated_at": "2026-07-08T00:02:00Z",
                    "closed_at": "2026-07-08T00:02:00Z",
                    "closure_status": "done",
                    "requires_human_gate": "false",
                    "notes": "",
                },
            ],
        )
        self.write_csv(
            repo / "registries" / "AGENT_JOB_REGISTRY.csv",
            [
                {
                    "job_id": "AJ-RT-PHYS",
                    "task_id": "RT-PHYS",
                    "decision_id": "DDR-PHYS",
                    "role_id": "candidate-constructor",
                    "role_version": "0.2.0",
                    "job_path": "research_control/tasks/RT-PHYS/jobs/AJ-RT-PHYS.yaml",
                    "completion_path": "research_control/tasks/RT-PHYS/jobs/completions/AJC-AJ-RT-PHYS.yaml",
                    "status": "completed",
                    "allowed_write_paths": "",
                    "output_paths": "",
                    "validation_status": "PASS",
                    "created_at": "2026-07-08T00:00:00Z",
                    "started_at": "2026-07-08T00:00:00Z",
                    "completed_at": "2026-07-08T00:00:00Z",
                    "requires_human_gate": "false",
                    "notes": "",
                },
                {
                    "job_id": "AJ-RT-PS1",
                    "task_id": "RT-PS1",
                    "decision_id": "DDR-PS1",
                    "role_id": "validator-engineer",
                    "role_version": "0.2.0",
                    "job_path": "research_control/tasks/RT-PS1/jobs/AJ-RT-PS1.yaml",
                    "completion_path": "research_control/tasks/RT-PS1/jobs/completions/AJC-AJ-RT-PS1.yaml",
                    "status": "completed",
                    "allowed_write_paths": "",
                    "output_paths": "",
                    "validation_status": "PASS",
                    "created_at": "2026-07-08T00:01:00Z",
                    "started_at": "2026-07-08T00:01:00Z",
                    "completed_at": "2026-07-08T00:01:00Z",
                    "requires_human_gate": "false",
                    "notes": "",
                },
                {
                    "job_id": "AJ-RT-PS2",
                    "task_id": "RT-PS2",
                    "decision_id": "DDR-PS2",
                    "role_id": "validator-engineer",
                    "role_version": "0.2.0",
                    "job_path": "research_control/tasks/RT-PS2/jobs/AJ-RT-PS2.yaml",
                    "completion_path": "research_control/tasks/RT-PS2/jobs/completions/AJC-AJ-RT-PS2.yaml",
                    "status": "completed",
                    "allowed_write_paths": "",
                    "output_paths": "",
                    "validation_status": "PASS",
                    "created_at": "2026-07-08T00:02:00Z",
                    "started_at": "2026-07-08T00:02:00Z",
                    "completed_at": "2026-07-08T00:02:00Z",
                    "requires_human_gate": "false",
                    "notes": "",
                },
            ],
        )

        self.write_task(
            repo,
            "RT-PHYS",
            "candidate_construction_fixture",
            "candidate-constructor",
            "0.2.0",
            "physics_progress_status:\n"
            '  status: "candidate_constructed_pending_audit"\n'
            "candidate_constructor_result:\n"
            '  result_type: "constructed_candidate"\n'
            "mathematical_payload_manifest:\n"
            '  - payload_type: "theorem_with_hypotheses_and_proof"\n'
            '    object_name: "FixtureCandidateLemma_v1"\n',
            0,
        )
        self.write_task(
            repo,
            "RT-PS1",
            "physics_payload_ratio_policy",
            "validator-engineer",
            "0.2.0",
            "",
            1,
        )
        self.write_task(
            repo,
            "RT-PS2",
            "route_history_payload_ratio_metrics",
            "validator-engineer",
            "0.2.0",
            "",
            2,
        )
        return repo

    def test_payload_ratio_diagnostics_count_tail_run_and_boundary(self) -> None:
        report = self.reporter.build_report(self.make_repo())
        diagnostics = report["metrics"]["physics_payload_ratio_diagnostics"]
        metrics = diagnostics["metrics"]

        self.assertTrue(diagnostics["authority_boundary"]["ai_system_diagnostics_only"])
        self.assertTrue(diagnostics["authority_boundary"]["does_not_rank_physics_truth"])
        self.assertFalse(diagnostics["authority_boundary"]["physics_claim_promotion_authorized"])
        self.assertEqual(metrics["project_system_task_run_length"], 2)
        self.assertEqual(metrics["physics_bearing_task_run_length"], 0)
        self.assertEqual(metrics["support_only_task_count_since_last_physics_payload"], 2)
        self.assertEqual(metrics["new_mathematical_payload_count"], 1)
        self.assertEqual(metrics["theorem_countermodel_candidate_count"], 1)
        self.assertEqual(metrics["candidate_construction_count"], 1)
        self.assertEqual(metrics["physics_bearing_to_project_system_task_ratio"], 0.5)

    def test_markdown_renders_payload_ratio_non_truth_ranking_guard(self) -> None:
        markdown = self.reporter.render_markdown(self.reporter.build_report(self.make_repo()))

        self.assertIn("## Physics-Payload Ratio Diagnostics", markdown)
        self.assertIn("AI-system diagnostics only", markdown)
        self.assertIn("do not rank physics truth", markdown)

    def test_project_system_detection_prefers_explicit_normalized_scope(self) -> None:
        task = {
            "task_id": "RT-NORMALIZED",
            "task_type": "validator_schema_control",
            "task_taxonomy": {
                "schema_id": "v21_task_taxonomy_v1",
                "work_kind": "formalization_or_theorem",
                "milestone": "source_equivalence_eqsrc",
                "candidate_family": "eqsrc_fixture",
                "result_kind": "theorem_or_precise_obstruction",
                "authority": "science_draft",
                "scope": "scientific",
            },
        }

        result = self.reporter.is_project_system_task(
            {"task_type": "validator_schema_control"},
            task,
            {},
            {"authority_level": "project_control", "role_kind": "project_system_validation"},
        )

        self.assertFalse(result)

    def test_project_system_formalization_does_not_count_as_science_signal(self) -> None:
        task = {
            "task_id": "RT-PROJECT-FORMALIZATION",
            "task_type": "schema_formalization",
            "task_taxonomy": {
                "schema_id": "v21_task_taxonomy_v1",
                "work_kind": "formalization_or_theorem",
                "milestone": "source_equivalence_eqsrc",
                "candidate_family": "not_applicable",
                "result_kind": "implemented_and_validated_or_precisely_blocked",
                "authority": "project_control",
                "scope": "project_system",
            },
        }

        result = self.reporter.task_has_theorem_countermodel_candidate_signal(
            {"progress_status": "", "candidate_result_type": "", "text": ""},
            {"task_type": "schema_formalization"},
            task,
            {},
        )

        self.assertFalse(result)

    def test_live_candidate_lineage_metrics_are_keyed_by_immutable_ids(self) -> None:
        lineage = self.reporter.collect_candidate_lineage_metrics(REPO_ROOT)

        self.assertEqual(lineage["status"], "measured")
        self.assertEqual(len(lineage["candidate_ids"]), 7)
        self.assertEqual(
            lineage["metrics"]["candidate_to_audit_conversion"]["value"],
            1.0,
        )
        self.assertEqual(
            lineage["metrics"]["audit_to_stress_survival"]["value"],
            0.5714,
        )
        self.assertEqual(
            lineage["metrics"]["stress_survival_rate"]["value"],
            0.0,
        )
        self.assertEqual(len(lineage["explicit_absences"]), 1)
        self.assertFalse(lineage["authority_boundary"]["candidate_adoption_authorized"])

    def test_ai_methodology_uses_exact_lineage_when_available(self) -> None:
        lineage = self.reporter.collect_candidate_lineage_metrics(REPO_ROOT)
        report = self.reporter.collect_ai_research_agent_methodology_metrics(
            [],
            [],
            {},
            {},
            {},
            [],
            lineage,
        )
        lifecycle = report["metrics"]

        self.assertEqual(lifecycle["candidate_to_audit_conversion"]["status"], "measured")
        self.assertEqual(lifecycle["audit_to_stress_survival"]["status"], "measured")
        self.assertEqual(lifecycle["stress_survival_rate"]["status"], "measured")
        self.assertIn(
            "EQSRC-GRADED-ORBIT-ROOT-V1",
            lifecycle["audit_to_stress_survival"]["breakdown"]["denominator_candidate_ids"],
        )
        self.assertNotIn(
            "EQSRC-GRADED-ORBIT-ROOT-V1",
            lifecycle["audit_to_stress_survival"]["breakdown"]["numerator_candidate_ids"],
        )


if __name__ == "__main__":
    unittest.main()
