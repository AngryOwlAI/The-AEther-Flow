"""Support-only typed pilot for the missing-certificate fail-closed branch.

This module is a task-local executable specification for RT-20260704-005.
It is not proof authority for project physics and does not promote any
source-law, matter-coupling, Einstein-equation, benchmark, or completed
derivation claim.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import json
from typing import Optional


OBSTRUCTION_MISSING_RRE_SEPARATION_DATA = (
    "OB-P3T02-MISSING-CERT-RRE-SEPARATION-DATA"
)
OBSTRUCTION_MALFORMED_CERTIFICATE = "OB-P15T02-MALFORMED-CERTIFICATE"
OBSTRUCTION_TARGET_IMPORT = "OB-P15T02-TARGET-IMPORT-CERTIFICATE"


class CertificateSlotStatus(str, Enum):
    VALID = "valid"
    MISSING = "missing"
    MALFORMED = "malformed"
    TARGET_IMPORTING = "target_importing"


class EvaluationStatus(str, Enum):
    VALID_CERTIFICATE = "valid_certificate"
    BOTTOM = "bottom"


class EvaluationKind(str, Enum):
    VALID_IDENTIFICATION = "valid_identification"
    MISSING_CERTIFICATE_SEPARATION_PRESERVED = (
        "missing_certificate_separation_preserved"
    )
    MISSING_CERTIFICATE_OBSTRUCTION = "missing_certificate_obstruction"
    MALFORMED_CERTIFICATE = "malformed_certificate"
    TARGET_IMPORTING_CERTIFICATE = "target_importing_certificate"


@dataclass(frozen=True)
class CertificateSlot:
    slot_id: str
    status: CertificateSlotStatus
    malformed_reason: str = ""


@dataclass(frozen=True)
class DeclaredRRERecord:
    left_object_id: Optional[str]
    right_object_id: Optional[str]
    declared_separated: bool = False

    def has_declared_object_pair(self) -> bool:
        return bool(self.left_object_id and self.right_object_id)

    def has_declared_separation(self) -> bool:
        return (
            self.has_declared_object_pair()
            and self.left_object_id != self.right_object_id
            and self.declared_separated
        )


@dataclass(frozen=True)
class EvaluationResult:
    evaluation: EvaluationStatus
    kind: EvaluationKind
    positive_identification_derived: bool
    preserved_declared_separation: bool
    obstruction_id: str
    proof_authority: bool
    support_only: bool
    physics_promotion_authorized: bool
    explanation: str

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["evaluation"] = self.evaluation.value
        data["kind"] = self.kind.value
        return data


def evaluate_certificate_slot(
    slot: CertificateSlot,
    source_record: DeclaredRRERecord,
) -> EvaluationResult:
    """Evaluate one certificate slot under the support-only P15-T02 kernel."""

    if slot.status == CertificateSlotStatus.VALID:
        return EvaluationResult(
            evaluation=EvaluationStatus.VALID_CERTIFICATE,
            kind=EvaluationKind.VALID_IDENTIFICATION,
            positive_identification_derived=True,
            preserved_declared_separation=False,
            obstruction_id="",
            proof_authority=False,
            support_only=True,
            physics_promotion_authorized=False,
            explanation=(
                "A valid source certificate may support the local typed "
                "identification branch, but this executable spec is not "
                "project-physics proof authority."
            ),
        )

    if slot.status == CertificateSlotStatus.MISSING:
        if source_record.has_declared_separation():
            return EvaluationResult(
                evaluation=EvaluationStatus.BOTTOM,
                kind=EvaluationKind.MISSING_CERTIFICATE_SEPARATION_PRESERVED,
                positive_identification_derived=False,
                preserved_declared_separation=True,
                obstruction_id="",
                proof_authority=False,
                support_only=True,
                physics_promotion_authorized=False,
                explanation=(
                    "The required certificate slot is missing, so positive "
                    "identification is not derived. The declared RR_E "
                    "separation is preserved."
                ),
            )
        return EvaluationResult(
            evaluation=EvaluationStatus.BOTTOM,
            kind=EvaluationKind.MISSING_CERTIFICATE_OBSTRUCTION,
            positive_identification_derived=False,
            preserved_declared_separation=False,
            obstruction_id=OBSTRUCTION_MISSING_RRE_SEPARATION_DATA,
            proof_authority=False,
            support_only=True,
            physics_promotion_authorized=False,
            explanation=(
                "The required certificate slot is missing and the declared "
                "source record is insufficient to state a preserved RR_E "
                "separation, so the obstruction is recorded."
            ),
        )

    if slot.status == CertificateSlotStatus.MALFORMED:
        reason = slot.malformed_reason or "malformed certificate"
        return EvaluationResult(
            evaluation=EvaluationStatus.BOTTOM,
            kind=EvaluationKind.MALFORMED_CERTIFICATE,
            positive_identification_derived=False,
            preserved_declared_separation=False,
            obstruction_id=OBSTRUCTION_MALFORMED_CERTIFICATE,
            proof_authority=False,
            support_only=True,
            physics_promotion_authorized=False,
            explanation=f"Malformed certificate fails closed: {reason}.",
        )

    if slot.status == CertificateSlotStatus.TARGET_IMPORTING:
        return EvaluationResult(
            evaluation=EvaluationStatus.BOTTOM,
            kind=EvaluationKind.TARGET_IMPORTING_CERTIFICATE,
            positive_identification_derived=False,
            preserved_declared_separation=False,
            obstruction_id=OBSTRUCTION_TARGET_IMPORT,
            proof_authority=False,
            support_only=True,
            physics_promotion_authorized=False,
            explanation=(
                "A target-importing certificate is invalid for source-side "
                "certificate algebra and fails closed."
            ),
        )

    raise ValueError(f"Unsupported certificate slot status: {slot.status!r}")


def support_only_receipt() -> dict[str, object]:
    return {
        "task_id": "RT-20260704-005",
        "pilot": "fail_closed_missing_certificate_lemma",
        "proof_authority": False,
        "support_only": True,
        "physics_promotion_authorized": False,
        "source_law_adopted": False,
        "matter_coupling_derived": False,
        "einstein_equations_derived": False,
        "benchmark_promoted": False,
        "completed_derivation_claimed": False,
    }


if __name__ == "__main__":
    print(json.dumps(support_only_receipt(), indent=2, sort_keys=True))
