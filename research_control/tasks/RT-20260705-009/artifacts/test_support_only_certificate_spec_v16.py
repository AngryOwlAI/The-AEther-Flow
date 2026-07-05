import importlib.util
import pathlib
import sys
import unittest


MODULE_PATH = pathlib.Path(__file__).with_name("support_only_certificate_spec_v16.py")
SPEC = importlib.util.spec_from_file_location("support_only_certificate_spec_v16", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class SupportOnlyCertificateSpecTests(unittest.TestCase):
    def positive_record(self):
        return module.CertificateRecord(
            certificate_instance_id="SCI-TRANSPORT-001",
            instance_kind=module.InstanceKind.VALID_TRANSPORT,
            domain=("A0", "A1", "A2"),
            codomain=("B0", "B1", "B2"),
            certificate_payload={"A0": "B0", "A1": "B1", "A2": "B2"},
            no_target_import_guard=module.NoTargetImportGuard(module.NoTargetGuardResult.PASS),
            status=module.CertificateStatus.VALID,
            expected_equivalence_result=module.ExpectedEquivalenceResult.ALLOWED,
            rr_e_separation_effect=module.RRESeparationEffect.NOT_APPLICABLE,
            fail_closed_reason=None,
            source_paths=(
                "research_control/tasks/RT-20260704-026/artifacts/finite_local_transport_certificate_instance_v1.tex",
            ),
            forbidden_overreads=("matter coupling", "Einstein equations", "benchmark promotion"),
        )

    def test_positive_transport_record_allows_declared_equivalence_support_only(self):
        result = module.evaluate_certificate(self.positive_record())
        self.assertTrue(result.is_valid)
        self.assertFalse(result.fail_closed)
        self.assertEqual(result.evaluation_kind, module.EvaluationKind.VALID)
        self.assertEqual(result.expected_equivalence_result, module.ExpectedEquivalenceResult.ALLOWED)
        self.assertTrue(result.support_only)
        self.assertFalse(result.proof_authority)
        self.assertFalse(result.physics_promotion_authorized)

    def test_missing_certificate_fails_closed(self):
        record = self.positive_record()
        missing = module.CertificateRecord(
            **{
                **record.__dict__,
                "certificate_instance_id": "SCI-NEG-MISSING-001",
                "instance_kind": module.InstanceKind.MISSING_NEGATIVE,
                "certificate_payload": None,
                "status": module.CertificateStatus.MISSING,
                "expected_equivalence_result": module.ExpectedEquivalenceResult.BLOCKED,
                "fail_closed_reason": "No source transport certificate payload is present.",
            }
        )
        result = module.evaluate_certificate(missing)
        self.assertFalse(result.is_valid)
        self.assertTrue(result.fail_closed)
        self.assertEqual(result.evaluation_kind, module.EvaluationKind.MISSING)
        self.assertEqual(result.expected_equivalence_result, module.ExpectedEquivalenceResult.BLOCKED)

    def test_malformed_domain_codomain_mismatch_fails_closed(self):
        record = self.positive_record()
        malformed = module.CertificateRecord(
            **{
                **record.__dict__,
                "certificate_instance_id": "SCI-NEG-MALFORMED-001",
                "instance_kind": module.InstanceKind.MALFORMED_NEGATIVE,
                "certificate_payload": {"A0": "B0", "A1": "B9", "A2": "B2"},
                "status": module.CertificateStatus.VALID,
                "expected_equivalence_result": module.ExpectedEquivalenceResult.BLOCKED,
                "fail_closed_reason": "The candidate map leaves the declared codomain.",
            }
        )
        result = module.evaluate_certificate(malformed)
        self.assertFalse(result.is_valid)
        self.assertTrue(result.fail_closed)
        self.assertEqual(result.evaluation_kind, module.EvaluationKind.DOMAIN_CODOMAIN_MISMATCH)

    def test_target_import_is_rejected(self):
        record = self.positive_record()
        target_import = module.CertificateRecord(
            **{
                **record.__dict__,
                "certificate_instance_id": "SCI-NEG-TARGET-METRIC-001",
                "instance_kind": module.InstanceKind.TARGET_IMPORT_REJECTED,
                "status": module.CertificateStatus.REJECTED_TARGET_IMPORT,
                "target_import_used": True,
                "expected_equivalence_result": module.ExpectedEquivalenceResult.BLOCKED,
                "fail_closed_reason": "Target metric import used as witness.",
            }
        )
        result = module.evaluate_certificate(target_import)
        self.assertEqual(result.evaluation_kind, module.EvaluationKind.TARGET_IMPORT)
        self.assertEqual(result.expected_equivalence_result, module.ExpectedEquivalenceResult.BLOCKED)

    def test_process_authority_is_rejected(self):
        record = self.positive_record()
        process_authority = module.CertificateRecord(
            **{
                **record.__dict__,
                "certificate_instance_id": "SCI-NEG-VALIDATOR-PASS-001",
                "instance_kind": module.InstanceKind.PROCESS_AUTHORITY_REJECTED,
                "status": module.CertificateStatus.REJECTED_PROCESS_AUTHORITY,
                "process_authority_used": True,
                "expected_equivalence_result": module.ExpectedEquivalenceResult.BLOCKED,
                "fail_closed_reason": "Validator PASS is process state, not certificate payload.",
            }
        )
        result = module.evaluate_certificate(process_authority)
        self.assertEqual(result.evaluation_kind, module.EvaluationKind.PROCESS_AUTHORITY)
        self.assertTrue(result.fail_closed)

    def test_scoped_evidence_does_not_fill_certificate_slot(self):
        record = self.positive_record()
        scoped_evidence = module.CertificateRecord(
            **{
                **record.__dict__,
                "certificate_instance_id": "SCI-NEG-SCOPED-EVIDENCE-001",
                "instance_kind": module.InstanceKind.PROCESS_AUTHORITY_REJECTED,
                "status": module.CertificateStatus.FAIL_CLOSED,
                "scoped_evidence_used": True,
                "expected_equivalence_result": module.ExpectedEquivalenceResult.BLOCKED,
                "fail_closed_reason": "Scoped evidence cannot be converted into source-law adoption.",
            }
        )
        result = module.evaluate_certificate(scoped_evidence)
        self.assertEqual(result.evaluation_kind, module.EvaluationKind.SCOPED_EVIDENCE_NOT_CERTIFICATE)
        self.assertTrue(result.fail_closed)


if __name__ == "__main__":
    unittest.main()
