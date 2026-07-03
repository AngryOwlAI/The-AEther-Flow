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


class ScientificPayloadDensityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reporter = load_module(
            "report_scientific_payload_density",
            "report_scientific_payload_density.py",
        )

    def write_csv(self, path: Path, rows: list[dict[str, str]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    def make_repo(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name)
        self.write_csv(
            repo / "registries" / "AGENT_JOB_REGISTRY.csv",
            [
                {
                    "job_id": "AJ-ONE",
                    "task_id": "RT-ONE",
                    "decision_id": "DDR-ONE",
                    "role_id": "ontology-formalizer",
                    "role_version": "0.2.0",
                    "job_path": "research_control/tasks/RT-ONE/jobs/AJ-ONE.yaml",
                    "completion_path": "research_control/tasks/RT-ONE/jobs/completions/AJC-ONE.yaml",
                    "status": "completed",
                    "allowed_write_paths": "",
                    "output_paths": "",
                    "validation_status": "PASS",
                    "created_at": "2026-07-03T00:00:00Z",
                    "started_at": "2026-07-03T00:00:00Z",
                    "completed_at": "2026-07-03T00:00:00Z",
                    "requires_human_gate": "false",
                    "notes": "scientific payload fixture",
                },
                {
                    "job_id": "AJ-TWO",
                    "task_id": "RT-TWO",
                    "decision_id": "DDR-TWO",
                    "role_id": "validator-engineer",
                    "role_version": "0.2.0",
                    "job_path": "research_control/tasks/RT-TWO/jobs/AJ-TWO.yaml",
                    "completion_path": "research_control/tasks/RT-TWO/jobs/completions/AJC-TWO.yaml",
                    "status": "completed",
                    "allowed_write_paths": "",
                    "output_paths": "",
                    "validation_status": "PASS",
                    "created_at": "2026-07-03T00:01:00Z",
                    "started_at": "2026-07-03T00:01:00Z",
                    "completed_at": "2026-07-03T00:01:00Z",
                    "requires_human_gate": "false",
                    "notes": "process fixture",
                },
            ],
        )
        self.write_csv(
            repo / "registries" / "RESEARCH_TASK_REGISTRY.csv",
            [
                {
                    "task_id": "RT-ONE",
                    "task_path": "research_control/tasks/RT-ONE",
                    "task_type": "source_certificate_operation_laws_fail_closed_lemma",
                    "status": "completed",
                    "current_decision_id": "DDR-ONE",
                    "current_job_id": "AJ-ONE",
                    "parent_task_id": "",
                    "created_at": "2026-07-03T00:00:00Z",
                    "updated_at": "2026-07-03T00:00:00Z",
                    "closed_at": "2026-07-03T00:00:00Z",
                    "closure_status": "done",
                    "requires_human_gate": "false",
                    "notes": "",
                },
                {
                    "task_id": "RT-TWO",
                    "task_path": "research_control/tasks/RT-TWO",
                    "task_type": "distance_to_gr_delta_report_enforcement",
                    "status": "completed",
                    "current_decision_id": "DDR-TWO",
                    "current_job_id": "AJ-TWO",
                    "parent_task_id": "",
                    "created_at": "2026-07-03T00:01:00Z",
                    "updated_at": "2026-07-03T00:01:00Z",
                    "closed_at": "2026-07-03T00:01:00Z",
                    "closure_status": "done",
                    "requires_human_gate": "false",
                    "notes": "",
                },
            ],
        )
        (repo / "research_control/tasks/RT-ONE/jobs/completions").mkdir(parents=True)
        (repo / "research_control/tasks/RT-TWO/jobs/completions").mkdir(parents=True)
        (repo / "research_control/tasks/RT-ONE/jobs/AJ-ONE.yaml").write_text(
            'target_derivation_milestone: "source_certificate_operation_laws"\n',
            encoding="utf-8",
        )
        (repo / "research_control/tasks/RT-TWO/jobs/AJ-TWO.yaml").write_text(
            'target_derivation_milestone: "none"\n',
            encoding="utf-8",
        )
        (repo / "research_control/tasks/RT-ONE/00_TASK.yaml").write_text(
            'task_type: "source_certificate_operation_laws_fail_closed_lemma"\n'
            "implementation_plan:\n"
            '  plan_phase_id: "P3"\n',
            encoding="utf-8",
        )
        (repo / "research_control/tasks/RT-TWO/00_TASK.yaml").write_text(
            'task_type: "distance_to_gr_delta_report_enforcement"\n'
            "implementation_plan:\n"
            '  plan_phase_id: "P9"\n',
            encoding="utf-8",
        )
        (repo / "research_control/tasks/RT-ONE/jobs/completions/AJC-ONE.yaml").write_text(
            "implementation_plan_receipt:\n"
            '  plan_phase_id: "P3"\n'
            "physics_progress_status:\n"
            '  target_derivation_milestone: "source_certificate_operation_laws"\n'
            "mathematical_payload_manifest:\n"
            '  - payload_type: "theorem_with_hypotheses_and_proof"\n'
            '    object_name: "FixtureConditionalTheorem_v1"\n'
            '    claim_status: "draft/control"\n'
            '  - payload_type: "dependency_map_update"\n'
            '    object_name: "FixtureDependencyMap_v1"\n',
            encoding="utf-8",
        )
        (repo / "research_control/tasks/RT-TWO/jobs/completions/AJC-TWO.yaml").write_text(
            "implementation_plan_receipt:\n"
            '  plan_phase_id: "P9"\n',
            encoding="utf-8",
        )
        return repo

    def test_report_declares_operational_non_promotion_boundary(self) -> None:
        report = self.reporter.build_report(self.make_repo())
        boundary = report["authority_boundary"]

        self.assertTrue(boundary["metrics_are_operational_diagnostics_only"])
        self.assertTrue(boundary["not_physics_proof"])
        self.assertFalse(boundary["physics_claim_promotion_authorized"])
        self.assertIn("not physics proof", boundary["statement"])

    def test_report_groups_density_by_required_dimensions(self) -> None:
        report = self.reporter.build_report(self.make_repo())

        self.assertIn("P3", report["by_phase"])
        self.assertIn("P9", report["by_phase"])
        self.assertIn("ontology-formalizer", report["by_role"])
        self.assertIn("validator-engineer", report["by_role"])
        self.assertIn("source_certificate_operation_laws", report["by_milestone"])
        self.assertIn("none", report["by_milestone"])
        self.assertIn("source_certificate_operation_laws_fail_closed_lemma", report["by_task_family"])
        self.assertIn("distance_to_gr_delta_report_enforcement", report["by_task_family"])
        self.assertEqual(report["overall"]["task_count"], 2)

    def test_process_only_work_is_separated_from_mathematical_payload(self) -> None:
        report = self.reporter.build_report(self.make_repo())

        self.assertEqual(report["by_role"]["validator-engineer"]["process_only_task_count"], 1)
        self.assertEqual(report["by_role"]["validator-engineer"]["mathematical_payload_item_count"], 0)
        self.assertEqual(report["by_role"]["ontology-formalizer"]["mathematical_payload_task_count"], 1)
        self.assertGreater(report["by_role"]["ontology-formalizer"]["payload_density"], 0)


if __name__ == "__main__":
    unittest.main()
