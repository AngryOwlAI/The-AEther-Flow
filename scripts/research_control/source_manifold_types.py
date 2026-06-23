#!/usr/bin/env python3
"""Typed draft/control namespace for source-manifold regularity semantics.

This module is a deterministic specification aid. It does not prove a
regularity or soldering theorem, does not adopt FVR_src^GSC or
RegSold_src^GSC, and does not authorize M_src or downstream GR claims.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Sequence


INVARIANT_IDS = (
    "SepSrcNoTargetTopology",
    "ChartNamesAreNotCoordinates",
    "TransitionTokensAreNotSmoothMaps",
    "SolderingNoTargetMetric",
    "ValidationIsNotProof",
)

ALLOWED_CLAIM_STATUSES = {"draft/control", "proposal-only", "source-extension data"}


class SpecInvariantError(ValueError):
    """Raised when the typed source-manifold boundary is violated."""


class EvidenceKind(str, Enum):
    """Authority class for an asserted piece of evidence."""

    SOURCE = "source"
    SOURCE_SEPARATION = "source_separation"
    SOURCE_SUPPORT = "source_support"
    SOURCE_TRANSITION_TOKEN = "source_transition_token"
    SOURCE_INVERSE_TOKEN = "source_inverse_token"
    SOURCE_COCYCLE_TOKEN = "source_cocycle_token"
    SOURCE_EQUIVALENCE = "source_equivalence"
    SOURCE_SOLDERING = "source_soldering"
    SOURCE_VARIATION = "source_variation"
    SOURCE_READOUT = "source_readout"
    SOURCE_REGULARITY = "source_regularity"
    TARGET_TOPOLOGY = "target_topology"
    TARGET_OPEN_SET = "target_open_set"
    TARGET_ATLAS = "target_atlas"
    TARGET_COORDINATE_TRANSITION = "target_coordinate_transition"
    TARGET_METRIC = "target_metric"
    PROPER_TIME = "proper_time"
    EMPIRICAL_DETECTOR_SEMANTICS = "empirical_detector_semantics"
    VALIDATOR_PASS = "validator_pass"
    REGISTRY_METADATA = "registry_metadata"
    ROLE_AUTHORITY = "role_authority"
    HANDOFF_AUTHORITY = "handoff_authority"
    GENERATED_DERIVATIVE = "generated_derivative"
    FILE_ORDER = "file_order"
    PROCESS_AUTHORITY = "process_authority"


SOURCE_ONLY_EVIDENCE = frozenset(
    {
        EvidenceKind.SOURCE,
        EvidenceKind.SOURCE_SEPARATION,
        EvidenceKind.SOURCE_SUPPORT,
        EvidenceKind.SOURCE_TRANSITION_TOKEN,
        EvidenceKind.SOURCE_INVERSE_TOKEN,
        EvidenceKind.SOURCE_COCYCLE_TOKEN,
        EvidenceKind.SOURCE_EQUIVALENCE,
        EvidenceKind.SOURCE_SOLDERING,
        EvidenceKind.SOURCE_VARIATION,
        EvidenceKind.SOURCE_READOUT,
        EvidenceKind.SOURCE_REGULARITY,
    }
)

FORBIDDEN_EVIDENCE = frozenset(set(EvidenceKind) - set(SOURCE_ONLY_EVIDENCE))


class BottomCondition(str, Enum):
    """Fail-closed outcome marker for unsupported source-side branches."""

    NON_BOTTOM = "non_bottom"
    BOTTOM_SRC = "Bottom_src"
    FAILED = "failed"


def _require_nonblank(value: str, field_name: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise SpecInvariantError(f"{field_name} must be nonblank")
    return normalized


def _tuple(values: Iterable[object] | None) -> tuple[object, ...]:
    return tuple(values or ())


def _evidence_kind(value: EvidenceKind | str) -> EvidenceKind:
    if isinstance(value, EvidenceKind):
        return value
    try:
        return EvidenceKind(str(value))
    except ValueError as exc:
        raise SpecInvariantError(f"unknown evidence kind: {value}") from exc


def assert_source_only(
    evidence: Iterable[EvidenceKind | str],
    *,
    invariant_id: str = "SepSrcNoTargetTopology",
) -> tuple[EvidenceKind, ...]:
    """Return normalized source evidence or raise on target/process imports."""

    normalized = tuple(_evidence_kind(item) for item in evidence)
    for item in normalized:
        if item not in SOURCE_ONLY_EVIDENCE:
            raise SpecInvariantError(f"{invariant_id}: forbidden evidence {item.value}")
    return normalized


def validator_pass_can_instantiate_regularization(validator_pass: bool) -> bool:
    """Validator success is process evidence, not a regularity certificate."""

    return False


@dataclass(frozen=True)
class SourceToken:
    """A source-domain token with no target-space interpretation."""

    token_id: str
    evidence_kind: EvidenceKind = EvidenceKind.SOURCE

    def __post_init__(self) -> None:
        object.__setattr__(self, "token_id", _require_nonblank(self.token_id, "token_id"))
        assert_source_only((self.evidence_kind,))


@dataclass(frozen=True)
class QuotientSupport:
    """Named source quotient-support classes before any coordinate reading."""

    support_id: str
    class_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "support_id", _require_nonblank(self.support_id, "support_id"))
        classes = tuple(_require_nonblank(item, "class_id") for item in self.class_ids)
        if not classes:
            raise SpecInvariantError("QuotientSupport requires at least one class_id")
        object.__setattr__(self, "class_ids", classes)


@dataclass(frozen=True)
class SourceCarrier:
    """A carrier set for source tokens and quotient supports."""

    carrier_id: str
    tokens: tuple[SourceToken, ...] = field(default_factory=tuple)
    supports: tuple[QuotientSupport, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "carrier_id", _require_nonblank(self.carrier_id, "carrier_id"))
        if not self.tokens:
            raise SpecInvariantError("SourceCarrier requires at least one SourceToken")


@dataclass(frozen=True)
class SourceRelation:
    """A source-side relation; it is not target topology or target geometry."""

    relation_id: str
    left: SourceToken
    right: SourceToken
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE,)
    claim_status: str = "draft/control"

    def __post_init__(self) -> None:
        object.__setattr__(self, "relation_id", _require_nonblank(self.relation_id, "relation_id"))
        if self.claim_status not in ALLOWED_CLAIM_STATUSES:
            raise SpecInvariantError(f"unsupported claim_status: {self.claim_status}")
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(self.evidence, invariant_id="SepSrcNoTargetTopology"),
        )


@dataclass(frozen=True)
class ChartCandidate:
    """A named candidate chart support, not an adopted coordinate chart."""

    name: str
    support: QuotientSupport
    coordinate_symbols: tuple[str, ...] = field(default_factory=tuple)
    adopted_coordinate_chart: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _require_nonblank(self.name, "name"))
        if self.adopted_coordinate_chart or self.coordinate_symbols:
            raise SpecInvariantError(
                "ChartNamesAreNotCoordinates: a ChartCandidate cannot adopt coordinates"
            )

    @property
    def is_coordinate_chart(self) -> bool:
        return False


@dataclass(frozen=True)
class SourceCover:
    """A source cover assembled from chart candidates and source relations."""

    cover_id: str
    carrier: SourceCarrier
    charts: tuple[ChartCandidate, ...]
    separation_evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_SEPARATION,)

    def __post_init__(self) -> None:
        object.__setattr__(self, "cover_id", _require_nonblank(self.cover_id, "cover_id"))
        if not self.charts:
            raise SpecInvariantError("SourceCover requires at least one ChartCandidate")
        object.__setattr__(
            self,
            "separation_evidence",
            assert_source_only(
                self.separation_evidence,
                invariant_id="SepSrcNoTargetTopology",
            ),
        )


@dataclass(frozen=True)
class ChartSupport:
    """Selected support for a chart candidate under source-only evidence."""

    chart: ChartCandidate
    support: QuotientSupport
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_SUPPORT,)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(self.evidence, invariant_id="ChartNamesAreNotCoordinates"),
        )


@dataclass(frozen=True)
class InverseCheck:
    """Source inverse-token check; not a target-coordinate inverse map."""

    check_id: str
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_INVERSE_TOKEN,)
    passes: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "check_id", _require_nonblank(self.check_id, "check_id"))
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(
                self.evidence,
                invariant_id="TransitionTokensAreNotSmoothMaps",
            ),
        )


@dataclass(frozen=True)
class CocycleCheck:
    """Source cocycle-token check; not a target atlas compatibility proof."""

    check_id: str
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_COCYCLE_TOKEN,)
    passes: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "check_id", _require_nonblank(self.check_id, "check_id"))
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(
                self.evidence,
                invariant_id="TransitionTokensAreNotSmoothMaps",
            ),
        )


@dataclass(frozen=True)
class TransitionToken:
    """Transition token between source chart supports.

    A transition token is not a smooth map. A differentiability claim can be
    recorded only when a source regularity certificate id is supplied.
    """

    token_id: str
    source: ChartSupport
    target: ChartSupport
    inverse_check: InverseCheck | None = None
    cocycle_check: CocycleCheck | None = None
    regularity_certificate_id: str = ""
    differentiability_claim: str = ""
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_TRANSITION_TOKEN,)

    def __post_init__(self) -> None:
        object.__setattr__(self, "token_id", _require_nonblank(self.token_id, "token_id"))
        if self.differentiability_claim and not self.regularity_certificate_id:
            raise SpecInvariantError(
                "TransitionTokensAreNotSmoothMaps: differentiability needs Reg_src evidence"
            )
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(
                self.evidence,
                invariant_id="TransitionTokensAreNotSmoothMaps",
            ),
        )

    @property
    def implies_smooth_map(self) -> bool:
        return False


@dataclass(frozen=True)
class RespReadoutToken:
    """Source readout token separated from empirical detector semantics."""

    token_id: str
    source_token: SourceToken
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_READOUT,)

    def __post_init__(self) -> None:
        object.__setattr__(self, "token_id", _require_nonblank(self.token_id, "token_id"))
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(self.evidence, invariant_id="SolderingNoTargetMetric"),
        )


@dataclass(frozen=True)
class SolderingRelation:
    """Source soldering relation; target metric and proper time are forbidden."""

    relation_id: str
    support: ChartSupport
    readout: RespReadoutToken
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_SOLDERING,)
    target_metric_id: str = ""
    proper_time_id: str = ""
    empirical_detector_semantics_id: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "relation_id", _require_nonblank(self.relation_id, "relation_id"))
        if self.target_metric_id or self.proper_time_id or self.empirical_detector_semantics_id:
            raise SpecInvariantError(
                "SolderingNoTargetMetric: target metric, proper time, and detector semantics are forbidden"
            )
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(self.evidence, invariant_id="SolderingNoTargetMetric"),
        )


@dataclass(frozen=True)
class VariationFamily:
    """Finite source variation family over source-side relations."""

    family_id: str
    cover: SourceCover
    variations: tuple[SourceRelation, ...] = field(default_factory=tuple)
    finite: bool = True
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_VARIATION,)

    def __post_init__(self) -> None:
        object.__setattr__(self, "family_id", _require_nonblank(self.family_id, "family_id"))
        if not self.finite:
            raise SpecInvariantError("VariationFamily is finite-scope only in this Phase 9 spec")
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(self.evidence, invariant_id="SepSrcNoTargetTopology"),
        )


@dataclass(frozen=True)
class RegularityCertificate:
    """Draft/control regularity certificate record, not a formal proof."""

    certificate_id: str
    cover: SourceCover
    transitions: tuple[TransitionToken, ...]
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_REGULARITY,)
    claim_status: str = "draft/control"
    proof_validated: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "certificate_id",
            _require_nonblank(self.certificate_id, "certificate_id"),
        )
        if self.claim_status != "draft/control":
            raise SpecInvariantError("RegularityCertificate remains draft/control")
        if not self.transitions:
            raise SpecInvariantError("RegularityCertificate requires transition tokens")
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(
                self.evidence,
                invariant_id="ValidationIsNotProof",
            ),
        )


@dataclass(frozen=True)
class SolderingCertificate:
    """Draft/control soldering certificate record, not target metric authority."""

    certificate_id: str
    soldering: SolderingRelation
    evidence: tuple[EvidenceKind | str, ...] = (EvidenceKind.SOURCE_SOLDERING,)
    claim_status: str = "draft/control"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "certificate_id",
            _require_nonblank(self.certificate_id, "certificate_id"),
        )
        if self.claim_status != "draft/control":
            raise SpecInvariantError("SolderingCertificate remains draft/control")
        object.__setattr__(
            self,
            "evidence",
            assert_source_only(self.evidence, invariant_id="SolderingNoTargetMetric"),
        )


@dataclass(frozen=True)
class RegSoldLaw:
    """Proposal-only typed interface connecting regularity and soldering."""

    law_id: str
    regularity: RegularityCertificate
    soldering: SolderingCertificate
    variation_family: VariationFamily
    bottom_condition: BottomCondition = BottomCondition.NON_BOTTOM
    claim_status: str = "proposal-only"
    adoption_authorized: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "law_id", _require_nonblank(self.law_id, "law_id"))
        if self.claim_status != "proposal-only":
            raise SpecInvariantError("RegSoldLaw remains proposal-only")
        if self.adoption_authorized:
            raise SpecInvariantError("RegSoldLaw adoption is human-gated and not authorized here")

    def validate_invariants(self) -> tuple[str, ...]:
        """Validate the explicit Phase 9 invariant set."""

        assert_source_only(self.variation_family.evidence, invariant_id="SepSrcNoTargetTopology")
        for chart in self.variation_family.cover.charts:
            if chart.is_coordinate_chart:
                raise SpecInvariantError("ChartNamesAreNotCoordinates")
        for transition in self.regularity.transitions:
            if transition.implies_smooth_map:
                raise SpecInvariantError("TransitionTokensAreNotSmoothMaps")
        assert_source_only(self.soldering.evidence, invariant_id="SolderingNoTargetMetric")
        if validator_pass_can_instantiate_regularization(True):
            raise SpecInvariantError("ValidationIsNotProof")
        return INVARIANT_IDS


def make_regularity_certificate(
    *,
    certificate_id: str,
    cover: SourceCover,
    transitions: Sequence[TransitionToken],
    evidence: Iterable[EvidenceKind | str],
) -> RegularityCertificate:
    """Construct a draft/control certificate only from source-side evidence."""

    normalized = assert_source_only(evidence, invariant_id="ValidationIsNotProof")
    return RegularityCertificate(
        certificate_id=certificate_id,
        cover=cover,
        transitions=tuple(transitions),
        evidence=normalized,
    )


def regularity_certificate_from_validator_pass(
    *,
    certificate_id: str,
    cover: SourceCover,
    transitions: Sequence[TransitionToken],
    validator_pass: bool,
) -> RegularityCertificate:
    """Always fail: validator PASS is not proof or source evidence."""

    raise SpecInvariantError(
        "ValidationIsNotProof: validator PASS cannot instantiate RegularityCertificate"
    )


def check_reg_sold_law(law: RegSoldLaw) -> tuple[str, ...]:
    """Return the invariant ids enforced by a proposal-only RegSoldLaw."""

    return law.validate_invariants()


__all__ = [
    "BottomCondition",
    "ChartCandidate",
    "ChartSupport",
    "CocycleCheck",
    "EvidenceKind",
    "InverseCheck",
    "QuotientSupport",
    "RegularityCertificate",
    "RegSoldLaw",
    "RespReadoutToken",
    "SolderingCertificate",
    "SolderingRelation",
    "SourceCarrier",
    "SourceCover",
    "SourceRelation",
    "SourceToken",
    "SpecInvariantError",
    "TransitionToken",
    "VariationFamily",
    "assert_source_only",
    "check_reg_sold_law",
    "make_regularity_certificate",
    "regularity_certificate_from_validator_pass",
    "validator_pass_can_instantiate_regularization",
]
