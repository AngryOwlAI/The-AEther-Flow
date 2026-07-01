from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"


def load_module():
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(
        "render_current_frontier",
        SCRIPT_DIR / "render_current_frontier.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RenderCurrentFrontierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.renderer = load_module()

    def make_fixture_repo(self, root: Path) -> None:
        control = root / "research_control"
        design = control / "design"
        handoffs = control / "handoffs"
        task = control / "tasks" / "RT-TEST"
        registries = root / "registries"
        design.mkdir(parents=True)
        handoffs.mkdir(parents=True)
        task.mkdir(parents=True)
        registries.mkdir(parents=True)
        (control / "program_state.yaml").write_text(
            "\n".join(
                [
                    'active_task_id: "RT-TEST"',
                    'latest_handoff_id: "handoff-0001"',
                    'current_status: "fixture_completed_no_promotion"',
                    'next_recommended_action: "Run one bounded fixture validation packet."',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (design / "distance_to_gr_status_aliases.yaml").write_text(
            "\n".join(
                [
                    'schema_id: "distance_to_gr_status_aliases_v1"',
                    'authority: "control"',
                    "authority_rules:",
                    "  aliases_do_not_override_ledger: true",
                    "  aliases_are_physics_proof: false",
                    "  high_risk_rows_must_not_render_bare_accepted: true",
                    "row_aliases:",
                    "  matter_coupling:",
                    '    display_status: "accepted only as scoped source-extension evidence/precondition"',
                    '    required_qualifier: "Matter coupling remains not derived and not adopted."',
                    '    required_blocked_phrase: "No matter coupling or Einstein equations follow from this row."',
                    "    object_aliases:",
                    "      PositiveMSProfile_v1:",
                    '        display_status: "accepted only as scoped positive source-semantics evidence/precondition"',
                    '        required_qualifier: "Not adopted matter semantics."',
                    "      RR_ETransportCompletenessOrInvarianceLaw_v1:",
                    '        display_status: "accepted only as certificate-indexed RR_E transport-completeness or invariance evidence/precondition"',
                    '        required_qualifier: "Not source-law adoption."',
                    "  g_eff:",
                    '    display_status: "adopted only as scoped source-extension g_eff object"',
                    '    required_qualifier: "Not an unscoped Lorentzian metric."',
                    '    required_blocked_phrase: "No matter coupling or Einstein equations follow from this row."',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (handoffs / "handoff-0001.yaml").write_text(
            "\n".join(
                [
                    'handoff_id: "handoff-0001"',
                    'task_id: "RT-TEST"',
                    'status: "completed"',
                    'summary: "Fixture handoff summary."',
                    'next_action: "Run one bounded fixture validation packet."',
                    'loop_risk_route: "fixture_route"',
                    "claim_boundary:",
                    '  allowed_next_scope: "bounded fixture validation only"',
                    "distance_to_gr:",
                    '  milestone: "none"',
                    '  burden_id: "none"',
                    '  status: "unchanged_fixture_only"',
                    "required_next_packet:",
                    '  task_type: "fixture_validation"',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (task / "00_TASK.yaml").write_text(
            "\n".join(
                [
                    'task_id: "RT-TEST"',
                    'task_type: "p1_generated_current_state_report"',
                    'objective: "Render a fixture current frontier."',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (registries / "DISTANCE_TO_GR_LEDGER.csv").write_text(
            "\n".join(
                [
                    "burden_id,milestone,required_object,current_status,blocking_burden,accept_criteria,failure_or_freeze_criteria,last_evidence_path,updated_at,notes,control_status,mathematical_status,physical_status,promotion_status,overread_guard",
                    "matter_coupling,matter_coupling,universal coupling,accepted,scoped evidence only,accept,fail,research_control/program_state.yaml,2026-06-28T00:00:00Z,fixture,accepted_as_scoped_evidence_precondition,parameterized_finite_local_witness_precondition,not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics,scoped_source_evidence_only,no_coupling_law_adoption;no_matter_coupling_derivation;no_stress_energy_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation",
                    "g_eff,effective_metric_g_eff,effective metric,accepted,scoped source-extension object only,accept,fail,research_control/program_state.yaml,2026-06-28T00:00:00Z,fixture,gate_review_completed,scoped_source_extension_geff_object,not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations,scoped_source_object_only,no_unscoped_geff_adoption;no_matter_coupling_derivation;no_einstein_equations;no_benchmark_promotion;no_completed_derivation",
                    "einstein_equations,einstein_equations,field equations,not started,dynamics action or variation,accept,fail,research_control/program_state.yaml,2026-06-28T00:00:00Z,fixture,not_started,dynamics_action_or_variation_missing,no_field_equation_derivation,none,no_einstein_equations;no_benchmark_promotion;no_completed_derivation",
                    "benchmark_promotion,benchmark_promotion,exact-GR benchmark,blocked by missing primitive,all upstream derivation burdens,accept,fail,research_control/program_state.yaml,2026-06-28T00:00:00Z,fixture,blocked,upstream_burdens_missing,no_exact_gr_benchmark_promotion,none,no_benchmark_promotion;no_benchmark_gate_chair_closure;no_completed_derivation",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def test_render_payload_contains_authoritative_state_and_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            payload, markdown = self.renderer.render_payload(root)

            self.assertEqual(payload["active_task_id"], "RT-TEST")
            self.assertEqual(payload["latest_handoff_id"], "handoff-0001")
            self.assertTrue(payload["snapshot_only_not_authority"])
            self.assertFalse(payload["physics_claim_authority"])
            self.assertEqual(payload["status_alias_row_count"], 2)
            self.assertEqual(
                payload["status_alias_integration"],
                "reader_facing_status_column",
            )
            self.assertIn(
                "research_control/design/distance_to_gr_status_aliases.yaml",
                payload["source_paths"],
            )
            self.assertEqual(
                payload["layered_status_fields"],
                [
                    "control_status",
                    "mathematical_status",
                    "physical_status",
                    "promotion_status",
                    "overread_guard",
                ],
            )
            self.assertIn("generated synchronized snapshot only", markdown)
            self.assertIn("no `MetricData(E)` adoption", markdown)
            self.assertIn("Layered Distance-To-GR Boundary Notes", markdown)
            self.assertIn("| Burden ID | Milestone | Reader-facing status | Legacy status | Control status | Mathematical status | Physical status | Promotion status | Overread guard | Last evidence |", markdown)
            self.assertIn("Scoped-Positive Alias Pilot", markdown)
            self.assertIn("accepted only as scoped source-extension evidence/precondition", markdown)
            self.assertIn("PositiveMSProfile_v1", markdown)
            self.assertIn("RR_ETransportCompletenessOrInvarianceLaw_v1", markdown)
            self.assertIn("accepted_as_scoped_evidence_precondition", markdown)
            self.assertIn("not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics", markdown)
            self.assertIn("no_matter_coupling_derivation", markdown)
            self.assertIn("not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations", markdown)
            self.assertIn("no_unscoped_geff_adoption", markdown)
            self.assertIn("no_field_equation_derivation", markdown)
            self.assertIn("no_exact_gr_benchmark_promotion", markdown)

    def test_cli_write_then_check_passes_and_stale_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)

            with redirect_stdout(StringIO()):
                self.assertEqual(
                    self.renderer.main(["--repo-root", root.as_posix(), "--write"]),
                    0,
                )
            with redirect_stdout(StringIO()):
                self.assertEqual(
                    self.renderer.main(["--repo-root", root.as_posix(), "--check"]),
                    0,
                )

            frontier = root / "research_control" / "current_frontier.md"
            frontier.write_text(frontier.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertEqual(
                    self.renderer.main(["--repo-root", root.as_posix(), "--check"]),
                    1,
                )

    def test_cli_json_emits_machine_readable_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(
                    self.renderer.main(["--repo-root", root.as_posix(), "--json"]),
                    0,
                )

            payload = json.loads(output.getvalue())
            self.assertEqual(payload["schema_id"], "current_frontier_state_v1")
            self.assertEqual(payload["status"], "rendered")
            self.assertEqual(payload["distance_to_gr_row_count"], 4)
            self.assertIn("overread_guard", payload["layered_status_fields"])


if __name__ == "__main__":
    unittest.main()
