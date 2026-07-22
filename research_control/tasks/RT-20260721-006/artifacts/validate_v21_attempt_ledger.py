#!/usr/bin/env python3
"""Validate the v21 P10-T04 append-only attempt-history ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
LEDGER_PATH = ARTIFACT_DIR / "v21_research_attempt_ledger.json"
VALIDATION_PATH = ARTIFACT_DIR / "v21_attempt_history_validation.json"
RECEIPT_PATH = ARTIFACT_DIR / "v21_attempt_history_compact_receipt.json"

SCHEMA_ID = "v21_research_attempt_ledger_v1"
CHAIN_ALGORITHM = "sha256-canonical-json-v1"
LEDGER_FIELDS = {
    "schema_id",
    "ledger_id",
    "task_id",
    "plan_task_id",
    "status",
    "revision",
    "sealed_at",
    "append_only",
    "chain_algorithm",
    "schema_path",
    "schema_sha256",
    "redaction_policy_path",
    "redaction_policy_sha256",
    "candidate_registry_path",
    "candidate_registry_sha256",
    "build_compute_metadata",
    "explicit_absences",
    "authority_boundary",
    "events",
}
EVENT_TYPES = {
    "attempt_started": "active",
    "validation_failed": "blocked",
    "audit_finding": "finding_recorded",
    "repair_applied": "completed",
    "superseded": "superseded",
    "abandoned": "abandoned",
    "completed": "completed",
}
EVENT_FIELDS = {
    "event_id",
    "sequence",
    "event_type",
    "occurred_at",
    "task_id",
    "job_id",
    "candidate_ids",
    "source_refs",
    "summary",
    "disposition",
    "evidence_domain",
    "physics_result",
    "finalized",
    "related_event_ids",
    "compute_metadata",
    "authority",
    "prior_event_hash",
    "payload_sha256",
    "event_hash",
}
COMPUTE_FIELDS = {
    "availability",
    "model",
    "reasoning_effort",
    "environment",
    "cost_availability",
    "cost_value",
    "cost_currency",
}
BUILD_COMPUTE_FIELDS = COMPUTE_FIELDS | {"authority"}
AUTHORITY_FIELDS = {
    "scientific_claims_changed",
    "candidate_adoption_authorized",
    "candidate_rejection_authorized",
    "ontology_edit_authorized",
    "physics_promotion_authorized",
    "proof_authority",
    "publication_authority",
    "completed_derivation_authorized",
}
FORBIDDEN_KEYS = {
    "password",
    "credential",
    "api_key",
    "access_token",
    "refresh_token",
    "private_key",
    "personal_data",
    "user_message",
    "model_input",
    "private_reasoning",
    "chain_of_thought",
    "hidden_instruction",
    "raw_terminal_transcript",
    "environment_dump",
}
FORBIDDEN_KEY_FORMS = {re.sub(r"[^a-z0-9]", "", key) for key in FORBIDDEN_KEYS}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


class LedgerValidationError(ValueError):
    """Raised when the ledger violates its control contract."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def event_payload(event: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(event)
    for field in ("prior_event_hash", "payload_sha256", "event_hash"):
        payload.pop(field, None)
    return payload


def expected_event_hashes(
    event: dict[str, Any], prior_event_hash: str
) -> tuple[str, str]:
    payload_sha256 = sha256_bytes(canonical_bytes(event_payload(event)))
    event_hash = sha256_bytes(
        canonical_bytes(
            {
                "event_id": event.get("event_id"),
                "sequence": event.get("sequence"),
                "payload_sha256": payload_sha256,
                "prior_event_hash": prior_event_hash,
            }
        )
    )
    return payload_sha256, event_hash


