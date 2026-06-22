from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
PROJECT_SCRIPT_DIR = REPO_ROOT / "scripts" / "project_control"
TEMPLATE_DIR = REPO_ROOT / "research_control" / "templates"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "project_improvement_bridge"


def load_module(name: str, script_dir: Path, filename: str):
    for path in (RESEARCH_SCRIPT_DIR, PROJECT_SCRIPT_DIR):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    spec = importlib.util.spec_from_file_location(name, script_dir / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProjectImprovementBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.strict_yaml = load_module("strict_yaml", RESEARCH_SCRIPT_DIR, "strict_yaml.py")
        cls.resolver = load_module(
            "resolve_latest_handoff",
            RESEARCH_SCRIPT_DIR,
            "resolve_latest_handoff.py",
        )
        cls.generator = load_module(
            "generate_project_improvement_handoff",
            PROJECT_SCRIPT_DIR,
            "generate_project_improvement_handoff.py",
        )
        cls.bridge_validator = load_module(
            "project_improvement_handoff_validation",
            PROJECT_SCRIPT_DIR,
            "project_improvement_handoff_validation.py",
        )
        cls.checkpoint = load_module(
            "checkpoint_research_transaction_bridge_test",
            RESEARCH_SCRIPT_DIR,
            "checkpoint_research_transaction.py",
        )

    def test_project_improvement_handoff_yaml_template_parses(self) -> None:
        template_path = TEMPLATE_DIR / "IMPROVE_PROJECT_HANDOFF_TEMPLATE.yaml"
        data = self.strict_yaml.loads(template_path.read_text(encoding="utf-8"))

        self.assertEqual(data["status"], "open")
        self.assertEqual(
            data["project_boundary"]["recommended_skill"],
            "improve-project-system",
        )
        self.assertTrue(data["project_boundary"]["project_system_only"])
        self.assertFalse(data["project_boundary"]["physics_claim_promotion_authorized"])
        self.assertFalse(data["project_boundary"]["canonical_science_source_edits_authorized"])
        self.assertTrue(
            data["normal_research_continuation"]["sidecar_does_not_replace_regular_handoff"]
        )
        self.assertEqual(
            data["signal_summary"]["routing_basis"],
            "highest_severity_then_created_at_then_signal_id",
        )

    def test_project_improvement_handoff_fixture_preserves_boundary(self) -> None:
        fixture_path = FIXTURE_DIR / "improve-project-handoff_20260622_001.yaml"
        data = self.strict_yaml.loads(fixture_path.read_text(encoding="utf-8"))

        self.assertEqual(data["source"]["source_kind"], "backfilled_from_immutable_source")
        self.assertEqual(str(data["signal_summary"]["signal_count"]), "4")
        self.assertEqual(data["resolution"]["resolved_by_job_id"], "AJ-RT-20260621-010-001")
        self.assertTrue(
            data["normal_research_continuation"]["sidecar_does_not_replace_regular_handoff"]
        )
        self.assertFalse(data["project_boundary"]["generated_derivative_hand_edits_authorized"])

    def test_latest_handoff_resolver_ignores_project_improvement_sidecars(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            handoff_dir = root / "research_control" / "handoffs"
            sidecar_dir = root / "research_control" / "project_improvement_handoffs"
            handoff_dir.mkdir(parents=True)
            sidecar_dir.mkdir(parents=True)

            self.write_handoff_pair(handoff_dir, 1)
            self.write_handoff_pair(handoff_dir, 2)
            (sidecar_dir / "improve-project-handoff_20260622_999.yaml").write_text(
                'improvement_handoff_id: "improve-project-handoff_20260622_999"\n',
                encoding="utf-8",
            )
            (handoff_dir / "handoff-9999_project.yaml").write_text(
                'handoff_id: "handoff-9999_project"\n',
                encoding="utf-8",
            )

            with mock.patch.object(self.resolver, "REPO_ROOT", root), mock.patch.object(
                self.resolver,
                "HANDOFF_DIR",
                handoff_dir,
            ):
                latest = self.resolver.resolve_latest()

        self.assertEqual(latest["handoff_number"], 2)
        self.assertEqual(latest["handoff_id"], "handoff-0002")
        self.assertEqual(
            latest["yaml_path"],
            "research_control/handoffs/handoff-0002.yaml",
        )

    def test_generator_dry_run_reports_sidecar_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root)

            result = self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=False,
                repo_root=root,
            )

            self.assertTrue(result["ok"])
            self.assertTrue(result["bridge_required"])
            self.assertEqual(result["write_status"], "dry_run")
            self.assertEqual(
                result["improvement_handoff_id"],
                "improve-project-handoff_20260622_090",
            )
            self.assertFalse(
                (
                    root
                    / "research_control/project_improvement_handoffs/"
                    "improve-project-handoff_20260622_090.yaml"
                ).exists()
            )
            data = self.strict_yaml.loads(result["yaml_text"])
            self.assertEqual(data["signal_summary"]["selected_signal_id"], "PIS-RT-20260622-090-001")
            self.assertTrue(
                data["normal_research_continuation"]["sidecar_does_not_replace_regular_handoff"]
            )

    def test_generator_write_creates_yaml_and_markdown_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root)

            result = self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=True,
                repo_root=root,
            )

            self.assertTrue(result["ok"])
            yaml_path = root / result["output_paths"]["yaml"]
            markdown_path = root / result["output_paths"]["markdown"]
            self.assertTrue(yaml_path.exists())
            self.assertTrue(markdown_path.exists())
            data = self.strict_yaml.load(yaml_path)
            self.assertEqual(data["improvement_handoff_id"], "improve-project-handoff_20260622_090")
            self.assertFalse(data["project_boundary"]["physics_claim_promotion_authorized"])
            self.assertIn(
                "Project-Improvement Handoff",
                markdown_path.read_text(encoding="utf-8"),
            )

    def test_generator_updates_source_bridge_reference_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root)

            result = self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=True,
                update_source_bridge=True,
                repo_root=root,
            )

            self.assertTrue(result["ok"])
            self.assertEqual(len(result["source_bridge_updates"]), 1)
            self.assertEqual(
                result["source_bridge_updates"][0]["source_path"],
                (
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
            )
            completion_path = (
                root
                / "research_control/tasks/RT-20260622-090/jobs/completions/"
                "AJC-AJ-RT-20260622-090-001.yaml"
            )
            completion = self.strict_yaml.load(completion_path)
            self.assertTrue(completion["project_improvement_bridge"]["required"])
            self.assertEqual(
                completion["project_improvement_bridge"]["improvement_handoff_path"],
                "research_control/project_improvement_handoffs/improve-project-handoff_20260622_090.yaml",
            )
            self.assertEqual(completion["project_improvement_bridge"]["bridge_status"], "generated")

            report = self.bridge_validator.validate_project_improvement_handoffs(root)
            self.assertEqual(report["errors"], [])

    def test_generator_blank_signal_placeholder_noops(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root, blank_signal=True)

            result = self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=True,
                repo_root=root,
            )

            self.assertTrue(result["ok"])
            self.assertFalse(result["bridge_required"])
            self.assertEqual(result["write_status"], "not_required")

    def test_generator_rejects_missing_signal_registry_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root, omit_signal_row=True)

            result = self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=True,
                repo_root=root,
            )

            self.assertFalse(result["ok"])
            self.assertIn(
                "PIS-RT-20260622-090-001: missing registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv row",
                result["errors"],
            )

    def test_bridge_validator_accepts_generated_sidecar_parity(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root, include_bridge_reference=True)

            self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=True,
                repo_root=root,
            )

            report = self.bridge_validator.validate_project_improvement_handoffs(root)
            self.assertEqual(report["errors"], [])
            self.assertEqual(report["improvement_handoff_count"], 1)
            self.assertEqual(report["open_improvement_handoff_count"], 1)

    def test_bridge_validator_rejects_missing_sidecar_after_activation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root, include_bridge_reference=True)

            report = self.bridge_validator.validate_project_improvement_handoffs(root)

            self.assertTrue(
                any("project_improvement_bridge sidecar does not exist" in error for error in report["errors"])
            )

    def test_bridge_validator_rejects_missing_bridge_reference_after_activation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root)

            report = self.bridge_validator.validate_project_improvement_handoffs(root)

            self.assertTrue(
                any("require project_improvement_bridge" in error for error in report["errors"])
            )

    def test_bridge_validator_rejects_markdown_yaml_signal_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root, include_bridge_reference=True)
            result = self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=True,
                repo_root=root,
            )
            markdown_path = root / result["output_paths"]["markdown"]
            markdown_path.write_text(
                markdown_path.read_text(encoding="utf-8").replace(
                    "PIS-RT-20260622-090-001",
                    "PIS-RT-20260622-090-DRIFTED",
                ),
                encoding="utf-8",
            )

            report = self.bridge_validator.validate_project_improvement_handoffs(root)

            self.assertTrue(any("Markdown mirror missing signal_id" in error for error in report["errors"]))

    def test_conditional_checkpoint_sidecar_paths_accepts_bridge_referenced_pair(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root, include_bridge_reference=True)
            result = self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=True,
                repo_root=root,
            )
            source_path = (
                "research_control/tasks/RT-20260622-090/jobs/completions/"
                "AJC-AJ-RT-20260622-090-001.yaml"
            )
            changed_paths = [
                source_path,
                result["output_paths"]["yaml"],
                result["output_paths"]["markdown"],
            ]

            allowed = self.bridge_validator.conditional_checkpoint_sidecar_paths(
                root,
                changed_paths,
                [source_path],
            )

            self.assertEqual(
                allowed,
                [
                    "research_control/project_improvement_handoffs/improve-project-handoff_20260622_090.md",
                    "research_control/project_improvement_handoffs/improve-project-handoff_20260622_090.yaml",
                ],
            )

    def test_conditional_checkpoint_sidecar_paths_rejects_unreferenced_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root)
            result = self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=True,
                repo_root=root,
            )
            source_path = (
                "research_control/tasks/RT-20260622-090/jobs/completions/"
                "AJC-AJ-RT-20260622-090-001.yaml"
            )

            allowed = self.bridge_validator.conditional_checkpoint_sidecar_paths(
                root,
                [source_path, result["output_paths"]["yaml"], result["output_paths"]["markdown"]],
                [source_path],
            )

            self.assertEqual(allowed, [])

    def test_checkpoint_extends_allowlist_only_for_valid_sidecar_pair(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_generator_fixture(root, include_bridge_reference=True)
            result = self.generator.generate_project_improvement_handoff(
                completion_path=(
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml"
                ),
                source_handoff_path="research_control/handoffs/handoff-0090.yaml",
                created_at="2026-06-22T05:00:00Z",
                write=True,
                repo_root=root,
            )
            source_path = (
                "research_control/tasks/RT-20260622-090/jobs/completions/"
                "AJC-AJ-RT-20260622-090-001.yaml"
            )
            changed_paths = [
                source_path,
                result["output_paths"]["yaml"],
                result["output_paths"]["markdown"],
            ]
            job_row = {
                "allowed_write_paths": source_path,
                "output_paths": "",
            }

            with mock.patch.object(self.checkpoint, "REPO_ROOT", root):
                allowed = self.checkpoint.allowed_patterns_for_changed_paths(
                    job_row,
                    {},
                    changed_paths,
                )

            self.assertTrue(self.checkpoint.allowed_by_any(result["output_paths"]["yaml"], allowed))
            self.assertTrue(self.checkpoint.allowed_by_any(result["output_paths"]["markdown"], allowed))
            self.assertFalse(
                self.checkpoint.allowed_by_any(
                    "research_control/project_improvement_handoffs/improve-project-handoff_20260622_999.yaml",
                    allowed,
                )
            )

    @staticmethod
    def write_handoff_pair(handoff_dir: Path, number: int) -> None:
        handoff_id = f"handoff-{number:04d}"
        yaml_path = handoff_dir / f"{handoff_id}.yaml"
        yaml_path.write_text(
            "\n".join(
                [
                    f'handoff_id: "{handoff_id}"',
                    'created_at: "2026-06-22T03:27:07Z"',
                    'task_id: "RT-TEST"',
                    'job_id: "AJ-RT-TEST-001"',
                    'completion_path: "research_control/tasks/RT-TEST/jobs/completions/AJC-AJ-RT-TEST-001.yaml"',
                    'next_action: "Continue normal research handoff."',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (handoff_dir / f"{handoff_id}.md").write_text(
            f"# {handoff_id}\n",
            encoding="utf-8",
        )

    @staticmethod
    def write_generator_fixture(
        root: Path,
        *,
        blank_signal: bool = False,
        omit_signal_row: bool = False,
        include_bridge_reference: bool = False,
    ) -> None:
        registry_dir = root / "registries"
        registry_dir.mkdir(parents=True)
        (registry_dir / "PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv").write_text(
            "\n".join(
                [
                    "signal_type,default_recommended_skill,default_recommended_role,status,notes",
                    "validator_gap,improve-project-system,validator-engineer,active,Validator coverage gap.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        signal_rows = [
            (
                "signal_id,created_at,source_task_id,source_job_id,source_role_id,"
                "signal_type,severity,status,evidence_path,recommended_skill,"
                "recommended_role,notes,resolved_by_job_id,resolution_evidence_path,resolved_at"
            )
        ]
        if not omit_signal_row:
            signal_rows.append(
                (
                    "PIS-RT-20260622-090-001,2026-06-22T05:00:00Z,"
                    "RT-20260622-090,AJ-RT-20260622-090-001,validator-engineer,"
                    "validator_gap,high,open,"
                    "research_control/tasks/RT-20260622-090/jobs/completions/"
                    "AJC-AJ-RT-20260622-090-001.yaml,"
                    "improve-project-system,validator-engineer,"
                    "Focused bridge generator fixture.,,,"
                )
            )
        signal_rows.append("")
        (registry_dir / "PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv").write_text(
            "\n".join(signal_rows),
            encoding="utf-8",
        )

        completion_dir = (
            root
            / "research_control/tasks/RT-20260622-090/jobs/completions"
        )
        completion_dir.mkdir(parents=True)
        signal_block = (
            "\n".join(
                [
                    "project_improvement_signals:",
                    "  - signal_id: \"\"",
                    "    signal_type: \"\"",
                    "    severity: \"\"",
                    "    evidence: \"\"",
                    "    evidence_path: \"\"",
                    "    recommended_skill: \"\"",
                    "    recommended_role: \"\"",
                ]
            )
            if blank_signal
            else "\n".join(
                [
                    "project_improvement_signals:",
                    "  - signal_id: \"PIS-RT-20260622-090-001\"",
                    "    signal_type: \"validator_gap\"",
                    "    severity: \"high\"",
                    "    evidence: \"Focused bridge generator fixture.\"",
                    "    evidence_path: \"research_control/tasks/RT-20260622-090/jobs/completions/AJC-AJ-RT-20260622-090-001.yaml\"",
                    "    recommended_skill: \"improve-project-system\"",
                    "    recommended_role: \"validator-engineer\"",
                ]
            )
        )
        bridge_block = (
            "\n".join(
                [
                    "project_improvement_bridge:",
                    "  required: true",
                    "  improvement_handoff_path: \"research_control/project_improvement_handoffs/improve-project-handoff_20260622_090.yaml\"",
                    "  signal_ids:",
                    "    - \"PIS-RT-20260622-090-001\"",
                    "  bridge_status: \"generated\"",
                    "  notes: \"Fixture bridge reference.\"",
                ]
            )
            if include_bridge_reference and not blank_signal
            else "\n".join(
                [
                    "project_improvement_bridge:",
                    "  required: false",
                    "  improvement_handoff_path: \"\"",
                    "  signal_ids:",
                    "    - \"\"",
                    "  bridge_status: \"not_required\"",
                    "  notes: \"\"",
                ]
            )
            if include_bridge_reference
            else ""
        )
        handoff_bridge_block = (
            "\n".join(
                [
                    "project_improvement_bridge:",
                    "  required: false",
                    "  improvement_handoff_path: \"\"",
                    "  signal_ids:",
                    "    - \"\"",
                    "  bridge_status: \"not_required\"",
                    "  notes: \"\"",
                ]
            )
            if include_bridge_reference
            else ""
        )
        (completion_dir / "AJC-AJ-RT-20260622-090-001.yaml").write_text(
            "\n".join(
                [
                    "completion_id: \"AJC-AJ-RT-20260622-090-001\"",
                    "job_id: \"AJ-RT-20260622-090-001\"",
                    "task_id: \"RT-20260622-090\"",
                    "decision_id: \"DDR-20260622-090\"",
                    "completed_at: \"2026-06-22T05:00:00Z\"",
                    "status: \"completed\"",
                    signal_block,
                    bridge_block,
                    "",
                ]
            ),
            encoding="utf-8",
        )

        handoff_dir = root / "research_control/handoffs"
        handoff_dir.mkdir(parents=True)
        (handoff_dir / "handoff-0090.yaml").write_text(
            "\n".join(
                [
                    "handoff_id: \"handoff-0090\"",
                    "created_at: \"2026-06-22T05:00:00Z\"",
                    "task_id: \"RT-20260622-090\"",
                    "decision_id: \"DDR-20260622-090\"",
                    "job_id: \"AJ-RT-20260622-090-001\"",
                    "completion_path: \"research_control/tasks/RT-20260622-090/jobs/completions/AJC-AJ-RT-20260622-090-001.yaml\"",
                    "next_action: \"Continue normal research.\"",
                    "project_improvement_signals:",
                    "  - signal_id: \"\"",
                    "    signal_type: \"\"",
                    "    severity: \"\"",
                    "    evidence: \"\"",
                    "    evidence_path: \"\"",
                    "    recommended_skill: \"\"",
                    "    recommended_role: \"\"",
                    handoff_bridge_block,
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (handoff_dir / "handoff-0090.md").write_text(
            "# handoff-0090\n",
            encoding="utf-8",
        )
