#!/usr/bin/env python3
"""Reseal one P10-T05 binding and its exact P10-T07 identity dependents."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260723-008"
CONTRACT_REL = (
    "research_control/tasks/RT-20260721-007/artifacts/"
    "v21_event_store_architecture_contract.json"
)
CONTRACT_PATH = REPO_ROOT / CONTRACT_REL
EVENT_VALIDATOR_REL = (
    "research_control/tasks/RT-20260721-007/artifacts/"
    "validate_v21_event_store_architecture.py"
)
EVENT_VALIDATOR_PATH = REPO_ROOT / EVENT_VALIDATOR_REL
IDENTITY_TOOL_REL = (
    "research_control/tasks/RT-20260722-002/artifacts/artifact_identity.py"
)
IDENTITY_TOOL_PATH = REPO_ROOT / IDENTITY_TOOL_REL
RECEIPT_REL = (
    "research_control/tasks/RT-20260723-008/artifacts/"
    "p10_t05_p10_t07_identity_recovery_receipt.json"
)
RECEIPT_PATH = REPO_ROOT / RECEIPT_REL

SOURCE_REL = "scripts/research_control/report_physics_progress_metrics.py"
SOURCE_PATH = REPO_ROOT / SOURCE_REL
OLD_SOURCE_SHA256 = (
    "46289a1b861e350b4d0a0bd27de3a8fbff8c9589de0a019ecd36d3fdd2a59112"
)
NEW_SOURCE_SHA256 = (
    "07cd220950e4b85632385da1dcaa932c8a6c48c50b33e2736dd6f181bc9abfd1"
)
OLD_CONTRACT_SHA256 = (
    "cc7d678328f2242cd49a83ce9a3eaa47e30e830d48a8b70a6a29434bb4a6477d"
)
NEW_CONTRACT_SHA256 = (
    "299400cc29ec0b234cf6b8174272e687ca05618e65187136691d1950af2302b4"
)

P10_T05_DERIVED_PATHS = (
    "research_control/tasks/RT-20260721-007/artifacts/"
    "v21_event_store_architecture_validation.json",
    "research_control/tasks/RT-20260721-007/artifacts/"
    "v21_event_store_architecture_compact_receipt.json",
)
P10_T07_CURRENT_PATHS = (
    "research_control/tasks/RT-20260722-002/artifacts/artifact_refs.json",
    "research_control/tasks/RT-20260722-002/artifacts/ca/"
    f"{NEW_CONTRACT_SHA256}.json",
    "research_control/tasks/RT-20260722-002/artifacts/compact_receipt.json",
)
AUTHORIZED_WRITE_PATHS = (
    CONTRACT_REL,
    *P10_T05_DERIVED_PATHS,
    *P10_T07_CURRENT_PATHS,
)
PREDECESSOR_COPIES = {
    (
        "research_control/tasks/RT-20260722-002/artifacts/ca/"
        "e22bde41e45def27a32d99bdf4ca9e6517a2acedbf18393cac22e172b9423c51.json"
    ): "e22bde41e45def27a32d99bdf4ca9e6517a2acedbf18393cac22e172b9423c51",
    (
        "research_control/tasks/RT-20260722-002/artifacts/ca/"
        f"{OLD_CONTRACT_SHA256}.json"
    ): OLD_CONTRACT_SHA256,
}


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes()) if path.is_file() else ""


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_binding(contract: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in contract.get("source_bindings", [])
        if item.get("path") == SOURCE_REL
    ]


def candidate_contract(contract: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    candidate = copy.deepcopy(contract)
    matches = source_binding(candidate)
    if len(matches) == 1:
        matches[0]["sha256"] = NEW_SOURCE_SHA256
    payload = canonical_json_bytes(candidate)
    return candidate, payload


def reverse_contract_matches_predecessor(contract: dict[str, Any]) -> bool:
    predecessor = copy.deepcopy(contract)
    matches = source_binding(predecessor)
    if len(matches) != 1:
        return False
    matches[0]["sha256"] = OLD_SOURCE_SHA256
    predecessor_path = (
        REPO_ROOT
        / "research_control/tasks/RT-20260722-002/artifacts/ca/"
        f"{OLD_CONTRACT_SHA256}.json"
    )
    predecessor_contract = json.loads(
        predecessor_path.read_text(encoding="utf-8")
    )
    return predecessor == predecessor_contract


def predecessor_hashes() -> dict[str, str]:
    return {
        path_text: file_sha256(REPO_ROOT / path_text)
        for path_text in PREDECESSOR_COPIES
    }


def final_receipt(
    contract: dict[str, Any],
    event_result: dict[str, Any],
    identity_validation: dict[str, Any],
    identity_drift: list[str],
) -> dict[str, Any]:
    activation = contract.get("activation_state", {})
    authority = contract.get("authority_contract", {})
    path_hashes = {
        path_text: file_sha256(REPO_ROOT / path_text)
        for path_text in AUTHORIZED_WRITE_PATHS
    }
    return {
        "activation_state": activation,
        "authorized_write_path_count": len(AUTHORIZED_WRITE_PATHS),
        "authorized_write_paths": list(AUTHORIZED_WRITE_PATHS),
        "event_store_activation_changed": False,
        "event_store_validator": {
            "drift": event_result.get("drift", []),
            "failed_checks": event_result.get("failed_checks", []),
            "status": event_result.get("status"),
            "validation_status": event_result.get("validation_status"),
        },
        "identity_validation": {
            "check_count": identity_validation.get("check_count"),
            "drift": identity_drift,
            "failed_check_count": identity_validation.get("failed_check_count"),
            "reference_count": identity_validation.get("reference_count"),
            "status": identity_validation.get("status"),
        },
        "new_contract_sha256": file_sha256(CONTRACT_PATH),
        "new_source_sha256": file_sha256(SOURCE_PATH),
        "old_contract_sha256": OLD_CONTRACT_SHA256,
        "old_source_sha256": OLD_SOURCE_SHA256,
        "path_sha256": path_hashes,
        "physics_promotion_authorized": False,
        "predecessor_content_copies": predecessor_hashes(),
        "predecessor_content_copies_changed": False,
        "proof_authority": False,
        "registered_tex_authority_preserved": authority.get(
            "registered_tex_authority_preserved"
        ),
        "schema_id": "p10_t05_p10_t07_identity_recovery_receipt_v1",
        "scientific_claims_changed": False,
        "source_binding_path": SOURCE_REL,
        "source_binding_replacement_count": 1,
        "status": "PASS",
        "task_id": TASK_ID,
    }


def final_state(
    event_module: ModuleType,
    identity_module: ModuleType,
) -> tuple[dict[str, Any], dict[str, Any], list[str], dict[str, Any]]:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    event_result = event_module.run("check")
    identity_outputs, identity_validation = identity_module.expected_outputs()
    identity_drift = identity_module.drift_paths(identity_outputs)
    receipt = final_receipt(
        contract,
        event_result,
        identity_validation,
        identity_drift,
    )
    return contract, event_result, identity_drift, receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    event_module = load_module("p10_t05_event_validator", EVENT_VALIDATOR_PATH)
    identity_module = load_module("p10_t07_identity_tool", IDENTITY_TOOL_PATH)
    contract_before = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    contract_before_sha256 = file_sha256(CONTRACT_PATH)
    binding_before = source_binding(contract_before)
    candidate, candidate_bytes = candidate_contract(contract_before)
    candidate_sha256 = sha256_bytes(candidate_bytes)
    predecessors_before = predecessor_hashes()

    before_event = event_module.run("check")
    before_identity_outputs, before_identity_validation = (
        identity_module.expected_outputs()
    )
    before_identity_drift = identity_module.drift_paths(before_identity_outputs)

    initial_write = args.write and contract_before_sha256 == OLD_CONTRACT_SHA256
    receipt_recovery = (
        args.write
        and contract_before_sha256 == NEW_CONTRACT_SHA256
        and before_event.get("status") == "PASS"
        and before_event.get("validation_status") == "PASS"
        and not before_event.get("drift")
        and not before_event.get("failed_checks")
        and before_identity_validation.get("status") == "PASS"
        and not before_identity_drift
    )

    if initial_write:
        preconditions = {
            "candidate_contract_hash_exact": candidate_sha256
            == NEW_CONTRACT_SHA256,
            "current_contract_is_exact_predecessor": contract_before_sha256
            == OLD_CONTRACT_SHA256,
            "current_source_hash_exact": file_sha256(SOURCE_PATH)
            == NEW_SOURCE_SHA256,
            "event_validator_failure_is_exact": (
                before_event.get("failed_checks")
                == [f"source_hash::{SOURCE_REL}"]
                and tuple(before_event.get("drift", [])) == P10_T05_DERIVED_PATHS
            ),
            "identity_outputs_current_before_reseal": (
                before_identity_validation.get("status") == "PASS"
                and not before_identity_drift
            ),
            "one_old_source_binding_exact": (
                len(binding_before) == 1
                and binding_before[0].get("sha256") == OLD_SOURCE_SHA256
            ),
            "predecessor_copies_exact": predecessors_before
            == PREDECESSOR_COPIES,
        }
        written_paths: list[str] = []
        if all(preconditions.values()):
            identity_module.atomic_write(CONTRACT_PATH, candidate_bytes)
            written_paths.append(CONTRACT_REL)

            event_write_result = event_module.run("write")
            if event_write_result.get("status") != "PASS":
                raise RuntimeError(
                    f"P10-T05 deterministic write failed: {event_write_result}"
                )
            written_paths.extend(P10_T05_DERIVED_PATHS)

            identity_outputs, identity_validation = identity_module.expected_outputs()
            identity_drift = identity_module.drift_paths(identity_outputs)
            if (
                identity_validation.get("status") != "PASS"
                or tuple(identity_drift) != P10_T07_CURRENT_PATHS
            ):
                raise RuntimeError(
                    "P10-T07 drift is not the exact authorized set: "
                    f"{identity_drift}"
                )
            for path_text in P10_T07_CURRENT_PATHS:
                identity_module.atomic_write(
                    REPO_ROOT / path_text,
                    identity_outputs[path_text],
                )
                written_paths.append(path_text)
        else:
            event_write_result = {"status": "NOT_RUN"}
        write_phase = "initial_reseal"
    elif receipt_recovery:
        preconditions = {
            "candidate_contract_hash_exact": candidate_sha256
            == NEW_CONTRACT_SHA256,
            "current_contract_is_exact_successor": contract_before_sha256
            == NEW_CONTRACT_SHA256,
            "current_source_hash_exact": file_sha256(SOURCE_PATH)
            == NEW_SOURCE_SHA256,
            "event_outputs_current_after_reseal": (
                before_event.get("status") == "PASS"
                and before_event.get("validation_status") == "PASS"
                and not before_event.get("drift")
                and not before_event.get("failed_checks")
            ),
            "identity_outputs_current_after_reseal": (
                before_identity_validation.get("status") == "PASS"
                and not before_identity_drift
            ),
            "one_new_source_binding_exact": (
                len(binding_before) == 1
                and binding_before[0].get("sha256") == NEW_SOURCE_SHA256
            ),
            "predecessor_copies_exact": predecessors_before
            == PREDECESSOR_COPIES,
        }
        written_paths = []
        event_write_result = {"status": "NOT_RUN"}
        write_phase = "receipt_recovery"
    else:
        preconditions = {
            "candidate_contract_hash_exact": contract_before_sha256
            == NEW_CONTRACT_SHA256,
            "current_contract_is_exact_successor": contract_before_sha256
            == NEW_CONTRACT_SHA256,
            "current_source_hash_exact": file_sha256(SOURCE_PATH)
            == NEW_SOURCE_SHA256,
            "one_new_source_binding_exact": (
                len(binding_before) == 1
                and binding_before[0].get("sha256") == NEW_SOURCE_SHA256
            ),
            "reverse_binding_recovers_exact_predecessor_semantics": (
                reverse_contract_matches_predecessor(contract_before)
            ),
            "predecessor_copies_exact": predecessors_before
            == PREDECESSOR_COPIES,
        }
        written_paths = []
        event_write_result = {"status": "NOT_RUN"}
        write_phase = "check"

    (
        contract_after,
        event_after,
        identity_drift_after,
        receipt_expected,
    ) = final_state(event_module, identity_module)
    identity_outputs_after, identity_validation_after = (
        identity_module.expected_outputs()
    )
    del identity_outputs_after

    postconditions = {
        "repair_write_set_exact": (
            tuple(written_paths) == AUTHORIZED_WRITE_PATHS
            if write_phase == "initial_reseal"
            else not written_paths
        ),
        "contract_hash_exact": file_sha256(CONTRACT_PATH)
        == NEW_CONTRACT_SHA256,
        "event_validator_pass": (
            event_after.get("status") == "PASS"
            and event_after.get("validation_status") == "PASS"
            and not event_after.get("drift")
            and not event_after.get("failed_checks")
        ),
        "identity_validator_pass": (
            identity_validation_after.get("status") == "PASS"
            and not identity_drift_after
        ),
        "predecessor_copies_preserved": (
            predecessors_before
            == predecessor_hashes()
            == PREDECESSOR_COPIES
        ),
        "reverse_binding_recovers_exact_predecessor_semantics": (
            reverse_contract_matches_predecessor(contract_after)
        ),
    }

    if args.write and all(preconditions.values()) and all(postconditions.values()):
        identity_module.atomic_write(
            RECEIPT_PATH,
            canonical_json_bytes(receipt_expected),
        )

    receipt_current = (
        RECEIPT_PATH.is_file()
        and RECEIPT_PATH.read_bytes() == canonical_json_bytes(receipt_expected)
    )
    postconditions["receipt_current"] = receipt_current
    status = (
        "PASS"
        if all(preconditions.values()) and all(postconditions.values())
        else "FAIL"
    )
    payload = {
        "authorized_write_paths": list(AUTHORIZED_WRITE_PATHS),
        "candidate_contract_sha256": candidate_sha256,
        "contract_sha256_after": file_sha256(CONTRACT_PATH),
        "contract_sha256_before": contract_before_sha256,
        "event_write_status": event_write_result.get("status"),
        "identity_drift_after": identity_drift_after,
        "identity_drift_before": before_identity_drift,
        "mode": "write" if args.write else "check",
        "postconditions": postconditions,
        "preconditions": preconditions,
        "receipt_path": RECEIPT_REL,
        "schema_id": "p10_t05_p10_t07_identity_recovery_run_v1",
        "status": status,
        "write_phase": write_phase,
        "written_paths": written_paths,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
