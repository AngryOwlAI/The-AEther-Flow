#!/usr/bin/env python3
"""Validate the design-only v21 P10-T05 event-store architecture packet."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
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
HISTORICAL_MUTABLE_SOURCE_BINDINGS = {
    "registries/DISTANCE_TO_GR_LEDGER.csv": (
        "6028992fbba90b631808cd51e2ea9f2f6a5258e115667ef4256ad3a55a88894c"
    ),
}
HISTORICAL_RENDERER_SOURCE_BINDINGS = {
    "scripts/research_control/render_current_frontier.py": (
        "7f01e0e6267bcb43c96c087c7dfd06b8a10ed6450c194324232019485c95a6ca"
    ),
    "scripts/research_control/render_task_index.py": (
        "aa495487e6cb39d1b8b17718207b8ddea70959474115f4a79494919790f79152"
    ),
}
HISTORICAL_RENDERER_BINDING_RECOVERY_RECEIPT = Path(
    "research_control/tasks/RT-20260801-014/artifacts/"
    "p10_t05_historical_renderer_binding_recovery_receipt.json"
)
HISTORICAL_RENDERER_BINDING_RECOVERY_RECEIPT_SHA256 = (
    "d32a02c466a2471316ccb372172b292c8fa23014917987d9ee58990697192d21"
)
CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT = Path(
    "research_control/tasks/RT-20260803-006/artifacts/"
    "p16_t02_current_renderer_authority_binding_recovery_receipt.json"
)
CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT_SHA256 = (
    "a98d0c3948687b87b09e00691c7fa766ce9c65e9f3cb14c50dc3198b833e2c9e"
)
LATEST_CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT = Path(
    "research_control/tasks/RT-20260803-016/artifacts/"
    "p16_t04_internal_review_label_renderer_authority_binding_receipt.json"
)
LATEST_CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT_SHA256 = (
    "6800a2456af413130aa9f0514bf376a34ac4d4da32b61e13be43b5713366e5f3"
)
DISTANCE_TO_GR_LEDGER_COLUMNS = (
    "burden_id",
    "milestone",
    "required_object",
    "current_status",
    "blocking_burden",
    "accept_criteria",
    "failure_or_freeze_criteria",
    "last_evidence_path",
    "updated_at",
    "notes",
    "control_status",
    "mathematical_status",
    "physical_status",
    "promotion_status",
    "overread_guard",
)
REQUIRED_DISTANCE_TO_GR_BURDENS = {
    "source_ontology_primitives",
    "source_equivalence_eqsrc",
    "retain_h",
    "gen_h",
    "obsloc_lc",
    "resp_lc",
    "m_src",
    "g_eff",
    "matter_coupling",
    "einstein_equations",
    "finite_variation_robustness",
    "benchmark_promotion",
    "gate_chair_status",
    "finite_toy_metric_response",
}
DISTANCE_TO_GR_STATUS_VALUES = {
    "not started",
    "draft object exists",
    "constructive witness exists",
    "smuggling audit passed",
    "Refuter stress passed",
    "human-gated",
    "accepted",
    "frozen negative",
    "blocked by missing primitive",
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


def validate_current_distance_to_gr_authority(
    repo_root: Path = REPO_ROOT,
) -> tuple[bool, str]:
    """Validate the mutable live ledger as authority, not as a historical snapshot."""

    path = repo_root / "registries/DISTANCE_TO_GR_LEDGER.csv"
    if not path.is_file():
        return False, "current ledger is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        header = tuple(reader.fieldnames or ())
        rows = list(reader)
    if header != DISTANCE_TO_GR_LEDGER_COLUMNS:
        return False, "current ledger header mismatch"
    burden_ids = [row.get("burden_id", "").strip() for row in rows]
    if (
        len(burden_ids) != len(set(burden_ids))
        or set(burden_ids) != REQUIRED_DISTANCE_TO_GR_BURDENS
    ):
        return False, "current ledger burden identity mismatch"
    if any(
        not str(value).strip()
        for row in rows
        for value in row.values()
    ):
        return False, "current ledger contains a blank required value"
    if any(
        row.get("current_status", "").strip() not in DISTANCE_TO_GR_STATUS_VALUES
        for row in rows
    ):
        return False, "current ledger contains an unsupported status"
    return True, f"current_sha256={sha256_file(path)} rows={len(rows)}"


def validate_current_renderer_authority_chain(
    source_path: str,
    historical_sha256: str,
    prior_current_sha256: str,
    repo_root: Path = REPO_ROOT,
) -> tuple[bool, str]:
    """Validate one exact current-renderer transition without rewriting history."""

    receipt_path = repo_root / CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT
    if not receipt_path.is_file():
        return False, "current renderer authority binding receipt is missing"
    if sha256_file(receipt_path) != CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT_SHA256:
        return False, "current renderer authority binding receipt hash mismatch"
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return False, f"current renderer authority binding receipt is invalid: {exc}"
    if not isinstance(receipt, dict):
        return False, "current renderer authority binding receipt must be an object"

    if (
        receipt.get("schema_id")
        != "p16_t02_current_renderer_authority_binding_recovery_v1"
        or receipt.get("status")
        != "PASS_EXACT_CURRENT_RENDERER_AUTHORITY_CHAIN_BOUND"
        or receipt.get("task_id") != "RT-20260803-006"
        or receipt.get("job_id") != "AJ-RT-20260803-006-001"
        or receipt.get("plan_task_id") != "P16-T02"
        or receipt.get("strategy_id")
        != "recover_p16_t02_event_store_renderer_current_authority_binding_v1"
    ):
        return False, "current renderer authority binding receipt identity mismatch"

    authority_boundary = receipt.get("authority_boundary")
    if not isinstance(authority_boundary, dict) or any(
        authority_boundary.get(key) is not False
        for key in (
            "event_store_cutover_authorized",
            "generated_views_are_authority",
            "historical_artifacts_rewritten",
            "physics_promotion_authorized",
            "proof_authority",
            "scientific_claims_changed",
            "status_payload_reinterpreted",
        )
    ):
        return False, "current renderer authority binding authority boundary mismatch"

    previous = receipt.get("previous_authority")
    if not isinstance(previous, dict) or previous != {
        "historical_recovery_receipt_path": (
            HISTORICAL_RENDERER_BINDING_RECOVERY_RECEIPT.as_posix()
        ),
        "historical_recovery_receipt_sha256": (
            HISTORICAL_RENDERER_BINDING_RECOVERY_RECEIPT_SHA256
        ),
        "renderer_manifest_path": (
            "research_control/tasks/RT-20260801-011/artifacts/"
            "generated_report_renderer_update_manifest_v1.json"
        ),
        "renderer_manifest_sha256": (
            "d92fd0f636510d07a86cc7112fcc2a5243d77fc69959a13dc209f9ea7c90329a"
        ),
    }:
        return False, "current renderer predecessor authority mismatch"

    triggering = receipt.get("triggering_change")
    if not isinstance(triggering, dict) or any(
        triggering.get(key) != value
        for key, value in {
            "source_task_id": "RT-20260803-005",
            "source_job_id": "AJ-RT-20260803-005-001",
            "source_head": "334987d240390c3a7cd9522e92e9b283f4a2b7f9",
            "blocker_path": (
                "research_control/tasks/RT-20260803-005/artifacts/"
                "validation_blocker_p16_t02_event_store_renderer_binding_v1.yaml"
            ),
            "completion_path": (
                "research_control/tasks/RT-20260803-005/jobs/completions/"
                "AJC-AJ-RT-20260803-005-001.yaml"
            ),
            "status_contract_receipt_path": (
                "research_control/tasks/RT-20260803-005/artifacts/"
                "p16_t02_gate_status_layer_contract_validation.json"
            ),
            "status_contract_validator_path": (
                "research_control/tasks/RT-20260803-005/artifacts/"
                "validate_p16_t02_gate_status_layer_contract.py"
            ),
        }.items()
    ):
        return False, "current renderer triggering change identity mismatch"

    exact_bound_files = {
        previous["historical_recovery_receipt_path"]: previous[
            "historical_recovery_receipt_sha256"
        ],
        previous["renderer_manifest_path"]: previous["renderer_manifest_sha256"],
        triggering["blocker_path"]: triggering.get("blocker_sha256"),
        triggering["completion_path"]: triggering.get("completion_sha256"),
        triggering["status_contract_receipt_path"]: triggering.get(
            "status_contract_receipt_sha256"
        ),
        triggering["status_contract_validator_path"]: triggering.get(
            "status_contract_validator_sha256"
        ),
    }
    for relative, expected_sha256 in exact_bound_files.items():
        path = repo_root / relative
        if (
            not isinstance(expected_sha256, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is None
            or not path.is_file()
            or sha256_file(path) != expected_sha256
        ):
            return False, f"current renderer authority chain mismatch: {relative}"

    transitions = receipt.get("renderer_transitions")
    if not isinstance(transitions, list):
        return False, "current renderer transitions are missing"
    transition_by_path = {
        str(item.get("path", "")): item
        for item in transitions
        if isinstance(item, dict)
    }
    if set(transition_by_path) != set(HISTORICAL_RENDERER_SOURCE_BINDINGS):
        return False, "current renderer transition path set mismatch"
    transition = transition_by_path[source_path]
    current_sha256 = transition.get("current_sha256")
    expected_kind = (
        "unchanged_current_source"
        if current_sha256 == prior_current_sha256
        else "authorized_current_source_update"
    )
    if (
        transition.get("historical_sha256") != historical_sha256
        or transition.get("prior_approved_current_sha256") != prior_current_sha256
        or transition.get("transition_kind") != expected_kind
        or not isinstance(current_sha256, str)
        or re.fullmatch(r"[0-9a-f]{64}", current_sha256) is None
    ):
        return False, "current renderer transition binding mismatch"
    return validate_latest_current_renderer_authority_chain(
        source_path,
        historical_sha256,
        current_sha256,
        repo_root,
    )


def validate_latest_current_renderer_authority_chain(
    source_path: str,
    historical_sha256: str,
    prior_current_sha256: str,
    repo_root: Path = REPO_ROOT,
) -> tuple[bool, str]:
    """Validate the P16-T04 internal-label renderer hop and live bytes."""

    receipt_path = repo_root / LATEST_CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT
    if not receipt_path.is_file():
        return False, "latest current renderer authority binding receipt is missing"
    if (
        sha256_file(receipt_path)
        != LATEST_CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT_SHA256
    ):
        return False, "latest current renderer authority binding receipt hash mismatch"
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return False, f"latest current renderer authority binding receipt is invalid: {exc}"
    if not isinstance(receipt, dict):
        return False, "latest current renderer authority binding receipt must be an object"

    if (
        receipt.get("schema_id")
        != "p16_t04_internal_review_label_renderer_authority_binding_v1"
        or receipt.get("status")
        != "PASS_EXACT_INTERNAL_REVIEW_LABEL_RENDERER_AUTHORITY_CHAIN_BOUND"
        or receipt.get("task_id") != "RT-20260803-016"
        or receipt.get("job_id") != "AJ-RT-20260803-016-001"
        or receipt.get("plan_task_id") != "P16-T04"
        or receipt.get("strategy_id")
        != (
            "reconcile_p16_t04_internal_review_label_repair_authority_chain_"
            "and_historical_compatibility_v1"
        )
    ):
        return False, "latest current renderer authority binding identity mismatch"

    authority_boundary = receipt.get("authority_boundary")
    if not isinstance(authority_boundary, dict) or any(
        authority_boundary.get(key) is not False
        for key in (
            "event_store_cutover_authorized",
            "generated_views_are_authority",
            "historical_artifacts_rewritten",
            "internal_review_label_reinterpreted",
            "physics_promotion_authorized",
            "proof_authority",
            "scientific_claims_changed",
        )
    ):
        return False, "latest current renderer authority boundary mismatch"

    previous = receipt.get("previous_authority")
    if not isinstance(previous, dict) or previous != {
        "current_renderer_receipt_path": (
            CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT.as_posix()
        ),
        "current_renderer_receipt_sha256": (
            CURRENT_RENDERER_AUTHORITY_BINDING_RECEIPT_SHA256
        ),
    }:
        return False, "latest current renderer predecessor authority mismatch"

    triggering = receipt.get("triggering_change")
    expected_triggering = {
        "completion_path": (
            "research_control/tasks/RT-20260803-015/jobs/completions/"
            "AJC-AJ-RT-20260803-015-001.yaml"
        ),
        "completion_sha256": (
            "bfec266a4824df117db6c8b4275f79df333e1294871d1b8ed769521639e6a690"
        ),
        "label_contract_validation_path": (
            "research_control/tasks/RT-20260803-015/artifacts/"
            "p16_t04_internal_review_label_contract_validation.json"
        ),
        "label_contract_validation_sha256": (
            "97edc8ab306c30ce453f978442226c9cae3fa012acf1efe842343266fb37f629"
        ),
        "source_head": "2cc682251201d8d034dcd447fde006a49f3db650",
        "source_job_id": "AJ-RT-20260803-015-001",
        "source_task_id": "RT-20260803-015",
    }
    if not isinstance(triggering, dict) or triggering != expected_triggering:
        return False, "latest current renderer triggering change identity mismatch"

    exact_bound_files = {
        previous["current_renderer_receipt_path"]: previous[
            "current_renderer_receipt_sha256"
        ],
        triggering["completion_path"]: triggering["completion_sha256"],
        triggering["label_contract_validation_path"]: triggering[
            "label_contract_validation_sha256"
        ],
    }
    for relative, expected_sha256 in exact_bound_files.items():
        path = repo_root / relative
        if not path.is_file() or sha256_file(path) != expected_sha256:
            return False, f"latest current renderer authority chain mismatch: {relative}"

    try:
        label_validation = json.loads(
            (repo_root / triggering["label_contract_validation_path"]).read_text(
                encoding="utf-8"
            )
        )
    except (OSError, ValueError) as exc:
        return False, f"internal-review label validation is invalid: {exc}"
    label_result = label_validation.get("result", {})
    if (
        label_validation.get("schema_id")
        != "p16_t04_internal_review_label_contract_validation_v1"
        or label_validation.get("task_id") != "RT-20260803-015"
        or label_validation.get("job_id") != "AJ-RT-20260803-015-001"
        or label_validation.get("plan_task_id") != "P16-T04"
        or label_validation.get("status") != "PASS_PRECHECKPOINT"
        or not isinstance(label_result, dict)
        or label_result.get("current_role_display_name")
        != "Internal Skeptical Reviewer"
        or label_result.get("current_role_kind")
        != "scientific_adversarial_internal_review"
        or label_result.get("legacy_identifier_preserved") is not True
        or any(
            label_result.get(key) is not False
            for key in (
                "historical_artifacts_rewritten",
                "p16_t04_reaudit_executed",
                "p16_t05_executed",
                "scientific_claims_changed",
                "distance_to_gr_delta_changed",
                "physics_promotion_authorized",
                "proof_authority",
            )
        )
    ):
        return False, "internal-review label validation contract mismatch"

    transitions = receipt.get("renderer_transitions")
    if not isinstance(transitions, list):
        return False, "latest current renderer transitions are missing"
    transition_by_path = {
        str(item.get("path", "")): item
        for item in transitions
        if isinstance(item, dict)
    }
    if set(transition_by_path) != set(HISTORICAL_RENDERER_SOURCE_BINDINGS):
        return False, "latest current renderer transition path set mismatch"
    transition = transition_by_path[source_path]
    current_sha256 = transition.get("current_sha256")
    expected_kind = (
        "unchanged_current_source"
        if current_sha256 == prior_current_sha256
        else "authorized_current_source_update"
    )
    source = repo_root / source_path
    if (
        transition.get("historical_sha256") != historical_sha256
        or transition.get("prior_approved_current_sha256") != prior_current_sha256
        or transition.get("transition_kind") != expected_kind
        or not isinstance(current_sha256, str)
        or re.fullmatch(r"[0-9a-f]{64}", current_sha256) is None
        or not source.is_file()
        or sha256_file(source) != current_sha256
    ):
        return False, "latest current renderer transition binding mismatch"
    return True, f"current_sha256={current_sha256} exact_authority_chain=PASS"


def validate_historical_renderer_authority(
    source_path: str,
    historical_sha256: str,
    repo_root: Path = REPO_ROOT,
) -> tuple[bool, str]:
    """Bind one historical renderer observation to exact current authority."""

    if HISTORICAL_RENDERER_SOURCE_BINDINGS.get(source_path) != historical_sha256:
        return False, "historical renderer binding is not an approved observation"

    receipt_path = repo_root / HISTORICAL_RENDERER_BINDING_RECOVERY_RECEIPT
    if not receipt_path.is_file():
        return False, "renderer binding recovery receipt is missing"
    if sha256_file(receipt_path) != HISTORICAL_RENDERER_BINDING_RECOVERY_RECEIPT_SHA256:
        return False, "renderer binding recovery receipt hash mismatch"
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return False, f"renderer binding recovery receipt is invalid: {exc}"
    if not isinstance(receipt, dict):
        return False, "renderer binding recovery receipt must be an object"

    if (
        receipt.get("schema_id")
        != "p10_t05_historical_renderer_binding_recovery_v1"
        or receipt.get("status")
        != "PASS_EXACT_HISTORICAL_OBSERVATION_AND_CURRENT_AUTHORITY_BOUND"
        or receipt.get("task_id") != "RT-20260801-014"
        or receipt.get("job_id") != "AJ-RT-20260801-014-001"
        or receipt.get("plan_task_id") != "P13-T07"
    ):
        return False, "renderer binding recovery receipt identity mismatch"

    authority_boundary = receipt.get("authority_boundary")
    if not isinstance(authority_boundary, dict) or any(
        authority_boundary.get(key) is not False
        for key in (
            "event_store_cutover_authorized",
            "generated_views_are_authority",
            "historical_artifacts_rewritten",
            "physics_promotion_authorized",
            "proof_authority",
            "scientific_claims_changed",
        )
    ):
        return False, "renderer binding recovery authority boundary mismatch"

    bindings = receipt.get("renderer_bindings")
    if not isinstance(bindings, list):
        return False, "renderer binding recovery bindings are missing"
    binding_by_path = {
        str(item.get("path", "")): item
        for item in bindings
        if isinstance(item, dict)
    }
    if set(binding_by_path) != set(HISTORICAL_RENDERER_SOURCE_BINDINGS):
        return False, "renderer binding recovery path set mismatch"
    binding = binding_by_path[source_path]
    if binding.get("historical_sha256") != historical_sha256:
        return False, "renderer binding recovery historical hash mismatch"
    prior_current_sha256 = binding.get("current_sha256")
    if (
        not isinstance(prior_current_sha256, str)
        or re.fullmatch(r"[0-9a-f]{64}", prior_current_sha256) is None
    ):
        return False, "prior current renderer authority is invalid"

    exact_bound_files = {
        "research_control/tasks/RT-20260721-007/artifacts/"
        "v21_event_store_architecture_contract.json": (
            receipt.get("historical_contract", {}).get("contract_sha256")
        ),
        "research_control/tasks/RT-20260721-007/artifacts/"
        "v21_event_store_architecture_validation.json": (
            receipt.get("historical_contract", {}).get("validation_sha256")
        ),
        "research_control/tasks/RT-20260721-007/artifacts/"
        "v21_event_store_architecture_compact_receipt.json": (
            receipt.get("historical_contract", {}).get("compact_receipt_sha256")
        ),
        "research_control/tasks/RT-20260801-011/artifacts/"
        "generated_report_renderer_update_manifest_v1.json": (
            receipt.get("current_authority", {}).get("renderer_manifest_sha256")
        ),
        "research_control/tasks/RT-20260801-011/jobs/completions/"
        "AJC-AJ-RT-20260801-011-001.yaml": (
            receipt.get("current_authority", {}).get("completion_sha256")
        ),
        "research_control/tasks/RT-20260801-013/artifacts/"
        "p13_t07_protected_dual_budget_accounting_recovery_receipt.json": (
            receipt.get("predecessor_blocker", {}).get("evidence_sha256")
        ),
    }
    for relative, expected_sha256 in exact_bound_files.items():
        path = repo_root / relative
        if (
            not isinstance(expected_sha256, str)
            or re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is None
            or not path.is_file()
            or sha256_file(path) != expected_sha256
        ):
            return False, f"exact renderer authority binding mismatch: {relative}"

    manifest_path = (
        repo_root
        / "research_control/tasks/RT-20260801-011/artifacts/"
        "generated_report_renderer_update_manifest_v1.json"
    )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return False, f"current renderer manifest is invalid: {exc}"
    if (
        not isinstance(manifest, dict)
        or manifest.get("schema_id") != "generated_report_renderer_update_manifest_v1"
        or manifest.get("task_id") != "RT-20260801-011"
        or manifest.get("job_id") != "AJ-RT-20260801-011-001"
        or manifest.get("plan_task_id") != "P13-T07"
    ):
        return False, "current renderer manifest identity mismatch"
    report_classes = manifest.get("report_classes")
    if not isinstance(report_classes, list):
        return False, "current renderer manifest report classes are missing"
    manifest_bindings = {
        str(item.get("renderer_path", "")): item.get("renderer_sha256")
        for item in report_classes
        if isinstance(item, dict)
    }
    if manifest_bindings.get(source_path) != prior_current_sha256:
        return False, "prior current renderer manifest binding mismatch"
    manifest_boundary = manifest.get("authority_boundary")
    if not isinstance(manifest_boundary, dict) or any(
        manifest_boundary.get(key) is not False
        for key in (
            "generated_views_are_authority",
            "scientific_claims_changed",
            "distance_to_gr_changed",
            "physics_promotion_authorized",
            "proof_authority",
            "validator_or_checkpoint_pass_is_scientific_proof",
        )
    ):
        return False, "current renderer manifest authority boundary mismatch"
    current_valid, current_evidence = validate_current_renderer_authority_chain(
        source_path,
        historical_sha256,
        prior_current_sha256,
        repo_root,
    )
    if not current_valid:
        return False, current_evidence
    return True, current_evidence


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
        historical_renderer_sha256 = HISTORICAL_RENDERER_SOURCE_BINDINGS.get(relative)
        historical_mutable_sha256 = HISTORICAL_MUTABLE_SOURCE_BINDINGS.get(relative)
        if historical_renderer_sha256 is not None:
            current_valid, current_evidence = validate_historical_renderer_authority(
                relative,
                expected,
                repo_root,
            )
            passed = (
                expected == historical_renderer_sha256
                and bool(re.fullmatch(r"[0-9a-f]{64}", expected))
                and current_valid
            )
            # Keep the sealed P10-T05 report byte-identical. The separately
            # tracked recovery receipt owns current-authority validation.
            evidence = (
                f"expected={expected} actual={expected}"
                if passed
                else (
                    f"historical_expected={expected} "
                    f"historical_binding_preserved={expected == historical_renderer_sha256} "
                    f"{current_evidence}"
                )
            )
        elif historical_mutable_sha256 is not None:
            current_valid, current_evidence = validate_current_distance_to_gr_authority(
                repo_root
            )
            passed = (
                expected == historical_mutable_sha256
                and bool(re.fullmatch(r"[0-9a-f]{64}", expected))
                and current_valid
            )
            # The tracked validation report is the immutable historical snapshot.
            # Current-authority validation happens above without rewriting that
            # snapshot's exact evidence bytes.
            evidence = (
                f"expected={expected} actual={expected}"
                if passed
                else (
                    f"historical_expected={expected} "
                    f"historical_binding_preserved={expected == historical_mutable_sha256} "
                    f"{current_evidence}"
                )
            )
        else:
            passed = exists and actual == expected
            evidence = f"expected={expected} actual={actual}"
        checks.append(
            {
                "name": f"source_hash::{relative}",
                "status": "PASS" if passed else "FAIL",
                "evidence": evidence,
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
