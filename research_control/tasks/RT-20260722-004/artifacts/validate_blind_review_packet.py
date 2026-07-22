#!/usr/bin/env python3
"""Validate blind-review packet separation and write deterministic receipts."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path(__file__).resolve().parent
SOURCE_PATH = ARTIFACT_DIR / "blind_review_source_fixture.json"
PACKET_PATH = ARTIFACT_DIR / "blind_review_packet_fixture.json"
CONTEXT_PATH = ARTIFACT_DIR / "blind_review_context_manifest_fixture.json"
VALIDATION_PATH = ARTIFACT_DIR / "blind_review_validation.json"
RECEIPT_PATH = ARTIFACT_DIR / "blind_review_compact_receipt.json"
SCHEMA_PATH = ARTIFACT_DIR / "blind_review_packet_schema.md"
INSTRUCTIONS_PATH = ARTIFACT_DIR / "reviewer_instructions.md"
BUILDER_PATH = ARTIFACT_DIR / "build_blind_review_packet.py"

FORBIDDEN_KEYS = {
    "task_id",
    "job_id",
    "decision_id",
    "plan_task_id",
    "handoff_id",
    "generation",
    "lease",
    "checkpoint",
    "route",
    "route_history",
    "selected_next_action",
    "worker_skill",
    "role_id",
    "role_version",
    "task_verdict",
    "verdict",
    "status",
    "validator_status",
    "validation_status",
    "test_status",
    "internal_confidence",
    "reviewer_identity",
    "model_family",
    "prior_context_access",
    "independence_label",
}
FORBIDDEN_PATTERNS = {
    "research_task_id": re.compile(r"\bRT-\d{8}-\d+\b", re.IGNORECASE),
    "agent_job_id": re.compile(r"\bAJ-RT-\d{8}-\d+-\d+\b", re.IGNORECASE),
    "decision_id": re.compile(r"\bDDR-\d{8}-\d+\b", re.IGNORECASE),
    "handoff_id": re.compile(r"\bhandoff-\d+\b", re.IGNORECASE),
    "plan_task_id": re.compile(r"\bP\d+-T\d+\b", re.IGNORECASE),
    "workflow_result": re.compile(
        r"\b(?:validator|validation status|route history|internal confidence|task verdict|workflow status|checkpoint|worker skill)\b",
        re.IGNORECASE,
    ),
}


def _load_builder():
    spec = importlib.util.spec_from_file_location("v21_blind_packet_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load packet builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def scan_packet(value: Any, location: str = "$", findings: list[dict[str, str]] | None = None) -> list[dict[str, str]]:
    if findings is None:
        findings = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = key.lower().replace("-", "_")
            if normalized in FORBIDDEN_KEYS:
                findings.append({"kind": "forbidden_key", "location": f"{location}.{key}", "match": key})
            scan_packet(child, f"{location}.{key}", findings)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_packet(child, f"{location}[{index}]", findings)
    elif isinstance(value, str):
        for pattern_id, pattern in FORBIDDEN_PATTERNS.items():
            match = pattern.search(value)
            if match:
                findings.append({"kind": pattern_id, "location": location, "match": match.group(0)})
    return findings


def validate_objects(
    manifest: dict[str, Any],
    packet: dict[str, Any],
    context: dict[str, Any],
    *,
    packet_path: Path = PACKET_PATH,
    context_path: Path = CONTEXT_PATH,
) -> dict[str, Any]:
    builder = _load_builder()
    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    try:
        expected_packet, expected_context = builder.build_objects(manifest)
        rebuild_error = ""
    except Exception as exc:  # validation must report fail-closed detail
        expected_packet, expected_context = {}, {}
        rebuild_error = str(exc)
    check("source_manifest_rebuild", not rebuild_error, rebuild_error or "source hashes and excerpts verified")
    check("packet_canonical_rebuild", packet == expected_packet, "packet equals deterministic rebuild")
    check("context_canonical_rebuild", context == expected_context, "context equals deterministic rebuild")

    findings = scan_packet(packet)
    check("forbidden_key_scan", not any(item["kind"] == "forbidden_key" for item in findings), "recursive key scan")
    check("forbidden_value_scan", not any(item["kind"] != "forbidden_key" for item in findings), "recursive value scan")

    assumption_ids = {item.get("assumption_id") for item in packet.get("assumption_register", [])}
    required_assumptions = {item["assumption_id"] for item in manifest.get("assumption_register", [])}
    referenced_assumptions = {
        assumption_id
        for item in packet.get("scientific_material", [])
        for assumption_id in item.get("assumption_ids", [])
    }
    check("assumption_register_exact", assumption_ids == required_assumptions, "all and only source assumptions retained")
    check("assumptions_referenced", referenced_assumptions == required_assumptions, "every assumption is attached to material")

    packet_hash = sha256_bytes(canonical_bytes(packet))
    check("context_packet_hash", context.get("blind_packet_sha256") == packet_hash, "context binds exact packet bytes")
    check("packet_context_path_separation", packet_path.resolve() != context_path.resolve(), "packet and context paths differ")
    check("context_separation_flag", context.get("context_manifest_separate_from_packet") is True, "separation declared")
    check("no_independence_claim", context.get("reviewer_independence_claimed") is False, "independence remains unclassified")

    expected_withheld = sorted(manifest.get("process_metadata", {}))
    actual_withheld = context.get("reviewer_not_received", {}).get("process_metadata_field_names")
    check("withheld_field_names_exact", actual_withheld == expected_withheld, "withheld process fields recorded by name")
    metadata_hash = sha256_bytes(canonical_bytes(manifest.get("process_metadata", {})))
    check(
        "withheld_metadata_hash",
        context.get("reviewer_not_received", {}).get("process_metadata_sha256") == metadata_hash,
        "withheld metadata bound without exposing values",
    )
    check(
        "source_paths_withheld",
        context.get("reviewer_not_received", {}).get("source_paths_withheld") is True
        and "research_control/" not in json.dumps(packet, ensure_ascii=False),
        "repository paths absent from blind packet",
    )
    check("claim_boundary_exact", packet.get("claim_boundary") == manifest.get("claim_boundary"), "claim boundaries retained")

    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "v21_blind_review_validation_v1",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "leak_finding_count": len(findings),
        "findings": findings,
        "checks": checks,
        "packet_sha256": packet_hash,
        "context_sha256": sha256_bytes(canonical_bytes(context)),
        "source_hashes": {
            item["blind_source_id"]: item["sha256"] for item in manifest.get("sources", [])
        },
        "assumption_count": len(required_assumptions),
        "material_count": len(manifest.get("scientific_material", [])),
        "reviewer_independence_claimed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def build_receipt(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "v21_blind_review_compact_receipt_v1",
        "status": report["status"],
        "plan_task_id": "P11-T01",
        "recommendation_ids": ["V21-R36", "V21-R38", "V21-R51"],
        "source_hashes": report["source_hashes"],
        "packet_sha256": report["packet_sha256"],
        "context_sha256": report["context_sha256"],
        "assumption_count": report["assumption_count"],
        "material_count": report["material_count"],
        "check_count": report["check_count"],
        "failed_check_count": report["failed_check_count"],
        "leak_finding_count": report["leak_finding_count"],
        "validator_ids": [
            "source_manifest_rebuild",
            "packet_canonical_rebuild",
            "context_canonical_rebuild",
            "forbidden_key_scan",
            "forbidden_value_scan",
            "assumption_register_exact",
            "packet_context_path_separation",
            "no_independence_claim",
        ],
        "artifact_hashes": {
            "schema": sha256_file(SCHEMA_PATH),
            "reviewer_instructions": sha256_file(INSTRUCTIONS_PATH),
            "source_manifest": sha256_file(SOURCE_PATH),
            "packet_builder": sha256_file(BUILDER_PATH),
            "redaction_validator": sha256_file(Path(__file__)),
        },
        "claim_boundary_summary": "Reproducible context separation only; no reviewer-independence, proof, ontology, physics, publication, benchmark, or completed-derivation authority.",
        "reviewer_independence_claimed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        manifest = load_json(SOURCE_PATH)
        packet = load_json(PACKET_PATH)
        context = load_json(CONTEXT_PATH)
        report = validate_objects(manifest, packet, context)
        receipt = build_receipt(report)
        if args.write:
            VALIDATION_PATH.write_bytes(canonical_bytes(report))
            RECEIPT_PATH.write_bytes(canonical_bytes(receipt))
        else:
            if not VALIDATION_PATH.is_file() or load_json(VALIDATION_PATH) != report:
                raise ValueError("validation report drift")
            if not RECEIPT_PATH.is_file() or load_json(RECEIPT_PATH) != receipt:
                raise ValueError("compact receipt drift")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"status": "FAIL", "error": str(exc)}
        print(json.dumps(result, sort_keys=True) if args.json else f"FAIL: {exc}")
        return 1

    if args.json:
        print(json.dumps({"status": report["status"], "check_count": report["check_count"], "failed_check_count": report["failed_check_count"], "leak_finding_count": report["leak_finding_count"]}, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
