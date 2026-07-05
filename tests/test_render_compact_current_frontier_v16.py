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
        "render_compact_current_frontier_v16",
        SCRIPT_DIR / "render_compact_current_frontier_v16.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RenderCompactCurrentFrontierV16Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.renderer = load_module()

    def make_fixture_repo(self, root: Path) -> None:
        control = root / "research_control"
        handoffs = control / "handoffs"
        registries = root / "registries"
        control.mkdir(parents=True)
        handoffs.mkdir(parents=True)
        registries.mkdir(parents=True)
        (control / "program_state.yaml").write_text(
            "\n".join(
                [
                    'mode: "director_led_research_control"',
                    'active_task_id: "RT-COMPACT"',
                    'latest_handoff_id: "handoff-compact"',
                    'current_status: "v16_compact_fixture_completed_no_physics_delta"',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (handoffs / "handoff-compact.yaml").write_text(
            "\n".join(
                [
                    'handoff_id: "handoff-compact"',
                    'task_id: "RT-COMPACT"',
                    'status: "completed"',
                    'summary: "Fixture completed v16 compact renderer packet."',
                    "selected_next_route:",
                    '  route_id: "compact_current_frontier_check_integration_v16"',
                    '  plan_task_id: "P15-T03"',
                    '  role_family: "validator-engineer@0.2.0"',
                    '  target_derivation_milestone: "matter_coupling"',
                    '  milestone_burden: "Integrate compact frontier synchronization check."',
                    "  requires_human_gate: false",
                    "hard_blocks:",
                    '  - "source-law adoption"',
                    '  - "matter-coupling derivation or adoption"',
                    "validation_summary:",
                    '  task_local_validator_status: "PASS"',
                    "distance_to_gr:",
                    '  effect: "no_distance_delta"',
                    '  milestone: "matter_coupling"',
                    '  burden_id: "none"',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (control / "current_frontier.md").write_text(
            "\n".join(
                [
                    "# Current Research Frontier",
                    "| Burden ID | Milestone | Reader-facing status | Legacy status | Control status | Mathematical status | Physical status | Promotion status | Overread guard | Last evidence |",
                    "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                    "| `m_src` | `source_manifold_m_src` | adopted only as scoped source-only M_src object | accepted | gate_review_completed | scoped_source_only_adopted_object | not_target_manifold_not_metric_not_gr_derivation | scoped_source_object_only | no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |",
                    "| `g_eff` | `effective_metric_g_eff` | adopted only as scoped source-extension g_eff object | accepted | gate_review_completed | scoped_source_extension_geff_object | not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations | scoped_source_object_only | no_unscoped_geff_adoption<br>no_matter_coupling_derivation<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |",
                    "| `matter_coupling` | `matter_coupling` | accepted only as scoped source-extension evidence/precondition | accepted | accepted_as_scoped_evidence_precondition | parameterized_finite_local_witness_precondition | not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics | scoped_source_evidence_only | no_source_law_adoption<br>no_coupling_law_adoption<br>no_matter_coupling_derivation<br>no_stress_energy_semantics<br>no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |",
                    "| `einstein_equations` | `einstein_equations` | not started; no positive derivation status | not started | not_started | dynamics_action_or_variation_missing | no_field_equation_derivation | none | no_einstein_equations<br>no_benchmark_promotion<br>no_completed_derivation | `research_control/program_state.yaml` |",
                    "| `benchmark_promotion` | `benchmark_promotion` | no benchmark promotion from scoped evidence/precondition alone | blocked by missing primitive | blocked | upstream_burdens_missing | no_exact_gr_benchmark_promotion | none | no_benchmark_promotion<br>no_benchmark_gate_chair_closure<br>no_completed_derivation | `research_control/program_state.yaml` |",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (registries / "DISTANCE_TO_GR_LEDGER.csv").write_text(
            "\n".join(
                [
                    "burden_id,milestone,required_object,current_status,blocking_burden,accept_criteria,failure_or_freeze_criteria,last_evidence_path,updated_at,notes,control_status,mathematical_status,physical_status,promotion_status,overread_guard",
                    "m_src,source_manifold_m_src,M_src,accepted,scoped source-only object,accept,freeze,research_control/program_state.yaml,2026-07-05T00:00:00Z,fixture,gate_review_completed,scoped_source_only_adopted_object,not_target_manifold_not_metric_not_gr_derivation,scoped_source_object_only,no_matter_coupling_derivation;no_einstein_equations;no_benchmark_promotion;no_completed_derivation",
                    "g_eff,effective_metric_g_eff,g_eff,accepted,scoped source-extension object,accept,freeze,research_control/program_state.yaml,2026-07-05T00:00:00Z,fixture,gate_review_completed,scoped_source_extension_geff_object,not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations,scoped_source_object_only,no_unscoped_geff_adoption;no_matter_coupling_derivation;no_einstein_equations;no_benchmark_promotion;no_completed_derivation",
                    "matter_coupling,matter_coupling,universal coupling,accepted,source evidence only,accept,freeze,research_control/program_state.yaml,2026-07-05T00:00:00Z,fixture,accepted_as_scoped_evidence_precondition,parameterized_finite_local_witness_precondition,not_matter_coupling_not_stress_energy_not_matter_action_not_detector_semantics,scoped_source_evidence_only,no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_stress_energy_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation",
                    "einstein_equations,einstein_equations,field equations,not started,dynamics action or variation,accept,freeze,research_control/program_state.yaml,2026-07-05T00:00:00Z,fixture,not_started,dynamics_action_or_variation_missing,no_field_equation_derivation,none,no_einstein_equations;no_benchmark_promotion;no_completed_derivation",
                    "benchmark_promotion,benchmark_promotion,exact-GR benchmark,blocked by missing primitive,all upstream derivation burdens,accept,freeze,research_control/program_state.yaml,2026-07-05T00:00:00Z,fixture,blocked,upstream_burdens_missing,no_exact_gr_benchmark_promotion,none,no_benchmark_promotion;no_benchmark_gate_chair_closure;no_completed_derivation",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (registries / "MARKDOWN_SOURCE_REGISTRY.csv").write_text(
            "\n".join(
                [
                    "object_id,path,format,kind,authority_status,owner_skill,audit_status",
                    "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V16,implementations_plans/recommendations_implementation_plan_continue_task-v16.md,markdown,implementation_plan,control,project-control,PASS",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def test_snapshot_has_required_shape_boundaries_and_high_risk_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_fixture_repo(root)
            snapshot = self.renderer.build_snapshot(root)

            self.assertEqual(snapshot["schema_id"], "compact_current_frontier_v16")
            self.assertEqual(snapshot["active_state"]["active_task_id"], "RT-COMPACT")
            self.assertTrue(snapshot["active_state"]["v15_completed"])
            self.assertFalse(snapshot["active_state"]["v16_completed"])
            self.assertTrue(snapshot["active_state"]["v16_plan_registered"])
            self.assertEqual(
                snapshot["next_route"]["route_id"],
                "compact_current_frontier_check_integration_v16",
            )
            self.assertFalse(snapshot["claim_boundary"]["physics_claim_authority"])
            self.assertFalse(snapshot["claim_boundary"]["proof_authority"])
            self.assertIn("completed derivation", snapshot["claim_boundary"]["blocked_claims"])
            rows = snapshot["distance_to_gr"]["high_risk_rows"]
            self.assertEqual(
                {row["burden_id"] for row in rows},
                {"m_src", "g_eff", "matter_coupling", "einstein_equations", "benchmark_promotion"},
            )
            self.assertNotIn(
                "accepted",
                [
                    row["reader_facing_status"]
                    for row in rows
                    if row["burden_id"] in {"m_src", "g_eff", "matter_coupling"}
                ],
            )
            self.assertTrue(snapshot["authority_warning"]["snapshot_only_not_authority"])
            self.assertEqual(self.renderer.validate_snapshot(snapshot), [])

    def test_cli_write_then_check_and_json(self) -> None:
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
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(
                    self.renderer.main(["--repo-root", root.as_posix(), "--json"]),
                    0,
                )
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["schema_id"], "compact_current_frontier_v16")
            self.assertEqual(payload["validation"]["latest_required_status"], "PASS")


if __name__ == "__main__":
    unittest.main()
