#!/usr/bin/env python3
"""Validate the bounded RT-20260724-007 repository-test contract recovery."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260724-007"
RECEIPT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260724-007/artifacts/"
    "repository_test_contract_recovery_receipt.json"
)
LEDGER_PATH = ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv"
EVENT_CONTRACT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260721-007/artifacts/"
    "v21_event_store_architecture_contract.json"
)
EVENT_VALIDATION_PATH = (
    ROOT
    / "research_control/tasks/RT-20260721-007/artifacts/"
    "v21_event_store_architecture_validation.json"
)
EVENT_RECEIPT_PATH = (
    ROOT
    / "research_control/tasks/RT-20260721-007/artifacts/"
    "v21_event_store_architecture_compact_receipt.json"
)
ARTIFACT_ROOT = ROOT / "research_control/tasks/RT-20260722-002/artifacts"
TAXONOMY_TASK_PATH = ROOT / "research_control/tasks/RT-20260724-004/00_TASK.yaml"
DASHBOARD_TEST_PATH = ROOT / "tests/test_research_control.py"
BLOCKER_PATH = (
    ROOT
    / "research_control/tasks/RT-20260724-006/artifacts/"
    "validation_blocker_checkpoint_repository_test_contract_drift_v1.yaml"
)
EXACT_PATH_VALIDATOR = (
    ROOT
    / "research_control/tasks/RT-20260724-006/artifacts/"
    "validate_exact_path_whitespace_policy.py"
)

OLD_LEDGER_SHA256 = "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61"
LIVE_LEDGER_SHA256 = "6028992fbba90b631808cd51e2ea9f2f6a5258e115667ef4256ad3a55a88894c"
OLD_EVENT_CONTRACT_SHA256 = (
    "299400cc29ec0b234cf6b8174272e687ca05618e65187136691d1950af2302b4"
)
NEW_EVENT_CONTRACT_SHA256 = (
    "d5fa22e7bbc1d92f29acd6c8418d06ce7d81a042589ade77c7ba4fdebb0eda44"
)
EVENT_VALIDATION_SHA256 = (
    "6358f829c9e07adc6095a471621664830b37e7797c10b321b562b3f894b68b23"
)
EVENT_RECEIPT_SHA256 = (
    "04cc34d38b1b0125fb77c38f639895bfc49e0864ad62bfc43aba78666bef72b3"
)
ARTIFACT_REFS_SHA256 = (
    "321b470f2c03dcba402300b9d9e03bf387a3e8b4aa00d4272dda008965e6cccd"
)
ARTIFACT_RECEIPT_SHA256 = (
    "0fef04187d465489e977ab93cd372ac8d254de5c6f4fcf3f75a177ca8a53bae5"
)
OLD_TAXONOMY_TASK_SHA256 = (
    "8f356e0faee842497e2b951d4fce81cc61501c5da77df6d2067cd5df625dba47"
)
NEW_TAXONOMY_TASK_SHA256 = (
    "2dd31dcd422dfc88f1c2c7cad1ab79959817c352a02825ba8d2e1247edf8bf49"
)
OLD_DASHBOARD_TEST_SHA256 = (
    "7e11317d735d7a717e40469310c2d72795c69439277d9197abf604007ec4a9ea"
)
NEW_DASHBOARD_TEST_SHA256 = (
    "83464024e5acfc9267c126a7893cab90781ca8d26558d0bb754a2aa654c6a346"
)
BLOCKER_SHA256 = "fa0be9a6eeb3097172a440c09dd754b4898ed37bc48f5618d6c7ea82ce73b953"
GITATTRIBUTES_SHA256 = (
    "34089430a0c826871432018cd36ae5452c7571b2a3d26ce1eceb7aaeb9e7c04b"
)
HISTORICAL_CONTENT = {
    "299400cc29ec0b234cf6b8174272e687ca05618e65187136691d1950af2302b4.json":
        "299400cc29ec0b234cf6b8174272e687ca05618e65187136691d1950af2302b4",
    "cc7d678328f2242cd49a83ce9a3eaa47e30e830d48a8b70a6a29434bb4a6477d.json":
        "cc7d678328f2242cd49a83ce9a3eaa47e30e830d48a8b70a6a29434bb4a6477d",
    "e22bde41e45def27a32d99bdf4ca9e6517a2acedbf18393cac22e172b9423c51.json":
        "e22bde41e45def27a32d99bdf4ca9e6517a2acedbf18393cac22e172b9423c51",
}

OLD_TAXONOMY_BLOCK = (
    '  result_kind: "protected_verdict"\n'
    '  authority: "human_gate"\n'
)
NEW_TAXONOMY_BLOCK = (
    '  result_kind: "protected_verdict_or_deferred_human_gate"\n'
    '  authority: "human_gated"\n'
)
OLD_DASHBOARD_ASSERTIONS = (
    '        self.assertIn("post_gate_cycle_repeat", route_warning_ids)\n'
    '        self.assertIn("gate_ready_without_gate", route_warning_ids)\n'
)
NEW_DASHBOARD_ASSERTIONS = (
    '        expected_route_warning_ids = set(\n'
    '            report["metrics"]["physics_payload_ratio_diagnostics"]["metrics"][\n'
    '                "route_orbit_warning_status"\n'
    '            ]["warning_ids"]\n'
    '        )\n'
    '        self.assertEqual(expected_route_warning_ids, route_warning_ids)\n'
    '        self.assertEqual(\n'
    '            len(route_warning_ids),\n'
    '            dashboard["summary_cards"]["route_orbit_warning_count"],\n'
    '        )\n'
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def exact_reverse_hash(
    *,
    path: Path,
    old_block: str,
    new_block: str,
    old_sha256: str,
    new_sha256: str,
    errors: list[str],
) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    current_sha256 = sha256(path)
    if current_sha256 != new_sha256:
        errors.append(f"unexpected recovered file hash: {path.relative_to(ROOT)}")
    if text.count(new_block) != 1:
        errors.append(
            f"recovered block must occur exactly once: {path.relative_to(ROOT)}"
        )
        reconstructed_sha256 = ""
    else:
        reconstructed = text.replace(new_block, old_block, 1).encode("utf-8")
        reconstructed_sha256 = hashlib.sha256(reconstructed).hexdigest()
        if reconstructed_sha256 != old_sha256:
            errors.append(
                f"reversing authorized block does not restore predecessor: "
                f"{path.relative_to(ROOT)}"
            )
    return {
        "path": str(path.relative_to(ROOT)),
        "predecessor_sha256": old_sha256,
        "reconstructed_predecessor_sha256": reconstructed_sha256,
        "recovered_sha256": current_sha256,
        "authorized_block_occurrences": text.count(new_block),
    }


def run_json(*args: str) -> tuple[int, dict[str, Any] | None, str]:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = None
    return result.returncode, payload, result.stdout


def validate() -> dict[str, Any]:
    errors: list[str] = []

    ledger_sha256 = sha256(LEDGER_PATH)
    if ledger_sha256 != LIVE_LEDGER_SHA256:
        errors.append("live Distance-to-GR ledger identity changed")

    contract = json.loads(EVENT_CONTRACT_PATH.read_text(encoding="utf-8"))
    contract_sha256 = sha256(EVENT_CONTRACT_PATH)
    if contract_sha256 != NEW_EVENT_CONTRACT_SHA256:
        errors.append("event-store contract does not have the admitted recovered identity")
    if EVENT_CONTRACT_PATH.read_bytes() != canonical_json_bytes(contract):
        errors.append("event-store contract is not canonically encoded")
    ledger_bindings = [
        row
        for row in contract.get("source_bindings", [])
        if row.get("path") == "registries/DISTANCE_TO_GR_LEDGER.csv"
    ]
    if len(ledger_bindings) != 1:
        errors.append("event-store contract must have one Distance-to-GR binding")
    elif ledger_bindings[0].get("sha256") != LIVE_LEDGER_SHA256:
        errors.append("event-store contract does not bind the live Distance-to-GR hash")
    predecessor_contract = json.loads(json.dumps(contract))
    predecessor_bindings = [
        row
        for row in predecessor_contract.get("source_bindings", [])
        if row.get("path") == "registries/DISTANCE_TO_GR_LEDGER.csv"
    ]
    if len(predecessor_bindings) == 1:
        predecessor_bindings[0]["sha256"] = OLD_LEDGER_SHA256
    reconstructed_contract_sha256 = hashlib.sha256(
        canonical_json_bytes(predecessor_contract)
    ).hexdigest()
    if reconstructed_contract_sha256 != OLD_EVENT_CONTRACT_SHA256:
        errors.append("event-store reverse binding does not restore predecessor contract")

    event_validation = json.loads(EVENT_VALIDATION_PATH.read_text(encoding="utf-8"))
    event_receipt = json.loads(EVENT_RECEIPT_PATH.read_text(encoding="utf-8"))
    if sha256(EVENT_VALIDATION_PATH) != EVENT_VALIDATION_SHA256:
        errors.append("event-store validation receipt identity changed")
    if event_validation.get("status") != "PASS":
        errors.append("event-store validation report is not PASS")
    if sha256(EVENT_RECEIPT_PATH) != EVENT_RECEIPT_SHA256:
        errors.append("event-store compact receipt identity changed")
    if event_receipt.get("contract_sha256") != NEW_EVENT_CONTRACT_SHA256:
        errors.append("event-store compact receipt does not bind recovered contract")
    if (
        event_receipt.get("source_sha256", {}).get(
            "registries/DISTANCE_TO_GR_LEDGER.csv"
        )
        != LIVE_LEDGER_SHA256
    ):
        errors.append("event-store compact receipt does not bind the live ledger")

    artifact_refs_path = ARTIFACT_ROOT / "artifact_refs.json"
    artifact_receipt_path = ARTIFACT_ROOT / "compact_receipt.json"
    artifact_refs = json.loads(artifact_refs_path.read_text(encoding="utf-8"))
    artifact_receipt = json.loads(artifact_receipt_path.read_text(encoding="utf-8"))
    if sha256(artifact_refs_path) != ARTIFACT_REFS_SHA256:
        errors.append("artifact-reference manifest identity changed")
    if sha256(artifact_receipt_path) != ARTIFACT_RECEIPT_SHA256:
        errors.append("artifact-identity compact receipt identity changed")
    event_refs = [
        row
        for row in artifact_refs.get("references", [])
        if row.get("stable_alias") == "event-architecture-v1"
    ]
    expected_content_path = (
        "research_control/tasks/RT-20260722-002/artifacts/ca/"
        f"{NEW_EVENT_CONTRACT_SHA256}.json"
    )
    if len(event_refs) != 1:
        errors.append("artifact-reference manifest must have one event alias")
    else:
        event_ref = event_refs[0]
        if event_ref.get("source_sha256") != NEW_EVENT_CONTRACT_SHA256:
            errors.append("event artifact reference has stale source identity")
        if event_ref.get("content_path") != expected_content_path:
            errors.append("event artifact reference has stale content path")
    current_copy = ARTIFACT_ROOT / "ca" / f"{NEW_EVENT_CONTRACT_SHA256}.json"
    if sha256(current_copy) != NEW_EVENT_CONTRACT_SHA256:
        errors.append("recovered content-addressed event contract is not exact")
    if artifact_receipt.get("manifest_sha256") != ARTIFACT_REFS_SHA256:
        errors.append("artifact compact receipt does not bind recovered manifest")

    historical_hashes: dict[str, str] = {}
    for name, expected in HISTORICAL_CONTENT.items():
        path = ARTIFACT_ROOT / "ca" / name
        observed = sha256(path)
        historical_hashes[name] = observed
        if observed != expected:
            errors.append(f"historical content-addressed copy changed: {name}")

    taxonomy_change = exact_reverse_hash(
        path=TAXONOMY_TASK_PATH,
        old_block=OLD_TAXONOMY_BLOCK,
        new_block=NEW_TAXONOMY_BLOCK,
        old_sha256=OLD_TAXONOMY_TASK_SHA256,
        new_sha256=NEW_TAXONOMY_TASK_SHA256,
        errors=errors,
    )
    dashboard_test_change = exact_reverse_hash(
        path=DASHBOARD_TEST_PATH,
        old_block=OLD_DASHBOARD_ASSERTIONS,
        new_block=NEW_DASHBOARD_ASSERTIONS,
        old_sha256=OLD_DASHBOARD_TEST_SHA256,
        new_sha256=NEW_DASHBOARD_TEST_SHA256,
        errors=errors,
    )

    exact_returncode, exact_receipt, exact_output = run_json(
        str(ROOT / ".venv/bin/python"),
        str(EXACT_PATH_VALIDATOR),
        "--check",
        "--json",
    )
    if (
        exact_returncode != 0
        or not isinstance(exact_receipt, dict)
        or exact_receipt.get("status") != "PASS"
    ):
        errors.append("predecessor exact-path and protected-hash validation failed")
    if sha256(ROOT / ".gitattributes") != GITATTRIBUTES_SHA256:
        errors.append("six-rule exact-path policy changed")
    if sha256(BLOCKER_PATH) != BLOCKER_SHA256:
        errors.append("generation-101 checkpoint blocker changed")

    handoff = yaml.safe_load(
        (ROOT / "research_control/handoffs/handoff-0856.yaml").read_text(
            encoding="utf-8"
        )
    )
    p4_t06_flags: list[bool] = []

    def collect_p4_t06_flags(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {"p4_t06_executed", "next_plan_item_executed"}:
                    p4_t06_flags.append(bool(item))
                collect_p4_t06_flags(item)
        elif isinstance(value, list):
            for item in value:
                collect_p4_t06_flags(item)

    collect_p4_t06_flags(handoff)
    if not p4_t06_flags or any(p4_t06_flags):
        errors.append("handoff-0856 does not preserve P4-T06 nonexecution")

    return {
        "schema_id": "repository_test_contract_recovery_validation_v1",
        "authority": "operational_validation_only",
        "task_id": TASK_ID,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "event_store_reseal": {
            "ledger_sha256": ledger_sha256,
            "old_binding_sha256": OLD_LEDGER_SHA256,
            "new_binding_sha256": LIVE_LEDGER_SHA256,
            "predecessor_contract_sha256": OLD_EVENT_CONTRACT_SHA256,
            "reconstructed_predecessor_contract_sha256":
                reconstructed_contract_sha256,
            "recovered_contract_sha256": contract_sha256,
            "validation_sha256": sha256(EVENT_VALIDATION_PATH),
            "compact_receipt_sha256": sha256(EVENT_RECEIPT_PATH),
        },
        "artifact_identity_reseal": {
            "manifest_sha256": sha256(artifact_refs_path),
            "compact_receipt_sha256": sha256(artifact_receipt_path),
            "current_content_path": expected_content_path,
            "current_content_sha256": sha256(current_copy),
            "historical_content_sha256": historical_hashes,
        },
        "taxonomy_change": taxonomy_change,
        "dashboard_test_change": dashboard_test_change,
        "predecessor_preservation": {
            "exact_path_validator_returncode": exact_returncode,
            "exact_path_validator_status":
                exact_receipt.get("status")
                if isinstance(exact_receipt, dict)
                else "UNPARSEABLE",
            "exact_path_validator_output_if_failed":
                "" if exact_returncode == 0 else exact_output,
            "gitattributes_sha256": sha256(ROOT / ".gitattributes"),
            "checkpoint_blocker_sha256": sha256(BLOCKER_PATH),
            "p4_t06_flag_count": len(p4_t06_flags),
            "p4_t06_executed": any(p4_t06_flags),
        },
        "claim_limits": {
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "ontology_or_source_law_adopted": False,
            "p4_t06_executed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    receipt = validate()
    if args.write_report:
        RECEIPT_PATH.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(receipt["status"])
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
