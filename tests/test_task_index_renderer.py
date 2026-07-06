from __future__ import annotations

import csv
import importlib.util
import json
import shutil
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


class TaskIndexRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.renderer = load_module("render_task_index", "render_task_index.py")
        cls.validator = load_module("validate_task_index", "validate_task_index.py")

    def make_fixture_repo(self, root: Path, *, physics_delta: bool = False) -> None:
        task_id = "RT-20260706-999"
        job_id = "AJ-RT-20260706-999-001"
        decision_id = "DDR-20260706-999"
        task_root = root / "research_control" / "tasks" / task_id
        job_root = task_root / "jobs"
        completion_root = job_root / "completions"
        registries = root / "registries"
        design = root / "research_control" / "design"
        for path in (completion_root, registries, design, root / "wiki" / "indexes"):
            path.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            REPO_ROOT / "research_control" / "design" / "task_index_schema_v1.md",
            design / "task_index_schema_v1.md",
        )
        (task_root / "00_TASK.yaml").write_text(
            "\n".join(
                [
                    f'task_id: "{task_id}"',
                    'task_type: "research_control_task_index_validator"',
                    'status: "completed"',
                    'created_at: "2026-07-06T00:00:00Z"',
                    'closed_at: "2026-07-06T00:01:00Z"',
                    f'current_decision_id: "{decision_id}"',
                    f'current_job_id: "{job_id}"',
                    'target_derivation_milestone: "matter_coupling"',
                    'milestone_burden: "Validate generated task index against tracked tasks and completions."',
                    'next_recommended_action: "Run one bounded fixture follow-up."',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (job_root / f"{job_id}.yaml").write_text(
            "\n".join(
                [
                    f'job_id: "{job_id}"',
                    f'task_id: "{task_id}"',
                    f'decision_id: "{decision_id}"',
                    'role_id: "validator-engineer"',
                    'role_version: "0.2.0"',
                    'status: "completed"',
                    'target_derivation_milestone: "matter_coupling"',
                    'milestone_burden: "Validate generated task index against tracked tasks and completions."',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (completion_root / f"AJC-{job_id}.yaml").write_text(
            "\n".join(
                [
                    f'completion_id: "AJC-{job_id}"',
                    f'job_id: "{job_id}"',
                    f'task_id: "{task_id}"',
                    'source_role_id: "validator-engineer"',
                    'completed_at: "2026-07-06T00:01:00Z"',
                    'status: "completed"',
                    'validation_status: "PASS"',
                    'distance_to_gr_delta:',
                    f"  changed: {'true' if physics_delta else 'false'}",
                    '  burden_id: "matter_coupling"',
                    '  milestone: "matter_coupling"',
                    'next_recommendation: "Run one bounded fixture follow-up."',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (registries / "RESEARCH_TASK_REGISTRY.csv").write_text(
            "\n".join(
                [
                    "task_id,task_path,task_type,status,current_decision_id,current_job_id,parent_task_id,created_at,updated_at,closed_at,closure_status,requires_human_gate,notes",
                    f'{task_id},research_control/tasks/{task_id},research_control_task_index_validator,completed,{decision_id},{job_id},,2026-07-06T00:00:00Z,2026-07-06T00:01:00Z,2026-07-06T00:01:00Z,fixture_completed,false,Fixture task',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (registries / "AGENT_JOB_REGISTRY.csv").write_text(
            "\n".join(
                [
                    "job_id,task_id,decision_id,role_id,role_version,job_path,completion_path,status,allowed_write_paths,output_paths,validation_status,created_at,started_at,completed_at,requires_human_gate,notes",
                    f'{job_id},{task_id},{decision_id},validator-engineer,0.2.0,research_control/tasks/{task_id}/jobs/{job_id}.yaml,research_control/tasks/{task_id}/jobs/completions/AJC-{job_id}.yaml,completed,scripts/research_control/validate_task_index.py,tests/test_task_index_renderer.py,PASS,2026-07-06T00:00:00Z,2026-07-06T00:00:00Z,2026-07-06T00:01:00Z,false,Fixture job',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (registries / "DIRECTOR_DECISION_REGISTRY.csv").write_text(
            "\n".join(
                [
                    "decision_id,task_id,decision_path,director_version,decision_type,selected_role_id,selected_role_version,agent_job_id,status,supersedes_decision_id,requires_human_gate,created_at,activated_at,completed_at,validation_status,notes",
                    f'{decision_id},{task_id},research_control/tasks/{task_id}/{decision_id}.md,director-of-research@0.3.0,task_overlay,validator-engineer,0.2.0,{job_id},completed,,false,2026-07-06T00:00:00Z,2026-07-06T00:00:00Z,2026-07-06T00:01:00Z,PASS,Fixture decision',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (task_root / f"{decision_id}.md").write_text(
            "---\nauthority: control\n---\n\n# Fixture decision\n",
            encoding="utf-8",
        )

    def render_outputs(self, root: Path) -> None:
        index = self.renderer.build_index(root)
        csv_text, markdown_text, wiki_text = self.renderer.rendered_texts(index)
        self.renderer.write_text(root, self.renderer.DEFAULT_CSV_PATH, csv_text)
        self.renderer.write_text(root, self.renderer.DEFAULT_MARKDOWN_PATH, markdown_text)
        self.renderer.write_text(root, self.renderer.DEFAULT_WIKI_MARKDOWN_PATH, wiki_text)

    def test_validator_passes_for_fresh_generated_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            self.render_outputs(root)

            report = self.validator.validate_task_index(root)

        self.assertEqual(report.errors, [])
        self.assertEqual(report.row_count, 1)
        self.assertTrue(report.checks["header"]["matches"])

    def test_validator_rejects_header_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            self.render_outputs(root)
            csv_path = root / self.renderer.DEFAULT_CSV_PATH
            rows = list(csv.reader(csv_path.read_text(encoding="utf-8").splitlines()))
            rows[0][0] = "bad_task_id"
            csv_path.write_text("\n".join(",".join(row) for row in rows) + "\n", encoding="utf-8")

            report = self.validator.validate_task_index(root)

        self.assertIn("required_header_mismatch", {error.code for error in report.errors})

    def test_validator_rejects_stale_markdown_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            self.render_outputs(root)
            (root / self.renderer.DEFAULT_MARKDOWN_PATH).write_text("stale\n", encoding="utf-8")

            report = self.validator.validate_task_index(root)

        self.assertIn("generated_output_stale", {error.code for error in report.errors})

    def test_validator_rejects_support_only_physics_delta(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root, physics_delta=True)
            self.render_outputs(root)

            report = self.validator.validate_task_index(root)

        self.assertIn("support_only_physics_delta", {error.code for error in report.errors})

    def test_renderer_reports_missing_metadata_without_inventing_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            task_yaml = root / "research_control" / "tasks" / "RT-20260706-999" / "00_TASK.yaml"
            task_yaml.write_text(
                task_yaml.read_text(encoding="utf-8").replace(
                    'milestone_burden: "Validate generated task index against tracked tasks and completions."\n',
                    "",
                ),
                encoding="utf-8",
            )
            job_yaml = (
                root
                / "research_control"
                / "tasks"
                / "RT-20260706-999"
                / "jobs"
                / "AJ-RT-20260706-999-001.yaml"
            )
            job_yaml.write_text(
                job_yaml.read_text(encoding="utf-8").replace(
                    'milestone_burden: "Validate generated task index against tracked tasks and completions."\n',
                    "",
                ),
                encoding="utf-8",
            )
            self.render_outputs(root)

            report = self.validator.validate_task_index(root)

        self.assertEqual(report.errors, [])
        self.assertIn("missing_field", {warning.code for warning in report.warnings})


if __name__ == "__main__":
    unittest.main()
