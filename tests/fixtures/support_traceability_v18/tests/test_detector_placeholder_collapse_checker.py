from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT
    / "scripts"
    / "research_control"
    / "support_formalization"
    / "detector_placeholder_collapse_checker.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "detector_placeholder_collapse_checker", SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DetectorPlaceholderCollapseCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = load_module()

    def test_report_covers_required_semantic_states_and_boundary(self) -> None:
        report = self.checker.generate_report()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["case_count"], len(self.checker.CASES))
        self.assertTrue(report["support_only"])
        self.assertFalse(report["proof_authority"])
        self.assertFalse(report["physics_promotion_authorized"])
        self.assertFalse(report["validator_behavior_changed"])
        self.assertGreaterEqual(report["semantic_state_counts"]["explicit_placeholder_block"], 1)
        self.assertGreaterEqual(
            report["semantic_state_counts"]["draft_control_source_readout_candidate"],
            1,
        )
        self.assertGreaterEqual(report["semantic_state_counts"]["adopted_detector_semantics"], 1)

    def test_explicit_placeholder_block_passes_without_adoption(self) -> None:
        result = self.checker.check_record(
            {
                "case_id": "safe_placeholder",
                "semantic_state": "explicit_placeholder_block",
                "text": "DetPlaceholder(E_*) = missing_and_blocked; not detector semantics.",
                "authority_flags": {
                    "detector_semantics_adopted": False,
                    "det_src_adopted": False,
                },
            }
        )
        self.assertEqual(result["semantic_state"], "explicit_placeholder_block")
        self.assertEqual(result["observed_status"], "pass")
        self.assertIn("pass_placeholder_block_preserved", result["observed_status_codes"])

    def test_draft_source_readout_candidate_passes_without_adoption(self) -> None:
        result = self.checker.check_record(
            {
                "case_id": "safe_candidate",
                "semantic_state": "draft_control_source_readout_candidate",
                "text": (
                    "SourceReadoutCandidate_EStar_v1 remains draft_control_candidate; "
                    "Det_src and Readout_src are not detector-semantics adoption."
                ),
                "authority_flags": {
                    "detector_semantics_adopted": False,
                    "det_src_adopted": False,
                    "readout_src_adopted": False,
                },
            }
        )
        self.assertEqual(result["semantic_state"], "draft_control_source_readout_candidate")
        self.assertEqual(result["observed_status"], "pass")
        self.assertIn(
            "pass_draft_control_candidate_preserved",
            result["observed_status_codes"],
        )

    def test_placeholder_and_candidate_overreads_fail_closed(self) -> None:
        report = self.checker.generate_report()
        by_id = {result["case_id"]: result for result in report["case_results"]}
        placeholder = by_id["placeholder_as_adopted_detector_semantics"]
        candidate = by_id["source_readout_candidate_as_detector_semantics"]
        self.assertEqual(placeholder["observed_status"], "fail")
        self.assertIn(
            "fail_placeholder_as_detector_semantics_collapse",
            placeholder["observed_status_codes"],
        )
        self.assertEqual(candidate["observed_status"], "fail")
        self.assertIn(
            "fail_candidate_as_detector_semantics_collapse",
            candidate["observed_status_codes"],
        )
        self.assertIn("fail_matter_coupling_overread", candidate["observed_status_codes"])

    def test_adopted_detector_semantics_state_is_distinguished_as_protected_failure(self) -> None:
        result = self.checker.check_record(
            {
                "case_id": "unprotected_adoption",
                "semantic_state": "adopted_detector_semantics",
                "text": "adopted detector semantics",
                "authority_flags": {"detector_semantics_adopted": True},
            }
        )
        self.assertEqual(result["semantic_state"], "adopted_detector_semantics")
        self.assertEqual(result["observed_status"], "fail")
        self.assertIn(
            "fail_unprotected_adopted_detector_semantics",
            result["observed_status_codes"],
        )

    def test_cli_json_output_is_deterministic(self) -> None:
        command = [sys.executable, str(SCRIPT_PATH), "--case", "all", "--json"]
        first = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        second = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        parsed = json.loads(first.stdout)
        self.assertEqual(parsed["checker_id"], "detector_placeholder_collapse_checker")
        self.assertEqual(parsed["status"], "PASS")
        self.assertFalse(parsed["proof_authority"])

    def test_cli_record_mode_fails_for_unledgered_adoption_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            record_path = Path(temp_dir) / "bad_record.json"
            record_path.write_text(
                json.dumps(
                    {
                        "case_id": "bad_record",
                        "semantic_state": "draft_control_source_readout_candidate",
                        "text": "SourceReadoutCandidate_EStar_v1 proves detector semantics.",
                        "authority_flags": {"detector_semantics_adopted": False},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            proc = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--record", str(record_path), "--json"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
            )
        self.assertEqual(proc.returncode, 1)
        parsed = json.loads(proc.stdout)
        self.assertEqual(parsed["status"], "FAIL")
        self.assertIn(
            "fail_candidate_as_detector_semantics_collapse",
            parsed["file_result"]["observed_status_codes"],
        )

    def test_markdown_report_contains_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.md"
            subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--markdown", str(report_path)],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            text = report_path.read_text(encoding="utf-8")
        self.assertIn(self.checker.BOUNDARY_STATEMENT, text)
        self.assertIn("source_readout_candidate_as_detector_semantics", text)


if __name__ == "__main__":
    unittest.main()
