"""Common immutable result models for project validation reporters.

These models carry operational validation evidence only.  They do not confer
source, scientific, ontology, benchmark, or Gate Chair authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable


STATUSES = (
    "PASS",
    "FAIL",
    "WARN",
    "SKIP_NOT_APPLICABLE",
    "SKIP_SUPERSEDED",
    "CACHE_HIT",
    "BLOCKED_CONFIGURATION",
)
LEVELS = ("ERROR", "WARN", "INFO")
SEVERITIES = ("blocking", "advisory", "diagnostic")
_FINDING_ID = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\Z")
_STATUS_PRIORITY = {
    "BLOCKED_CONFIGURATION": 4,
    "FAIL": 3,
    "WARN": 2,
    "PASS": 1,
    "CACHE_HIT": 1,
    "SKIP_NOT_APPLICABLE": 1,
    "SKIP_SUPERSEDED": 1,
}
_LEVEL_PRIORITY = {"ERROR": 0, "WARN": 1, "INFO": 2}


def _nonblank(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonblank string")
    return value


def _bounded_identity(value: str, name: str, limit: int = 128) -> str:
    _nonblank(value, name)
    if len(value.encode("utf-8")) > limit:
        raise ValueError(f"{name} must be at most {limit} UTF-8 bytes")
    return value


@dataclass(frozen=True, slots=True)
class ValidationFinding:
    """One stable validation finding."""

    finding_id: str
    level: str
    code: str
    message: str
    artifact_ref: str | None = None

    def __post_init__(self) -> None:
        _bounded_identity(self.finding_id, "finding_id")
        if not _FINDING_ID.fullmatch(self.finding_id):
            raise ValueError("finding_id must be a stable uppercase hyphenated ID")
        if self.level not in LEVELS:
            raise ValueError(f"unsupported finding level: {self.level}")
        _bounded_identity(self.code, "code", 64)
        _nonblank(self.message, "message")
        if self.artifact_ref is not None:
            _bounded_identity(self.artifact_ref, "artifact_ref")

    @property
    def sort_key(self) -> tuple[int, str, str, str]:
        return (
            _LEVEL_PRIORITY[self.level],
            self.finding_id,
            self.code,
            self.message,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_id": "validation_finding_v1",
            "finding_id": self.finding_id,
            "level": self.level,
            "code": self.code,
            "message": self.message,
            "artifact_ref": self.artifact_ref,
        }


@dataclass(frozen=True, slots=True)
class ValidationGateResult:
    """One gate result with complete in-memory findings."""

    gate_id: str
    status: str
    severity: str = "blocking"
    exit_code: int = 0
    findings: tuple[ValidationFinding, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _bounded_identity(self.gate_id, "gate_id", 64)
        if self.status not in STATUSES:
            raise ValueError(f"unsupported gate status: {self.status}")
        if self.severity not in SEVERITIES:
            raise ValueError(f"unsupported gate severity: {self.severity}")
        if not isinstance(self.exit_code, int) or self.exit_code < 0:
            raise ValueError("exit_code must be a nonnegative integer")
        object.__setattr__(self, "findings", tuple(self.findings))
        seen: set[str] = set()
        for finding in self.findings:
            if not isinstance(finding, ValidationFinding):
                raise TypeError("findings must contain ValidationFinding values")
            if finding.finding_id in seen:
                raise ValueError(f"duplicate finding_id in gate: {finding.finding_id}")
            seen.add(finding.finding_id)

    @property
    def sorted_findings(self) -> tuple[ValidationFinding, ...]:
        return tuple(sorted(self.findings, key=lambda finding: finding.sort_key))

    @property
    def error_count(self) -> int:
        return sum(finding.level == "ERROR" for finding in self.findings)

    @property
    def warning_count(self) -> int:
        return sum(finding.level == "WARN" for finding in self.findings)

    @property
    def finding_count(self) -> int:
        return len(self.findings)

    def to_full_dict(self) -> dict[str, object]:
        return {
            "gate_id": self.gate_id,
            "status": self.status,
            "severity": self.severity,
            "exit_code": self.exit_code,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "finding_count": self.finding_count,
            "findings": [finding.to_dict() for finding in self.sorted_findings],
        }


@dataclass(frozen=True, slots=True)
class ValidationRun:
    """One validation invocation with exact status and exit-code semantics."""

    run_id: str
    tree_hash: str
    status: str
    exit_code: int
    gate_results: tuple[ValidationGateResult, ...] = field(default_factory=tuple)
    profile: str = "default"

    def __post_init__(self) -> None:
        _bounded_identity(self.run_id, "run_id")
        _bounded_identity(self.tree_hash, "tree_hash")
        _bounded_identity(self.profile, "profile")
        if self.status not in STATUSES:
            raise ValueError(f"unsupported run status: {self.status}")
        if not isinstance(self.exit_code, int) or self.exit_code < 0:
            raise ValueError("exit_code must be a nonnegative integer")
        object.__setattr__(self, "gate_results", tuple(self.gate_results))
        gate_ids: set[str] = set()
        finding_ids: set[str] = set()
        for gate in self.gate_results:
            if not isinstance(gate, ValidationGateResult):
                raise TypeError("gate_results must contain ValidationGateResult values")
            if gate.gate_id in gate_ids:
                raise ValueError(f"duplicate gate_id: {gate.gate_id}")
            gate_ids.add(gate.gate_id)
            for finding in gate.findings:
                if finding.finding_id in finding_ids:
                    raise ValueError(f"duplicate finding_id in run: {finding.finding_id}")
                finding_ids.add(finding.finding_id)

    @classmethod
    def from_gates(
        cls,
        *,
        run_id: str,
        tree_hash: str,
        exit_code: int,
        gate_results: Iterable[ValidationGateResult],
        profile: str = "default",
    ) -> "ValidationRun":
        gates = tuple(gate_results)
        status = aggregate_status(gates)
        return cls(run_id, tree_hash, status, exit_code, gates, profile)

    @property
    def sorted_gate_results(self) -> tuple[ValidationGateResult, ...]:
        return tuple(sorted(self.gate_results, key=lambda gate: gate.gate_id))

    @property
    def error_count(self) -> int:
        return sum(gate.error_count for gate in self.gate_results)

    @property
    def warning_count(self) -> int:
        return sum(gate.warning_count for gate in self.gate_results)

    @property
    def finding_count(self) -> int:
        return sum(gate.finding_count for gate in self.gate_results)

    @property
    def counts(self) -> dict[str, int]:
        return {
            "gate_count": len(self.gate_results),
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "finding_count": self.finding_count,
        }

    def to_full_receipt(self) -> dict[str, object]:
        return {
            "schema_id": "validation_full_receipt_v1",
            "schema_version": 1,
            "run_id": self.run_id,
            "tree_hash": self.tree_hash,
            "profile": self.profile,
            "status": self.status,
            "exit_code": self.exit_code,
            "counts": self.counts,
            "gate_results": [gate.to_full_dict() for gate in self.sorted_gate_results],
            "authority": {
                "scope": "operational_validation_only",
                "source_authoritative": False,
                "full_receipts_authoritative": False,
                "physics_claim_authority": False,
                "ontology_authority": False,
                "benchmark_authority": False,
                "gate_chair_authority": False,
            },
        }


def aggregate_status(gates: Iterable[ValidationGateResult]) -> str:
    """Aggregate exact gate statuses using the canonical v1 priority."""

    values = tuple(gates)
    if not values:
        return "BLOCKED_CONFIGURATION"
    highest = max(_STATUS_PRIORITY[gate.status] for gate in values)
    return {
        4: "BLOCKED_CONFIGURATION",
        3: "FAIL",
        2: "WARN",
        1: "PASS",
    }[highest]
