from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
TEMPLATE_DIR = REPO_ROOT / "research_control" / "templates"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "project_improvement_bridge"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProjectImprovementBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.strict_yaml = load_module("strict_yaml", "strict_yaml.py")
        cls.resolver = load_module("resolve_latest_handoff", "resolve_latest_handoff.py")

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
