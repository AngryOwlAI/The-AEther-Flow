from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-009/artifacts/proof_build_adapter.py"
)
FIXTURE_PATH = (
    REPO_ROOT
    / "research_control/tasks/RT-20260722-009/artifacts/proof_evidence_fixtures.json"
)


def _load_adapter():
    spec = importlib.util.spec_from_file_location("proof_build_adapter", ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load proof-build adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProofEvidenceRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.adapter = _load_adapter()
        cls.suite = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def _case_record(self, case_id: str):
        case = next(item for item in self.suite["cases"] if item["case_id"] == case_id)
        return self.adapter.apply_mutations(self.suite["base_record"], case["mutations"]), case

    def test_live_p2_migration_record_passes(self) -> None:
        record, case = self._case_record("p2_t05_migration_pass")
        result = self.adapter.validate_record(record, verify_live_files=True)
        self.assertEqual(case["expected_status"], result["status"])
        self.assertEqual([], result["issues"])

    def test_declared_allowed_axiom_is_visible_warning(self) -> None:
        record, case = self._case_record("declared_axiom_warning")
        result = self.adapter.validate_record(record, verify_live_files=False)
        self.assertEqual(case["expected_status"], result["status"])
        self.assertEqual(1, result["warning_count"])

    def test_source_hash_drift_fails_closed(self) -> None:
        record, _ = self._case_record("source_hash_mismatch_fails")
        result = self.adapter.validate_record(record, verify_live_files=True)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        self.assertIn("live_source_hash", {item["check_id"] for item in result["issues"]})

    def test_missing_trust_metadata_fails_closed(self) -> None:
        record, _ = self._case_record("missing_trust_metadata_fails")
        result = self.adapter.validate_record(record, verify_live_files=False)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        self.assertIn("trust_fields", {item["check_id"] for item in result["issues"]})

    def test_undeclared_axiom_fails_closed(self) -> None:
        record, _ = self._case_record("undeclared_axiom_fails")
        result = self.adapter.validate_record(record, verify_live_files=False)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        self.assertIn("undeclared_axiom", {item["check_id"] for item in result["issues"]})

    def test_formal_gap_fails_closed(self) -> None:
        record, _ = self._case_record("formal_gap_fails")
        result = self.adapter.validate_record(record, verify_live_files=False)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        self.assertIn("untrusted_formal_gap", {item["check_id"] for item in result["issues"]})

    def test_reproducibility_requires_two_clean_builds(self) -> None:
        record, _ = self._case_record("single_build_reproducibility_claim_fails")
        result = self.adapter.validate_record(record, verify_live_files=False)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        self.assertIn("reproducible_build_count", {item["check_id"] for item in result["issues"]})

    def test_proof_object_hashes_must_agree(self) -> None:
        record, _ = self._case_record("proof_object_hash_disagreement_fails")
        result = self.adapter.validate_record(record, verify_live_files=False)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        self.assertIn("proof_object_hash_parity", {item["check_id"] for item in result["issues"]})

    def test_protected_authority_is_never_inferred(self) -> None:
        record, _ = self._case_record("proof_authority_promotion_fails")
        result = self.adapter.validate_record(record, verify_live_files=False)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        checks = {item["check_id"] for item in result["issues"]}
        self.assertIn("claim_boundary_false", checks)
        self.assertIn("authorization_false", checks)

    def test_generated_source_path_is_rejected(self) -> None:
        record, _ = self._case_record("generated_source_path_fails")
        result = self.adapter.validate_record(record, verify_live_files=True)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        self.assertIn("canonical_source_path", {item["check_id"] for item in result["issues"]})

    def test_release_commit_must_match_build_receipt(self) -> None:
        record, _ = self._case_record("release_commit_receipt_mismatch_fails")
        result = self.adapter.validate_record(record, verify_live_files=True)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        self.assertIn(
            "validation_receipt_toolchain_identity",
            {item["check_id"] for item in result["issues"]},
        )

    def test_trust_report_count_must_match_build_receipt(self) -> None:
        record, _ = self._case_record("trust_receipt_count_mismatch_fails")
        result = self.adapter.validate_record(record, verify_live_files=True)
        self.assertEqual(self.adapter.FAIL_STATUS, result["status"])
        self.assertIn(
            "validation_receipt_axiom_report_count",
            {item["check_id"] for item in result["issues"]},
        )

    def test_fixture_report_matches_every_expected_status(self) -> None:
        report = self.adapter.build_report(FIXTURE_PATH)
        self.assertEqual("PASS", report["status"])
        self.assertEqual(12, report["fixture_count"])
        self.assertEqual(0, report["unexpected_fixture_result_count"])
        self.assertTrue(report["formal_failure_visible"])
        self.assertTrue(report["formal_assumption_warning_visible"])
        self.assertFalse(report["proof_authority"])

    def test_write_then_check_is_byte_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            report_path = Path(temporary_directory) / "report.json"
            compact_path = Path(temporary_directory) / "compact.json"
            write_code = self.adapter.main(
                [
                    "--write",
                    "--fixtures",
                    str(FIXTURE_PATH),
                    "--report",
                    str(report_path),
                    "--compact",
                    str(compact_path),
                ]
            )
            check_code = self.adapter.main(
                [
                    "--check",
                    "--fixtures",
                    str(FIXTURE_PATH),
                    "--report",
                    str(report_path),
                    "--compact",
                    str(compact_path),
                ]
            )
            self.assertEqual(0, write_code)
            self.assertEqual(0, check_code)


if __name__ == "__main__":
    unittest.main()
