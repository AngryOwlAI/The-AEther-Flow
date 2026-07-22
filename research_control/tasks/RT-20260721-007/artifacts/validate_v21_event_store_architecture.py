#!/usr/bin/env python3
"""Validate the design-only v21 P10-T05 event-store architecture packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[4]
CONTRACT_PATH = ARTIFACT_DIR / "v21_event_store_architecture_contract.json"
VALIDATION_PATH = ARTIFACT_DIR / "v21_event_store_architecture_validation.json"
RECEIPT_PATH = ARTIFACT_DIR / "v21_event_store_architecture_compact_receipt.json"
DOC_PATHS = (
    ARTIFACT_DIR / "v21_event_store_architecture_decision.md",
    ARTIFACT_DIR / "v21_event_store_schema.md",
    ARTIFACT_DIR / "v21_generated_view_contract.md",
    ARTIFACT_DIR / "v21_event_store_migration_rollback_plan.md",
)

REQUIRED_DOMAINS = {
    "task",
    "decision",
    "agent_job",
    "candidate",
    "claim",
    "validation",
    "authority",
    "handoff",
}
REQUIRED_VIEW_IDS = {
    "research_task_registry",
    "director_decision_registry",
    "agent_job_registry",
    "claim_boundary_registry",
    "current_frontier",
    "task_index_csv",
    "task_index_markdown",
    "frontier_theorem_inventory",
    "operational_dashboard",
    "sqlite_query_index",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def validate_contract_data(contract: dict[str, Any]) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(name: str, passed: bool, evidence: str) -> None:
        checks.append(
            {
                "name": name,
                "status": "PASS" if passed else "FAIL",
                "evidence": evidence,
            }
        )

    options = contract.get("architecture_options", [])
    selected = [item.get("id") for item in options if item.get("selected") is True]
    add(
        "exactly_one_architecture_selected",
        selected == ["hybrid_tracked_jsonl_plus_generated_sqlite"]
        and contract.get("selected_architecture") == selected[0],
        f"selected={selected!r}",
    )
    option_ids = {item.get("id") for item in options}
    add(
        "storage_comparison_complete",
        option_ids
        == {
            "tracked_jsonl_only",
            "sqlite_only",
            "hybrid_tracked_jsonl_plus_generated_sqlite",
        }
        and all(item.get("strengths") and item.get("risks") for item in options),
        f"options={sorted(str(value) for value in option_ids)}",
    )

    activation = contract.get("activation_state", {})
    add(
        "pilot_and_cutover_not_executed",
        bool(activation)
        and all(value is False for value in activation.values())
        and contract.get("status") == "design_selected_not_activated",
        f"activation_state={activation!r}",
    )

    encoding = contract.get("canonical_encoding", {})
    add(
        "tracked_jsonl_and_disposable_sqlite",
        encoding.get("container") == "segmented_json_lines"
        and encoding.get("record_serialization")
        == "RFC_8785_JSON_Canonicalization_Scheme"
        and encoding.get("sqlite_role") == "generated_disposable_query_index"
        and encoding.get("sqlite_tracking") == "untracked_local_cache",
        "canonical text history and generated local query index are separated",
    )

    identity = contract.get("event_identity", {})
    identity_fields = set(identity.get("identity_basis_fields", []))
    add(
        "deterministic_content_identity",
        identity.get("event_id_format") == "EVT-V21-<sha256_64hex>"
        and identity.get("event_id_preimage")
        == "RFC8785 canonical JSON of identity_basis"
        and {
            "event_schema_id",
            "event_domain",
            "event_type",
            "subject_id",
            "operation_id",
            "source_refs",
            "payload",
        }
        == identity_fields
        and "idempotent no-op" in identity.get("duplicate_rule", ""),
        f"identity_basis_fields={sorted(identity_fields)}",
    )
    add(
        "append_only_corrections",
        "immutable" in identity.get("correction_rule", "").lower()
        and "new correction events" in identity.get("correction_rule", "")
        and "never rewrite or delete" in identity.get("correction_rule", ""),
        identity.get("correction_rule", "missing correction rule"),
    )

    envelope = contract.get("event_envelope", {})
    required_envelope_fields = {
        "event_schema_id",
        "event_id",
        "sequence",
        "prior_event_hash",
        "event_hash",
        "event_domain",
        "event_type",
        "subject_id",
        "operation_id",
        "effective_at",
        "actor_role_ref",
        "source_refs",
        "payload",
        "authority",
    }
    add(
        "event_envelope_complete",
        set(envelope.get("required_fields", [])) == required_envelope_fields
        and set(envelope.get("source_ref_required_fields", []))
        == {"object_id", "path", "sha256", "authority_status"}
        and "sequence defines replay order" in envelope.get("time_rule", ""),
        f"required_field_count={len(envelope.get('required_fields', []))}",
    )

    domains = contract.get("event_domains", [])
    domain_ids = {item.get("id") for item in domains}
    add(
        "required_event_domains_present",
        domain_ids == REQUIRED_DOMAINS
        and all(item.get("event_types") and item.get("legacy_projection") for item in domains),
        f"domains={sorted(str(value) for value in domain_ids)}",
    )

    views = contract.get("generated_views", [])
    view_ids = {item.get("id") for item in views}
    add(
        "required_generated_views_present",
        view_ids == REQUIRED_VIEW_IDS,
        f"views={sorted(str(value) for value in view_ids)}",
    )
    add(
        "generated_views_non_authoritative_and_deterministic",
        bool(views)
        and all(item.get("authority") is False for item in views)
        and all(item.get("deterministic") is True for item in views),
        f"view_count={len(views)}",
    )
    sqlite_views = [item for item in views if item.get("id") == "sqlite_query_index"]
    add(
        "sqlite_is_local_cache",
        len(sqlite_views) == 1
        and str(sqlite_views[0].get("path", "")).startswith(".local/")
        and sqlite_views[0].get("authority") is False,
        f"sqlite_view={sqlite_views!r}",
    )

    projection = contract.get("projection_contract", {})
    add(
        "projection_determinism_and_parity",
        "byte-identical" in projection.get("determinism_rule", "")
        and "field-level allowlist" in projection.get("parity_rule", "")
        and "fail closed" in projection.get("failure_rule", "")
        and "registered TeX source remains scientific authority"
        in projection.get("theorem_inventory_rule", ""),
        "byte-level determinism, explicit parity, and theorem authority are specified",
    )

    transaction = contract.get("transaction_contract", {})
    write_order = transaction.get("write_order", [])
    add(
        "single_writer_checkpoint_transaction",
        transaction.get("unit")
        == "one_Git_commit_containing_events_manifest_views_and_receipts"
        and transaction.get("expected_head_compare_and_swap") is True
        and write_order[:2]
        == ["acquire_single_writer_lock", "verify_expected_manifest_head"]
        and "create_one_Git_checkpoint_commit" in write_order
        and "no authoritative transaction"
        in transaction.get("failure_atomicity", ""),
        f"write_order={write_order!r}",
    )

    concurrency = contract.get("concurrency_contract", {})
    add(
        "concurrency_and_reader_pinning",
        concurrency.get("writers") == "single_writer"
        and concurrency.get("lock_scope") == "repository_common_dir"
        and "age alone cannot break" in concurrency.get("stale_lock_rule", "")
        and "one Git revision and one manifest hash"
        in concurrency.get("reader_rule", "")
        and "direct segment merge is forbidden" in concurrency.get("merge_rule", ""),
        "single writer, CAS recovery, pinned readers, and no raw segment merge",
    )

    migration = contract.get("migration_contract", {})
    phases = migration.get("phases", [])
    phase_map = {item.get("id"): item for item in phases}
    add(
        "migration_is_shadow_then_explicit_cutover",
        migration.get("mode") == "shadow_then_explicit_cutover"
        and phase_map.get("design", {}).get("status") == "completed_by_this_packet"
        and phase_map.get("bounded_shadow_pilot", {}).get("owner_task") == "P10-T06"
        and phase_map.get("bounded_shadow_pilot", {}).get("status") == "not_executed"
        and phase_map.get("reader_cutover", {}).get("status") == "not_authorized"
        and all(item.get("writes_authorized") is False for item in phases)
        and "does not select or implement" in migration.get("pilot_slice_rule", ""),
        f"phase_statuses={{{', '.join(f'{key}: {value.get("status")}' for key, value in phase_map.items())}}}",
    )

    rollback = contract.get("rollback_contract", {})
    add(
        "rollback_preserves_history_and_legacy_readability",
        "existing tracked sources and registries" in rollback.get("pre_cutover_action", "")
        and "last-known-good legacy-authority revision"
        in rollback.get("post_cutover_action", "")
        and "Do not delete or mutate committed events" in rollback.get("history_rule", "")
        and "no migration phase may make historical checkout dependent on SQLite"
        in rollback.get("legacy_readability_rule", ""),
        "rollback retains committed events and legacy text surfaces",
    )

    authority = contract.get("authority_contract", {})
    add(
        "authority_hierarchy_preserved",
        authority.get("registered_tex_authority_preserved") is True
        and authority.get("gate_chair_authority_preserved") is True
        and authority.get("generated_views_are_authority") is False
        and authority.get("generated_sqlite_is_authority") is False
        and authority.get("event_payload_is_scientific_proof") is False
        and authority.get("event_payload_may_replace_science_source") is False,
        "registered TeX and Gate Chair authority remain outside event-store projections",
    )

    next_route = contract.get("next_route", {})
    add(
        "next_route_is_unexecuted_p10_t06",
        next_route.get("dependency_ready_task") == "P10-T06"
        and next_route.get("executed_by_this_packet") is False
        and "P10-T07" in next_route.get("also_dependency_ready", []),
        f"next_route={next_route!r}",
    )
    return checks


def validate_source_bindings(
    contract: dict[str, Any], repo_root: Path = REPO_ROOT
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    bindings = contract.get("source_bindings", [])
    paths = [str(item.get("path", "")) for item in bindings]
    unique = len(paths) == len(set(paths)) and len(paths) >= 10
    checks.append(
        {
            "name": "source_bindings_unique_and_bounded",
            "status": "PASS" if unique else "FAIL",
            "evidence": f"binding_count={len(paths)} unique_count={len(set(paths))}",
        }
    )
    for item in bindings:
        relative = str(item.get("path", ""))
        expected = str(item.get("sha256", ""))
        source = repo_root / relative
        exists = source.is_file()
        actual = sha256_file(source) if exists else "missing"
        checks.append(
            {
                "name": f"source_hash::{relative}",
                "status": "PASS" if exists and actual == expected else "FAIL",
                "evidence": f"expected={expected} actual={actual}",
            }
        )
    return checks


def validate_documents() -> list[dict[str, str]]:
    required_tokens = {
        "v21_event_store_architecture_decision.md": (
            "hybrid_tracked_jsonl_plus_generated_sqlite",
            "This packet is design-only",
            "Registered TeX remains canonical",
            "P10-T06",
        ),
        "v21_event_store_schema.md": (
            "RFC 8785",
            "Deterministic identity",
            "Append-only corrections",
            "Gate Chair",
        ),
        "v21_generated_view_contract.md": (
            "byte-identical",
            "field allowlist",
            "SQLite query index",
            "not scientific proof",
        ),
        "v21_event_store_migration_rollback_plan.md": (
            "No event-store segment",
            "Not executed",
            "last-known-good",
            "SQLite is never required",
        ),
    }
    checks: list[dict[str, str]] = []
    for path in DOC_PATHS:
        exists = path.is_file()
        content = path.read_text(encoding="utf-8") if exists else ""
        missing = [token for token in required_tokens[path.name] if token not in content]
        checks.append(
            {
                "name": f"document_contract::{path.name}",
                "status": "PASS" if exists and not missing else "FAIL",
                "evidence": f"missing_tokens={missing!r}",
            }
        )
    return checks


def build_outputs(contract: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    checks = (
        validate_contract_data(contract)
        + validate_source_bindings(contract)
        + validate_documents()
    )
    failures = [item["name"] for item in checks if item["status"] != "PASS"]
    contract_hash = sha256_file(CONTRACT_PATH)
    doc_hashes = {path.name: sha256_file(path) for path in DOC_PATHS}
    source_hashes = {
        item["path"]: item["sha256"] for item in contract.get("source_bindings", [])
    }
    status = "PASS" if not failures else "FAIL"
    report = {
        "schema_id": "v21_event_store_architecture_validation_v1",
        "task_id": contract.get("task_id"),
        "plan_task_id": contract.get("plan_task_id"),
        "status": status,
        "selected_architecture": contract.get("selected_architecture"),
        "contract_sha256": contract_hash,
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failures),
        "failed_check_count": len(failures),
        "failed_checks": failures,
        "source_binding_count": len(contract.get("source_bindings", [])),
        "event_domain_count": len(contract.get("event_domains", [])),
        "generated_view_count": len(contract.get("generated_views", [])),
        "activation_state": contract.get("activation_state", {}),
        "checks": checks,
    }
    receipt = {
        "schema_id": "v21_event_store_architecture_compact_receipt_v1",
        "task_id": contract.get("task_id"),
        "plan_task_id": contract.get("plan_task_id"),
        "validation_status": status,
        "architecture_status": contract.get("status"),
        "selected_architecture": contract.get("selected_architecture"),
        "contract_sha256": contract_hash,
        "document_sha256": doc_hashes,
        "source_sha256": source_hashes,
        "source_binding_count": len(source_hashes),
        "event_domain_count": len(contract.get("event_domains", [])),
        "generated_view_count": len(contract.get("generated_views", [])),
        "canonical_event_store_active": contract.get("activation_state", {}).get(
            "canonical_event_store_active"
        ),
        "pilot_executed": contract.get("activation_state", {}).get("pilot_executed"),
        "reader_cutover_executed": contract.get("activation_state", {}).get(
            "reader_cutover_executed"
        ),
        "legacy_registry_authority_changed": contract.get("activation_state", {}).get(
            "legacy_registry_authority_changed"
        ),
        "registered_tex_authority_preserved": contract.get("authority_contract", {}).get(
            "registered_tex_authority_preserved"
        ),
        "gate_chair_authority_preserved": contract.get("authority_contract", {}).get(
            "gate_chair_authority_preserved"
        ),
        "generated_views_are_authority": contract.get("authority_contract", {}).get(
            "generated_views_are_authority"
        ),
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "next_dependency_ready_task": contract.get("next_route", {}).get(
            "dependency_ready_task"
        ),
        "next_task_executed": contract.get("next_route", {}).get(
            "executed_by_this_packet"
        ),
    }
    return report, receipt


def run(mode: str) -> dict[str, Any]:
    contract = load_contract()
    report, receipt = build_outputs(contract)
    expected = {
        VALIDATION_PATH: canonical_text(report),
        RECEIPT_PATH: canonical_text(receipt),
    }
    drift: list[str] = []
    if mode == "write":
        for path, content in expected.items():
            path.write_text(content, encoding="utf-8")
    else:
        for path, content in expected.items():
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                drift.append(str(path.relative_to(REPO_ROOT)))
    return {
        "status": "PASS" if report["status"] == "PASS" and not drift else "FAIL",
        "mode": mode,
        "validation_status": report["status"],
        "failed_checks": report["failed_checks"],
        "drift": drift,
        "validation_path": str(VALIDATION_PATH.relative_to(REPO_ROOT)),
        "receipt_path": str(RECEIPT_PATH.relative_to(REPO_ROOT)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run("write" if args.write else "check")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
