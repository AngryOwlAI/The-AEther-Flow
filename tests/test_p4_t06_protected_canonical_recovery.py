from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from scripts.research_control import validate_research_control as validator
from scripts.research_control.strict_yaml import load as load_yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_JOB_PATH = (
    ROOT
    / "research_control/tasks/RT-20260724-010/jobs/"
    "AJ-RT-20260724-010-001.yaml"
)


class P4T06ProtectedCanonicalRecoveryTests(unittest.TestCase):
    @staticmethod
    def source_row() -> dict[str, str]:
        return {
            "job_id": "AJ-RT-20260724-010-001",
            "task_id": "RT-20260724-010",
            "role_id": "ontology-formalizer",
            "job_path": (
                "research_control/tasks/RT-20260724-010/jobs/"
                "AJ-RT-20260724-010-001.yaml"
            ),
            "created_at": "2026-07-24T23:57:27Z",
            "started_at": "2026-07-24T23:57:27Z",
            "completed_at": "2026-07-25T00:20:26Z",
        }

    def test_exact_p4_t06_protected_canonical_integration_is_admitted(self) -> None:
        report = validator.ValidationReport()
        validator.validate_future_physics_job_authority(
            report,
            self.source_row(),
            load_yaml(SOURCE_JOB_PATH),
        )
        self.assertFalse(
            any("may not allow direct write path" in error for error in report.errors),
            report.errors,
        )
        self.assertFalse(
            any(
                "protected canonical integration admission invalid" in error
                for error in report.errors
            ),
            report.errors,
        )

    def test_protected_canonical_integration_rejects_broadened_path(self) -> None:
        job = load_yaml(SOURCE_JOB_PATH)
        job["allowed_write_paths"] = [
            *job["allowed_write_paths"],
            "ontology/tex/unapproved_extension.tex",
        ]
        report = validator.ValidationReport()
        validator.validate_future_physics_job_authority(
            report,
            self.source_row(),
            job,
        )
        self.assertTrue(
            any("protected_paths_not_exact" in error for error in report.errors),
            report.errors,
        )
        self.assertTrue(
            any("unapproved_extension.tex" in error for error in report.errors),
            report.errors,
        )

    def test_protected_canonical_integration_rejects_stale_authorization(self) -> None:
        original_sha256_file = validator.sha256_file

        def stale_route_hash(path: Path) -> str:
            if path.name == "canonical_next_route_authorization_v1.yaml":
                return "0" * 64
            return original_sha256_file(path)

        report = validator.ValidationReport()
        with mock.patch.object(
            validator,
            "sha256_file",
            side_effect=stale_route_hash,
        ):
            validator.validate_future_physics_job_authority(
                report,
                self.source_row(),
                load_yaml(SOURCE_JOB_PATH),
            )
        self.assertTrue(
            any("route_authorization_hash_mismatch" in error for error in report.errors),
            report.errors,
        )
        self.assertTrue(
            any("may not allow direct write path" in error for error in report.errors),
            report.errors,
        )

    def test_ordinary_direct_ontology_write_remains_rejected(self) -> None:
        report = validator.ValidationReport()
        validator.validate_future_physics_job_authority(
            report,
            {
                "job_id": "AJ-TEST",
                "task_id": "RT-TEST",
                "role_id": "refuter",
                "job_path": "research_control/tasks/RT-TEST/jobs/AJ-TEST.yaml",
                "created_at": "2026-06-16T20:00:00Z",
                "started_at": "",
                "completed_at": "",
            },
            {
                "allowed_write_paths": ["ontology/tex/example.tex"],
                "forbidden_source_classes": sorted(
                    validator.PHYSICS_JOB_REQUIRED_FORBIDDEN_SOURCE_CLASSES
                ),
            },
        )
        self.assertTrue(
            any("may not allow direct write path" in error for error in report.errors)
        )

    def test_changed_sources_require_current_active_hash_and_preserve_history(self) -> None:
        object_ids = {
            "TEX-ONTOLOGY-AETHER-FLOW-FOUNDATIONS",
            "TEX-ONTOLOGY-AETHER-FLOW-DYNAMICS",
            "TEX-ONTOLOGY-AETHER-FLOW-GEOMETRY",
            "MD-RESEARCH-CONTROL-DESIGN-EPISTEMIC-CATEGORY-GLOSSARY",
        }
        self.assertTrue(
            object_ids.issubset(validator.MUTABLE_MEMORY_PREFLIGHT_SOURCE_OBJECT_IDS)
        )
        active_task_id = validator.active_program_task_id()
        self.assertTrue(active_task_id)
        for object_id in object_ids:
            with self.subTest(object_id=object_id):
                self.assertTrue(
                    validator.memory_preflight_hash_must_be_current(
                        {"task_id": active_task_id},
                        object_id,
                    )
                )
                self.assertFalse(
                    validator.memory_preflight_hash_must_be_current(
                        {"task_id": "RT-HISTORICAL"},
                        object_id,
                    )
                )

    def test_exact_handoff_0861_historical_route_count_is_preserved(self) -> None:
        path = ROOT / "research_control/handoffs/handoff-0861.yaml"
        data = load_yaml(path)
        self.assertTrue(
            validator.immutable_historical_ordinary_route_guard_is_compatible(
                path,
                data,
                ["consecutive_project_system_task_count_mismatch"],
            )
        )

    def test_handoff_0861_compatibility_rejects_hash_drift(self) -> None:
        path = ROOT / "research_control/handoffs/handoff-0861.yaml"
        data = load_yaml(path)
        with mock.patch.object(validator, "sha256_file", return_value="0" * 64):
            self.assertFalse(
                validator.immutable_historical_ordinary_route_guard_is_compatible(
                    path,
                    data,
                    ["consecutive_project_system_task_count_mismatch"],
                )
            )


if __name__ == "__main__":
    unittest.main()
