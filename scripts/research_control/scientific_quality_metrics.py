#!/usr/bin/env python3
"""Evaluate denominator-bound durable scientific-quality diagnostics.

The values produced here are advisory project-control evidence. They summarize
only an explicitly declared eligible population and never establish theorem
truth, scientific status, ontology adoption, physics promotion, or
Distance-to-GR progress.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ID = "durable_scientific_quality_metrics_v1"
EVIDENCE_SCHEMA_ID = "durable_scientific_quality_evidence_v1"
ATTEMPT_LEDGER_PATH = (
    "research_control/tasks/RT-20260721-006/artifacts/"
    "v21_research_attempt_ledger.json"
)
CANDIDATE_LINEAGE_REGISTRY_PATH = (
    "research_control/tasks/RT-20260721-005/artifacts/"
    "v21_candidate_lineage_registry.json"
)
QUALITY_TAXONOMY_PATH = (
    "research_control/tasks/RT-20260723-004/artifacts/"
    "scientific_quality_metric_taxonomy_v1.md"
)
CALIBRATION_POLICY_PATH = (
    "research_control/tasks/RT-20260723-004/artifacts/"
    "scientific_quality_calibration_warning_policy_v1.md"
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
IMMUTABLE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")

METRIC_SPECS: dict[str, dict[str, str]] = {
    "assumption_reduction_rate": {
        "family": "assumption_reduction",
        "identity_kind": "candidate_or_theorem_comparison",
        "definition": (
            "Fraction of eligible identity-bound before/after comparisons that "
            "remove at least one declared assumption without adding an "
            "unaccounted stronger assumption."
        ),
        "qualifier": "eligible comparisons with a validated net assumption reduction",
        "guardrail": (
            "A reduction is scoped to the declared comparison and does not prove "
            "the resulting theorem, candidate, or physical interpretation."
        ),
    },
    "theorem_generality_rate": {
        "family": "theorem_generality",
        "identity_kind": "declared_theorem_application",
        "definition": (
            "Fraction of a theorem's declared eligible application universe that "
            "is covered by explicit, hypothesis-preserving subsumption records."
        ),
        "qualifier": "eligible applications with explicit theorem subsumption",
        "guardrail": (
            "Subsuming a shared coordinate does not reopen, adopt, or prove an "
            "exact historical family."
        ),
    },
    "countermodel_novelty_rate": {
        "family": "countermodel_novelty",
        "identity_kind": "countermodel",
        "definition": (
            "Fraction of eligible countermodels with a distinct immutable "
            "witness identity and a non-duplicate falsified assumption set."
        ),
        "qualifier": "eligible countermodels with distinct witness and burden bindings",
        "guardrail": (
            "Novelty is relative to the declared comparison corpus and is not a "
            "global no-go theorem or theory rejection."
        ),
    },
    "obstruction_unification_and_reuse_rate": {
        "family": "obstruction_unification_and_reuse",
        "identity_kind": "obstruction",
        "definition": (
            "Fraction of eligible immutable obstruction identities that are "
            "explicitly reused by a later tracked result or unified by a "
            "declared stronger scoped obstruction."
        ),
        "qualifier": "eligible obstructions with explicit later reuse or scoped unification",
        "guardrail": (
            "Reuse preserves the original obstruction scope and does not upgrade "
            "it into a global impossibility result."
        ),
    },
    "independent_review_survival_rate": {
        "family": "independent_review_survival",
        "identity_kind": "reviewed_scientific_object",
        "definition": (
            "Fraction of eligible objects receiving a provenance-qualified "
            "independent review that retain a non-promotional scoped result after "
            "all recorded findings are dispositioned."
        ),
        "qualifier": "eligible independently reviewed objects retaining scoped status",
        "guardrail": (
            "Survival is not replication, adoption, proof authority, or a Gate "
            "Chair verdict."
        ),
    },
    "benchmark_breadth_rate": {
        "family": "benchmark_breadth",
        "identity_kind": "benchmark_case",
        "definition": (
            "Fraction of a prospectively declared benchmark universe with "
            "identity-bound results under one fixed assumption contract."
        ),
        "qualifier": "eligible benchmark cases with assumption-compatible results",
        "guardrail": (
            "Breadth does not establish benchmark recovery, physical adequacy, "
            "or promotion."
        ),
    },
    "retraction_repair_visibility_rate": {
        "family": "retraction_repair_visibility",
        "identity_kind": "attempt_event",
        "definition": (
            "Fraction of eligible failed, superseded, repaired, abandoned, or "
            "audit-finding events that remain visible as finalized immutable "
            "ledger records."
        ),
        "qualifier": "eligible rework events visible with valid immutable event bindings",
        "guardrail": (
            "Visibility measures process memory, not scientific merit or "
            "Distance-to-GR progress."
        ),
    },
    "ledger_durability_rate": {
        "family": "ledger_durability",
        "identity_kind": "attempt_event",
        "definition": (
            "Fraction of eligible attempt events whose sequence, payload hash, "
            "event hash, and predecessor binding validate."
        ),
        "qualifier": "eligible attempt events with a valid append-only hash chain",
        "guardrail": (
            "Ledger integrity is project-control evidence only and does not make "
            "the recorded scientific content true."
        ),
    },
}
REQUIRED_METRIC_IDS = tuple(METRIC_SPECS)

AUTHORITY_BOUNDARY = {
    "record_kind": "project_control",
    "metrics_are_advisory": True,
    "aggregate_scientific_truth_score_created": False,
    "scientific_claims_changed": False,
    "distance_to_gr_delta_changed": False,
    "theorem_truth_inferred": False,
    "candidate_adoption_authorized": False,
    "candidate_rejection_authorized": False,
    "ontology_or_source_law_adopted": False,
    "benchmark_promotion_authorized": False,
    "physics_promotion_authorized": False,
    "gate_chair_verdict_created": False,
    "proof_authority": False,
    "publication_authority": False,
    "completed_derivation_authorized": False,
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unknown_metric_evidence(reason: str, source_paths: list[str]) -> dict[str, Any]:
    return {
        "denominator_status": "unknown",
        "eligible_items": [],
        "qualifying_ids": [],
        "calculation_window": "tracked_repository_snapshot",
        "source_paths": sorted(set(source_paths)),
        "uncertainty_note": reason,
    }


def _warning(
    metric_id: str,
    code: str,
    message: str,
    *,
    severity: str = "warning",
    hard_gate: bool = False,
) -> dict[str, Any]:
    return {
        "warning_id": f"{metric_id}:{code}",
        "metric_id": metric_id,
        "code": code,
        "severity": severity,
        "hard_gate": hard_gate,
        "physics_claim_authority": False,
        "message": message,
    }


def _identity_item(
    identity: str,
    identity_sha256: str,
    source_path: str,
    *,
    identity_kind: str,
) -> dict[str, str]:
    return {
        "identity": identity,
        "identity_sha256": identity_sha256,
        "identity_kind": identity_kind,
        "source_path": source_path,
    }


def evaluate_metric(metric_id: str, evidence: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one explicit eligible-set metric record."""

    if metric_id not in METRIC_SPECS:
        raise ValueError(f"unsupported metric_id: {metric_id}")
    spec = METRIC_SPECS[metric_id]
    errors: list[str] = []
    warnings: list[dict[str, Any]] = []
    if not isinstance(evidence, dict):
        evidence = {}
        errors.append("metric evidence must be an object")

    denominator_status = evidence.get("denominator_status")
    eligible_items = evidence.get("eligible_items", [])
    qualifying_ids = evidence.get("qualifying_ids", [])
    source_paths = evidence.get("source_paths", [])
    if not isinstance(source_paths, list):
        source_paths = []
        errors.append("source_paths must be an array")

    if denominator_status not in {"known", "unknown"}:
        errors.append("denominator_status must be known or unknown")
    if not isinstance(eligible_items, list):
        eligible_items = []
        errors.append("eligible_items must be an array")
    if not isinstance(qualifying_ids, list):
        qualifying_ids = []
        errors.append("qualifying_ids must be an array")

    normalized_items: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    binding_to_id: dict[str, str] = {}
    for index, raw_item in enumerate(eligible_items):
        location = f"eligible_items[{index}]"
        if not isinstance(raw_item, dict):
            errors.append(f"{location} must be an object")
            continue
        identity = raw_item.get("identity")
        binding = raw_item.get("identity_sha256")
        identity_kind = raw_item.get("identity_kind")
        source_path = raw_item.get("source_path")
        if not isinstance(identity, str) or not identity.strip():
            errors.append(f"{location}.identity must be nonblank")
            continue
        if identity in seen_ids:
            errors.append(f"duplicate eligible identity: {identity}")
            warnings.append(
                _warning(
                    metric_id,
                    "duplicate_identity",
                    f"Eligible identity {identity} appears more than once.",
                    severity="error",
                    hard_gate=True,
                )
            )
            continue
        seen_ids.add(identity)
        if not isinstance(binding, str) or HEX64.fullmatch(binding) is None:
            errors.append(f"{location}.identity_sha256 must be lowercase SHA-256")
        elif binding in binding_to_id and binding_to_id[binding] != identity:
            errors.append(
                "multiple eligible identities share one immutable binding: "
                f"{binding_to_id[binding]} and {identity}"
            )
            warnings.append(
                _warning(
                    metric_id,
                    "artifact_splitting_or_alias",
                    (
                        f"{binding_to_id[binding]} and {identity} share one identity "
                        "binding; one logical result cannot earn multiple credit."
                    ),
                    severity="error",
                    hard_gate=True,
                )
            )
        elif isinstance(binding, str):
            binding_to_id[binding] = identity
        if identity_kind != spec["identity_kind"]:
            errors.append(
                f"{location}.identity_kind must be {spec['identity_kind']}"
            )
        if not isinstance(source_path, str) or not source_path.strip():
            errors.append(f"{location}.source_path must be nonblank")
        normalized_items.append(
            {
                "identity": identity,
                "identity_sha256": str(binding or ""),
                "identity_kind": str(identity_kind or ""),
                "source_path": str(source_path or ""),
            }
        )

    normalized_qualifying: list[str] = []
    seen_qualifying: set[str] = set()
    for index, identity in enumerate(qualifying_ids):
        if not isinstance(identity, str) or not identity.strip():
            errors.append(f"qualifying_ids[{index}] must be nonblank")
            continue
        if identity in seen_qualifying:
            errors.append(f"duplicate qualifying identity: {identity}")
            warnings.append(
                _warning(
                    metric_id,
                    "duplicate_qualifying_identity",
                    f"Qualifying identity {identity} appears more than once.",
                    severity="error",
                    hard_gate=True,
                )
            )
            continue
        seen_qualifying.add(identity)
        normalized_qualifying.append(identity)
        if identity not in seen_ids:
            errors.append(f"qualifying identity is outside the eligible set: {identity}")
            warnings.append(
                _warning(
                    metric_id,
                    "numerator_outside_denominator",
                    f"Qualifying identity {identity} is not denominator-eligible.",
                    severity="error",
                    hard_gate=True,
                )
            )

    value: float | None = None
    status = "invalid" if errors else "not_measured"
    if denominator_status == "unknown":
        if normalized_items or normalized_qualifying:
            errors.append("unknown denominator cannot contain eligible or qualifying items")
            status = "invalid"
        else:
            warnings.append(
                _warning(
                    metric_id,
                    "unknown_denominator",
                    (
                        "No authoritative eligible-set population is available; "
                        "the metric remains not_measured and is not treated as zero."
                    ),
                )
            )
            status = "invalid" if errors else "not_measured"
    elif denominator_status == "known":
        if not normalized_items:
            warnings.append(
                _warning(
                    metric_id,
                    "empty_eligible_set",
                    (
                        "The eligible set is known but empty; the metric remains "
                        "not_measured and is not treated as zero."
                    ),
                )
            )
            status = "invalid" if errors else "not_measured"
        elif not errors:
            value = round(len(normalized_qualifying) / len(normalized_items), 6)
            status = "measured"

    reported_value = evidence.get("reported_value")
    if reported_value is not None:
        if (
            not isinstance(reported_value, (int, float))
            or isinstance(reported_value, bool)
        ):
            errors.append("reported_value must be numeric when present")
        else:
            reported = float(reported_value)
            if reported < 0.0 or reported > 1.0:
                errors.append("reported_value is outside the logical range [0, 1]")
                warnings.append(
                    _warning(
                        metric_id,
                        "logical_range_violation",
                        f"Reported value {reported} is outside [0, 1].",
                        severity="error",
                        hard_gate=True,
                    )
                )
            elif value is not None and abs(reported - value) > 0.000001:
                errors.append(
                    f"reported_value {reported} does not match computed value {value}"
                )
                warnings.append(
                    _warning(
                        metric_id,
                        "reported_value_mismatch",
                        (
                            f"Reported value {reported} does not match the "
                            f"identity-derived value {value}."
                        ),
                        severity="error",
                        hard_gate=True,
                    )
                )
    if value is not None and not 0.0 <= value <= 1.0:
        errors.append("computed value is outside the logical range [0, 1]")
        warnings.append(
            _warning(
                metric_id,
                "computed_range_violation",
                f"Computed value {value} is outside [0, 1].",
                severity="error",
                hard_gate=True,
            )
        )
    if errors:
        status = "invalid"

    return {
        "metric_id": metric_id,
        "family": spec["family"],
        "status": status,
        "definition": spec["definition"],
        "value": value,
        "numerator": {
            "label": spec["qualifier"],
            "value": len(normalized_qualifying) if denominator_status == "known" else None,
            "qualifying_ids": sorted(normalized_qualifying),
        },
        "denominator": {
            "status": denominator_status,
            "value": len(normalized_items) if denominator_status == "known" else None,
            "eligible_ids": sorted(item["identity"] for item in normalized_items),
            "eligible_items": sorted(
                normalized_items,
                key=lambda item: item["identity"],
            ),
        },
        "calculation_window": str(
            evidence.get("calculation_window") or "tracked_repository_snapshot"
        ),
        "source_paths": sorted(
            set(
                str(path)
                for path in source_paths
                if isinstance(path, str) and path.strip()
            )
            | {
                item["source_path"]
                for item in normalized_items
                if item["source_path"]
            }
        ),
        "uncertainty_note": str(evidence.get("uncertainty_note") or ""),
        "interpretation_guardrail": spec["guardrail"],
        "warnings": warnings,
        "errors": errors,
        "authority_boundary": dict(AUTHORITY_BOUNDARY),
    }


