"""Deterministic aggregate transaction receipts for validation evidence.

The aggregate layer consumes existing planner and execution receipts.  It does
not select gates, execute commands, change child outcomes, or confer source,
scientific, ontology, benchmark, proof, or Gate Chair authority.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Mapping, Sequence


SCHEMA_ID = "validation_transaction_aggregate_receipt_v1"
SCHEMA_VERSION = 1
GATE_STATUSES = (
    "PASS",
    "FAIL",
    "WARN",
    "SKIP_NOT_APPLICABLE",
    "SKIP_SUPERSEDED",
    "CACHE_HIT",
    "BLOCKED_CONFIGURATION",
)
CACHE_STATUSES = ("NOT_ELIGIBLE", "MISS", "HIT", "BYPASSED")
SOURCE_KINDS = ("role", "skill", "profile", "checkpoint")
MODES = ("legacy", "shadow", "planner")
SUPPORTED_CHILD_RECEIPT_SCHEMAS = {
    "validation_execution_receipt_v1",
    "validation_run_receipt_v1",
}
_RAW_OUTPUT_KEYS = {"stdout", "stderr", "stdout_tail", "stderr_tail"}
_STATUS_PRIORITY = {
    "BLOCKED_CONFIGURATION": 4,
    "FAIL": 3,
    "WARN": 2,
    "PASS": 1,
    "CACHE_HIT": 1,
    "SKIP_NOT_APPLICABLE": 1,
    "SKIP_SUPERSEDED": 1,
}
_AUTHORITY = {
    "scope": "operational_validation_only",
    "source_authoritative": False,
    "child_receipts_authoritative": False,
    "physics_claim_authority": False,
    "ontology_authority": False,
    "benchmark_authority": False,
    "proof_authority": False,
    "gate_chair_authority": False,
}


class AggregateReceiptError(ValueError):
    """Raised when inputs cannot be represented without guessing."""


def _nonblank(value: object, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AggregateReceiptError(f"{context} must be a nonblank string")
    return value


def _bool(value: object, context: str) -> bool:
    if not isinstance(value, bool):
        raise AggregateReceiptError(f"{context} must be a boolean")
    return value


def _string_array(
    value: object,
    context: str,
    *,
    deterministic_sort: bool = False,
) -> list[str]:
    if not isinstance(value, (list, tuple)) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise AggregateReceiptError(f"{context} must be an array of nonblank strings")
    result = list(value)
    if len(result) != len(set(result)):
        raise AggregateReceiptError(f"{context} contains duplicates")
    return sorted(result) if deterministic_sort else result


def _canonical_bytes(value: object, context: str) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise AggregateReceiptError(f"{context} is not canonical JSON: {error}") from error


def _sha256(value: object, context: str) -> tuple[str, int]:
    payload = _canonical_bytes(value, context)
    return f"sha256:{hashlib.sha256(payload).hexdigest()}", len(payload)


def _normalized_path(value: object, context: str) -> str:
    text = _nonblank(value, context)
    if "\\" in text or "\x00" in text:
        raise AggregateReceiptError(f"{context} is not a normalized relative path")
    path = PurePosixPath(text)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise AggregateReceiptError(f"{context} is not a normalized relative path")
    return path.as_posix()


def _reject_embedded_raw_output(value: object, context: str) -> None:
    if isinstance(value, Mapping):
        forbidden = sorted(_RAW_OUTPUT_KEYS & set(value))
        if forbidden:
            raise AggregateReceiptError(
                f"{context} embeds forbidden raw output fields: {forbidden}"
            )
        for key, child in value.items():
            _reject_embedded_raw_output(child, f"{context}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_embedded_raw_output(child, f"{context}[{index}]")


def _hash_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    try:
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)
                size += len(chunk)
    except OSError as error:
        raise AggregateReceiptError(f"artifact hash failed for {path}: {error}") from error
    return f"sha256:{digest.hexdigest()}", size


def _blocker(
    blockers: list[dict[str, str]],
    code: str,
    message: str,
    *,
    subject: str = "",
) -> None:
    record = {"code": code, "message": " ".join(message.split())}
    if subject:
        record["subject"] = subject
    blockers.append(record)


def _plan_entries(plan: Mapping[str, object]) -> dict[str, Mapping[str, object]]:
    entries = plan.get("entries", [])
    if not isinstance(entries, (list, tuple)):
        raise AggregateReceiptError("plan.entries must be an array")
    by_gate: dict[str, Mapping[str, object]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            raise AggregateReceiptError(f"plan.entries[{index}] must be an object")
        gate_id = entry.get("gate_id")
        if gate_id is None:
            continue
        gate_text = _nonblank(gate_id, f"plan.entries[{index}].gate_id")
        if gate_text in by_gate:
            raise AggregateReceiptError(f"duplicate plan entry for gate {gate_text}")
        by_gate[gate_text] = entry
    return by_gate


def _cache_status(result: Mapping[str, object], gate_status: str) -> str:
    explicit = result.get("cache_status")
    if explicit is not None:
        if explicit not in CACHE_STATUSES:
            raise AggregateReceiptError(f"unsupported cache_status: {explicit}")
        if gate_status == "CACHE_HIT" and explicit != "HIT":
            raise AggregateReceiptError("CACHE_HIT result must report cache_status HIT")
        if gate_status != "CACHE_HIT" and explicit == "HIT":
            raise AggregateReceiptError("only CACHE_HIT may report cache_status HIT")
        return str(explicit)
    if gate_status == "CACHE_HIT":
        return "HIT"
    if gate_status.startswith("SKIP_"):
        return "NOT_ELIGIBLE"
    return "MISS" if result.get("cache_eligible") is True else "NOT_ELIGIBLE"


def _duration_ms(result: Mapping[str, object]) -> int:
    if "duration_ms" in result:
        value = result["duration_ms"]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise AggregateReceiptError("gate duration_ms must be a nonnegative integer")
        return value
    value = result.get("duration_seconds", 0)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        raise AggregateReceiptError("gate duration_seconds must be nonnegative")
    return round(float(value) * 1000)


def _output_bytes(result: Mapping[str, object]) -> int:
    if "output_bytes" in result:
        value = result["output_bytes"]
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise AggregateReceiptError("gate output_bytes must be a nonnegative integer")
        return value
    total = 0
    for field in ("stdout_bytes", "stderr_bytes"):
        value = result.get(field, 0)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise AggregateReceiptError(f"gate {field} must be a nonnegative integer")
        total += value
    return total


def _normalize_gate_result(
    result: Mapping[str, object],
    *,
    receipt_id: str,
    plan_entry: Mapping[str, object] | None,
) -> dict[str, object]:
    gate_id = _nonblank(result.get("gate_id"), "gate_result.gate_id")
    status = _nonblank(result.get("status"), f"{gate_id}.status")
    if status not in GATE_STATUSES:
        raise AggregateReceiptError(f"unsupported gate status: {status}")
    severity = _nonblank(result.get("severity", "blocking"), f"{gate_id}.severity")
    if severity not in {"blocking", "advisory", "diagnostic", "local_only"}:
        raise AggregateReceiptError(f"unsupported gate severity: {severity}")

    result_reasons = result.get("plan_reasons", [])
    if not isinstance(result_reasons, (list, tuple)):
        raise AggregateReceiptError(f"{gate_id}.plan_reasons must be an array")
    entry_reasons: object = [] if plan_entry is None else plan_entry.get("reasons", [])
    reasons = sorted(
        set(_string_array(result_reasons, f"{gate_id}.plan_reasons"))
        | set(_string_array(entry_reasons, f"{gate_id}.entry_reasons"))
    )
    obligations = result.get(
        "satisfied_obligation_ids",
        result.get("satisfied_obligations", []),
    )
    child_gates = result.get("child_gate_ids", result.get("child_gates", []))
    raw_artifact_ids = result.get("raw_artifact_ids", [])
    return {
        "gate_id": gate_id,
        "status": status,
        "severity": severity,
        "reason": str(result.get("reason", "")),
        "plan_reasons": reasons,
        "satisfied_obligation_ids": _string_array(
            obligations,
            f"{gate_id}.satisfied_obligation_ids",
            deterministic_sort=True,
        ),
        "child_gate_ids": _string_array(
            child_gates,
            f"{gate_id}.child_gate_ids",
            deterministic_sort=True,
        ),
        "duration_ms": _duration_ms(result),
        "output_bytes": _output_bytes(result),
        "cache_status": _cache_status(result, status),
        "child_receipt_id": receipt_id,
        "raw_artifact_ids": _string_array(
            raw_artifact_ids,
            f"{gate_id}.raw_artifact_ids",
            deterministic_sort=True,
        ),
    }


def _child_receipt_refs(
    child_receipts: Sequence[Mapping[str, object]],
    plan_entries: Mapping[str, Mapping[str, object]],
    blockers: list[dict[str, str]],
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]], bool]:
    refs: list[dict[str, object]] = []
    gate_results: dict[str, dict[str, object]] = {}
    cancelled = False
    seen_receipts: set[str] = set()
    for index, wrapper in enumerate(child_receipts):
        if not isinstance(wrapper, Mapping):
            raise AggregateReceiptError(f"child_receipts[{index}] must be an object")
        payload = wrapper.get("receipt")
        if not isinstance(payload, Mapping):
            raise AggregateReceiptError(f"child_receipts[{index}].receipt must be an object")
        _reject_embedded_raw_output(payload, f"child_receipts[{index}].receipt")
        schema_id = _nonblank(payload.get("schema_id"), f"child_receipts[{index}].schema_id")
        if schema_id not in SUPPORTED_CHILD_RECEIPT_SCHEMAS:
            raise AggregateReceiptError(f"unsupported child receipt schema_id: {schema_id}")
        schema_version = payload.get("schema_version")
        if schema_version != 1 or isinstance(schema_version, bool):
            raise AggregateReceiptError(
                f"unsupported child receipt schema_version: {schema_version}"
            )
        receipt_id = _nonblank(
            wrapper.get("receipt_id", payload.get("run_id")),
            f"child_receipts[{index}].receipt_id",
        )
        if receipt_id in seen_receipts:
            raise AggregateReceiptError(f"duplicate child receipt_id: {receipt_id}")
        seen_receipts.add(receipt_id)
        path = _normalized_path(wrapper.get("path"), f"{receipt_id}.path")
        content_hash, content_bytes = _sha256(payload, f"{receipt_id}.receipt")
        refs.append(
            {
                "artifact_id": f"child-receipt:{receipt_id}",
                "kind": "child_receipt",
                "path": path,
                "content_hash": content_hash,
                "bytes": content_bytes,
                "schema_id": schema_id,
                "status": str(payload.get("status", "")),
                "local_only": _bool(
                    wrapper.get("local_only", True),
                    f"{receipt_id}.local_only",
                ),
                "authoritative": False,
            }
        )

        raw_gate_results = payload.get("gate_results", [])
        if not isinstance(raw_gate_results, (list, tuple)):
            raise AggregateReceiptError(f"{receipt_id}.gate_results must be an array")
        receipt_statuses: list[str] = []
        for result_index, raw_result in enumerate(raw_gate_results):
            if not isinstance(raw_result, Mapping):
                raise AggregateReceiptError(
                    f"{receipt_id}.gate_results[{result_index}] must be an object"
                )
            gate_id = _nonblank(
                raw_result.get("gate_id"),
                f"{receipt_id}.gate_results[{result_index}].gate_id",
            )
            if gate_id in gate_results:
                raise AggregateReceiptError(f"duplicate gate result across children: {gate_id}")
            normalized = _normalize_gate_result(
                raw_result,
                receipt_id=receipt_id,
                plan_entry=plan_entries.get(gate_id),
            )
            gate_results[gate_id] = normalized
            receipt_statuses.append(str(normalized["status"]))

        child_cancelled = payload.get("cancelled", False)
        if not isinstance(child_cancelled, bool):
            raise AggregateReceiptError(f"{receipt_id}.cancelled must be a boolean")
        cancelled = cancelled or child_cancelled
        derived = _aggregate_gate_status(receipt_statuses, force_blocked=child_cancelled)
        declared = str(payload.get("status", ""))
        if declared not in {"PASS", "WARN", "FAIL", "BLOCKED_CONFIGURATION"}:
            _blocker(
                blockers,
                "CHILD_STATUS_UNSUPPORTED",
                f"Child receipt declares unsupported aggregate status {declared!r}.",
                subject=receipt_id,
            )
        elif declared != derived:
            _blocker(
                blockers,
                "CHILD_STATUS_MISMATCH",
                f"Child receipt declares {declared} but its gate evidence derives {derived}.",
                subject=receipt_id,
            )
    refs.sort(key=lambda item: str(item["artifact_id"]))
    return refs, gate_results, cancelled


def _raw_artifact_refs(
    raw_artifacts: Sequence[Mapping[str, object]],
    *,
    artifact_root: Path,
) -> list[dict[str, object]]:
    refs: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_artifacts):
        if not isinstance(raw, Mapping):
            raise AggregateReceiptError(f"raw_artifacts[{index}] must be an object")
        artifact_id = _nonblank(raw.get("artifact_id"), f"raw_artifacts[{index}].artifact_id")
        if artifact_id in seen:
            raise AggregateReceiptError(f"duplicate raw artifact_id: {artifact_id}")
        seen.add(artifact_id)
        path = _normalized_path(raw.get("path"), f"{artifact_id}.path")
        root = Path(artifact_root).resolve()
        candidate = (root / path).resolve()
        if not candidate.is_relative_to(root):
            raise AggregateReceiptError(f"{artifact_id}.path escapes artifact_root")
        content_hash, content_bytes = _hash_file(candidate)
        refs.append(
            {
                "artifact_id": artifact_id,
                "kind": _nonblank(raw.get("kind"), f"{artifact_id}.kind"),
                "path": path,
                "content_hash": content_hash,
                "bytes": content_bytes,
                "local_only": _bool(raw.get("local_only", True), f"{artifact_id}.local_only"),
                "authoritative": False,
                "description": _nonblank(
                    raw.get("description", "Hashed raw validation evidence."),
                    f"{artifact_id}.description",
                ),
            }
        )
    refs.sort(key=lambda item: str(item["artifact_id"]))
    return refs


def _aggregate_gate_status(statuses: Sequence[str], *, force_blocked: bool = False) -> str:
    if force_blocked or not statuses:
        return "BLOCKED_CONFIGURATION"
    priority = max(_STATUS_PRIORITY[status] for status in statuses)
    return {
        4: "BLOCKED_CONFIGURATION",
        3: "FAIL",
        2: "WARN",
        1: "PASS",
    }[priority]


def _obligation_coverage(
    obligations: Sequence[Mapping[str, object]],
    gate_results: Mapping[str, Mapping[str, object]],
    blockers: list[dict[str, str]],
) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, obligation in enumerate(obligations):
        if not isinstance(obligation, Mapping):
            raise AggregateReceiptError(f"obligations[{index}] must be an object")
        obligation_id = _nonblank(
            obligation.get("obligation_id"),
            f"obligations[{index}].obligation_id",
        )
        if obligation_id in seen:
            raise AggregateReceiptError(f"duplicate obligation_id: {obligation_id}")
        seen.add(obligation_id)
        source_kind = _nonblank(
            obligation.get("source_kind"),
            f"{obligation_id}.source_kind",
        )
        if source_kind not in SOURCE_KINDS:
            raise AggregateReceiptError(f"unsupported obligation source_kind: {source_kind}")
        required = _bool(obligation.get("required", True), f"{obligation_id}.required")
        candidate_gate_ids = _string_array(
            obligation.get("candidate_gate_ids", []),
            f"{obligation_id}.candidate_gate_ids",
            deterministic_sort=True,
        )
        providers = sorted(
            gate_id
            for gate_id, result in gate_results.items()
            if obligation_id in result["satisfied_obligation_ids"]
            and result["status"] in {"PASS", "CACHE_HIT"}
        )
        invalid_claims = sorted(
            gate_id
            for gate_id, result in gate_results.items()
            if obligation_id in result["satisfied_obligation_ids"]
            and result["status"] not in {"PASS", "CACHE_HIT"}
        )
        condition_false = obligation.get("condition_proven_false", False)
        if not isinstance(condition_false, bool):
            raise AggregateReceiptError(
                f"{obligation_id}.condition_proven_false must be a boolean"
            )
        evidence = str(obligation.get("condition_evidence", "")).strip()

        if invalid_claims:
            coverage_status = "BLOCKED"
            _blocker(
                blockers,
                "OBLIGATION_INVALID_PROVIDER",
                "A non-passing or skipped gate claimed obligation satisfaction.",
                subject=f"{obligation_id}:{','.join(invalid_claims)}",
            )
        elif providers:
            coverage_status = "SATISFIED"
        elif not required and condition_false and evidence:
            coverage_status = "NOT_APPLICABLE_PROVEN"
        else:
            coverage_status = "BLOCKED"
            reason = (
                "Required obligation has no PASS or CACHE_HIT provider."
                if required
                else "Non-applicability lacks explicit condition-false evidence."
            )
            _blocker(
                blockers,
                "OBLIGATION_UNCOVERED",
                reason,
                subject=obligation_id,
            )
        rows.append(
            {
                "obligation_id": obligation_id,
                "source_kind": source_kind,
                "required": required,
                "coverage_status": coverage_status,
                "provider_gate_ids": providers,
                "invalid_provider_gate_ids": invalid_claims,
                "candidate_gate_ids": candidate_gate_ids,
                "condition_proven_false": condition_false,
                "condition_evidence": evidence,
            }
        )
    if not rows:
        _blocker(
            blockers,
            "OBLIGATION_TABLE_EMPTY",
            "The transaction supplied no role skill profile or checkpoint obligations.",
        )
    rows.sort(key=lambda row: (str(row["source_kind"]), str(row["obligation_id"])))
    status_counts = Counter(str(row["coverage_status"]) for row in rows)
    source_counts = Counter(str(row["source_kind"]) for row in rows)
    return {
        "rows": rows,
        "counts": {
            "total": len(rows),
            "satisfied": status_counts["SATISFIED"],
            "not_applicable_proven": status_counts["NOT_APPLICABLE_PROVEN"],
            "blocked": status_counts["BLOCKED"],
            "by_source_kind": {kind: source_counts[kind] for kind in SOURCE_KINDS},
        },
    }


def _generator_changes(
    values: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, value in enumerate(values):
        if not isinstance(value, Mapping):
            raise AggregateReceiptError(f"generator_changes[{index}] must be an object")
        generator_id = _nonblank(
            value.get("generator_id"),
            f"generator_changes[{index}].generator_id",
        )
        if generator_id in seen:
            raise AggregateReceiptError(f"duplicate generator_id: {generator_id}")
        seen.add(generator_id)
        normalized.append(
            {
                "generator_id": generator_id,
                "status": _nonblank(value.get("status"), f"{generator_id}.status"),
                "changed_paths": _string_array(
                    value.get("changed_paths", []),
                    f"{generator_id}.changed_paths",
                    deterministic_sort=True,
                ),
                "before_tree_hash": str(value.get("before_tree_hash", "")),
                "after_tree_hash": str(value.get("after_tree_hash", "")),
            }
        )
    return sorted(normalized, key=lambda item: str(item["generator_id"]))


def _shadow_receipt(
    shadow: Mapping[str, object],
    blockers: list[dict[str, str]],
) -> dict[str, object]:
    status = _nonblank(shadow.get("status"), "shadow_comparison.status")
    if status not in {"MATCH", "MISMATCH", "NOT_APPLICABLE"}:
        raise AggregateReceiptError(f"unsupported shadow comparison status: {status}")
    affected = _string_array(
        shadow.get("affected_blocking_gate_ids", []),
        "shadow_comparison.affected_blocking_gate_ids",
        deterministic_sort=True,
    )
    unexplained = _bool(
        shadow.get("unexplained_mismatch", False),
        "shadow_comparison.unexplained_mismatch",
    )
    if affected and status != "MATCH":
        _blocker(
            blockers,
            "SHADOW_BLOCKING_MISMATCH",
            "Affected blocking gates do not have legacy/planner MATCH evidence.",
            subject=",".join(affected),
        )
    if unexplained:
        _blocker(
            blockers,
            "SHADOW_UNEXPLAINED_MISMATCH",
            "Legacy/planner comparison contains an unexplained mismatch.",
        )
    if not affected and status == "MISMATCH":
        _blocker(
            blockers,
            "SHADOW_SCOPE_MISMATCH",
            "A mismatch was reported without naming an affected blocking gate.",
        )
    payload = {
        "status": status,
        "legacy_status": str(shadow.get("legacy_status", "")),
        "planner_status": str(shadow.get("planner_status", "")),
        "affected_blocking_gate_ids": affected,
        "unexplained_mismatch": unexplained,
        "evidence": str(shadow.get("evidence", "")),
    }
    payload["content_hash"], _ = _sha256(payload, "shadow_comparison")
    return payload


def aggregate_transaction_receipt(
    *,
    transaction_id: str,
    mode: str,
    profile: str,
    scope: str,
    base_ref: str,
    staged_tree_hash: str,
    classification: Mapping[str, object],
    plan: Mapping[str, object],
    child_receipts: Sequence[Mapping[str, object]],
    obligations: Sequence[Mapping[str, object]],
    generator_changes: Sequence[Mapping[str, object]] = (),
    raw_artifacts: Sequence[Mapping[str, object]] = (),
    artifact_root: Path = Path("."),
    residue: Mapping[str, object],
    rollback: Mapping[str, object],
    shadow_comparison: Mapping[str, object],
) -> dict[str, object]:
    """Build one complete fail-closed aggregate receipt.

    Child receipts are provided as ``{"receipt_id", "path", "receipt"}``
    wrappers.  Their canonical JSON is hashed and referenced, never embedded.
    Raw artifacts are hashed from normalized paths beneath ``artifact_root``.
    """

    transaction_id = _nonblank(transaction_id, "transaction_id")
    if mode not in MODES:
        raise AggregateReceiptError(f"unsupported mode: {mode}")
    profile = _nonblank(profile, "profile")
    scope = _nonblank(scope, "scope")
    base_ref = _nonblank(base_ref, "base_ref")
    staged_tree_hash = _nonblank(staged_tree_hash, "staged_tree_hash")
    if not isinstance(classification, Mapping):
        raise AggregateReceiptError("classification must be an object")
    if not isinstance(plan, Mapping):
        raise AggregateReceiptError("plan must be an object")
    if not isinstance(residue, Mapping):
        raise AggregateReceiptError("residue must be an object")
    if not isinstance(rollback, Mapping):
        raise AggregateReceiptError("rollback must be an object")
    if not isinstance(shadow_comparison, Mapping):
        raise AggregateReceiptError("shadow_comparison must be an object")
    _reject_embedded_raw_output(classification, "classification")
    _reject_embedded_raw_output(plan, "plan")

    blockers: list[dict[str, str]] = []
    selected_gate_ids = _string_array(
        plan.get("ordered_gate_ids", []),
        "plan.ordered_gate_ids",
    )
    declared_selected_gate_ids = _string_array(
        plan.get("selected_gate_ids", selected_gate_ids),
        "plan.selected_gate_ids",
    )
    superseded_gate_ids = _string_array(
        plan.get("superseded_gate_ids", []),
        "plan.superseded_gate_ids",
    )
    plan_skipped_gate_ids = _string_array(
        plan.get("skipped_gate_ids", []),
        "plan.skipped_gate_ids",
    )
    if set(declared_selected_gate_ids) != set(selected_gate_ids):
        raise AggregateReceiptError(
            "plan selected_gate_ids and ordered_gate_ids must contain the same gates"
        )
    if set(plan_skipped_gate_ids) & set(selected_gate_ids):
        raise AggregateReceiptError("selected and skipped plan gates must be disjoint")
    if set(superseded_gate_ids) - set(selected_gate_ids):
        raise AggregateReceiptError("superseded gates must be selected")
    entries = _plan_entries(plan)
    child_refs, results_by_gate, cancelled = _child_receipt_refs(
        child_receipts,
        entries,
        blockers,
    )

    unknown_gate_ids = sorted(set(results_by_gate) - set(selected_gate_ids))
    if unknown_gate_ids:
        _blocker(
            blockers,
            "UNSELECTED_GATE_EXECUTED",
            "Child receipts contain gates absent from the selected plan.",
            subject=",".join(unknown_gate_ids),
        )
    unaccounted_gate_ids = [
        gate_id for gate_id in selected_gate_ids if gate_id not in results_by_gate
    ]
    if unaccounted_gate_ids:
        _blocker(
            blockers,
            "SELECTED_GATE_UNACCOUNTED",
            "Selected gates have no result or explicit skip evidence.",
            subject=",".join(unaccounted_gate_ids),
        )

    ordered_result_ids = [
        gate_id for gate_id in selected_gate_ids if gate_id in results_by_gate
    ] + unknown_gate_ids
    gate_results = [results_by_gate[gate_id] for gate_id in ordered_result_ids]
    executed_gate_ids = [
        str(result["gate_id"])
        for result in gate_results
        if not str(result["status"]).startswith("SKIP_")
    ]
    selected_skip_ids = [
        str(result["gate_id"])
        for result in gate_results
        if str(result["status"]).startswith("SKIP_")
    ]
    skipped_gate_ids = list(
        dict.fromkeys(plan_skipped_gate_ids + selected_skip_ids)
    )
    observed_superseded = [
        str(result["gate_id"])
        for result in gate_results
        if result["status"] == "SKIP_SUPERSEDED"
    ]
    if set(observed_superseded) - set(superseded_gate_ids):
        _blocker(
            blockers,
            "SUPERSEDENCE_UNDECLARED",
            "A child reported SKIP_SUPERSEDED without planner supersedence.",
            subject=",".join(sorted(set(observed_superseded) - set(superseded_gate_ids))),
        )

    raw_refs = _raw_artifact_refs(raw_artifacts, artifact_root=Path(artifact_root))
    child_artifact_ids = {str(item["artifact_id"]) for item in child_refs}
    raw_artifact_ids = {str(item["artifact_id"]) for item in raw_refs}
    if child_artifact_ids & raw_artifact_ids:
        raise AggregateReceiptError("child and raw artifact IDs must be disjoint")
    for result in gate_results:
        missing_refs = sorted(set(result["raw_artifact_ids"]) - raw_artifact_ids)
        if missing_refs:
            _blocker(
                blockers,
                "RAW_ARTIFACT_REFERENCE_MISSING",
                "Gate result names a raw artifact without a hashed reference.",
                subject=f"{result['gate_id']}:{','.join(missing_refs)}",
            )

    coverage = _obligation_coverage(obligations, results_by_gate, blockers)
    generators = _generator_changes(generator_changes)
    shadow = _shadow_receipt(shadow_comparison, blockers)

    classification_hash, _ = _sha256(classification, "classification")
    plan_hash, _ = _sha256(plan, "plan")
    changed_paths = _string_array(
        classification.get("changed_paths", []),
        "classification.changed_paths",
        deterministic_sort=True,
    )
    path_tags = _string_array(
        classification.get("path_family_tags", []),
        "classification.path_family_tags",
        deterministic_sort=True,
    )
    blocked_paths = _string_array(
        classification.get("blocked_paths", []),
        "classification.blocked_paths",
        deterministic_sort=True,
    )
    if blocked_paths or str(plan.get("status", "")) == "BLOCKED_CONFIGURATION":
        _blocker(
            blockers,
            "PLAN_BLOCKED",
            "Classifier or planner reports blocked configuration.",
            subject=",".join(blocked_paths),
        )

    residue_status = _nonblank(residue.get("status"), "residue.status")
    residue_paths = _string_array(
        residue.get("paths", residue.get("changed_paths", [])),
        "residue.paths",
        deterministic_sort=True,
    )
    if residue_status != "CLEAN" or residue_paths:
        _blocker(
            blockers,
            "FINAL_RESIDUE_NOT_CLEAN",
            "Final transaction residue is not clean.",
            subject=",".join(residue_paths),
        )
    residue_receipt = {
        "status": residue_status,
        "paths": residue_paths,
        "evidence": str(residue.get("evidence", "")),
    }

    rollback_required = _bool(rollback.get("required", False), "rollback.required")
    rollback_performed = _bool(rollback.get("performed", False), "rollback.performed")
    if rollback_required and not rollback_performed:
        _blocker(
            blockers,
            "ROLLBACK_REQUIRED_NOT_PERFORMED",
            "Rollback is required but has not been performed.",
        )
    rollback_receipt = {
        "required": rollback_required,
        "performed": rollback_performed,
        "authority": str(rollback.get("authority", "")),
        "reason": str(rollback.get("reason", "")),
        "before_tree_hash": str(rollback.get("before_tree_hash", "")),
        "after_tree_hash": str(rollback.get("after_tree_hash", "")),
        "changed_paths": _string_array(
            rollback.get("changed_paths", []),
            "rollback.changed_paths",
            deterministic_sort=True,
        ),
    }

    statuses = [str(result["status"]) for result in gate_results]
    aggregate_status = _aggregate_gate_status(
        statuses,
        force_blocked=bool(blockers) or cancelled or rollback_performed,
    )
    if rollback_performed:
        outcome = "rolled_back"
    elif cancelled:
        outcome = "cancelled"
    elif unaccounted_gate_ids:
        outcome = "partial"
    elif "BLOCKED_CONFIGURATION" in statuses:
        outcome = "blocked"
    elif "FAIL" in statuses:
        outcome = "failed"
    elif blockers:
        outcome = "blocked"
    elif aggregate_status == "WARN":
        outcome = "complete_with_warnings"
    else:
        outcome = "complete"

    status_counts = Counter(statuses)
    cache_counts = Counter(str(result["cache_status"]) for result in gate_results)
    performance = {
        "duration_ms": sum(int(result["duration_ms"]) for result in gate_results),
        "output_bytes": sum(int(result["output_bytes"]) for result in gate_results),
        "subprocess_count": sum(
            not str(result["status"]).startswith("SKIP_") for result in gate_results
        ),
        "cache_hits": cache_counts["HIT"],
        "cache_misses": cache_counts["MISS"],
        "child_receipt_bytes": sum(int(item["bytes"]) for item in child_refs),
        "raw_artifact_bytes": sum(int(item["bytes"]) for item in raw_refs),
    }
    blockers.sort(
        key=lambda item: (
            item["code"],
            item.get("subject", ""),
            item["message"],
        )
    )
    receipt: dict[str, object] = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "transaction_id": transaction_id,
        "mode": mode,
        "migration_epoch": str(plan.get("migration_epoch", "shadow_planner")),
        "profile": profile,
        "scope": scope,
        "base_ref": base_ref,
        "staged_tree_hash": staged_tree_hash,
        "status": aggregate_status,
        "outcome": outcome,
        "classification": {
            "content_hash": classification_hash,
            "changed_paths": changed_paths,
            "path_family_tags": path_tags,
            "blocked_paths": blocked_paths,
        },
        "plan": {
            "content_hash": plan_hash,
            "status": str(plan.get("status", "")),
            "execution_authority": str(plan.get("execution_authority", "")),
            "selected_gate_ids": selected_gate_ids,
            "executed_gate_ids": executed_gate_ids,
            "skipped_gate_ids": skipped_gate_ids,
            "superseded_gate_ids": superseded_gate_ids,
            "unaccounted_gate_ids": unaccounted_gate_ids,
        },
        "gate_results": gate_results,
        "obligation_coverage": coverage,
        "generator_changes": generators,
        "artifacts": child_refs + raw_refs,
        "shadow_comparison": shadow,
        "final_tree_identity": {
            "staged_tree_hash": staged_tree_hash,
            "residue": residue_receipt,
        },
        "rollback": rollback_receipt,
        "performance": performance,
        "counts": {
            "selected_gate_count": len(selected_gate_ids),
            "executed_gate_count": len(executed_gate_ids),
            "skipped_gate_count": len(skipped_gate_ids),
            "superseded_gate_count": len(superseded_gate_ids),
            "unaccounted_gate_count": len(unaccounted_gate_ids),
            "status_counts": {
                status: status_counts[status] for status in GATE_STATUSES
            },
            "blocker_count": len(blockers),
        },
        "blockers": blockers,
        "authority": dict(_AUTHORITY),
        "output_policy": {
            "raw_stdout_stderr_embedded": False,
            "child_receipts_embedded": False,
            "complete_json_available": True,
        },
    }
    receipt["receipt_hash"], _ = _sha256(receipt, "aggregate_receipt")
    return receipt


def canonical_json(receipt: Mapping[str, object]) -> str:
    """Render the complete aggregate receipt as deterministic compact JSON."""

    if receipt.get("schema_id") != SCHEMA_ID or receipt.get("schema_version") != 1:
        raise AggregateReceiptError("unsupported aggregate receipt schema")
    return _canonical_bytes(receipt, "aggregate_receipt").decode("utf-8")


def _single_line(value: object, limit: int = 240) -> str:
    text = " ".join(str(value).split())
    encoded = text.encode("utf-8")
    if len(encoded) <= limit:
        return text
    prefix = encoded[: max(0, limit - 3)]
    while True:
        try:
            return prefix.decode("utf-8") + "..."
        except UnicodeDecodeError:
            prefix = prefix[:-1]


def render_console_summary(
    receipt: Mapping[str, object],
    *,
    max_blockers: int = 5,
    byte_budget: int = 2048,
) -> str:
    """Render a bounded deterministic summary while leaving full JSON separate."""

    if not isinstance(max_blockers, int) or not 0 <= max_blockers <= 10:
        raise AggregateReceiptError("max_blockers must be from 0 through 10")
    if not isinstance(byte_budget, int) or byte_budget < 256:
        raise AggregateReceiptError("byte_budget must be at least 256")
    counts = receipt.get("counts")
    coverage = receipt.get("obligation_coverage")
    if not isinstance(counts, Mapping) or not isinstance(coverage, Mapping):
        raise AggregateReceiptError("receipt lacks aggregate counts")
    coverage_counts = coverage.get("counts")
    if not isinstance(coverage_counts, Mapping):
        raise AggregateReceiptError("receipt lacks obligation counts")
    lines = [
        (
            f"{receipt.get('status')} transaction={receipt.get('transaction_id')} "
            f"outcome={receipt.get('outcome')} selected={counts.get('selected_gate_count')} "
            f"executed={counts.get('executed_gate_count')} "
            f"obligations={coverage_counts.get('total')} "
            f"blocked_obligations={coverage_counts.get('blocked')} "
            f"blockers={counts.get('blocker_count')} "
            f"tree={_single_line(receipt.get('staged_tree_hash'), 96)}"
        )
    ]
    blockers = receipt.get("blockers", [])
    if not isinstance(blockers, list):
        raise AggregateReceiptError("receipt.blockers must be an array")
    for blocker in blockers[:max_blockers]:
        if not isinstance(blocker, Mapping):
            raise AggregateReceiptError("receipt blocker must be an object")
        lines.append(
            f"BLOCKER {blocker.get('code')} "
            f"{_single_line(blocker.get('subject', ''), 96)}: "
            f"{_single_line(blocker.get('message', ''), 240)}"
        )
    if len(blockers) > max_blockers:
        lines.append(f"MORE_BLOCKERS count={len(blockers) - max_blockers}")
    output = "\n".join(lines) + "\n"
    encoded = output.encode("utf-8")
    if len(encoded) <= byte_budget:
        return output
    prefix = encoded[: byte_budget - 4]
    while True:
        try:
            return prefix.decode("utf-8") + "...\n"
        except UnicodeDecodeError:
            prefix = prefix[:-1]
