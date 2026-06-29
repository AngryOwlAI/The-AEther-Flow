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
        handoffs = control / "handoffs"
        task = control / "tasks" / "RT-TEST"
        registries = root / "registries"
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
                    "burden_id,milestone,required_object,current_status,blocking_burden,accept_criteria,failure_or_freeze_criteria,last_evidence_path,updated_at,notes",
                    "matter_coupling,matter_coupling,universal coupling,accepted scoped evidence/precondition only,no coupling adoption,accept,fail,research_control/program_state.yaml,2026-06-28T00:00:00Z,fixture",
                    "einstein_equations,einstein_equations,field equations,not started,dynamics action or variation,accept,fail,research_control/program_state.yaml,2026-06-28T00:00:00Z,fixture",
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
            self.assertIn("generated synchronized snapshot only", markdown)
            self.assertIn("no `MetricData(E)` adoption", markdown)
            self.assertIn("| `matter_coupling` | `matter_coupling` | accepted scoped evidence/precondition only |", markdown)

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
            self.assertEqual(payload["distance_to_gr_row_count"], 2)


if __name__ == "__main__":
    unittest.main()