def scan_for_private_material(value: Any, location: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = re.sub(r"[^a-z0-9]", "", str(key).lower())
            if normalized in FORBIDDEN_KEY_FORMS:
                findings.append(f"forbidden field {location}.{key}")
            findings.extend(scan_for_private_material(child, f"{location}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(scan_for_private_material(child, f"{location}[{index}]"))
    elif isinstance(value, str):
        for pattern in SECRET_PATTERNS:
            if pattern.search(value):
                findings.append(f"credential-like value at {location}")
    return findings


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise LedgerValidationError(f"{path}: expected JSON object")
    return value


def tracked(path: str) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or value.startswith("/") or "\\" in value:
        return False
    parts = PurePosixPath(value).parts
    return bool(parts) and "." not in parts and ".." not in parts


def load_head_ledger() -> dict[str, Any] | None:
    relative = LEDGER_PATH.relative_to(REPO_ROOT).as_posix()
    result = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    value = json.loads(result.stdout)
    if not isinstance(value, dict):
        raise LedgerValidationError("HEAD ledger is not a JSON object")
    return value


def validate_head_prefix(
    current: dict[str, Any], baseline: dict[str, Any] | None
) -> int:
    if baseline is None:
        return 0
    old_events = baseline.get("events")
    new_events = current.get("events")
    if not isinstance(old_events, list) or not isinstance(new_events, list):
        raise LedgerValidationError("HEAD/current events must be arrays")
    if len(new_events) < len(old_events):
        raise LedgerValidationError("finalized HEAD event deletion detected")
    for index, old_event in enumerate(old_events):
        if canonical_bytes(old_event) != canonical_bytes(new_events[index]):
            raise LedgerValidationError(
                f"finalized HEAD event mutation detected at sequence {index + 1}"
            )
    return len(old_events)


def validate_ledger_data(
    ledger: dict[str, Any], *, verify_sources: bool = True, verify_head: bool = True
) -> dict[str, Any]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(set(ledger) == LEDGER_FIELDS, "ledger fields mismatch")
    require(ledger.get("schema_id") == SCHEMA_ID, "schema_id mismatch")
    require(ledger.get("append_only") is True, "append_only must be true")
    require(
        ledger.get("chain_algorithm") == CHAIN_ALGORITHM,
        "chain_algorithm mismatch",
    )
    require(ledger.get("status") == "draft/control", "status must be draft/control")
    revision = ledger.get("revision")
    require(
        isinstance(revision, int) and not isinstance(revision, bool) and revision >= 1,
        "revision must be a positive integer",
    )
    require(
        isinstance(ledger.get("sealed_at"), str)
        and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", ledger.get("sealed_at", ""))
        is not None,
        "sealed_at must be a UTC timestamp",
    )

    pinned_sources = (
        ("schema_path", "schema_sha256", False),
        ("redaction_policy_path", "redaction_policy_sha256", False),
        ("candidate_registry_path", "candidate_registry_sha256", True),
    )
    for path_field, hash_field, require_tracked in pinned_sources:
        relative = ledger.get(path_field)
        digest = ledger.get(hash_field)
        require(safe_relative_path(relative), f"{path_field} is not a safe relative path")
        require(
            isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest or "") is not None,
            f"{hash_field} is invalid",
        )
        if safe_relative_path(relative):
            source = REPO_ROOT / str(relative)
            require(source.is_file() and not source.is_symlink(), f"{path_field} is not a regular non-symlink file")
            if source.is_file():
                require(sha256_path(source) == digest, f"{hash_field} drift")
            if require_tracked:
                require(tracked(str(relative)), f"{path_field} is not tracked")

    build_compute = ledger.get("build_compute_metadata")
    require(isinstance(build_compute, dict), "build_compute_metadata must be an object")
    if isinstance(build_compute, dict):
        require(set(build_compute) == BUILD_COMPUTE_FIELDS, "build_compute_metadata fields mismatch")
        require(build_compute.get("availability") == "recorded", "build compute availability must be recorded")
        require(build_compute.get("authority") == "operational telemetry only", "build compute authority mismatch")
        require(build_compute.get("cost_value") is None, "build compute cost_value must be null when unavailable")

    authority = ledger.get("authority_boundary")
    require(isinstance(authority, dict), "authority_boundary must be an object")
    if isinstance(authority, dict):
        require(
            set(authority) == AUTHORITY_FIELDS,
            "authority_boundary fields mismatch",
        )
        for field in AUTHORITY_FIELDS:
            require(authority.get(field) is False, f"authority_boundary.{field} must be false")

    privacy_findings = scan_for_private_material(ledger)
    errors.extend(privacy_findings)

    candidate_path = REPO_ROOT / str(ledger.get("candidate_registry_path", ""))
    candidate_ids: set[str] = set()
    if candidate_path.is_file():
        candidate_registry = load_json(candidate_path)
        index = candidate_registry.get("candidate_identity_index", {})
        if isinstance(index, dict):
            candidate_ids = set(index)
    else:
        errors.append("candidate_registry_path is not a regular file")

    events = ledger.get("events")
    require(isinstance(events, list) and bool(events), "events must be a nonempty array")
    if not isinstance(events, list):
        events = []

    seen_ids: set[str] = set()
    prior_hash = ""
    event_type_counts: Counter[str] = Counter()
    source_ref_count = 0
    for index, event in enumerate(events, start=1):
        location = f"events[{index - 1}]"
        if not isinstance(event, dict):
            errors.append(f"{location} must be an object")
            continue
        require(set(event) == EVENT_FIELDS, f"{location} fields mismatch")
        event_id = event.get("event_id")
        require(isinstance(event_id, str) and re.fullmatch(r"AEV-\d{4}", event_id or "") is not None, f"{location}.event_id invalid")
        require(event_id not in seen_ids, f"{location}.event_id duplicate")
        if isinstance(event_id, str):
            seen_ids.add(event_id)
        require(event.get("sequence") == index, f"{location}.sequence must be {index}")
        require(
            isinstance(event.get("occurred_at"), str)
            and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", event.get("occurred_at", ""))
            is not None,
            f"{location}.occurred_at must be a UTC timestamp",
        )
        require(re.fullmatch(r"RT-\d{8}-\d{3}", str(event.get("task_id", ""))) is not None, f"{location}.task_id invalid")
        require(re.fullmatch(r"AJ-RT-\d{8}-\d{3}-\d{3}", str(event.get("job_id", ""))) is not None, f"{location}.job_id invalid")
        require(isinstance(event.get("summary"), str) and bool(event.get("summary", "").strip()), f"{location}.summary is required")
        event_type = event.get("event_type")
        require(event_type in EVENT_TYPES, f"{location}.event_type invalid")
        if isinstance(event_type, str):
            event_type_counts[event_type] += 1
            require(
                event.get("disposition") == EVENT_TYPES.get(event_type),
                f"{location}.disposition incompatible",
            )
        require(event.get("evidence_domain") in {"process", "scientific_review"}, f"{location}.evidence_domain invalid")
        require(event.get("physics_result") is False, f"{location}.physics_result must be false")
        require(event.get("finalized") is True, f"{location}.finalized must be true")

        event_authority = event.get("authority")
        require(isinstance(event_authority, dict), f"{location}.authority must be an object")
        if isinstance(event_authority, dict):
            require(set(event_authority) == AUTHORITY_FIELDS, f"{location}.authority fields mismatch")
            for field in AUTHORITY_FIELDS:
                require(event_authority.get(field) is False, f"{location}.authority.{field} must be false")

        compute = event.get("compute_metadata")
        require(isinstance(compute, dict), f"{location}.compute_metadata must be an object")
        if isinstance(compute, dict):
            require(set(compute) == COMPUTE_FIELDS, f"{location}.compute_metadata fields mismatch")
            require(compute.get("availability") in {"recorded", "not_recorded"}, f"{location}.compute_metadata.availability invalid")
            if compute.get("availability") == "not_recorded":
                for field in ("model", "reasoning_effort", "environment", "cost_availability", "cost_currency"):
                    require(compute.get(field) == "not_recorded", f"{location}.compute_metadata.{field} must be not_recorded")
                require(compute.get("cost_value") is None, f"{location}.compute_metadata.cost_value must be null")

        event_candidates = event.get("candidate_ids")
        require(isinstance(event_candidates, list), f"{location}.candidate_ids must be an array")
        if isinstance(event_candidates, list):
            require(len(event_candidates) == len(set(event_candidates)), f"{location}.candidate_ids duplicate")
            for candidate_id in event_candidates:
                require(candidate_id in candidate_ids, f"{location}.candidate_ids contains unknown ID {candidate_id}")

        related = event.get("related_event_ids")
        require(isinstance(related, list), f"{location}.related_event_ids must be an array")
        if isinstance(related, list):
            require(len(related) == len(set(related)), f"{location}.related_event_ids duplicate")
            for related_id in related:
                require(related_id in seen_ids and related_id != event_id, f"{location}.related_event_ids must name an earlier event")
        if event_type == "repair_applied":
            require(bool(related), f"{location}.repair_applied requires related_event_ids")

        refs = event.get("source_refs")
        require(isinstance(refs, list) and bool(refs), f"{location}.source_refs must be nonempty")
        if isinstance(refs, list):
            for ref_index, ref in enumerate(refs):
                ref_location = f"{location}.source_refs[{ref_index}]"
                require(isinstance(ref, dict) and set(ref) == {"path", "sha256"}, f"{ref_location} fields mismatch")
                if not isinstance(ref, dict):
                    continue
                relative = ref.get("path")
                digest = ref.get("sha256")
                require(safe_relative_path(relative), f"{ref_location}.path invalid")
                require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest or "") is not None, f"{ref_location}.sha256 invalid")
                if verify_sources and safe_relative_path(relative):
                    source = REPO_ROOT / relative
                    require(source.is_file() and not source.is_symlink(), f"{ref_location}.path not a regular non-symlink file")
                    require(tracked(relative), f"{ref_location}.path is not tracked")
                    if source.is_file():
                        require(sha256_path(source) == digest, f"{ref_location}.sha256 drift")
                source_ref_count += 1

        require(event.get("prior_event_hash") == prior_hash, f"{location}.prior_event_hash mismatch")
        expected_payload, expected_hash = expected_event_hashes(event, prior_hash)
        require(event.get("payload_sha256") == expected_payload, f"{location}.payload_sha256 mismatch")
        require(event.get("event_hash") == expected_hash, f"{location}.event_hash mismatch")
        prior_hash = expected_hash

    absences = ledger.get("explicit_absences")
    require(isinstance(absences, list), "explicit_absences must be an array")
    absent_types: set[str] = set()
    if isinstance(absences, list):
        for index, absence in enumerate(absences):
            location = f"explicit_absences[{index}]"
            require(
                isinstance(absence, dict)
                and set(absence)
                == {"absence_id", "event_type", "reason", "source_search_scope", "inference_performed"},
                f"{location} fields mismatch",
            )
            if not isinstance(absence, dict):
                continue
            absent_type = absence.get("event_type")
            require(absent_type in EVENT_TYPES, f"{location}.event_type invalid")
            require(absence.get("inference_performed") is False, f"{location}.inference_performed must be false")
            require(isinstance(absence.get("reason"), str) and bool(absence.get("reason", "").strip()), f"{location}.reason is required")
            require(isinstance(absence.get("source_search_scope"), str) and bool(absence.get("source_search_scope", "").strip()), f"{location}.source_search_scope is required")
            if isinstance(absent_type, str):
                absent_types.add(absent_type)
                require(event_type_counts[absent_type] == 0, f"{location} contradicts an observed event")

    for event_type in EVENT_TYPES:
        if event_type_counts[event_type] == 0:
            require(event_type in absent_types, f"missing explicit absence for {event_type}")
        else:
            require(event_type not in absent_types, f"unexpected explicit absence for {event_type}")

    head_prefix_count = 0
    if verify_head:
        try:
            head_prefix_count = validate_head_prefix(ledger, load_head_ledger())
        except (LedgerValidationError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    if errors:
        raise LedgerValidationError("; ".join(errors))

    return {
        "event_count": len(events),
        "event_type_counts": {name: event_type_counts[name] for name in sorted(EVENT_TYPES)},
        "source_ref_count": source_ref_count,
        "candidate_link_count": sum(len(event["candidate_ids"]) for event in events),
        "explicit_absence_count": len(absences or []),
        "head_prefix_count": head_prefix_count,
        "head_event_hash": prior_hash,
        "privacy_finding_count": len(privacy_findings),
    }


def build_outputs(ledger: dict[str, Any], metrics: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    ledger_sha256 = sha256_path(LEDGER_PATH)
    checks = {
        "append_only_hash_chain": "PASS",
        "candidate_identity_links": "PASS",
        "event_schema": "PASS",
        "explicit_absence_without_inference": "PASS",
        "head_prefix_immutability": "PASS",
        "process_physics_classification": "PASS",
        "secret_and_private_material_scan": "PASS",
        "source_hash_exactness": "PASS",
    }
    validation = {
        "schema_id": "v21_attempt_history_validation_v1",
        "status": "PASS",
        "task_id": ledger["task_id"],
        "plan_task_id": ledger["plan_task_id"],
        "ledger_path": LEDGER_PATH.relative_to(REPO_ROOT).as_posix(),
        "ledger_sha256": ledger_sha256,
        "checked_revision": ledger["revision"],
        "checked_at": ledger["sealed_at"],
        "checks": checks,
        "metrics": metrics,
        "authority_note": "Project-control history only; process or review evidence is not physics evidence.",
    }
    receipt = {
        "schema_id": "v21_attempt_history_compact_receipt_v1",
        "status": "PASS",
        "task_id": ledger["task_id"],
        "ledger_sha256": ledger_sha256,
        "head_event_hash": metrics["head_event_hash"],
        "event_count": metrics["event_count"],
        "event_type_counts": metrics["event_type_counts"],
        "explicit_absence_count": metrics["explicit_absence_count"],
        "source_ref_count": metrics["source_ref_count"],
        "privacy_finding_count": 0,
        "physics_result_count": 0,
        "scientific_authority_changed": False,
    }
    return validation, receipt


def rendered_json(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        ledger = load_json(LEDGER_PATH)
        metrics = validate_ledger_data(ledger)
        validation, receipt = build_outputs(ledger, metrics)
        expected = {
            VALIDATION_PATH: rendered_json(validation),
            RECEIPT_PATH: rendered_json(receipt),
        }
        if args.write:
            for path, content in expected.items():
                path.write_text(content, encoding="utf-8")
        else:
            for path, content in expected.items():
                if not path.is_file() or path.read_text(encoding="utf-8") != content:
                    raise LedgerValidationError(f"generated output stale: {path.relative_to(REPO_ROOT)}")
    except (LedgerValidationError, FileNotFoundError, json.JSONDecodeError) as exc:
        result = {"status": "FAIL", "error": str(exc)}
        print(json.dumps(result, sort_keys=True) if args.json else f"FAIL: {exc}")
        return 1

    result = {
        "status": "PASS",
        "ledger_sha256": validation["ledger_sha256"],
        "event_count": metrics["event_count"],
        "head_event_hash": metrics["head_event_hash"],
        "head_prefix_count": metrics["head_prefix_count"],
    }
    print(json.dumps(result, sort_keys=True) if args.json else "PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
