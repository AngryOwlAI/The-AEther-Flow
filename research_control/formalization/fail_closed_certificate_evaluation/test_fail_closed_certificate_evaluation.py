from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("fail_closed_certificate_evaluation.py")
SPEC = importlib.util.spec_from_file_location("fail_closed_certificate_evaluation", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)

REPO_ROOT = Path(__file__).resolve().parents[3]


class FailClosedCertificateEvaluationTests(unittest.TestCase):
    def test_positive_source_certificate_allows_declared_equivalence_support_only(self) -> None:
        result = module.evaluate_certificate(module.positive_record())
        self.assertTrue(result.is_valid)
        self.assertFalse(result.fail_closed)
        self.assertEqual(result.outcome, module.EvaluationOutcome.ALLOWED)
        self.assertEqual(result.evaluation_kind, module.EvaluationKind.VALID_DECLARED_SCOPE)
        self.assertTrue(result.support_only)
        self.assertFalse(result.proof_authority)
        self.assertFalse(result.physics_promotion_authorized)

    def test_missing_certificate_fails_closed(self) -> None:
        record = module._replace(
            module.positive_record(),
            record_id="missing",
            status=module.CertificateStatus.MISSING,
            witness_map=None,
        )
        result = module.evaluate_certificate(record)
        self.assertFalse(result.is_valid)
        self.assertTrue(result.fail_closed)
        self.assertEqual(result.outcome, module.EvaluationOutcome.BLOCKED)
        self.assertEqual(result.evaluation_kind, module.EvaluationKind.MISSING_CERTIFICATE)

    def test_malformed_witness_fails_closed(self) -> None:
        record = module._replace(
            module.positive_record(),
            record_id="malformed",
            witness_map={"A0": "B0", "A1": "B9"},
        )
        result = module.evaluate_certificate(record)
        self.assertEqual(result.evaluation_kind, module.EvaluationKind.DOMAIN_CODOMAIN_MISMATCH)
        self.assertTrue(result.fail_closed)

    def test_target_detector_and_downstream_imports_fail_closed(self) -> None:
        cases = (
            ("target", {"target_metric_import": True}, module.EvaluationKind.TARGET_IMPORT),
            (
                "detector",
                {"detector_semantics_import": True},
                module.EvaluationKind.DETECTOR_SEMANTICS_IMPORT,
            ),
            (
                "stress",
                {"stress_energy_import": True},
                module.EvaluationKind.STRESS_ENERGY_IMPORT,
            ),
            (
                "matter-action",
                {"matter_action_import": True},
                module.EvaluationKind.MATTER_ACTION_IMPORT,
            ),
            (
                "benchmark",
                {"benchmark_behavior_import": True},
                module.EvaluationKind.BENCHMARK_BEHAVIOR_IMPORT,
            ),
            ("geff", {"geff_import": True}, module.EvaluationKind.METRICDATA_OR_GEFF_IMPORT),
        )
        for record_id, updates, expected_kind in cases:
            with self.subTest(record_id=record_id):
                record = module._replace(module.positive_record(), record_id=record_id, **updates)
                result = module.evaluate_certificate(record)
                self.assertEqual(result.evaluation_kind, expected_kind)
                self.assertTrue(result.fail_closed)
                self.assertEqual(result.outcome, module.EvaluationOutcome.BLOCKED)

    def test_process_generated_and_scoped_evidence_do_not_fill_certificate_slot(self) -> None:
        cases = (
            (
                {"process_authority_import": True},
                module.EvaluationKind.PROCESS_AUTHORITY_IMPORT,
            ),
            (
                {"validator_status_import": True},
                module.EvaluationKind.GENERATED_OR_REGISTRY_AUTHORITY_IMPORT,
            ),
            (
                {"scoped_evidence_used_as_certificate": True},
                module.EvaluationKind.SCOPED_EVIDENCE_NOT_CERTIFICATE,
            ),
        )
        for updates, expected_kind in cases:
            with self.subTest(expected_kind=expected_kind):
                record = module._replace(module.positive_record(), record_id=expected_kind.value, **updates)
                result = module.evaluate_certificate(record)
                self.assertEqual(result.evaluation_kind, expected_kind)
                self.assertTrue(result.fail_closed)

    def test_report_is_support_only_and_blocks_authority_overread(self) -> None:
        report = module.run_formalization().to_dict()
        self.assertEqual(report["status"], "pass_support_only")
        self.assertEqual(report["checker_id"], module.CHECKER_ID)
        self.assertTrue(report["support_only"])
        self.assertFalse(report["proof_authority"])
        self.assertFalse(report["physics_promotion_authorized"])
        self.assertEqual(report["proof_normal_form_row_id"], module.PROOF_NORMAL_FORM_ROW_ID)
        self.assertFalse(any(report["forbidden_authority_flags"].values()))
        self.assertIn("proof_authority=false", report["boundary_statement"])

    def test_cli_json_output_is_deterministic(self) -> None:
        command = [sys.executable, str(MODULE_PATH), "--json"]
        first = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        second = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        parsed = json.loads(first.stdout)
        self.assertEqual(parsed["status"], "pass_support_only")
        self.assertEqual(parsed["result_count"], 12)

    def test_cli_json_output_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "validation_report.json"
            subprocess.run(
                [
                    sys.executable,
                    str(MODULE_PATH),
                    "--json-output",
                    str(report_path),
                    "--json",
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            parsed = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(parsed["checker_id"], module.CHECKER_ID)
        self.assertEqual(parsed["status"], "pass_support_only")

    def test_source_artifact_hash_matches_registry_value(self) -> None:
        self.assertEqual(module.source_artifact_sha256(REPO_ROOT), module.SOURCE_ARTIFACT_HASH)


if __name__ == "__main__":
    unittest.main()
