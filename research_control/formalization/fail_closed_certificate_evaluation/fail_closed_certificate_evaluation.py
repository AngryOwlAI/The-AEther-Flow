#!/usr/bin/env python3
"""Support-only fail-closed source-certificate evaluator.

This module mechanizes the v17 P8-T02 selected fragment as a deterministic
finite checker. It is executable support, not proof authority for project
physics claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


CHECKER_ID = "fail_closed_certificate_evaluation_support_formalization"
CHECKER_VERSION = "0.1.0"
FORMALIZATION_ID = "support_formalization_fail_closed_certificate_evaluation_v1"
PROOF_NORMAL_FORM_ROW_ID = "PNF-RT-20260706-014-003"
SOURCE_ARTIFACT_PATH = (
    "research_control/tasks/RT-20260702-064/artifacts/"
    "source_certificate_operation_laws_v1.tex"
)
SOURCE_ARTIFACT_OBJECT_ID = "TEX-V15-P3-T02-SOURCE-CERTIFICATE-OPERATION-LAWS"
SOURCE_ARTIFACT_HASH = (
    "2ebc781bd82b4d39ab394255e5d3836d992625bdece8b8f912a8ab809669b986"
)
SELECTOR_ARTIFACT_PATH = (
    "research_control/tasks/RT-20260706-017/artifacts/"
    "support_only_formalization_target_selector.md"
)
SELECTOR_ARTIFACT_OBJECT_ID = (
    "MD-RESEARCH-CONTROL-TASKS-RT-20260706-017-"
    "SUPPORT-ONLY-FORMALIZATION-TARGET-SELECTOR"
)
SELECTOR_ARTIFACT_HASH = (
    "fd2bde2f530c78f7d45bbe105a8433dba87440ca14cf36d4bec89c0f24da4ef1"
)
SUPPORT_ONLY = True
PROOF_AUTHORITY = False
PHYSICS_PROMOTION_AUTHORIZED = False
BOUNDARY_STATEMENT = (
    "This support-only formalization has proof_authority=false. It is not "
    "proof authority, not canonical ontology adoption, not source-law "
    "adoption, not MetricData(E) adoption, not g_eff adoption or scope "
    "expansion, not coupling-law adoption, not matter coupling, not "
    "stress-energy semantics, not a stress-energy tensor, not detector "
    "semantics, not a matter action, not Einstein equations, not benchmark "
    "promotion, and not completed derivation."
)


class CertificateKind(str, Enum):
    SOURCE_TRANSPORT = "source_transport"
    SOURCE_INVARIANCE = "source_invariance"
    SOURCE_FACTORIZATION = "source_factorization"


class CertificateStatus(str, Enum):
    VALID = "valid"
    MISSING = "missing"
    MALFORMED = "malformed"
    FAIL_CLOSED = "fail_closed"


class EvaluationKind(str, Enum):
    VALID_DECLARED_SCOPE = "valid_declared_scope"
    MISSING_CERTIFICATE = "fail_closed_missing_certificate"
    MALFORMED_CERTIFICATE = "fail_closed_malformed_certificate"
    DOMAIN_CODOMAIN_MISMATCH = "fail_closed_domain_codomain_mismatch"
    SOURCE_SCOPE_MISMATCH = "fail_closed_source_scope_mismatch"
    NO_TARGET_GUARD_FAILED = "fail_closed_no_target_import_guard"
    TARGET_IMPORT = "fail_closed_target_import"
    DETECTOR_SEMANTICS_IMPORT = "fail_closed_detector_semantics_import"
    PROCESS_AUTHORITY_IMPORT = "fail_closed_process_authority_import"
    STRESS_ENERGY_IMPORT = "fail_closed_stress_energy_import"
    MATTER_ACTION_IMPORT = "fail_closed_matter_action_import"
    BENCHMARK_BEHAVIOR_IMPORT = "fail_closed_benchmark_behavior_import"
    SCOPED_EVIDENCE_NOT_CERTIFICATE = "fail_closed_scoped_evidence_not_certificate"
    GENERATED_OR_REGISTRY_AUTHORITY_IMPORT = (
        "fail_closed_generated_or_registry_authority_import"
    )
    METRICDATA_OR_GEFF_IMPORT = "fail_closed_metricdata_or_geff_import"


class EvaluationOutcome(str, Enum):
    ALLOWED = "declared_equivalence_allowed"
    BLOCKED = "declared_equivalence_blocked"


@dataclass(frozen=True)
class CertificateRecord:
    record_id: str
    kind: CertificateKind
    status: CertificateStatus
    declared_source_scope: tuple[str, ...]
    domain: tuple[str, ...]
    codomain: tuple[str, ...]
    witness_map: Mapping[str, str] | None
    no_target_import_guard: bool = True
    fail_closed_reason: str = ""
    target_topology_import: bool = False
    target_atlas_import: bool = False
    target_metric_import: bool = False
    proper_time_import: bool = False
    detector_semantics_import: bool = False
    stress_energy_import: bool = False
    matter_action_import: bool = False
    benchmark_behavior_import: bool = False
    metricdata_e_import: bool = False
    geff_import: bool = False
    generated_derivative_import: bool = False
    registry_status_import: bool = False
    validator_status_import: bool = False
    role_status_import: bool = False
    handoff_status_import: bool = False
    approval_status_import: bool = False
    local_cache_import: bool = False
    file_order_import: bool = False
    commit_state_import: bool = False
    process_authority_import: bool = False
    scoped_evidence_used_as_certificate: bool = False


@dataclass(frozen=True)
class EvaluationResult:
    record_id: str
    is_valid: bool
    outcome: EvaluationOutcome
    evaluation_kind: EvaluationKind
    fail_closed: bool
    reason: str
    support_only: bool = SUPPORT_ONLY
    proof_authority: bool = PROOF_AUTHORITY
    physics_promotion_authorized: bool = PHYSICS_PROMOTION_AUTHORIZED

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_kind": self.evaluation_kind.value,
            "fail_closed": self.fail_closed,
            "is_valid": self.is_valid,
            "outcome": self.outcome.value,
            "physics_promotion_authorized": self.physics_promotion_authorized,
            "proof_authority": self.proof_authority,
            "reason": self.reason,
            "record_id": self.record_id,
            "support_only": self.support_only,
        }


@dataclass(frozen=True)
class PropositionResult:
    proposition_id: str
    status: str
    message: str
    evidence: dict[str, Any] = field(default_factory=dict)
    proof_authority: bool = PROOF_AUTHORITY

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence": self.evidence,
            "message": self.message,
            "proof_authority": self.proof_authority,
            "proposition_id": self.proposition_id,
            "status": self.status,
        }


def evaluate_certificate(record: CertificateRecord) -> EvaluationResult:
    """Evaluate one finite certificate record with fail-closed precedence."""

    target_import_flags = (
        record.target_topology_import,
        record.target_atlas_import,
        record.target_metric_import,
        record.proper_time_import,
    )
    if any(target_import_flags):
        return _blocked(
            record,
            EvaluationKind.TARGET_IMPORT,
            "Target topology, atlas, metric, or proper time cannot fill a source certificate slot.",
        )
    if record.detector_semantics_import:
        return _blocked(
            record,
            EvaluationKind.DETECTOR_SEMANTICS_IMPORT,
            "Detector semantics cannot fill a source certificate slot.",
        )
    if record.process_authority_import:
        return _blocked(
            record,
            EvaluationKind.PROCESS_AUTHORITY_IMPORT,
            "Process authority cannot serve as certificate payload.",
        )
    if record.stress_energy_import:
        return _blocked(
            record,
            EvaluationKind.STRESS_ENERGY_IMPORT,
            "Stress-energy semantics are outside source-certificate data.",
        )
    if record.matter_action_import:
        return _blocked(
            record,
            EvaluationKind.MATTER_ACTION_IMPORT,
            "Matter-action semantics are outside source-certificate data.",
        )
    if record.benchmark_behavior_import:
        return _blocked(
            record,
            EvaluationKind.BENCHMARK_BEHAVIOR_IMPORT,
            "Benchmark behavior cannot serve as certificate data.",
        )
    if record.metricdata_e_import or record.geff_import:
        return _blocked(
            record,
            EvaluationKind.METRICDATA_OR_GEFF_IMPORT,
            "MetricData(E) and g_eff cannot fill this source-certificate slot.",
        )
    if _uses_generated_or_process_state(record):
        return _blocked(
            record,
            EvaluationKind.GENERATED_OR_REGISTRY_AUTHORITY_IMPORT,
            "Generated, registry, validator, approval, cache, file-order, or commit state cannot be mathematical certificate data.",
        )
    if record.scoped_evidence_used_as_certificate:
        return _blocked(
            record,
            EvaluationKind.SCOPED_EVIDENCE_NOT_CERTIFICATE,
            "Scoped evidence/precondition status is not an explicit certificate payload.",
        )
    if not record.no_target_import_guard:
        return _blocked(
            record,
            EvaluationKind.NO_TARGET_GUARD_FAILED,
            record.fail_closed_reason or "No-target-import guard did not pass.",
        )
    if record.status is CertificateStatus.MISSING or record.witness_map is None:
        return _blocked(
            record,
            EvaluationKind.MISSING_CERTIFICATE,
            record.fail_closed_reason or "Certificate witness payload is missing.",
        )
    if record.status in {CertificateStatus.MALFORMED, CertificateStatus.FAIL_CLOSED}:
        return _blocked(
            record,
            EvaluationKind.MALFORMED_CERTIFICATE,
            record.fail_closed_reason or "Certificate record is malformed.",
        )
    if not record.declared_source_scope or not record.domain or not record.codomain:
        return _blocked(
            record,
            EvaluationKind.MALFORMED_CERTIFICATE,
            "Declared source scope, domain, and codomain must be nonempty.",
        )
    if not _scope_contains(record.declared_source_scope, record.domain, record.codomain):
        return _blocked(
            record,
            EvaluationKind.SOURCE_SCOPE_MISMATCH,
            "Domain or codomain element is outside the declared source scope.",
        )
    if not _witness_map_matches(record.witness_map, record.domain, record.codomain):
        return _blocked(
            record,
            EvaluationKind.DOMAIN_CODOMAIN_MISMATCH,
            "Witness map does not match declared domain and codomain.",
        )
    return EvaluationResult(
        record_id=record.record_id,
        is_valid=True,
        outcome=EvaluationOutcome.ALLOWED,
        evaluation_kind=EvaluationKind.VALID_DECLARED_SCOPE,
        fail_closed=False,
        reason="Valid finite source certificate record inside declared source scope only.",
    )


def positive_record() -> CertificateRecord:
    return CertificateRecord(
        record_id="P8T02-SRC-CERT-VALID-001",
        kind=CertificateKind.SOURCE_TRANSPORT,
        status=CertificateStatus.VALID,
        declared_source_scope=("A0", "A1", "B0", "B1"),
        domain=("A0", "A1"),
        codomain=("B0", "B1"),
        witness_map={"A0": "B0", "A1": "B1"},
    )


def sample_records() -> tuple[CertificateRecord, ...]:
    base = positive_record()
    return (
        base,
        _replace(base, record_id="P8T02-SRC-CERT-MISSING-001", status=CertificateStatus.MISSING, witness_map=None),
        _replace(
            base,
            record_id="P8T02-SRC-CERT-MALFORMED-001",
            witness_map={"A0": "B0", "A1": "B9"},
        ),
        _replace(base, record_id="P8T02-SRC-CERT-TARGET-001", target_metric_import=True),
        _replace(base, record_id="P8T02-SRC-CERT-DETECTOR-001", detector_semantics_import=True),
        _replace(base, record_id="P8T02-SRC-CERT-PROCESS-001", process_authority_import=True),
        _replace(base, record_id="P8T02-SRC-CERT-STRESS-001", stress_energy_import=True),
        _replace(base, record_id="P8T02-SRC-CERT-MATTER-ACTION-001", matter_action_import=True),
        _replace(base, record_id="P8T02-SRC-CERT-BENCHMARK-001", benchmark_behavior_import=True),
        _replace(base, record_id="P8T02-SRC-CERT-SCOPED-EVIDENCE-001", scoped_evidence_used_as_certificate=True),
        _replace(base, record_id="P8T02-SRC-CERT-GENERATED-001", validator_status_import=True),
        _replace(base, record_id="P8T02-SRC-CERT-GEFF-001", geff_import=True),
    )


def proposition_results(results: Sequence[EvaluationResult]) -> tuple[PropositionResult, ...]:
    by_id = {result.record_id: result for result in results}
    negative_kinds = sorted(
        {
            result.evaluation_kind.value
            for result in results
            if result.fail_closed
        }
    )
    return (
        PropositionResult(
            proposition_id="valid_source_certificate_allows_declared_equivalence_support_only",
            status="pass",
            message="The positive finite source certificate branch allows only declared equivalence within declared scope.",
            evidence=by_id["P8T02-SRC-CERT-VALID-001"].to_dict(),
        ),
        PropositionResult(
            proposition_id="missing_certificate_fails_closed",
            status="pass",
            message="An absent certificate payload blocks declared equivalence.",
            evidence=by_id["P8T02-SRC-CERT-MISSING-001"].to_dict(),
        ),
        PropositionResult(
            proposition_id="malformed_certificate_fails_closed",
            status="pass",
            message="A malformed witness map blocks declared equivalence.",
            evidence=by_id["P8T02-SRC-CERT-MALFORMED-001"].to_dict(),
        ),
        PropositionResult(
            proposition_id="target_and_detector_imports_fail_closed",
            status="pass",
            message="Target-metric and detector-semantics imports are invalid certificate inputs.",
            evidence={
                "detector": by_id["P8T02-SRC-CERT-DETECTOR-001"].to_dict(),
                "target": by_id["P8T02-SRC-CERT-TARGET-001"].to_dict(),
            },
        ),
        PropositionResult(
            proposition_id="downstream_physics_imports_fail_closed",
            status="pass",
            message="Stress-energy, matter-action, benchmark, MetricData(E), and g_eff imports are blocked.",
            evidence={
                "benchmark": by_id["P8T02-SRC-CERT-BENCHMARK-001"].to_dict(),
                "geff": by_id["P8T02-SRC-CERT-GEFF-001"].to_dict(),
                "matter_action": by_id["P8T02-SRC-CERT-MATTER-ACTION-001"].to_dict(),
                "stress_energy": by_id["P8T02-SRC-CERT-STRESS-001"].to_dict(),
            },
        ),
        PropositionResult(
            proposition_id="process_and_generated_authority_imports_fail_closed",
            status="pass",
            message="Process authority and validator/registry-like state cannot fill certificate slots.",
            evidence={
                "generated": by_id["P8T02-SRC-CERT-GENERATED-001"].to_dict(),
                "process": by_id["P8T02-SRC-CERT-PROCESS-001"].to_dict(),
            },
        ),
        PropositionResult(
            proposition_id="scoped_evidence_does_not_fill_certificate_slot",
            status="pass",
            message="Scoped evidence/precondition status cannot be converted into a certificate payload.",
            evidence=by_id["P8T02-SRC-CERT-SCOPED-EVIDENCE-001"].to_dict(),
        ),
        PropositionResult(
            proposition_id="all_negative_branches_are_fail_closed",
            status="pass",
            message="Every negative sample branch returns declared_equivalence_blocked and fail_closed=true.",
            evidence={"negative_evaluation_kinds": negative_kinds},
        ),
    )


@dataclass(frozen=True)
class FormalizationReport:
    results: tuple[EvaluationResult, ...]
    propositions: tuple[PropositionResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_statement": BOUNDARY_STATEMENT,
            "checker_id": CHECKER_ID,
            "checker_version": CHECKER_VERSION,
            "formal_objects": [
                "CertificateRecord",
                "EvaluationResult",
                "evaluate_certificate",
                "fail_closed_certificate_evaluation",
                "valid_declared_scope_branch",
                "missing_certificate_branch",
                "malformed_certificate_branch",
                "target_import_branch",
                "detector_semantics_branch",
                "process_authority_branch",
                "downstream_physics_import_branch",
                "scoped_evidence_not_certificate_branch",
            ],
            "forbidden_authority_flags": forbidden_authority_flags(),
            "formalization_id": FORMALIZATION_ID,
            "physics_promotion_authorized": PHYSICS_PROMOTION_AUTHORIZED,
            "proof_authority": PROOF_AUTHORITY,
            "proof_normal_form_row_id": PROOF_NORMAL_FORM_ROW_ID,
            "proposition_results": [
                proposition.to_dict() for proposition in self.propositions
            ],
            "result_count": len(self.results),
            "results": [result.to_dict() for result in self.results],
            "source_artifact_hash": SOURCE_ARTIFACT_HASH,
            "source_artifact_object_id": SOURCE_ARTIFACT_OBJECT_ID,
            "source_artifact_path": SOURCE_ARTIFACT_PATH,
            "source_artifacts": [
                {
                    "object_id": SOURCE_ARTIFACT_OBJECT_ID,
                    "path": SOURCE_ARTIFACT_PATH,
                    "registry_name": "TEX_SOURCE_REGISTRY.csv",
                    "source_hash": SOURCE_ARTIFACT_HASH,
                },
                {
                    "object_id": SELECTOR_ARTIFACT_OBJECT_ID,
                    "path": SELECTOR_ARTIFACT_PATH,
                    "registry_name": "MARKDOWN_SOURCE_REGISTRY.csv",
                    "source_hash": SELECTOR_ARTIFACT_HASH,
                },
            ],
            "status": "pass_support_only",
            "support_only": SUPPORT_ONLY,
        }


def run_formalization() -> FormalizationReport:
    results = tuple(evaluate_certificate(record) for record in sample_records())
    if not _report_passes(results):
        raise RuntimeError("internal report fixture failed support-only invariants")
    return FormalizationReport(results, proposition_results(results))


def forbidden_authority_flags() -> dict[str, bool]:
    return {
        "benchmark_promotion_authority": False,
        "canonical_ontology_adoption": False,
        "completed_derivation_claimed": False,
        "coupling_law_adopted": False,
        "downstream_gr_promotion_authorized": False,
        "einstein_equations_derived": False,
        "future_source_extension_impossibility_claimed": False,
        "g_eff_adopted": False,
        "geff_scope_changed": False,
        "global_theory_rejected": False,
        "matter_action_imported": False,
        "matter_coupling_adopted": False,
        "matter_coupling_derived": False,
        "metric_data_adopted": False,
        "source_law_adopted": False,
        "stress_energy_semantics_imported": False,
        "stress_energy_tensor_constructed": False,
        "target_metric_imported": False,
    }


def source_artifact_sha256(repo_root: Path) -> str:
    return hashlib.sha256((repo_root / SOURCE_ARTIFACT_PATH).read_bytes()).hexdigest()


def _replace(record: CertificateRecord, **updates: Any) -> CertificateRecord:
    data = record.__dict__.copy()
    data.update(updates)
    return CertificateRecord(**data)


def _uses_generated_or_process_state(record: CertificateRecord) -> bool:
    return any(
        (
            record.generated_derivative_import,
            record.registry_status_import,
            record.validator_status_import,
            record.role_status_import,
            record.handoff_status_import,
            record.approval_status_import,
            record.local_cache_import,
            record.file_order_import,
            record.commit_state_import,
        )
    )


def _scope_contains(
    source_scope: Sequence[str],
    domain: Iterable[str],
    codomain: Iterable[str],
) -> bool:
    scope = set(source_scope)
    return set(domain) <= scope and set(codomain) <= scope


def _witness_map_matches(
    witness_map: Mapping[str, str],
    domain: Sequence[str],
    codomain: Sequence[str],
) -> bool:
    return set(witness_map.keys()) == set(domain) and set(witness_map.values()) <= set(codomain)


def _blocked(
    record: CertificateRecord,
    kind: EvaluationKind,
    reason: str,
) -> EvaluationResult:
    return EvaluationResult(
        record_id=record.record_id,
        is_valid=False,
        outcome=EvaluationOutcome.BLOCKED,
        evaluation_kind=kind,
        fail_closed=True,
        reason=reason,
    )


def _report_passes(results: Sequence[EvaluationResult]) -> bool:
    positives = [result for result in results if not result.fail_closed]
    negatives = [result for result in results if result.fail_closed]
    return (
        len(positives) == 1
        and positives[0].outcome is EvaluationOutcome.ALLOWED
        and all(result.outcome is EvaluationOutcome.BLOCKED for result in negatives)
        and all(result.support_only and not result.proof_authority for result in results)
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    parser.add_argument("--json-output", help="Write JSON report to this path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = run_formalization().to_dict()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.json_output:
        Path(args.json_output).write_text(rendered, encoding="utf-8")
    if args.json or not args.json_output:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
