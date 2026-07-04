import unittest

from fail_closed_missing_certificate_pilot import (
    OBSTRUCTION_MALFORMED_CERTIFICATE,
    OBSTRUCTION_MISSING_RRE_SEPARATION_DATA,
    OBSTRUCTION_TARGET_IMPORT,
    CertificateSlot,
    CertificateSlotStatus,
    DeclaredRRERecord,
    EvaluationKind,
    EvaluationStatus,
    evaluate_certificate_slot,
    support_only_receipt,
)


class FailClosedMissingCertificatePilotTests(unittest.TestCase):
    def test_valid_certificate_is_local_positive_branch_without_proof_authority(self):
        result = evaluate_certificate_slot(
            CertificateSlot("tau", CertificateSlotStatus.VALID),
            DeclaredRRERecord("RR_E_A", "RR_E_A", declared_separated=False),
        )

        self.assertEqual(result.evaluation, EvaluationStatus.VALID_CERTIFICATE)
        self.assertEqual(result.kind, EvaluationKind.VALID_IDENTIFICATION)
        self.assertTrue(result.positive_identification_derived)
        self.assertFalse(result.proof_authority)
        self.assertTrue(result.support_only)
        self.assertFalse(result.physics_promotion_authorized)

    def test_missing_certificate_preserves_declared_rr_e_separation(self):
        result = evaluate_certificate_slot(
            CertificateSlot("tau", CertificateSlotStatus.MISSING),
            DeclaredRRERecord("RR_E_A", "RR_E_B", declared_separated=True),
        )

        self.assertEqual(result.evaluation, EvaluationStatus.BOTTOM)
        self.assertEqual(
            result.kind,
            EvaluationKind.MISSING_CERTIFICATE_SEPARATION_PRESERVED,
        )
        self.assertFalse(result.positive_identification_derived)
        self.assertTrue(result.preserved_declared_separation)
        self.assertEqual(result.obstruction_id, "")

    def test_missing_certificate_records_obstruction_when_data_are_insufficient(self):
        result = evaluate_certificate_slot(
            CertificateSlot("tau", CertificateSlotStatus.MISSING),
            DeclaredRRERecord("RR_E_A", None, declared_separated=False),
        )

        self.assertEqual(result.evaluation, EvaluationStatus.BOTTOM)
        self.assertEqual(result.kind, EvaluationKind.MISSING_CERTIFICATE_OBSTRUCTION)
        self.assertFalse(result.positive_identification_derived)
        self.assertFalse(result.preserved_declared_separation)
        self.assertEqual(result.obstruction_id, OBSTRUCTION_MISSING_RRE_SEPARATION_DATA)

    def test_malformed_certificate_fails_closed(self):
        result = evaluate_certificate_slot(
            CertificateSlot(
                "tau",
                CertificateSlotStatus.MALFORMED,
                malformed_reason="domain-codomain mismatch",
            ),
            DeclaredRRERecord("RR_E_A", "RR_E_B", declared_separated=True),
        )

        self.assertEqual(result.evaluation, EvaluationStatus.BOTTOM)
        self.assertEqual(result.kind, EvaluationKind.MALFORMED_CERTIFICATE)
        self.assertEqual(result.obstruction_id, OBSTRUCTION_MALFORMED_CERTIFICATE)
        self.assertFalse(result.positive_identification_derived)

    def test_target_importing_certificate_fails_closed(self):
        result = evaluate_certificate_slot(
            CertificateSlot("tau", CertificateSlotStatus.TARGET_IMPORTING),
            DeclaredRRERecord("RR_E_A", "RR_E_B", declared_separated=True),
        )

        self.assertEqual(result.evaluation, EvaluationStatus.BOTTOM)
        self.assertEqual(result.kind, EvaluationKind.TARGET_IMPORTING_CERTIFICATE)
        self.assertEqual(result.obstruction_id, OBSTRUCTION_TARGET_IMPORT)
        self.assertFalse(result.positive_identification_derived)

    def test_support_only_receipt_blocks_physics_promotion(self):
        receipt = support_only_receipt()

        self.assertFalse(receipt["proof_authority"])
        self.assertTrue(receipt["support_only"])
        self.assertFalse(receipt["physics_promotion_authorized"])
        self.assertFalse(receipt["matter_coupling_derived"])
        self.assertFalse(receipt["einstein_equations_derived"])
        self.assertFalse(receipt["completed_derivation_claimed"])


if __name__ == "__main__":
    unittest.main()
