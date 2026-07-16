from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
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


class RouteSignatureExtractorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extractor = load_module("extract_route_signatures", "extract_route_signatures.py")
        cls.validator = sys.modules["validate_route_orbits"]

    def test_recent_matter_coupling_report_uses_v15_schema_and_is_advisory(self) -> None:
        report = self.extractor.build_report(REPO_ROOT, sample="recent-matter-coupling")

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["schema_id"], "route_signature_pilot_report_v1")
        self.assertEqual(report["signature_schema_id"], "route_signature_schema_v1")
        self.assertFalse(report["pilot_blocks_research"])
        self.assertFalse(report["route_orbit_warning_should_emit"])
        self.assertEqual(report["task_count"], 23)
        self.assertEqual(report["route_signature_count"], 23)

        first_signature = report["route_signatures"][0]
        for field in self.extractor.REQUIRED_V15_FIELDS:
            self.assertIn(field, first_signature)

        no_payload_task_ids = {
            task["task_id"] for task in report["no_new_mathematical_payload_tasks"]
        }
        self.assertIn("RT-20260701-010", no_payload_task_ids)
        self.assertIn("RT-20260701-031", no_payload_task_ids)
        self.assertEqual(
            report["suggested_freeze_or_continuation_consequence"],
            "no_freeze_from_pilot_continue_to_p10_t03_freeze_threshold_policy",
        )

    def test_repeated_process_refresh_cycle_emits_advisory_warning(self) -> None:
        base = {
            "signature_schema_id": "route_signature_schema_v1",
            "source_task_id": "RT-SYN-001",
            "source_job_id": "AJ-RT-SYN-001-001",
            "source_completion_path": "",
            "target_derivation_milestone": "matter_coupling",
            "milestone_burden": "synthetic_burden",
            "object_or_claim_name": "SyntheticClaim_v1",
            "route_family": "selector",
            "role_family": "theoretical-continuation-selector",
            "mathematical_payload_class": "route_selector_only",
            "distance_to_gr_delta": {
                "effect": "no_distance_delta",
                "changed": False,
                "burden_id": "",
                "milestone": "",
            },
            "source_extension_classification": "none",
            "obstruction_id": "none",
            "freeze_criteria_status": {
                "evaluated": False,
                "triggered": False,
                "decision": "not_applicable",
                "freeze_scope": "none",
            },
            "next_route_selected": "selector",
            "new_mathematics_signature": False,
            "process_refresh_signature": True,
        }
        second = dict(base)
        second["source_task_id"] = "RT-SYN-002"
        analysis = self.extractor.summarize_route_orbits([base, second])

        self.assertEqual(analysis["repeated_burden_cycle_count"], 1)
        self.assertEqual(analysis["repeated_no_new_payload_cycle_count"], 1)
        self.assertTrue(analysis["route_orbit_warning_should_emit"])
        self.assertEqual(
            analysis["suggested_freeze_or_continuation_consequence"],
            "emit_advisory_route_orbit_warning_and_route_p10_t03_freeze_threshold_review",
        )

    def test_compact_output_preserves_full_receipt_and_task_filter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            receipt_path = Path(temporary_directory) / "route-signatures.json"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = self.extractor.main(
                    [
                        "--repo-root",
                        str(REPO_ROOT),
                        "--task-id",
                        "RT-20260701-010",
                        "--output",
                        str(receipt_path),
                        "--json-summary",
                    ]
                )

            summary = json.loads(stdout.getvalue())
            full_report = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(result, 0)
            self.assertEqual(summary["schema_id"], "validation_console_summary_v1")
            self.assertEqual(summary["diagnostic"]["counts"]["source_tasks"], 1)
            self.assertEqual(full_report["task_count"], 1)
            self.assertEqual(len(full_report["route_signatures"]), 1)
            self.assertFalse(summary["authority_boundary"]["route_freeze_authorized"])
            self.assertFalse(summary["authority_boundary"]["physics_promotion_authorized"])
            common_receipt = json.loads(Path(summary["full_receipt"]).read_text(encoding="utf-8"))
            self.assertEqual(common_receipt["schema_id"], "validation_full_receipt_v1")

            default_stdout = io.StringIO()
            with redirect_stdout(default_stdout):
                default_result = self.extractor.main(
                    ["--repo-root", str(REPO_ROOT), "--task-id", "RT-20260701-010"]
                )
            self.assertEqual(default_result, 0)
            self.assertIn("gate=route_signature_diagnostic", default_stdout.getvalue())
            self.assertIn("guard_action=", default_stdout.getvalue())
            self.assertLess(len(default_stdout.getvalue().encode("utf-8")), 2048)
            self.assertLess(len(default_stdout.getvalue()), len(receipt_path.read_text(encoding="utf-8")))

    def test_route_orbit_full_json_matches_receipt_and_advisory_exit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            input_path = root / "route-history.json"
            output_path = root / "route-orbits.json"
            input_path.write_text(
                json.dumps(
                    {
                        "schema_id": "route_history_extractor_v1",
                        "task_count": 0,
                        "signatures": [],
                        "extraction_errors": ["synthetic extraction failure"],
                    }
                ),
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                result = self.validator.main(
                    [
                        "--repo-root",
                        str(root),
                        "--input",
                        str(input_path),
                        "--output",
                        str(output_path),
                        "--full-json",
                        "--advisory-only",
                    ]
                )

            self.assertEqual(result, 0)
            self.assertEqual(stdout.getvalue(), output_path.read_text(encoding="utf-8"))
            self.assertEqual(json.loads(stdout.getvalue())["status"], "FAIL")
            common_receipts = list(root.glob(".local/validation-receipts/**/full.json"))
            self.assertEqual(len(common_receipts), 1)
            common_receipt = json.loads(common_receipts[0].read_text(encoding="utf-8"))
            self.assertEqual(common_receipt["status"], "FAIL")
            self.assertEqual(common_receipt["exit_code"], 0)
            self.assertEqual(list(root.rglob("*.tmp")), [])

            blocked_stdout = io.StringIO()
            with redirect_stdout(blocked_stdout):
                blocked_result = self.validator.main(
                    ["--repo-root", str(root), "--input", str(input_path), "--output", str(root)]
                )
            self.assertEqual(blocked_result, 2)
            self.assertIn("BLOCKED_CONFIGURATION receipt_write_failed", blocked_stdout.getvalue())
            self.assertEqual(list(root.rglob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
