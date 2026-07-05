"""Support-only v16 certificate record evaluator.

This task-local module models the P6-T01 selected finite/local certificate
record type and validity predicate. It is executable validation support, not
proof authority for project physics claims.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Optional, Sequence, Tuple


PROOF_AUTHORITY = False
PHYSICS_PROMOTION_AUTHORIZED = False
SUPPORT_ONLY = True
GENERATED_DERIVATIVE_OR_TEST_SUPPORT_ONLY = True


class InstanceKind(str, Enum):
    VALID_TRANSPORT = "valid_transport_certificate"
    VALID_INVARIANCE = "valid_invariance_certificate"
    VALID_FACTORIZATION = "valid_factorization_certificate"
    MISSING_NEGATIVE = "missing_certificate_negative"
    MALFORMED_NEGATIVE = "malformed_certificate_negative"
    TARGET_IMPORT_REJECTED = "target_import_rejected_certificate"
    DETECTOR_SEMANTICS_REJECTED = "detector_semantics_rejected_certificate"
    PROCESS_AUTHORITY_REJECTED = "process_authority_rejected_certificate"


class CertificateStatus(str, Enum):
    VALID = "valid"
    MISSING = "missing"
    MALFORMED = "malformed"
    REJECTED_TARGET_IMPORT = "rejected_target_import"
    REJECTED_DETECTOR_SEMANTICS = "rejected_detector_semantics"
    REJECTED_PROCESS_AUTHORITY = "rejected_process_authority"
    FAIL_CLOSED = "fail_closed"


class ExpectedEquivalenceResult(str, Enum):
    ALLOWED = "declared_equivalence_allowed"
    BLOCKED = "declared_equivalence_blocked"
    NOT_APPLICABLE = "not_applicable"


class RRESeparationEffect(str, Enum):
    PRESERVES_DECLARED_SEPARATION = "preserves_declared_separation"
    DOES_NOT_IDENTIFY = "does_not_identify"
    NOT_APPLICABLE = "not_applicable"
    OBSTRUCTION_RECORDED = "obstruction_recorded"


class NoTargetGuardResult(str, Enum):
    PASS = "pass"
    FAIL_CLOSED = "fail_closed"


class EvaluationKind(str, Enum):
    VALID = "valid_support_only_record"
    MISSING = "fail_closed_missing_certificate"
    MALFORMED = "fail_closed_malformed_certificate"
    DOMAIN_CODOMAIN_MISMATCH = "fail_closed_domain_codomain_mismatch"
    TARGET_IMPORT = "rejected_target_import"
    DETECTOR_SEMANTICS = "rejected_detector_semantics"
    PROCESS_AUTHORITY = "rejected_process_authority"
    SCOPED_EVIDENCE_NOT_CERTIFICATE = "fail_closed_scoped_evidence_not_certificate"
    FORBIDDEN_IMPORT = "fail_closed_forbidden_import"
    GUARD_FAILED = "fail_closed_no_target_guard"


POSITIVE_KINDS = {
    InstanceKind.VALID_TRANSPORT,
    InstanceKind.VALID_INVARIANCE,
    InstanceKind.VALID_FACTORIZATION,
}


@dataclass(frozen=True)
class NoTargetImportGuard:
    result: NoTargetGuardResult
    reason: str = ""


@dataclass(frozen=True)
class CertificateRecord:
    certificate_instance_id: str
    instance_kind: InstanceKind
    domain: Tuple[str, ...]
    codomain: Tuple[str, ...]
    certificate_payload: Optional[Mapping[str, str]]
    no_target_import_guard: NoTargetImportGuard
    status: CertificateStatus
    expected_equivalence_result: ExpectedEquivalenceResult
    rr_e_separation_effect: RRESeparationEffect
    fail_closed_reason: Optional[str]
    source_paths: Tuple[str, ...] = field(default_factory=tuple)
    forbidden_overreads: Tuple[str, ...] = field(default_factory=tuple)
    target_import_used: bool = False
    detector_semantics_used: bool = False
    stress_energy_used: bool = False
    matter_action_used: bool = False
    benchmark_behavior_used: bool = False
    process_authority_used: bool = False
    scoped_evidence_used: bool = False


@dataclass(frozen=True)
class EvaluationResult:
    is_valid: bool
    evaluation_kind: EvaluationKind
    expected_equivalence_result: ExpectedEquivalenceResult
    fail_closed: bool
    reason: str
    support_only: bool = SUPPORT_ONLY
    proof_authority: bool = PROOF_AUTHORITY
    physics_promotion_authorized: bool = PHYSICS_PROMOTION_AUTHORIZED


def evaluate_certificate(record: CertificateRecord) -> EvaluationResult:
    """Evaluate one finite/local source certificate record."""

    if record.target_import_used or record.status is CertificateStatus.REJECTED_TARGET_IMPORT:
        return _blocked(
            EvaluationKind.TARGET_IMPORT,
            "Target-side data cannot fill a source certificate slot.",
        )
    if record.detector_semantics_used or record.status is CertificateStatus.REJECTED_DETECTOR_SEMANTICS:
        return _blocked(
            EvaluationKind.DETECTOR_SEMANTICS,
            "Detector semantics cannot fill a source certificate slot.",
        )
    if record.process_authority_used or record.status is CertificateStatus.REJECTED_PROCESS_AUTHORITY:
        return _blocked(
            EvaluationKind.PROCESS_AUTHORITY,
            "Process authority cannot serve as certificate payload.",
        )
    if record.scoped_evidence_used:
        return _blocked(
            EvaluationKind.SCOPED_EVIDENCE_NOT_CERTIFICATE,
            "Scoped evidence is not an explicit certificate payload.",
        )
    if record.stress_energy_used or record.matter_action_used or record.benchmark_behavior_used:
        return _blocked(
            EvaluationKind.FORBIDDEN_IMPORT,
            "Stress-energy, matter action, and benchmark behavior are outside the P6 certificate datum.",
        )
    if record.status is CertificateStatus.MISSING or record.certificate_payload is None:
        return _blocked(
            EvaluationKind.MISSING,
            record.fail_closed_reason or "Certificate payload is missing.",
        )
    if record.status is CertificateStatus.MALFORMED:
        return _blocked(
            EvaluationKind.MALFORMED,
            record.fail_closed_reason or "Certificate payload is malformed.",
        )
    if record.no_target_import_guard.result is not NoTargetGuardResult.PASS:
        return _blocked(
            EvaluationKind.GUARD_FAILED,
            record.no_target_import_guard.reason or "No-target import guard did not pass.",
        )
    if not _witness_map_matches(record.certificate_payload, record.domain, record.codomain):
        return _blocked(
            EvaluationKind.DOMAIN_CODOMAIN_MISMATCH,
            "Witness map does not match declared domain and codomain.",
        )
    if (
        record.status is CertificateStatus.VALID
        and record.instance_kind in POSITIVE_KINDS
        and record.expected_equivalence_result is ExpectedEquivalenceResult.ALLOWED
        and record.fail_closed_reason is None
    ):
        return EvaluationResult(
            is_valid=True,
            evaluation_kind=EvaluationKind.VALID,
            expected_equivalence_result=ExpectedEquivalenceResult.ALLOWED,
            fail_closed=False,
            reason="Valid finite/local source certificate record inside declared scope only.",
        )
    return _blocked(
        EvaluationKind.MALFORMED,
        "Record fields are internally inconsistent for a positive certificate.",
    )


def _witness_map_matches(
    witness_map: Mapping[str, str],
    domain: Sequence[str],
    codomain: Sequence[str],
) -> bool:
    return set(witness_map.keys()) == set(domain) and set(witness_map.values()).issubset(set(codomain))


def _blocked(kind: EvaluationKind, reason: str) -> EvaluationResult:
    return EvaluationResult(
        is_valid=False,
        evaluation_kind=kind,
        expected_equivalence_result=ExpectedEquivalenceResult.BLOCKED,
        fail_closed=True,
        reason=reason,
    )
