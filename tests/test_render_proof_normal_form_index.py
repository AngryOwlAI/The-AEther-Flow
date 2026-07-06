from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.research_control import render_proof_normal_form_index as renderer


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "research_control" / "render_proof_normal_form_index.py"


class ProofNormalFormIndexRendererTests(unittest.TestCase):
    def test_snapshot_preserves_non_authority_boundary(self) -> None:
        snapshot = renderer.build_snapshot()

        self.assertEqual(snapshot["schema_id"], renderer.SCHEMA_ID)
        self.assertFalse(snapshot["authority_boundary"]["proof_authority"])
        self.assertFalse(snapshot["authority_boundary"]["physics_promotion_authorized"])
        self.assertTrue(snapshot["authority_boundary"]["source_artifacts_remain_authority"])
        self.assertEqual(snapshot["summary"]["row_count"], 7)
        self.assertEqual(snapshot["summary"]["scientific_gate_row_count"], 3)

    def test_high_risk_rows_keep_non_conclusions(self) -> None:
        snapshot = renderer.build_snapshot()
        high_risk_rows = [row for row in snapshot["rows"] if row["high_risk"]]

        self.assertGreaterEqual(len(high_risk_rows), 1)
        for row in high_risk_rows:
            self.assertTrue(row["non_conclusions"], row["proof_normal_form_row_id"])

    def test_cli_write_and_check_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = Path(tmpdir) / "proof_normal_form_index.json"
            markdown_path = Path(tmpdir) / "proof_normal_form_index.md"

            write_result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--json",
                    str(json_path),
                    "--markdown",
                    str(markdown_path),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(write_result.returncode, 0, write_result.stderr)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["summary"]["row_count"], 7)
            self.assertIn("Proof Normal Form Index", markdown_path.read_text(encoding="utf-8"))

            check_result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--json",
                    str(json_path),
                    "--markdown",
                    str(markdown_path),
                    "--check",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(check_result.returncode, 0, check_result.stderr)
            report = json.loads(check_result.stdout)
            self.assertEqual(report["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