def evaluate_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a complete eight-metric evidence bundle without aggregation."""

    errors: list[str] = []
    if not isinstance(evidence, dict):
        evidence = {}
        errors.append("evidence bundle must be an object")
    if evidence.get("schema_id") != EVIDENCE_SCHEMA_ID:
        errors.append(f"schema_id must be {EVIDENCE_SCHEMA_ID}")
    metric_evidence = evidence.get("metrics")
    if not isinstance(metric_evidence, dict):
        metric_evidence = {}
        errors.append("metrics must be an object")

    missing = sorted(set(REQUIRED_METRIC_IDS) - set(metric_evidence))
    unexpected = sorted(set(metric_evidence) - set(REQUIRED_METRIC_IDS))
    if missing:
        errors.append(f"missing metric evidence: {missing}")
    if unexpected:
        errors.append(f"unexpected metric evidence: {unexpected}")

    metrics: dict[str, dict[str, Any]] = {}
    warnings: list[dict[str, Any]] = []
    for metric_id in REQUIRED_METRIC_IDS:
        record = metric_evidence.get(metric_id)
        if not isinstance(record, dict):
            record = unknown_metric_evidence(
                "Metric evidence is absent.",
                [],
            )
        result = evaluate_metric(metric_id, record)
        metrics[metric_id] = result
        warnings.extend(result["warnings"])
        errors.extend(f"{metric_id}: {item}" for item in result["errors"])

    status_counts: dict[str, int] = {
        status: sum(1 for record in metrics.values() if record["status"] == status)
        for status in ("measured", "not_measured", "invalid")
    }
    return {
        "schema_id": SCHEMA_ID,
        "status": "FAIL" if errors else "PASS",
        "quality_surface": "primary_scientific_quality_diagnostic",
        "raw_volume_is_primary_quality": False,
        "metric_count": len(REQUIRED_METRIC_IDS),
        "status_counts": status_counts,
        "metrics": metrics,
        "warnings": warnings,
        "errors": errors,
        "aggregate_metric": None,
        "aggregate_metric_reason": (
            "Scientific truth and durable quality are not reduced to a scalar score."
        ),
        "source_basis": sorted(
            set(
                str(path)
                for path in evidence.get("source_paths", [])
                if isinstance(path, str) and path.strip()
            )
            | {
                path
                for record in metrics.values()
                for path in record["source_paths"]
            }
        ),
        "authority_boundary": dict(AUTHORITY_BOUNDARY),
    }


def _event_payload(event: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(event)
    for field in ("prior_event_hash", "payload_sha256", "event_hash"):
        payload.pop(field, None)
    return payload


def _expected_event_hashes(
    event: dict[str, Any],
    prior_event_hash: str,
) -> tuple[str, str]:
    payload_sha256 = sha256_value(_event_payload(event))
    event_hash = sha256_value(
        {
            "event_id": event.get("event_id"),
            "sequence": event.get("sequence"),
            "payload_sha256": payload_sha256,
            "prior_event_hash": prior_event_hash,
        }
    )
    return payload_sha256, event_hash


def _attempt_ledger_evidence(repo_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    path = repo_root / ATTEMPT_LEDGER_PATH
    if not path.is_file():
        reason = "The append-only attempt ledger is unavailable."
        return (
            unknown_metric_evidence(reason, [ATTEMPT_LEDGER_PATH]),
            unknown_metric_evidence(reason, [ATTEMPT_LEDGER_PATH]),
        )
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        reason = f"The append-only attempt ledger could not be loaded: {exc}"
        return (
            unknown_metric_evidence(reason, [ATTEMPT_LEDGER_PATH]),
            unknown_metric_evidence(reason, [ATTEMPT_LEDGER_PATH]),
        )
    events = ledger.get("events")
    if not isinstance(events, list):
        reason = "The append-only attempt ledger has no event array."
        return (
            unknown_metric_evidence(reason, [ATTEMPT_LEDGER_PATH]),
            unknown_metric_evidence(reason, [ATTEMPT_LEDGER_PATH]),
        )

    durability_items: list[dict[str, str]] = []
    durability_qualifying: list[str] = []
    visibility_items: list[dict[str, str]] = []
    visibility_qualifying: list[str] = []
    rework_types = {
        "validation_failed",
        "audit_finding",
        "repair_applied",
        "superseded",
        "abandoned",
    }
    prior_hash = ""
    for sequence, event in enumerate(events, start=1):
        if not isinstance(event, dict):
            continue
        event_id = str(event.get("event_id") or f"INVALID-EVENT-{sequence}")
        identity_binding = sha256_value(
            {
                "ledger_id": ledger.get("ledger_id"),
                "event_id": event_id,
                "declared_event_hash": event.get("event_hash"),
            }
        )
        item = _identity_item(
            event_id,
            identity_binding,
            ATTEMPT_LEDGER_PATH,
            identity_kind="attempt_event",
        )
        durability_items.append(item)
        expected_payload, expected_hash = _expected_event_hashes(event, prior_hash)
        event_valid = (
            event.get("sequence") == sequence
            and event.get("prior_event_hash") == prior_hash
            and event.get("payload_sha256") == expected_payload
            and event.get("event_hash") == expected_hash
        )
        if event_valid:
            durability_qualifying.append(event_id)
        if event.get("event_type") in rework_types:
            visibility_items.append(item)
            if (
                event_valid
                and event.get("finalized") is True
                and isinstance(event.get("source_refs"), list)
                and bool(event.get("source_refs"))
            ):
                visibility_qualifying.append(event_id)
        prior_hash = expected_hash

    common = {
        "denominator_status": "known",
        "calculation_window": str(ledger.get("sealed_at") or "ledger_snapshot"),
        "source_paths": [ATTEMPT_LEDGER_PATH],
    }
    visibility = {
        **common,
        "eligible_items": visibility_items,
        "qualifying_ids": visibility_qualifying,
        "uncertainty_note": (
            "The metric covers the sealed ledger population only; it does not "
            "infer unrecorded historical failures."
        ),
    }
    durability = {
        **common,
        "eligible_items": durability_items,
        "qualifying_ids": durability_qualifying,
        "uncertainty_note": (
            "Durability is evaluated against the recorded append-only event chain."
        ),
    }
    return visibility, durability


def _obstruction_reuse_evidence(
    repo_root: Path,
    completion_records: list[dict[str, Any]],
) -> dict[str, Any]:
    first_by_id: dict[str, tuple[int, dict[str, Any]]] = {}
    for index, record in enumerate(completion_records):
        obstruction_id = str(record.get("obstruction_id") or "").strip()
        if (
            obstruction_id
            and IMMUTABLE_ID.fullmatch(obstruction_id) is not None
            and obstruction_id not in first_by_id
        ):
            first_by_id[obstruction_id] = (index, record)

    items: list[dict[str, str]] = []
    qualifying: list[str] = []
    for obstruction_id, (source_index, record) in sorted(first_by_id.items()):
        source_path = str(record.get("completion_path") or "")
        source_file = repo_root / source_path
        source_sha256 = (
            sha256_path(source_file)
            if source_path and source_file.is_file()
            else sha256_value({"missing_source_path": source_path})
        )
        items.append(
            _identity_item(
                obstruction_id,
                sha256_value(
                    {
                        "obstruction_id": obstruction_id,
                        "source_path": source_path,
                        "source_sha256": source_sha256,
                    }
                ),
                source_path or "registries/AGENT_JOB_REGISTRY.csv",
                identity_kind="obstruction",
            )
        )
        if any(
            obstruction_id in str(later.get("text") or "")
            for later in completion_records[source_index + 1 :]
        ):
            qualifying.append(obstruction_id)

    return {
        "denominator_status": "known",
        "eligible_items": items,
        "qualifying_ids": qualifying,
        "calculation_window": "all_tracked_completion_records",
        "source_paths": ["registries/AGENT_JOB_REGISTRY.csv"],
        "uncertainty_note": (
            "The current structured corpus supports explicit later-reference "
            "reuse. It does not infer semantic unification from similar prose."
        ),
    }


def build_repository_evidence(
    repo_root: Path = REPO_ROOT,
    completion_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a conservative live evidence bundle from tracked identity stores."""

    repo_root = Path(repo_root)
    completion_records = completion_records or []
    visibility, durability = _attempt_ledger_evidence(repo_root)
    common_sources = [
        ATTEMPT_LEDGER_PATH,
        CANDIDATE_LINEAGE_REGISTRY_PATH,
        "registries/AGENT_JOB_REGISTRY.csv",
        QUALITY_TAXONOMY_PATH,
        CALIBRATION_POLICY_PATH,
    ]
    metrics = {
        "assumption_reduction_rate": unknown_metric_evidence(
            (
                "Candidate lineage binds assumption hashes but does not yet expose "
                "an authoritative before/after assumption-set eligibility corpus."
            ),
            [CANDIDATE_LINEAGE_REGISTRY_PATH],
        ),
        "theorem_generality_rate": unknown_metric_evidence(
            (
                "The tracked theorem inventory is authoritative prose, but no "
                "normalized immutable theorem-application denominator is present."
            ),
            ["research_control/design/frontier_theorem_inventory.md"],
        ),
        "countermodel_novelty_rate": unknown_metric_evidence(
            (
                "No normalized countermodel witness-identity and falsified-burden "
                "comparison corpus is available."
            ),
            ["registries/AGENT_JOB_REGISTRY.csv"],
        ),
        "obstruction_unification_and_reuse_rate": _obstruction_reuse_evidence(
            repo_root,
            completion_records,
        ),
        "independent_review_survival_rate": unknown_metric_evidence(
            (
                "Review calibration records do not constitute executed independent "
                "review, and no authoritative review-survival denominator is present."
            ),
            [
                "research_control/tasks/RT-20260722-008/artifacts/"
                "reviewer_agreement_calibration_report.json"
            ],
        ),
        "benchmark_breadth_rate": unknown_metric_evidence(
            (
                "No prospectively fixed identity-bound benchmark universe is "
                "available for this measurement window."
            ),
            ["registries/AGENT_JOB_REGISTRY.csv"],
        ),
        "retraction_repair_visibility_rate": visibility,
        "ledger_durability_rate": durability,
    }
    return {
        "schema_id": EVIDENCE_SCHEMA_ID,
        "source_paths": common_sources,
        "metrics": metrics,
    }


def build_repository_report(
    repo_root: Path = REPO_ROOT,
    completion_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return evaluate_evidence(
        build_repository_evidence(
            repo_root,
            completion_records=completion_records,
        )
    )
