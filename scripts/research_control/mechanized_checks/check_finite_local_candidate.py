#!/usr/bin/env python3
"""Support-only checker for finite/local source-side candidate fixtures.

This mechanized report is support-only scaffolding. It is not proof authority,
not source-law adoption, not `MetricData(E)` adoption, not `g_eff` adoption or
scope expansion, not matter coupling, not stress-energy semantics, not a
stress-energy tensor, not a matter action, not Einstein equations, not
benchmark promotion, and not completed derivation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence


RESEARCH_CONTROL_DIR = Path(__file__).resolve().parents[1]
if str(RESEARCH_CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_DIR))

import strict_yaml  # noqa: E402


CHECKER_ID = "finite_local_candidate_checker"
CHECKER_VERSION = "0.1.0"
BOUNDARY_STATEMENT = (
    "This mechanized report is support-only scaffolding. It is not proof authority, "
    "not source-law adoption, not `MetricData(E)` adoption, not `g_eff` adoption or "
    "scope expansion, not matter coupling, not stress-energy semantics, not a "
    "stress-energy tensor, not a matter action, not Einstein equations, not "
    "benchmark promotion, and not completed derivation."
)

CONTROLLED_STATUSES = (
    "pass_support_only",
    "fail_malformed_fixture",
    "fail_target_import",
    "fail_evidence_as_adoption",
    "fail_geff_overread",
    "fail_process_authority_overread",
    "fail_relabeling_invariance",
    "fail_variation_stability",
    "bottom",
    "tooling_error",
)

STATUS_PRIORITY = (
    "tooling_error",
    "fail_malformed_fixture",
    "fail_target_import",
    "fail_evidence_as_adoption",
    "fail_geff_overread",
    "fail_process_authority_overread",
    "fail_relabeling_invariance",
    "fail_variation_stability",
    "bottom",
)

REQUIRED_SECTIONS = (
    "metadata",
    "source_family",
    "source_objects",
    "relations",
    "boundary_markers",
    "candidate",
    "variation_relabeling",
    "forbidden_imports",
)

REQUIRED_FALSE_IMPORTS = (
    "target_metric",
    "target_atlas",
    "target_topology",
    "lorentzian_signature",
    "proper_time",
    "stress_energy_semantics",
    "stress_energy_tensor",
    "matter_action",
    "detector_semantics",
    "einstein_equations",
    "benchmark_success",
    "source_law_adoption",
    "MetricData_E_adoption",
    "g_eff_adoption",
)

FORBIDDEN_KEY_FRAGMENTS = (
    "target_metric",
    "target_atlas",
    "target_topology",
    "lorentzian_signature",
    "proper_time",
    "stress_energy",
    "matter_action",
    "detector_semantics",
    "einstein",
    "benchmark_success",
    "source_law_adoption",
    "metricdata",
    "metric_data",
    "g_eff",
    "geff",
    "coupling_law_adoption",
    "matter_coupling",
)

CONTROLLED_OBSTRUCTION_LABELS = {
    "none",
    "bottom",
    "target_import",
    "evidence_as_adoption",
    "geff_overread",
    "process_authority_overread",
    "relabeling_invariance_failure",
    "variation_stability_failure",
    "malformed_fixture",
    "source_side_obstruction",
}

ALLOWED_VARIATION_RESULTS = {
    "preserved",
    "bottom",
    "controlled_obstruction",
}


class CheckerInputError(ValueError):
    """Raised when a fixture cannot be parsed into the required map shape."""


@dataclass(frozen=True)
class PredicateResult:
    predicate: str
    status: str
    message: str
    path: str = ""
    status_code: str = ""
    overread_flag: str = ""

    def to_dict(self) -> dict[str, str]:
        output = {
            "predicate": self.predicate,
            "status": self.status,
            "message": self.message,
        }
        if self.path:
            output["path"] = self.path
        if self.status_code:
            output["status_code"] = self.status_code
        if self.overread_flag:
            output["overread_flag"] = self.overread_flag
        return output


@dataclass
class CheckerReport:
    checker_id: str
    checker_version: str
    fixture_id: str
    fixture_hash: str
    status: str
    predicate_results: list[PredicateResult] = field(default_factory=list)
    obstruction_labels: list[str] = field(default_factory=list)
    forbidden_overread_flags: list[str] = field(default_factory=list)
    boundary_statement: str = BOUNDARY_STATEMENT
    source_artifact_refs: list[str] = field(default_factory=list)
    tooling_error: bool = False
    physics_obstruction: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_statement": self.boundary_statement,
            "checker_id": self.checker_id,
            "checker_version": self.checker_version,
            "fixture_hash": self.fixture_hash,
            "fixture_id": self.fixture_id,
            "forbidden_overread_flags": self.forbidden_overread_flags,
            "obstruction_labels": self.obstruction_labels,
            "physics_obstruction": self.physics_obstruction,
            "predicate_results": [
                predicate.to_dict() for predicate in self.predicate_results
            ],
            "source_artifact_refs": self.source_artifact_refs,
            "status": self.status,
            "tooling_error": self.tooling_error,
        }


def _as_map(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _text(value: Any) -> str:
    return str(value).strip()


def _ids(items: Sequence[Any]) -> set[str]:
    return {
        _text(item.get("id", ""))
        for item in items
        if isinstance(item, dict) and _text(item.get("id", ""))
    }


def _dedupe_sorted(values: Sequence[str]) -> list[str]:
    return sorted({value for value in values if value})


def _pass(predicate: str, message: str, path: str = "") -> PredicateResult:
    return PredicateResult(predicate=predicate, status="pass", message=message, path=path)


def _fail(
    predicate: str,
    status_code: str,
    message: str,
    path: str = "",
    overread_flag: str = "",
) -> PredicateResult:
    return PredicateResult(
        predicate=predicate,
        status="fail",
        message=message,
        path=path,
        status_code=status_code,
        overread_flag=overread_flag,
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_fixture(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if path.suffix == ".json" or stripped.startswith("{"):
        parsed = json.loads(text)
    else:
        parsed = strict_yaml.loads(text)
    if not isinstance(parsed, dict):
        raise CheckerInputError("top-level fixture must be a map")
    return parsed


def _walk(value: Any, path: str = "") -> list[tuple[str, Any]]:
    rows = [(path, value)]
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            rows.extend(_walk(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.extend(_walk(child, f"{path}[{index}]"))
    return rows


def predicate_fixture_is_finite(data: Mapping[str, Any]) -> PredicateResult:
    for section in REQUIRED_SECTIONS:
        if section not in data:
            return _fail(
                "fixture_is_finite",
                "fail_malformed_fixture",
                f"missing required section {section!r}",
                section,
            )
        if not isinstance(data[section], dict):
            return _fail(
                "fixture_is_finite",
                "fail_malformed_fixture",
                f"section {section!r} must be a map",
                section,
            )
    for path, value in _walk(data):
        if value is None:
            return _fail(
                "fixture_is_finite",
                "fail_malformed_fixture",
                "null values are not allowed in finite explicit fixtures",
                path,
            )
    family = _as_map(data.get("source_family"))
    objects = _as_map(data.get("source_objects"))
    required_lists = {
        "source_family.parameters": family.get("parameters"),
        "source_family.sectors": family.get("sectors"),
        "source_objects.tokens": objects.get("tokens"),
        "source_objects.states": objects.get("states"),
    }
    for path, value in required_lists.items():
        if not isinstance(value, list):
            return _fail(
                "fixture_is_finite",
                "fail_malformed_fixture",
                f"{path} must be an explicit finite list",
                path,
            )
    return _pass("fixture_is_finite", "fixture has explicit finite top-level support")


def predicate_sectors_nonempty_or_bottom(data: Mapping[str, Any]) -> PredicateResult:
    sectors = [_text(item) for item in _as_list(_as_map(data.get("source_family")).get("sectors"))]
    tokens = _as_list(_as_map(data.get("source_objects")).get("tokens"))
    bottom_triggers = {
        _text(row.get("trigger", ""))
        for row in _as_list(_as_map(data.get("relations")).get("bottom_results"))
        if isinstance(row, dict) and _text(row.get("result", "")) == "bottom"
    }
    for sector in sectors:
        has_token = any(isinstance(token, dict) and token.get("sector") == sector for token in tokens)
        if not has_token and f"empty_sector:{sector}" not in bottom_triggers:
            return _fail(
                "sectors_nonempty_or_bottom",
                "fail_malformed_fixture",
                f"sector {sector!r} has no token and no bottom branch",
                "source_family.sectors",
            )
    return _pass("sectors_nonempty_or_bottom", "declared sectors are nonempty or bottomed")


def predicate_token_state_references_resolve(data: Mapping[str, Any]) -> PredicateResult:
    objects = _as_map(data.get("source_objects"))
    token_ids = _ids(_as_list(objects.get("tokens")))
    state_ids = _ids(_as_list(objects.get("states")))
    if not token_ids or not state_ids:
        return _fail(
            "token_state_references_resolve",
            "fail_malformed_fixture",
            "tokens and states must both be nonempty",
            "source_objects",
        )
    for state in _as_list(objects.get("states")):
        if not isinstance(state, dict):
            continue
        token = _text(state.get("token", ""))
        if token not in token_ids:
            return _fail(
                "token_state_references_resolve",
                "fail_malformed_fixture",
                f"state {state.get('id', '')!r} references unknown token {token!r}",
                "source_objects.states",
            )
    for carrier in _as_list(objects.get("carriers")):
        if not isinstance(carrier, dict):
            continue
        for token in _as_list(carrier.get("tokens")):
            if _text(token) not in token_ids:
                return _fail(
                    "token_state_references_resolve",
                    "fail_malformed_fixture",
                    f"carrier {carrier.get('id', '')!r} references unknown token {token!r}",
                    "source_objects.carriers",
                )
        for state in _as_list(carrier.get("states")):
            if _text(state) not in state_ids:
                return _fail(
                    "token_state_references_resolve",
                    "fail_malformed_fixture",
                    f"carrier {carrier.get('id', '')!r} references unknown state {state!r}",
                    "source_objects.carriers",
                )
    return _pass("token_state_references_resolve", "token and state references resolve")


def predicate_balance_flux_closed_or_bottom(data: Mapping[str, Any]) -> PredicateResult:
    objects = _as_map(data.get("source_objects"))
    token_ids = _ids(_as_list(objects.get("tokens")))
    state_ids = _ids(_as_list(objects.get("states")))
    relations = _as_map(data.get("relations"))
    balance_ids = _ids(_as_list(relations.get("balance_predicates")))
    if not balance_ids:
        return _fail(
            "balance_flux_closed_or_bottom",
            "fail_malformed_fixture",
            "balance_predicates must be nonempty",
            "relations.balance_predicates",
        )
    for balance in _as_list(relations.get("balance_predicates")):
        if not isinstance(balance, dict):
            continue
        result = _text(balance.get("result", ""))
        if result not in {"balanced", "bottom", "controlled_obstruction"}:
            return _fail(
                "balance_flux_closed_or_bottom",
                "fail_malformed_fixture",
                f"balance predicate {balance.get('id', '')!r} has unsupported result {result!r}",
                "relations.balance_predicates",
            )
        missing = [_text(token) for token in _as_list(balance.get("support_tokens")) if _text(token) not in token_ids]
        if missing and result != "bottom":
            return _fail(
                "balance_flux_closed_or_bottom",
                "fail_malformed_fixture",
                f"balance predicate {balance.get('id', '')!r} references unknown tokens {missing}",
                "relations.balance_predicates.support_tokens",
            )
    for row in _as_list(relations.get("flux_ledger")):
        if not isinstance(row, dict):
            continue
        if _text(row.get("source_state", "")) not in state_ids:
            return _fail(
                "balance_flux_closed_or_bottom",
                "fail_malformed_fixture",
                f"flux row {row.get('id', '')!r} has unknown source_state",
                "relations.flux_ledger.source_state",
            )
        if _text(row.get("target_state", "")) not in state_ids:
            return _fail(
                "balance_flux_closed_or_bottom",
                "fail_malformed_fixture",
                f"flux row {row.get('id', '')!r} has unknown target_state",
                "relations.flux_ledger.target_state",
            )
        if _text(row.get("token", "")) not in token_ids:
            return _fail(
                "balance_flux_closed_or_bottom",
                "fail_malformed_fixture",
                f"flux row {row.get('id', '')!r} has unknown token",
                "relations.flux_ledger.token",
            )
        if _text(row.get("balance_id", "")) not in balance_ids:
            return _fail(
                "balance_flux_closed_or_bottom",
                "fail_malformed_fixture",
                f"flux row {row.get('id', '')!r} has unknown balance_id",
                "relations.flux_ledger.balance_id",
            )
    return _pass("balance_flux_closed_or_bottom", "balance and flux rows close over finite support")


def predicate_bottom_result_totality(data: Mapping[str, Any]) -> PredicateResult:
    bottom_results = _as_list(_as_map(data.get("relations")).get("bottom_results"))
    if not bottom_results:
        return _fail(
            "bottom_result_totality",
            "fail_malformed_fixture",
            "at least one controlled bottom result is required",
            "relations.bottom_results",
        )
    for row in bottom_results:
        if not isinstance(row, dict):
            continue
        label = _text(row.get("obstruction_label", ""))
        if not _text(row.get("id", "")) or not _text(row.get("trigger", "")):
            return _fail(
                "bottom_result_totality",
                "fail_malformed_fixture",
                "bottom result must name id and trigger",
                "relations.bottom_results",
            )
        if _text(row.get("result", "")) != "bottom":
            return _fail(
                "bottom_result_totality",
                "fail_malformed_fixture",
                "bottom result must fail closed with result=bottom",
                "relations.bottom_results.result",
            )
        if label not in CONTROLLED_OBSTRUCTION_LABELS:
            return _fail(
                "bottom_result_totality",
                "fail_malformed_fixture",
                f"bottom result uses uncontrolled label {label!r}",
                "relations.bottom_results.obstruction_label",
            )
        if not _as_list(row.get("blocked_overread")):
            return _fail(
                "bottom_result_totality",
                "fail_process_authority_overread",
                "bottom result must list blocked overreads",
                "relations.bottom_results.blocked_overread",
                "process_authority_as_proof",
            )
    return _pass("bottom_result_totality", "bottom results are total and fail closed")


def predicate_no_target_import_keys_absent(data: Mapping[str, Any]) -> PredicateResult:
    imports = _as_map(data.get("forbidden_imports"))
    for key in REQUIRED_FALSE_IMPORTS:
        if imports.get(key) is not False:
            return _fail(
                "no_target_import_keys_absent",
                "fail_target_import",
                f"forbidden import marker {key!r} must be explicitly false",
                f"forbidden_imports.{key}",
                key,
            )

    allowed_forbidden_paths = {
        "forbidden_imports",
        "boundary_markers.scoped_geff_boundary",
    }
    for path, value in _walk(data):
        if not path or path in allowed_forbidden_paths or path.startswith("forbidden_imports."):
            continue
        key = path.rsplit(".", 1)[-1].split("[", 1)[0].lower()
        if any(fragment in key for fragment in FORBIDDEN_KEY_FRAGMENTS):
            return _fail(
                "no_target_import_keys_absent",
                "fail_target_import",
                f"forbidden target or downstream authority key {key!r} appears outside forbidden_imports",
                path,
                key,
            )
    return _pass("no_target_import_keys_absent", "forbidden target-facing keys are absent or false")


def predicate_bridge_compatibility_marker_declared(data: Mapping[str, Any]) -> PredicateResult:
    markers = _as_map(data.get("boundary_markers"))
    if markers.get("bridge_compatibility") != "scoped_source_extension_evidence_precondition_only":
        return _fail(
            "bridge_compatibility_marker_declared",
            "fail_evidence_as_adoption",
            "bridge compatibility must be scoped evidence/precondition only",
            "boundary_markers.bridge_compatibility",
            "evidence_as_adoption",
        )
    if markers.get("no_target_import") is not True:
        return _fail(
            "bridge_compatibility_marker_declared",
            "fail_target_import",
            "no_target_import marker must be true",
            "boundary_markers.no_target_import",
            "target_import",
        )
    return _pass("bridge_compatibility_marker_declared", "bridge marker is scoped support only")


def predicate_scoped_geff_boundary_marker_blocks_adoption(data: Mapping[str, Any]) -> PredicateResult:
    marker = _as_map(data.get("boundary_markers")).get("scoped_geff_boundary")
    if marker != "no_adoption_no_scope_expansion":
        return _fail(
            "scoped_geff_boundary_marker_blocks_adoption",
            "fail_geff_overread",
            "scoped g_eff boundary must state no adoption and no scope expansion",
            "boundary_markers.scoped_geff_boundary",
            "geff_overread",
        )
    return _pass("scoped_geff_boundary_marker_blocks_adoption", "g_eff boundary blocks adoption")


def predicate_evidence_not_adoption_marker_present(data: Mapping[str, Any]) -> PredicateResult:
    if _as_map(data.get("boundary_markers")).get("evidence_not_adoption") is not True:
        return _fail(
            "evidence_not_adoption_marker_present",
            "fail_evidence_as_adoption",
            "accepted evidence must not be read as adoption",
            "boundary_markers.evidence_not_adoption",
            "evidence_as_adoption",
        )
    return _pass("evidence_not_adoption_marker_present", "evidence-as-adoption overread is blocked")


def predicate_process_authority_not_proof_marker_present(data: Mapping[str, Any]) -> PredicateResult:
    if _as_map(data.get("boundary_markers")).get("process_authority_not_proof") is not True:
        return _fail(
            "process_authority_not_proof_marker_present",
            "fail_process_authority_overread",
            "process authority must not be read as proof",
            "boundary_markers.process_authority_not_proof",
            "process_authority_as_proof",
        )
    return _pass("process_authority_not_proof_marker_present", "process-authority-as-proof overread is blocked")


def predicate_relabeling_maps_are_bijections(data: Mapping[str, Any]) -> PredicateResult:
    for relabeling in _as_list(_as_map(data.get("variation_relabeling")).get("relabelings")):
        if not isinstance(relabeling, dict):
            continue
        domain = [_text(item) for item in _as_list(relabeling.get("domain"))]
        codomain = [_text(item) for item in _as_list(relabeling.get("codomain"))]
        pairs = _as_list(relabeling.get("map"))
        if sorted(domain) != sorted(codomain):
            return _fail(
                "relabeling_maps_are_bijections_on_declared_finite_sets",
                "fail_relabeling_invariance",
                f"relabeling {relabeling.get('id', '')!r} domain and codomain differ",
                "variation_relabeling.relabelings",
            )
        seen_from: set[str] = set()
        seen_to: set[str] = set()
        for pair in pairs:
            if not isinstance(pair, dict):
                continue
            left = _text(pair.get("from", ""))
            right = _text(pair.get("to", ""))
            if left not in domain or right not in codomain:
                return _fail(
                    "relabeling_maps_are_bijections_on_declared_finite_sets",
                    "fail_relabeling_invariance",
                    f"relabeling {relabeling.get('id', '')!r} maps outside declared support",
                    "variation_relabeling.relabelings.map",
                )
            seen_from.add(left)
            seen_to.add(right)
        if sorted(seen_from) != sorted(domain) or sorted(seen_to) != sorted(codomain):
            return _fail(
                "relabeling_maps_are_bijections_on_declared_finite_sets",
                "fail_relabeling_invariance",
                f"relabeling {relabeling.get('id', '')!r} is not bijective",
                "variation_relabeling.relabelings.map",
            )
    return _pass("relabeling_maps_are_bijections_on_declared_finite_sets", "relabelings are finite bijections")


def predicate_restriction_maps_preserve_references(data: Mapping[str, Any]) -> PredicateResult:
    objects = _as_map(data.get("source_objects"))
    known = set()
    known.update(_ids(_as_list(objects.get("tokens"))))
    known.update(_ids(_as_list(objects.get("states"))))
    known.update(_ids(_as_list(objects.get("carriers"))))
    for restriction in _as_list(_as_map(data.get("relations")).get("restriction_maps")):
        if not isinstance(restriction, dict):
            continue
        for pair in _as_list(restriction.get("maps")):
            if not isinstance(pair, dict):
                continue
            if _text(pair.get("from", "")) not in known or _text(pair.get("to", "")) not in known:
                return _fail(
                    "restriction_maps_preserve_declared_references",
                    "fail_malformed_fixture",
                    f"restriction {restriction.get('id', '')!r} maps unknown references",
                    "relations.restriction_maps.maps",
                )
    return _pass("restriction_maps_preserve_declared_references", "restriction maps preserve declared references")


def predicate_finite_variations_have_allowed_results(data: Mapping[str, Any]) -> PredicateResult:
    for variation in _as_list(_as_map(data.get("variation_relabeling")).get("finite_variations")):
        if not isinstance(variation, dict):
            continue
        result = _text(variation.get("result", ""))
        if result not in ALLOWED_VARIATION_RESULTS:
            return _fail(
                "finite_variations_have_allowed_results",
                "fail_variation_stability",
                f"finite variation {variation.get('id', '')!r} has unsupported result {result!r}",
                "variation_relabeling.finite_variations.result",
            )
        if result == "preserved" and not _as_list(variation.get("preserves")):
            return _fail(
                "finite_variations_have_allowed_results",
                "fail_variation_stability",
                f"finite variation {variation.get('id', '')!r} preserves no predicates",
                "variation_relabeling.finite_variations.preserves",
            )
        if result != "preserved" and not _text(variation.get("obstruction_label", "")):
            return _fail(
                "finite_variations_have_allowed_results",
                "fail_variation_stability",
                f"finite variation {variation.get('id', '')!r} needs an obstruction label",
                "variation_relabeling.finite_variations.obstruction_label",
            )
    return _pass("finite_variations_have_allowed_results", "finite variations preserve predicates or fail closed")


def predicate_candidate_map_domain_codomain_declared(data: Mapping[str, Any]) -> PredicateResult:
    objects = _as_map(data.get("source_objects"))
    token_ids = _ids(_as_list(objects.get("tokens")))
    state_ids = _ids(_as_list(objects.get("states")))
    candidate_map = _as_map(_as_map(data.get("candidate")).get("candidate_map"))
    domain = [_text(item) for item in _as_list(candidate_map.get("domain"))]
    codomain = [_text(item) for item in _as_list(candidate_map.get("codomain"))]
    if not domain or not codomain:
        return _fail(
            "candidate_map_domain_codomain_declared",
            "fail_malformed_fixture",
            "candidate map must declare finite domain and codomain",
            "candidate.candidate_map",
        )
    if any(item not in token_ids for item in domain):
        return _fail(
            "candidate_map_domain_codomain_declared",
            "fail_malformed_fixture",
            "candidate map domain must use declared tokens",
            "candidate.candidate_map.domain",
        )
    if any(item not in state_ids for item in codomain):
        return _fail(
            "candidate_map_domain_codomain_declared",
            "fail_malformed_fixture",
            "candidate map codomain must use declared states",
            "candidate.candidate_map.codomain",
        )
    return _pass("candidate_map_domain_codomain_declared", "candidate map uses declared finite supports")


def predicate_certificate_object_references_declared(data: Mapping[str, Any]) -> PredicateResult:
    metadata = _as_map(data.get("metadata"))
    objects = _as_map(data.get("source_objects"))
    candidate = _as_map(data.get("candidate"))
    known = set(_as_list(metadata.get("source_artifact_paths")))
    known.update(_ids(_as_list(objects.get("tokens"))))
    known.update(_ids(_as_list(objects.get("states"))))
    known.update(_ids(_as_list(objects.get("carriers"))))
    candidate_map = _as_map(candidate.get("candidate_map"))
    if _text(candidate_map.get("id", "")):
        known.add(_text(candidate_map.get("id", "")))
    certificate = _as_map(candidate.get("certificate_object"))
    for ref in _as_list(certificate.get("references")):
        if _text(ref) not in known:
            return _fail(
                "certificate_object_references_declared",
                "fail_malformed_fixture",
                f"certificate references undeclared object {ref!r}",
                "candidate.certificate_object.references",
            )
    return _pass("certificate_object_references_declared", "certificate references declared objects only")


def predicate_obstruction_labels_from_controlled_vocabulary(data: Mapping[str, Any]) -> PredicateResult:
    labels = [_text(label) for label in _as_list(_as_map(data.get("candidate")).get("obstruction_labels"))]
    for label in labels:
        if label not in CONTROLLED_OBSTRUCTION_LABELS:
            return _fail(
                "obstruction_labels_from_controlled_vocabulary",
                "fail_malformed_fixture",
                f"uncontrolled obstruction label {label!r}",
                "candidate.obstruction_labels",
            )
    return _pass("obstruction_labels_from_controlled_vocabulary", "obstruction labels are controlled")


def predicate_report_disclaimer_exact_match(data: Mapping[str, Any]) -> PredicateResult:
    observed = _as_map(data.get("metadata")).get("boundary_statement")
    if observed != BOUNDARY_STATEMENT:
        return _fail(
            "report_disclaimer_exact_match",
            "fail_process_authority_overread",
            "fixture boundary statement must match the report disclaimer exactly",
            "metadata.boundary_statement",
            "process_authority_as_proof",
        )
    return _pass("report_disclaimer_exact_match", "boundary statement matches exactly")


def predicate_deterministic_output_order(_: Mapping[str, Any]) -> PredicateResult:
    return _pass("deterministic_output_order", "checker emits predicate and JSON fields in deterministic order")


PREDICATES = (
    predicate_fixture_is_finite,
    predicate_sectors_nonempty_or_bottom,
    predicate_token_state_references_resolve,
    predicate_balance_flux_closed_or_bottom,
    predicate_bottom_result_totality,
    predicate_no_target_import_keys_absent,
    predicate_bridge_compatibility_marker_declared,
    predicate_scoped_geff_boundary_marker_blocks_adoption,
    predicate_evidence_not_adoption_marker_present,
    predicate_process_authority_not_proof_marker_present,
    predicate_relabeling_maps_are_bijections,
    predicate_restriction_maps_preserve_references,
    predicate_finite_variations_have_allowed_results,
    predicate_candidate_map_domain_codomain_declared,
    predicate_certificate_object_references_declared,
    predicate_obstruction_labels_from_controlled_vocabulary,
    predicate_report_disclaimer_exact_match,
    predicate_deterministic_output_order,
)


def select_status(results: Sequence[PredicateResult]) -> str:
    codes = {result.status_code for result in results if result.status == "fail"}
    if not codes:
        return "pass_support_only"
    for code in STATUS_PRIORITY:
        if code in codes:
            return code
    return "fail_malformed_fixture"


def check_fixture(
    data: Mapping[str, Any],
    *,
    fixture_hash: str = "",
) -> CheckerReport:
    metadata = _as_map(data.get("metadata"))
    predicate_results = [predicate(data) for predicate in PREDICATES]
    status = select_status(predicate_results)
    labels = [_text(label) for label in _as_list(_as_map(data.get("candidate")).get("obstruction_labels"))]
    labels.extend(
        _text(row.get("obstruction_label", ""))
        for row in _as_list(_as_map(data.get("relations")).get("bottom_results"))
        if isinstance(row, dict)
    )
    overread_flags = [
        result.overread_flag for result in predicate_results if result.overread_flag
    ]
    physics_obstruction = ""
    if status == "bottom":
        physics_obstruction = "fixture_local_bottom_only"
    return CheckerReport(
        checker_id=CHECKER_ID,
        checker_version=CHECKER_VERSION,
        fixture_id=_text(metadata.get("fixture_id", "")) or "unknown_fixture",
        fixture_hash=fixture_hash,
        status=status,
        predicate_results=predicate_results,
        obstruction_labels=_dedupe_sorted(labels),
        forbidden_overread_flags=_dedupe_sorted(overread_flags),
        boundary_statement=BOUNDARY_STATEMENT,
        source_artifact_refs=sorted(_text(path) for path in _as_list(metadata.get("source_artifact_paths")) if _text(path)),
        tooling_error=False,
        physics_obstruction=physics_obstruction,
    )


def malformed_report(fixture_path: Path, message: str, *, status: str = "fail_malformed_fixture") -> CheckerReport:
    return CheckerReport(
        checker_id=CHECKER_ID,
        checker_version=CHECKER_VERSION,
        fixture_id=fixture_path.stem,
        fixture_hash=sha256_file(fixture_path) if fixture_path.exists() else "",
        status=status,
        predicate_results=[
            _fail(
                "fixture_is_finite",
                status,
                message,
                str(fixture_path),
            )
        ],
        obstruction_labels=["malformed_fixture"],
        forbidden_overread_flags=[],
        boundary_statement=BOUNDARY_STATEMENT,
        source_artifact_refs=[],
        tooling_error=status == "tooling_error",
        physics_obstruction="",
    )


def check_path(path: Path) -> CheckerReport:
    data = load_fixture(path)
    return check_fixture(data, fixture_hash=sha256_file(path))


def json_text(report: CheckerReport) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"


def markdown_text(report: CheckerReport) -> str:
    lines = [
        "# Finite/Local Candidate Checker Report",
        "",
        BOUNDARY_STATEMENT,
        "",
        f"- Checker: `{report.checker_id}`",
        f"- Version: `{report.checker_version}`",
        f"- Fixture: `{report.fixture_id}`",
        f"- Status: `{report.status}`",
        f"- Fixture hash: `{report.fixture_hash}`",
        "",
        "## Predicate Results",
        "",
    ]
    for result in report.predicate_results:
        lines.append(
            f"- `{result.predicate}`: `{result.status}`"
            + (f" ({result.status_code})" if result.status_code else "")
            + f" - {result.message}"
        )
    lines.extend(
        [
            "",
            "## Authority",
            "",
            "This report is reproducibility support only. It does not promote any physics state.",
            "",
        ]
    )
    return "\n".join(lines)


def write_if_requested(path: Path | None, text: str) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True, type=Path, help="Finite/local YAML or JSON fixture")
    parser.add_argument("--json", action="store_true", help="Emit JSON report on stdout")
    parser.add_argument("--json-output", type=Path, help="Write JSON report to a file")
    parser.add_argument("--markdown", type=Path, help="Write a Markdown report to a file")
    args = parser.parse_args(argv)

    try:
        report = check_path(args.fixture)
    except (CheckerInputError, strict_yaml.StrictYamlError, json.JSONDecodeError, OSError) as exc:
        report = malformed_report(args.fixture, str(exc))

    output = json_text(report)
    write_if_requested(args.json_output, output)
    write_if_requested(args.markdown, markdown_text(report))
    if args.json or not args.markdown:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
