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
RENDER_TEST_PATH = REPO_ROOT / "tests" / "test_render_compact_current_frontier_v16.py"


def load_script(name: str, path: Path):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_validator():
    return load_script(
        "validate_compact_current_frontier_v16",
        SCRIPT_DIR / "validate_compact_current_frontier_v16.py",
    )


def load_renderer():
    return load_script(
        "render_compact_current_frontier_v16",
        SCRIPT_DIR / "render_compact_current_frontier_v16.py",
    )


def make_fixture_repo(root: Path) -> None:
    fixture_module = load_script("render_compact_frontier_fixture_module", RENDER_TEST_PATH)
    fixture_module.RenderCompactCurrentFrontierV16Tests().make_fixture_repo(root)


def error_ids(report: dict) -> set[str]:
    return {error["id"] for error in report["errors"]}


class ValidateCompactCurrentFrontierV16Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = load_validator()
        self.renderer = load_renderer()

    def write_fixture_outputs(self, root: Path) -> None:
        make_fixture_repo(root)
        with redirect_stdout(StringIO()):
            self.assertEqual(self.renderer.main(["--repo-root", root.as_posix(), "--write"]), 0)

    def test_fresh_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture_outputs(root)

            report = self.validator.build_report(root)

            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["errors"], [])
            self.assertIn("active_task_mismatch", report["checked_failure_modes"])
            self.assertTrue(report["operational_receipt_only"])
            self.assertFalse(report["physics_proof_authority"])

    def test_active_task_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture_outputs(root)
            json_path = root / "output" / "compact_current_frontier_v16.json"
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            payload["active_state"]["active_task_id"] = "RT-STALE"
            json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            report = self.validator.build_report(root)

            ids = error_ids(report)
            self.assertEqual(report["status"], "FAIL")
            self.assertIn("active_task_mismatch", ids)
            self.assertIn("json_live_mismatch", ids)

    def test_missing_high_risk_row_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture_outputs(root)
            json_path = root / "output" / "compact_current_frontier_v16.json"
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            payload["distance_to_gr"]["high_risk_rows"] = [
                row
                for row in payload["distance_to_gr"]["high_risk_rows"]
                if row["burden_id"] != "matter_coupling"
            ]
            json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            report = self.validator.build_report(root)

            self.assertIn("high_risk_row_missing:matter_coupling", error_ids(report))

    def test_missing_status_card_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture_outputs(root)
            json_path = root / "output" / "compact_current_frontier_v16.json"
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            payload["high_risk_status_cards"] = [
                card
                for card in payload["high_risk_status_cards"]
                if card["object_id"] != "matter_coupling"
            ]
            for row in payload["distance_to_gr"]["high_risk_rows"]:
                if row["burden_id"] == "matter_coupling":
                    row.pop("high_risk_status_card", None)
            json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            report = self.validator.build_report(root)

            ids = error_ids(report)
            self.assertIn("high_risk_status_card_missing:matter_coupling", ids)
            self.assertIn("high_risk_status_card_missing:matter_coupling:nested", ids)

    def test_missing_status_card_next_burden_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture_outputs(root)
            json_path = root / "output" / "compact_current_frontier_v16.json"
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            for card in payload["high_risk_status_cards"]:
                if card["object_id"] == "matter_coupling":
                    card["next_burden"] = ""
            for row in payload["distance_to_gr"]["high_risk_rows"]:
                card = row.get("high_risk_status_card", {})
                if card.get("object_id") == "matter_coupling":
                    card["next_burden"] = ""
            json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            report = self.validator.build_report(root)

            self.assertIn(
                "high_risk_status_card_incomplete:matter_coupling:next_burden",
                error_ids(report),
            )

    def test_missing_metric_use_ledger_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture_outputs(root)
            json_path = root / "output" / "compact_current_frontier_v16.json"
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            payload.pop("metric_use_ledger", None)
            json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            report = self.validator.build_report(root)

            self.assertIn("metric_use_ledger_missing", error_ids(report))

    def test_overpromoted_einstein_equations_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture_outputs(root)
            json_path = root / "output" / "compact_current_frontier_v16.json"
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            for row in payload["distance_to_gr"]["high_risk_rows"]:
                if row["burden_id"] == "einstein_equations":
                    row["control_status"] = "derived"
                    row["reader_facing_status"] = "derived"
                    break
            json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            report = self.validator.build_report(root)

            self.assertIn("einstein_equations_overpromoted", error_ids(report))


if __name__ == "__main__":
    unittest.main()
