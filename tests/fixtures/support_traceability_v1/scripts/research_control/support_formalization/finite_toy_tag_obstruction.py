#!/usr/bin/env python3
"""Support-only finite toy tag-removal obstruction formalization.

This module encodes the existing RT-20260614-055 finite toy tag-removal
obstruction as deterministic project-control tooling. It has
proof_authority=false. A passing report is not canonical ontology, not
Resp_lc adoption, not MetricData(E), not g_eff, not matter coupling, not
Einstein equations, not benchmark promotion, and not completed derivation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


CHECKER_ID = "finite_toy_tag_removal_support_formalization"
CHECKER_VERSION = "0.1.0"
PROOF_AUTHORITY = False
SOURCE_ARTIFACT_PATH = (
    "research_control/tasks/RT-20260614-055/artifacts/"
    "96_RESP_LC_FINITE_TOY_METRIC_RESPONSE_MODEL_REFUTER_STRESS_TEST.tex"
)
SOURCE_ARTIFACT_OBJECT_ID = (
    "TEX-RESEARCH-CONTROL-RESP-LC-FINITE-TOY-METRIC-RESPONSE-MODEL-"
    "REFUTER-STRESS-TEST"
)
SOURCE_ARTIFACT_HASH = (
    "b589c29e440750e0dacaebb5d2ad86fd5bf0b593b7e27645052fcbf55839a161"
)
BOUNDARY_STATEMENT = (
    "This support-only formalization has proof_authority=false. It is not "
    "proof authority, not canonical ontology adoption, not source-law "
    "adoption, not MetricData(E) adoption, not g_eff adoption or scope "
    "expansion, not coupling-law adoption, not matter coupling, not "
    "stress-energy semantics, not a stress-energy tensor, not detector "
    "semantics, not a matter action, not Einstein equations, not benchmark "
    "promotion, and not completed derivation."
)

TOKEN_SWAP = {"a": "b", "b": "a"}


@dataclass(frozen=True)
class TagRecord:
    """Explicit toy source tags (epsilon, lambda, tau)."""

    orientation: int
    normalization: int
    token_semantics: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if self.orientation not in {-1, 1}:
            raise ValueError("orientation must be +1 or -1")
        if self.normalization <= 0:
            raise ValueError("normalization must be positive")
        if not self.token_semantics:
            raise ValueError("token_semantics must be nonempty")


@dataclass(frozen=True)
class TaggedToyObject:
    """Finite tagged toy source object."""

    object_id: str
    carrier: str
    event: str
    tag: TagRecord


@dataclass(frozen=True)
class UntaggedToyObject:
    """The tag-erased finite toy object X_empty."""

    object_id: str = "X_empty"
    carrier: str = "C_toy"
    event: str = "E"


@dataclass(frozen=True)
class ResponseTriple:
    """Partial response relation value (epsilon, lambda, tau)."""

    orientation: int
    normalization: int
    token_semantics: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class PropositionResult:
    proposition_id: str
    status: str
    message: str
    proof_authority: bool = PROOF_AUTHORITY
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence": self.evidence,
            "message": self.message,
            "proof_authority": self.proof_authority,
            "proposition_id": self.proposition_id,
            "status": self.status,
        }


@dataclass(frozen=True)
class FormalizationReport:
    checker_id: str
    checker_version: str
    status: str
    proposition_results: tuple[PropositionResult, ...]
    proof_authority: bool = PROOF_AUTHORITY
    support_only: bool = True
    boundary_statement: str = BOUNDARY_STATEMENT
    source_artifact_path: str = SOURCE_ARTIFACT_PATH
    source_artifact_object_id: str = SOURCE_ARTIFACT_OBJECT_ID
    source_artifact_hash: str = SOURCE_ARTIFACT_HASH
    formal_objects: tuple[str, ...] = (
        "TaggedToyObject",
        "TagRecord",
        "UntaggedToyObject",
        "tag_erasure",
        "partial_response_relation",
        "tag_erasure_makes_response_undefined",
        "no_new_source_data_totalization_obstruction",
    )
    forbidden_authority_flags: dict[str, bool] = field(
        default_factory=lambda: {
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
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_statement": self.boundary_statement,
            "checker_id": self.checker_id,
            "checker_version": self.checker_version,
            "forbidden_authority_flags": self.forbidden_authority_flags,
            "formal_objects": list(self.formal_objects),
            "proof_authority": self.proof_authority,
            "proposition_results": [
                proposition.to_dict() for proposition in self.proposition_results
            ],
            "source_artifact_hash": self.source_artifact_hash,
            "source_artifact_object_id": self.source_artifact_object_id,
            "source_artifact_path": self.source_artifact_path,
            "status": self.status,
            "support_only": self.support_only,
        }


def tau_ab() -> tuple[tuple[str, str], ...]:
    return (("U0", "a"), ("U1", "b"))


def tau_ba() -> tuple[tuple[str, str], ...]:
    return (("U0", "b"), ("U1", "a"))


def finite_toy_family() -> tuple[TaggedToyObject | UntaggedToyObject, ...]:
    """Return the finite family named by the canonical Refuter artifact."""

    return (
        TaggedToyObject("X_plus", "C_toy", "E", TagRecord(1, 1, tau_ab())),
        TaggedToyObject("X_flip", "C_toy", "E", TagRecord(-1, 1, tau_ab())),
        TaggedToyObject("X_scale", "C_toy", "E", TagRecord(1, 2, tau_ab())),
        TaggedToyObject("X_token", "C_toy", "E", TagRecord(1, 1, tau_ba())),
        UntaggedToyObject(),
    )


def tagged_objects(
    family: Iterable[TaggedToyObject | UntaggedToyObject] | None = None,
) -> tuple[TaggedToyObject, ...]:
    objects = finite_toy_family() if family is None else tuple(family)
    return tuple(item for item in objects if isinstance(item, TaggedToyObject))


def untagged_object() -> UntaggedToyObject:
    return UntaggedToyObject()


def tag_erasure(_source_object: TaggedToyObject | UntaggedToyObject) -> UntaggedToyObject:
    """Erase orientation, normalization, and token semantics."""

    return UntaggedToyObject()


def partial_response_relation(
    source_object: TaggedToyObject | UntaggedToyObject,
) -> ResponseTriple | None:
    """Return R_toy on tagged objects and None on the untagged object."""

    if isinstance(source_object, UntaggedToyObject):
        return None
    return ResponseTriple(
        source_object.tag.orientation,
        source_object.tag.normalization,
        source_object.tag.token_semantics,
    )


def _swap_token_map(token_semantics: tuple[tuple[str, str], ...]) -> tuple[tuple[str, str], ...]:
    return tuple((domain, TOKEN_SWAP.get(token, token)) for domain, token in token_semantics)


def tag_erasure_makes_response_undefined() -> PropositionResult:
    """Check the tag-removal collapse proposition."""

    failures: list[str] = []
    for source_object in tagged_objects():
        original_response = partial_response_relation(source_object)
        erased_response = partial_response_relation(tag_erasure(source_object))
        if original_response is None:
            failures.append(f"{source_object.object_id}: original response undefined")
        if erased_response is not None:
            failures.append(f"{source_object.object_id}: erased response defined")

    if failures:
        return PropositionResult(
            proposition_id="tag_erasure_makes_response_undefined",
            status="fail_tag_erasure_defined",
            message="Tag erasure failed to make every response undefined.",
            evidence={"failures": failures},
        )
    return PropositionResult(
        proposition_id="tag_erasure_makes_response_undefined",
        status="pass",
        message="Every tagged toy object maps to X_empty and R_toy is undefined there.",
        evidence={
            "checked_tagged_object_ids": [item.object_id for item in tagged_objects()],
            "erased_object_id": untagged_object().object_id,
        },
    )


def no_new_source_data_totalization_obstruction() -> PropositionResult:
    """Check the sign/token fixed-point obstruction for X_empty."""

    orientations = {-1, 1}
    fixed_orientations = sorted(value for value in orientations if -value == value)
    token_maps = {tau_ab(), tau_ba()}
    fixed_token_maps = sorted(item for item in token_maps if _swap_token_map(item) == item)

    if fixed_orientations or fixed_token_maps:
        return PropositionResult(
            proposition_id="no_new_source_data_totalization_obstruction",
            status="fail_totalization_fixed_point",
            message="A fixed response component was found under sign or token relabeling.",
            evidence={
                "fixed_orientation_count": len(fixed_orientations),
                "fixed_token_map_count": len(fixed_token_maps),
            },
        )
    return PropositionResult(
        proposition_id="no_new_source_data_totalization_obstruction",
        status="pass",
        message=(
            "X_empty is fixed by tag relabeling, but neither sign choice nor the "
            "explicit token maps are fixed without new source data."
        ),
        evidence={
            "fixed_orientation_count": 0,
            "fixed_token_map_count": 0,
            "untagged_object_fixed_under_relabeling": True,
        },
    )


def run_formalization() -> FormalizationReport:
    propositions = (
        tag_erasure_makes_response_undefined(),
        no_new_source_data_totalization_obstruction(),
    )
    status = (
        "pass_support_only"
        if all(proposition.status == "pass" for proposition in propositions)
        else "tooling_error"
    )
    return FormalizationReport(
        checker_id=CHECKER_ID,
        checker_version=CHECKER_VERSION,
        status=status,
        proposition_results=propositions,
    )


def source_artifact_sha256(repo_root: Path) -> str:
    return hashlib.sha256((repo_root / SOURCE_ARTIFACT_PATH).read_bytes()).hexdigest()


def write_json(path: Path, report: FormalizationReport) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the support-only finite toy tag-removal formalization."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    parser.add_argument("--json-output", type=Path, help="write JSON report to this path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_formalization()
    if args.json_output:
        write_json(args.json_output, report)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"{CHECKER_ID}: {report.status}")
    return 0 if report.status == "pass_support_only" else 1


if __name__ == "__main__":
    raise SystemExit(main())
