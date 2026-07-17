from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"

from scripts.project_control.classify_project_changes import classify_paths
from scripts.research_control import render_route_diagnostics as renderer
from scripts.validation.plan import build_plan, load_manifest


def warning_record(*warning_ids: str) -> dict[str, object]:
    return {
        "triggered": bool(warning_ids),
        "severity": "warning" if warning_ids else "none",
        "warning_ids": list(warning_ids),
        "recommended_guard_action": "Inspect direct diagnostics when needed.",
        "hard_gate": False,
        "physics_claim_authority": False,
        "advisory_only": True,
        "evidence": {},
    }


def diagnostics_context(*warning_ids: str) -> dict[str, object]:
    records = {
        "payload_density_warning": warning_record(
            *(warning_ids[:1] if warning_ids else ())
        ),
        "route_orbit_warning": warning_record(
            *(warning_ids[1:2] if len(warning_ids) > 1 else ())
        ),
        "same_burden_repetition_warning": warning_record(),
        "gate_ready_without_gate_warning": warning_record(),
    }
    return {
        "status": "PASS",
        "source": "direct_fixture",
        "warnings_are_advisory_only": True,
        "warning_hard_gates_created": False,
        "physics_claim_authority_created": False,
        **records,
        "recommended_guard_action": "Inspect direct diagnostics when needed.",
        "diagnostic_warning_count": len(warning_ids),
        "diagnostic_warning_ids": list(warning_ids),
        "payload_density_metrics": {"physics_payload_ratio": 0.5},
        "route_orbit_risk_metrics": {"warning_count": len(warning_ids)},
    }


def signature_summary(*, warning_count: int = 0) -> dict[str, object]:
    return {
        "status": "PASS",
        "source_task_count": 7,
        "signature_count": 7,
        "extraction_error_count": 0,
        "legacy_hard_candidate_count": 0,
        "warning_count": warning_count,
        "repeated_burden_cycle_count": 0,
        "repeated_no_new_payload_cycle_count": 0,
        "route_orbit_warning_should_emit": bool(warning_count),
        "advisory_only": True,
        "hard_gate": False,
        "route_freeze_authorized": False,
        "physics_claim_authority": False,
    }


def orbit_summary(*warning_ids: str) -> dict[str, object]:
    return {
        "status": "PASS",
        "source_task_count": 7,
        "signature_count": 7,
        "extraction_error_count": 0,
        "legacy_hard_candidate_count": 0,
        "warning_count": len(warning_ids),
        "legacy_hard_candidate_ids": [],
        "warning_ids": list(warning_ids),
        "affected_task_ids": ["RT-FIXTURE"] if warning_ids else [],
        "affected_task_ids_omitted": 0,
        "advisory_only": True,
        "hard_gate": False,
        "route_freeze_authorized": False,
        "physics_claim_authority": False,
    }


class RouteDiagnosticCacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(MANIFEST_PATH)

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.repo_root = Path(self.temporary_directory.name)
        self.cache_path = self.repo_root / renderer.DEFAULT_CACHE_PATH
        self._write_source_fixture()

    def _write(self, relative_path: str, content: str) -> Path:
        path = self.repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def _write_source_fixture(self) -> None:
        self._write(
            "registries/RESEARCH_TASK_REGISTRY.csv",
            "task_id,task_path\nRT-FIXTURE,research_control/tasks/RT-FIXTURE\n",
        )
        self._write(
            "registries/AGENT_JOB_REGISTRY.csv",
            (
                "job_id,job_path,completion_path\n"
                "AJ-FIXTURE,research_control/tasks/RT-FIXTURE/jobs/AJ-FIXTURE.yaml,"
                "research_control/tasks/RT-FIXTURE/jobs/completions/"
                "AJC-AJ-FIXTURE.yaml\n"
            ),
        )
        self._write(
            "registries/DIRECTOR_DECISION_REGISTRY.csv",
            "decision_id,decision_path\nDDR-FIXTURE,"
            "research_control/tasks/RT-FIXTURE/DDR-FIXTURE.md\n",
        )
        for registry in (
            "registries/AGENT_ROLE_REGISTRY.csv",
            "registries/CLAIM_BOUNDARY_REGISTRY.csv",
        ):
            self._write(registry, "id\n")
        self._write(
            "research_control/tasks/RT-FIXTURE/00_TASK.yaml",
            "task_id: RT-FIXTURE\n",
        )
        self._write(
            "research_control/tasks/RT-FIXTURE/jobs/AJ-FIXTURE.yaml",
            "job_id: AJ-FIXTURE\n",
        )
        self._write(
            "research_control/tasks/RT-FIXTURE/jobs/completions/"
            "AJC-AJ-FIXTURE.yaml",
            "completion_id: AJC-AJ-FIXTURE\n",
        )
        self._write(
            "research_control/tasks/RT-FIXTURE/DDR-FIXTURE.md",
            "# Fixture decision\n",
        )
        self._write(
            "research_control/handoffs/handoff-fixture.yaml",
            "handoff_id: handoff-fixture\n",
        )
        self._write(
            "research_control/design/route_signature_definition.md",
            "# Fixture policy\n",
        )

    def _build_cache(
        self,
        *,
        diagnostics: dict[str, object] | None = None,
        signature: dict[str, object] | None = None,
        orbit: dict[str, object] | None = None,
    ) -> dict[str, object]:
        diagnostics = diagnostics or diagnostics_context()
        signature = signature or signature_summary()
        orbit = orbit or orbit_summary()
        return renderer.build_cache(
            self.repo_root,
            diagnostics_builder=lambda _root: deepcopy(diagnostics),
            route_signature_builder=lambda _root: deepcopy(signature),
            route_orbit_builder=lambda _root: deepcopy(orbit),
        )

    def _write_cache(self, cache: dict[str, object]) -> None:
        renderer.atomic_write_cache(self.cache_path, cache)

    def test_warning_fixture_preserves_advisory_boundary(self) -> None:
        direct_diagnostics = diagnostics_context(
            "payload_density_warning",
            "route_cycle_warning",
        )
        direct_signature = signature_summary(warning_count=1)
        direct_orbit = orbit_summary("route_cycle_warning")
        cache = self._build_cache(
            diagnostics=direct_diagnostics,
            signature=direct_signature,
            orbit=direct_orbit,
        )

        self.assertEqual(cache["diagnostics"], direct_diagnostics)
        self.assertEqual(cache["route_signature_summary"], direct_signature)
        self.assertEqual(cache["route_orbit_summary"], direct_orbit)
        self.assertEqual(
            cache["warning_ids"],
            ["payload_density_warning", "route_cycle_warning"],
        )
        self.assertEqual(cache["warning_count"], 4)
        self.assertFalse(cache["authority_boundary"]["hard_gate_created"])
        self.assertFalse(
            cache["authority_boundary"]["physics_claim_authority"]
        )
        for field_name in renderer.WARNING_FIELDS:
            record = cache["diagnostics"][field_name]
            self.assertTrue(record["advisory_only"])
            self.assertFalse(record["hard_gate"])
            self.assertFalse(record["physics_claim_authority"])

    def test_no_warning_fixture_builds_valid_empty_findings(self) -> None:
        cache = self._build_cache()

        self.assertEqual(renderer.validate_cache(cache), [])
        self.assertEqual(cache["warning_count"], 0)
        self.assertEqual(cache["warning_ids"], [])
        self.assertFalse(cache["diagnostics"]["warning_hard_gates_created"])

    def test_fresh_cache_is_consumed_without_recomputation(self) -> None:
        self._write_cache(self._build_cache())

        inspection = renderer.inspect_cache(self.repo_root)
        context = renderer.routing_diagnostics_from_cache(self.repo_root)

        self.assertEqual(inspection["cache_status"], "fresh")
        self.assertEqual(context["status"], "fresh_cache")
        self.assertEqual(context["cache_status"], "fresh")
        self.assertFalse(context["freshness_notice"]["hard_gate"])
        self.assertEqual(list(self.cache_path.parent.glob("*.tmp")), [])

    def test_missing_cache_returns_empty_advisory_findings(self) -> None:
        context = renderer.routing_diagnostics_from_cache(self.repo_root)

        self.assertEqual(context["status"], "missing_cache")
        self.assertEqual(context["diagnostic_warning_count"], 0)
        self.assertFalse(context["warning_hard_gates_created"])
        self.assertFalse(context["physics_claim_authority_created"])

    def test_stale_cache_returns_empty_advisory_findings(self) -> None:
        self._write_cache(self._build_cache())
        self._write(
            "research_control/tasks/RT-FIXTURE/jobs/completions/"
            "AJC-AJ-FIXTURE.yaml",
            "completion_id: AJC-AJ-FIXTURE\nstatus: changed\n",
        )

        context = renderer.routing_diagnostics_from_cache(self.repo_root)

        self.assertEqual(context["status"], "stale_cache")
        self.assertEqual(context["diagnostic_warning_ids"], [])
        self.assertFalse(context["freshness_notice"]["hard_gate"])

    def test_parse_error_returns_empty_advisory_findings(self) -> None:
        self._write(
            renderer.DEFAULT_CACHE_PATH.as_posix(),
            "{not-json\n",
        )

        context = renderer.routing_diagnostics_from_cache(self.repo_root)

        self.assertEqual(context["status"], "parse_error_cache")
        self.assertEqual(context["diagnostic_warning_count"], 0)
        self.assertTrue(context["freshness_notice"]["errors"])

    def test_invalid_authority_cache_is_not_consumed(self) -> None:
        cache = self._build_cache()
        cache["authority_boundary"]["hard_gate_created"] = True
        self._write(
            renderer.DEFAULT_CACHE_PATH.as_posix(),
            json.dumps(cache),
        )

        context = renderer.routing_diagnostics_from_cache(self.repo_root)

        self.assertEqual(context["status"], "invalid_cache")
        self.assertEqual(context["diagnostic_warning_ids"], [])
        self.assertFalse(context["freshness_notice"]["hard_gate"])

    def test_source_fingerprint_covers_every_required_source_family(self) -> None:
        mutations = {
            "task": (
                "research_control/tasks/RT-FIXTURE/00_TASK.yaml",
                "task_id: RT-FIXTURE\nchanged: task\n",
            ),
            "job": (
                "research_control/tasks/RT-FIXTURE/jobs/AJ-FIXTURE.yaml",
                "job_id: AJ-FIXTURE\nchanged: job\n",
            ),
            "completion": (
                "research_control/tasks/RT-FIXTURE/jobs/completions/"
                "AJC-AJ-FIXTURE.yaml",
                "completion_id: AJC-AJ-FIXTURE\nchanged: completion\n",
            ),
            "handoff": (
                "research_control/handoffs/handoff-fixture.yaml",
                "handoff_id: handoff-fixture\nchanged: handoff\n",
            ),
            "policy": (
                "research_control/design/route_signature_definition.md",
                "# Changed fixture policy\n",
            ),
        }
        baseline = renderer.source_snapshot(self.repo_root)["source_fingerprint"]
        for family, (relative_path, replacement) in mutations.items():
            path = self.repo_root / relative_path
            original = path.read_text(encoding="utf-8")
            with self.subTest(source_family=family):
                path.write_text(replacement, encoding="utf-8")
                changed = renderer.source_snapshot(self.repo_root)[
                    "source_fingerprint"
                ]
                self.assertNotEqual(changed, baseline)
                path.write_text(original, encoding="utf-8")
                restored = renderer.source_snapshot(self.repo_root)[
                    "source_fingerprint"
                ]
                self.assertEqual(restored, baseline)

    def test_manifest_profiles_keep_expensive_diagnostics_explicit(self) -> None:
        ordinary = build_plan(
            self.manifest,
            classify_paths([]),
            profile="full",
        )
        doctor = build_plan(
            self.manifest,
            classify_paths([]),
            profile="doctor",
            scopes=("local_retrieval",),
        )
        explicit_cache = build_plan(
            self.manifest,
            classify_paths([]),
            profile="full",
            role_obligations=("route_diagnostic_cache_regeneration",),
        )
        explicit_orbit = build_plan(
            self.manifest,
            classify_paths([]),
            profile="full",
            role_obligations=("route_orbit_diagnostic",),
        )

        self.assertNotIn("route_signature_diagnostic", ordinary.selected_gate_ids)
        self.assertNotIn("route_orbit_diagnostic", ordinary.selected_gate_ids)
        self.assertIn("route_signature_diagnostic", doctor.selected_gate_ids)
        self.assertIn("route_orbit_diagnostic", doctor.selected_gate_ids)
        self.assertIn(
            "route_signature_diagnostic",
            explicit_cache.selected_gate_ids,
        )
        self.assertIn("route_orbit_diagnostic", explicit_orbit.selected_gate_ids)


if __name__ == "__main__":
    unittest.main()
