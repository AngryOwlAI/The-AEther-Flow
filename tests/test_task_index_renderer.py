from __future__ import annotations

import csv
from contextlib import redirect_stdout
import importlib.util
from io import StringIO
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.validation.reporting import (
    DEFAULT_NONPASS_BUDGET_BYTES,
    DEFAULT_PASS_BUDGET_BYTES,
    console_bytes,
    write_full_receipt,
)


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
            REPO_ROOT / self.renderer.SCHEMA_PATH,
            root / self.renderer.SCHEMA_PATH,
        )
        shutil.copyfile(
            REPO_ROOT / "research_control" / "design" / "v21_task_taxonomy_policy.md",
            design / "v21_task_taxonomy_policy.md",
        )
        (design / "v21_recommendation_backlog.yaml").write_text("items: []\n", encoding="utf-8")
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
        (registries / "AGENT_ROLE_REGISTRY.csv").write_text(
            "\n".join(
                [
                    "role_id,version,role_name,role_kind,role_contract_path,authority_level,status,may_execute_autonomously,may_create_outputs,may_modify_sources,may_promote_claims,requires_human_gate,default_output_format,default_validators,created_at,updated_at,notes",
                    "validator-engineer,0.2.0,Validator Engineer,project_system_validation,,project_control,active,true,true,true,false,false,yaml,,2026-07-06T00:00:00Z,2026-07-06T00:00:00Z,Fixture role",
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

    def test_validator_rejects_stale_csv_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            self.render_outputs(root)
            csv_path = root / self.renderer.DEFAULT_CSV_PATH
            csv_path.write_text(
                csv_path.read_text(encoding="utf-8").replace("RT-20260706-999", "RT-20260706-998"),
                encoding="utf-8",
            )

            report = self.validator.validate_task_index(root)

        hard_codes = {error.code for error in report.errors}
        self.assertIn("generated_output_stale", hard_codes)
        self.assertIn("csv_rows_mismatch", hard_codes)

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

    def test_validator_rejects_missing_normalized_fields_for_new_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            task_yaml = root / "research_control" / "tasks" / "RT-20260706-999" / "00_TASK.yaml"
            task_yaml.write_text(
                task_yaml.read_text(encoding="utf-8").replace(
                    'created_at: "2026-07-06T00:00:00Z"',
                    f'created_at: "{self.renderer.task_taxonomy.EFFECTIVE_AT}"',
                ),
                encoding="utf-8",
            )
            self.render_outputs(root)

            report = self.validator.validate_task_index(root)

        self.assertIn("taxonomy_required_missing", {error.code for error in report.errors})

    def test_renderer_prefers_explicit_taxonomy_and_preserves_raw_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            task_yaml = root / "research_control" / "tasks" / "RT-20260706-999" / "00_TASK.yaml"
            task_yaml.write_text(
                task_yaml.read_text(encoding="utf-8")
                .replace(
                    'task_type: "research_control_task_index_validator"',
                    'task_type: "research_control_task_index_validator"\n'
                    'title: "Readable fixture title"\n'
                    'task_taxonomy:\n'
                    '  schema_id: "v21_task_taxonomy_v1"\n'
                    '  work_kind: "integration_or_selection"\n'
                    '  milestone: "matter_coupling"\n'
                    '  candidate_family: "not_applicable"\n'
                    '  result_kind: "implemented_and_validated_or_precisely_blocked"\n'
                    '  authority: "project_control"\n'
                    '  scope: "project_system"',
                )
                .replace(
                    'created_at: "2026-07-06T00:00:00Z"',
                    f'created_at: "{self.renderer.task_taxonomy.EFFECTIVE_AT}"',
                ),
                encoding="utf-8",
            )

            row = self.renderer.build_index(root)["rows"][0]

        self.assertEqual(row["title"], "Readable fixture title")
        self.assertEqual(row["task_type"], "research_control_task_index_validator")
        self.assertEqual(row["work_kind"], "integration_or_selection")
        self.assertEqual(row["scope"], "project_system")
        self.assertEqual(row["taxonomy_source"], "explicit")

    def test_common_adapter_preserves_297_warnings_and_pass_semantics(self) -> None:
        report = self.validator.TaskIndexValidationReport(repo_root=REPO_ROOT)
        for index in range(297):
            report.warn(
                "missing_field",
                "Historical metadata field is absent.",
                task_id=f"RT-TEST-{index:03d}",
                field="milestone_burden",
            )

        run = self.validator.adapt_to_common_run(report)
        with tempfile.TemporaryDirectory() as tmp:
            receipt_path = write_full_receipt(run, Path(tmp))
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            output = self.validator.render_compact_summary(report, run, receipt_path)

        self.assertEqual(run.status, "PASS")
        self.assertEqual(run.exit_code, 0)
        self.assertEqual(run.warning_count, 297)
        self.assertEqual(receipt["counts"]["finding_count"], 297)
        self.assertEqual(len(receipt["gate_results"][0]["findings"]), 297)
        self.assertIn("WARN_GROUP missing_field count=297", output)
        self.assertIn("RT-TEST-000,RT-TEST-001,RT-TEST-002", output)
        self.assertLessEqual(console_bytes(output), DEFAULT_PASS_BUDGET_BYTES)

    def test_compact_summary_orders_hard_findings_before_warning_groups(self) -> None:
        report = self.validator.TaskIndexValidationReport(repo_root=REPO_ROOT)
        report.warn("missing_field", "Historical metadata field is absent.", task_id="RT-OLD-001")
        report.error("required_header_mismatch", "Header mismatch.")
        report.error("csv_rows_mismatch", "Row mismatch.")
        report.error("generated_output_stale", "CSV output is stale.", path="task-index.csv")
        run = self.validator.adapt_to_common_run(report)

        output = self.validator.render_compact_summary(report, run, Path("receipt.json"))

        stale_at = output.index("ERROR generated_output_stale")
        rows_at = output.index("ERROR csv_rows_mismatch")
        header_at = output.index("ERROR required_header_mismatch")
        warning_at = output.index("WARN_GROUP missing_field")
        self.assertLess(stale_at, rows_at)
        self.assertLess(rows_at, header_at)
        self.assertLess(header_at, warning_at)
        self.assertLessEqual(console_bytes(output), DEFAULT_NONPASS_BUDGET_BYTES)

    def test_common_adapter_preserves_legacy_hard_codes_and_exit_status(self) -> None:
        report = self.validator.TaskIndexValidationReport(repo_root=REPO_ROOT)
        report.error("generated_output_stale", "CSV output is stale.", path="task-index.csv")
        report.error("csv_rows_mismatch", "Row mismatch.")

        run = self.validator.adapt_to_common_run(report)

        common_codes = {finding.code for finding in run.gate_results[0].findings if finding.level == "ERROR"}
        self.assertEqual(common_codes, {finding.code for finding in report.errors})
        ordered_codes = [finding.code for finding in run.gate_results[0].sorted_findings]
        self.assertEqual(ordered_codes, ["generated_output_stale", "csv_rows_mismatch"])
        self.assertEqual(run.status, "FAIL")
        self.assertEqual(run.exit_code, 1)

    def test_json_and_full_json_preserve_legacy_compatibility(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            self.render_outputs(root)
            outputs: list[dict[str, object]] = []
            with mock.patch.object(self.validator, "utc_now", return_value="2026-07-16T00:00:00Z"):
                for flag in ("--json", "--full-json"):
                    stream = StringIO()
                    with redirect_stdout(stream):
                        exit_code = self.validator.main(["--repo-root", root.as_posix(), flag])
                    self.assertEqual(exit_code, 0)
                    outputs.append(json.loads(stream.getvalue()))

        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0]["schema_id"], self.validator.REPORT_SCHEMA_ID)
        self.assertIn("errors", outputs[0])
        self.assertIn("warnings", outputs[0])

    def test_receipt_write_failure_is_visible_and_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            self.render_outputs(root)
            stream = StringIO()
            with mock.patch.object(
                self.validator,
                "write_full_receipt",
                side_effect=OSError("receipt denied"),
            ), redirect_stdout(stream):
                exit_code = self.validator.main(["--repo-root", root.as_posix(), "--quiet"])

        self.assertEqual(exit_code, 2)
        self.assertIn("BLOCKED_CONFIGURATION receipt_write_failed", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
