#!/usr/bin/env python3
"""Render compact_current_frontier_v16 YAML and JSON from tracked state."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml, quote_scalar  # noqa: E402
import generated_report_provenance as report_provenance  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ID = "compact_current_frontier_v16"
PROGRAM_STATE_PATH = "research_control/program_state.yaml"
DISTANCE_LEDGER_PATH = "registries/DISTANCE_TO_GR_LEDGER.csv"
METRIC_USE_LEDGER_PATH = "registries/METRIC_USE_LEDGER.csv"
CURRENT_FRONTIER_PATH = "research_control/current_frontier.md"
MARKDOWN_REGISTRY_PATH = "registries/MARKDOWN_SOURCE_REGISTRY.csv"
ACCEPTED_STATUS_CALIBRATION_V1_PATH = "research_control/design/accepted_status_calibration_v1.yaml"
ACCEPTED_STATUS_CALIBRATION_V2_PATH = "research_control/design/accepted_status_calibration_v2.yaml"
ACCEPTED_STATUS_CALIBRATION_PATH = ACCEPTED_STATUS_CALIBRATION_V2_PATH
ACTIVE_STATE_BIFURCATION_POLICY_PATH = "research_control/design/active_state_bifurcation_policy_v1.md"
DEFAULT_YAML_PATH = "output/compact_current_frontier_v16.yaml"
DEFAULT_JSON_PATH = "output/compact_current_frontier_v16.json"
DEFAULT_MARKDOWN_PATH = "wiki/indexes/compact_current_frontier_v16.md"
TASK_REGISTRY_PATH = "registries/RESEARCH_TASK_REGISTRY.csv"
RENDERER_PATH = "scripts/research_control/render_compact_current_frontier_v16.py"
RENDERER_SHA256 = report_provenance.sha256_file(REPO_ROOT, RENDERER_PATH)
V16_PLAN_OBJECT_ID = "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V16"
HIGH_RISK_BURDEN_IDS = [
    "m_src",
    "g_eff",
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
]
REQUIRED_BLOCKED_CLAIMS = [
    "canonical ontology edit",
    "source-law adoption",
    "RR_ETransportCompletenessOrInvarianceLaw_v1 adoption",
    "unrestricted RR_E theorem status",
    "matter-semantics adoption",
    "detector-semantics adoption",
    "coupling-law adoption",
    "matter-coupling derivation or adoption",
    "stress-energy semantics",
    "stress-energy tensor",
    "matter action",
    "Einstein equations",
    "benchmark promotion",
    "Gate Chair verdict or closure",
    "proof authority",
    "completed derivation",
]
YAML_FIELD_ORDER = [
    "schema_id",
    "generated_from",
    "report_provenance",
    "active_state",
    "active_state_bifurcation",
    "next_route",
    "claim_boundary",
    "high_risk_status_cards",
    "scoped_positive_objects",
    "scoped_evidence_preconditions",
    "blocked_physical_targets",
    "distance_to_gr",
    "metric_use_ledger",
    "validation",
    "authority_warning",
]


class CompactFrontierError(RuntimeError):
    """Raised when compact frontier inputs or outputs are invalid."""


def repo_path(repo_root: Path, rel_path: str) -> Path:
    return repo_root / rel_path


def text_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return text_value(value).lower() == "true"


def split_tokens(value: Any) -> list[str]:
    return [item.strip() for item in text_value(value).split(";") if item.strip()]


def load_control_yaml(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        raise CompactFrontierError(f"missing YAML source: {rel_path}")
    try:
        data = load_yaml(path)
    except StrictYamlError as exc:
        raise CompactFrontierError(f"invalid YAML source {rel_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise CompactFrontierError(f"YAML source is not a mapping: {rel_path}")
    return data


def load_optional_control_yaml(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        return {}
    try:
        data = load_yaml(path)
    except StrictYamlError as exc:
        raise CompactFrontierError(f"invalid YAML source {rel_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise CompactFrontierError(f"YAML source is not a mapping: {rel_path}")
    return data


def read_text_source(repo_root: Path, rel_path: str) -> str:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        raise CompactFrontierError(f"missing text source: {rel_path}")
    return path.read_text(encoding="utf-8")


def read_csv_rows(repo_root: Path, rel_path: str) -> list[dict[str, str]]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        raise CompactFrontierError(f"missing CSV source: {rel_path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def handoff_path(handoff_id: str) -> str:
    return f"research_control/handoffs/{handoff_id}.yaml"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def row_by_burden(rows: list[dict[str, str]], burden_id: str) -> dict[str, str]:
    return next((item for item in rows if item.get("burden_id") == burden_id), {})


def dedupe_ordered(items: list[str]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for item in items:
        value = text_value(item)
        if value and value not in seen:
            output.append(value)
            seen.add(value)
    return output


def count_by_field(rows: list[dict[str, str]], field_name: str) -> dict[str, str]:
    counts: dict[str, int] = {}
    for row in rows:
        value = text_value(row.get(field_name)) or "unspecified"
        counts[value] = counts.get(value, 0) + 1
    return {key: str(value) for key, value in sorted(counts.items())}


def metric_use_ledger_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    forbidden_or_import_rows: set[str] = set()
    import_terms = ("import", "physical_metric", "blocked_physical_metric_use")
    for index, row in enumerate(rows):
        row_id = text_value(row.get("use_id")) or f"row-{index + 1}"
        if text_value(row.get("forbidden_interpretations")):
            forbidden_or_import_rows.add(row_id)
        haystack = " ".join(
            text_value(row.get(field))
            for field in ["use_category", "declared_scope", "allowed_use", "notes"]
        ).lower()
        if any(term in haystack for term in import_terms):
            forbidden_or_import_rows.add(row_id)

    return {
        "ledger_path": METRIC_USE_LEDGER_PATH,
        "total_row_count": str(len(rows)),
        "forbidden_or_import_row_count": str(len(forbidden_or_import_rows)),
        "blocked_physical_metric_use_row_count": str(sum(
            1 for row in rows if text_value(row.get("use_category")) == "blocked_physical_metric_use"
        )),
        "audited_clean_row_count": str(
            sum(1 for row in rows if text_value(row.get("audit_status")) == "audited_clean")
        ),
        "blocked_by_scope_row_count": str(
            sum(1 for row in rows if text_value(row.get("audit_status")) == "blocked_by_scope")
        ),
        "use_category_counts": count_by_field(rows, "use_category"),
        "audit_status_counts": count_by_field(rows, "audit_status"),
        "stress_status_counts": count_by_field(rows, "stress_status"),
    }


def markdown_registry_has_object(rows: list[dict[str, str]], object_id: str) -> bool:
    return any(row.get("object_id") == object_id for row in rows)


def reader_status_from_frontier(frontier_text: str, burden_id: str) -> str:
    marker = f"`{burden_id}`"
    for line in frontier_text.splitlines():
        if not line.startswith("|"):
            continue
        columns = [column.strip() for column in line.strip().strip("|").split("|")]
        if len(columns) >= 10 and columns[0] == marker:
            return columns[2]
    return ""


def guarded_reader_status(row: dict[str, str], frontier_text: str) -> str:
    status = reader_status_from_frontier(frontier_text, row.get("burden_id", ""))
    if status:
        return status
    raw_status = text_value(row.get("current_status"))
    if row.get("burden_id") in HIGH_RISK_BURDEN_IDS and raw_status == "accepted":
        return (
            "accepted only with layered guard "
            f"{text_value(row.get('control_status'))} "
            f"{text_value(row.get('promotion_status'))}"
        ).strip()
    return raw_status


def calibration_rows(calibration: dict[str, Any]) -> dict[str, dict[str, Any]]:
    for root_key in ("accepted_status_calibration_v2", "accepted_status_calibration_v1"):
        root = calibration.get(root_key)
        root = root if isinstance(root, dict) else {}
        rows = root.get("high_risk_objects")
        if isinstance(rows, dict):
            return {str(key): value for key, value in rows.items() if isinstance(value, dict)}
    return {}


def sentence_from_guard_token(token: str) -> str:
    raw = token.removeprefix("no_").strip()
    text = raw.replace("_", " ").strip()
    if not text:
        return ""
    return f"No {text} follows from this row."


def fallback_scope_sentence(row: dict[str, str]) -> str:
    return (
        "The status is limited to "
        f"control status {text_value(row.get('control_status')) or 'unspecified'}, "
        f"mathematical status {text_value(row.get('mathematical_status')) or 'unspecified'}, "
        f"physical status {text_value(row.get('physical_status')) or 'unspecified'}."
    )


def fallback_allowed_use_sentence(row: dict[str, str]) -> str:
    burden_id = text_value(row.get("burden_id"))
    if burden_id in {"einstein_equations", "benchmark_promotion"}:
        return "Later bounded packets may use this row only as a blocked-target boundary condition."
    return "Later bounded packets may use this row only under the listed scope and overread guards."


def fallback_blocked_overread_items(row: dict[str, str]) -> list[str]:
    return [
        sentence
        for sentence in (sentence_from_guard_token(token) for token in split_tokens(row.get("overread_guard", "")))
        if sentence
    ]


def status_card_for_row(
    row: dict[str, str],
    frontier_text: str,
    calibration: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    burden_id = text_value(row.get("burden_id"))
    card_source = calibration.get(burden_id, {})
    v2_card = card_source.get("status_card_v2") if isinstance(card_source, dict) else {}
    if isinstance(v2_card, dict) and v2_card:
        blocked_items = v2_card.get("blocked_overread")
        blocked_overread = [
            text_value(item)
            for item in blocked_items
            if text_value(item)
        ] if isinstance(blocked_items, list) else []
        full_non_conclusions = v2_card.get("full_control_non_conclusions")
        full_non_conclusions = [
            text_value(item)
            for item in full_non_conclusions
            if text_value(item)
        ] if isinstance(full_non_conclusions, list) else []
        return {
            "object_id": burden_id,
            "positive_status": text_value(v2_card.get("positive_status")),
            "exact_scope": text_value(v2_card.get("exact_scope")),
            "allowed_use": text_value(v2_card.get("allowed_use")),
            "blocked_overread": blocked_overread,
            "blocked_overread_sentence": "; ".join(blocked_overread),
            "next_burden": text_value(v2_card.get("next_burden")),
            "next_lawful_route": text_value(v2_card.get("next_lawful_route")),
            "public_summary": text_value(v2_card.get("public_summary")),
            "full_control_non_conclusions": full_non_conclusions,
            "evidence_source": text_value(card_source.get("source_v1_calibration_path"))
            or ACCEPTED_STATUS_CALIBRATION_V2_PATH,
            "status_card_version": "v2",
        }
    if card_source:
        blocked_items = card_source.get("full_control_blocked_items")
        blocked_overread = [
            text_value(item)
            for item in blocked_items
            if text_value(item)
        ] if isinstance(blocked_items, list) else [text_value(card_source.get("blocked_overread_sentence"))]
        non_conclusions = split_tokens(row.get("overread_guard", "")) or blocked_overread
        return {
            "object_id": burden_id,
            "positive_status": text_value(card_source.get("positive_status_sentence")),
            "exact_scope": text_value(card_source.get("exact_scope_sentence")),
            "allowed_use": text_value(card_source.get("allowed_use_sentence")),
            "blocked_overread": blocked_overread,
            "blocked_overread_sentence": text_value(card_source.get("blocked_overread_sentence")),
            "next_burden": f"Address the current blocking burden before any downstream promotion: {text_value(row.get('blocking_burden')) or 'unspecified'}.",
            "next_lawful_route": "one bounded continue-research packet authorized by the latest tracked handoff",
            "public_summary": text_value(card_source.get("positive_status_sentence")),
            "full_control_non_conclusions": non_conclusions,
            "evidence_source": text_value(card_source.get("evidence_source")),
            "status_card_version": "v1_compat",
        }
    blocked_overread = fallback_blocked_overread_items(row)
    non_conclusions = split_tokens(row.get("overread_guard", ""))
    return {
        "object_id": burden_id,
        "positive_status": guarded_reader_status(row, frontier_text),
        "exact_scope": fallback_scope_sentence(row),
        "allowed_use": fallback_allowed_use_sentence(row),
        "blocked_overread": blocked_overread,
        "blocked_overread_sentence": " ".join(blocked_overread),
        "next_burden": f"Address the current blocking burden before any downstream promotion: {text_value(row.get('blocking_burden')) or 'unspecified'}.",
        "next_lawful_route": "one bounded continue-research packet authorized by the latest tracked handoff",
        "public_summary": guarded_reader_status(row, frontier_text),
        "full_control_non_conclusions": non_conclusions,
        "evidence_source": text_value(row.get("last_evidence_path")),
        "status_card_version": "fallback",
    }


def high_risk_status_cards(
    rows: list[dict[str, str]],
    frontier_text: str,
    calibration: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for burden_id in HIGH_RISK_BURDEN_IDS:
        row = row_by_burden(rows, burden_id)
        if row:
            output.append(status_card_for_row(row, frontier_text, calibration))
    return output


def high_risk_row(
    row: dict[str, str],
    frontier_text: str,
    calibration: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    return {
        "burden_id": row.get("burden_id", ""),
        "reader_facing_status": guarded_reader_status(row, frontier_text),
        "legacy_status": row.get("current_status", ""),
        "control_status": row.get("control_status", ""),
        "mathematical_status": row.get("mathematical_status", ""),
        "physical_status": row.get("physical_status", ""),
        "promotion_status": row.get("promotion_status", ""),
        "overread_guard": split_tokens(row.get("overread_guard", "")),
        "last_evidence_path": row.get("last_evidence_path", ""),
        "high_risk_status_card": status_card_for_row(row, frontier_text, calibration),
    }


def scoped_positive_objects(rows: list[dict[str, str]], frontier_text: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for burden_id in ["m_src", "g_eff"]:
        row = row_by_burden(rows, burden_id)
        if not row:
            continue
        output.append(
            {
                "object_id": burden_id,
                "reader_facing_status": guarded_reader_status(row, frontier_text),
                "authority_path": row.get("last_evidence_path", ""),
                "scope_qualifier": row.get("physical_status", ""),
                "blocked_overread": split_tokens(row.get("overread_guard", "")),
            }
        )
    return output


def scoped_evidence_preconditions(rows: list[dict[str, str]], frontier_text: str) -> list[dict[str, Any]]:
    row = row_by_burden(rows, "matter_coupling")
    if not row:
        return []
    return [
        {
            "object_id": "matter_coupling",
            "reader_facing_status": guarded_reader_status(row, frontier_text),
            "authority_path": row.get("last_evidence_path", ""),
            "supports_target": "matter-semantics and matter-coupling continuation only",
            "does_not_establish": split_tokens(row.get("overread_guard", "")),
        }
    ]


def blocked_physical_targets(rows: list[dict[str, str]], frontier_text: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for burden_id in ["matter_coupling", "einstein_equations", "benchmark_promotion"]:
        row = row_by_burden(rows, burden_id)
        if not row:
            continue
        output.append(
            {
                "target_id": burden_id,
                "reader_facing_status": guarded_reader_status(row, frontier_text),
                "control_status": row.get("control_status", ""),
                "blocking_burden": row.get("blocking_burden", ""),
                "overread_guard": split_tokens(row.get("overread_guard", "")),
            }
        )
    return output


def pending_validation_layers(handoff: dict[str, Any]) -> list[dict[str, Any]]:
    layers = handoff.get("validation_layers")
    if not isinstance(layers, dict):
        return []
    pending: list[dict[str, Any]] = []
    for layer_name, layer in layers.items():
        if not isinstance(layer, dict):
            continue
        status = text_value(layer.get("status"))
        if status == "PENDING":
            evidence = layer.get("evidence")
            pending.append(
                {
                    "layer": layer_name,
                    "status": status,
                    "evidence": evidence if isinstance(evidence, list) else [],
                }
            )
    return pending


def latest_required_status(handoff: dict[str, Any]) -> str:
    validation_summary = handoff.get("validation_summary")
    if isinstance(validation_summary, dict):
        for key in ["task_local_validator_status", "compact_frontier_check_status", "final_validation_status"]:
            value = text_value(validation_summary.get(key))
            if value:
                return value
    value = text_value(handoff.get("validation_status"))
    return value if value else "PASS"


def distance_delta(handoff: dict[str, Any]) -> dict[str, Any]:
    distance = handoff.get("distance_to_gr")
    distance = distance if isinstance(distance, dict) else {}
    effect = text_value(distance.get("effect")) or text_value(distance.get("v16_delta")) or "no_distance_delta"
    changed_value = distance.get("changed")
    changed = bool_value(changed_value) if changed_value != "" else effect != "no_distance_delta"
    return {
        "effect": effect,
        "changed": changed,
        "milestone": text_value(distance.get("milestone")) or "matter_coupling",
        "burden_id": text_value(distance.get("burden_id")) or "none",
    }


def active_state_bifurcation_state(
    *,
    active_task_id: str,
    latest_handoff_id: str,
    next_action: str,
) -> dict[str, Any]:
    no_sidecar = "none"
    return {
        "latest_research_task_id": active_task_id,
        "latest_research_handoff_id": latest_handoff_id,
        "latest_research_next_action": next_action,
        "latest_project_system_task_id": no_sidecar,
        "latest_project_system_status": no_sidecar,
        "latest_project_system_sidecar_task_id": no_sidecar,
        "latest_project_system_sidecar_status": no_sidecar,
        "sidecar_supersedes_research_handoff": False,
        "next_research_route_source": "latest_research_handoff",
    }


def build_snapshot(
    repo_root: Path,
    *,
    source_commit: str | None = None,
    strict_provenance: bool | None = None,
) -> dict[str, Any]:
    program_state = load_control_yaml(repo_root, PROGRAM_STATE_PATH)
    active_task_id = text_value(program_state.get("active_task_id"))
    latest_handoff_id = text_value(program_state.get("latest_handoff_id"))
    if not active_task_id or not latest_handoff_id:
        raise CompactFrontierError("program_state.yaml must name active_task_id and latest_handoff_id")

    latest_handoff_path = handoff_path(latest_handoff_id)
    latest_handoff = load_control_yaml(repo_root, latest_handoff_path)
    ledger_rows = read_csv_rows(repo_root, DISTANCE_LEDGER_PATH)
    metric_use_rows = read_csv_rows(repo_root, METRIC_USE_LEDGER_PATH)
    markdown_rows = read_csv_rows(repo_root, MARKDOWN_REGISTRY_PATH)
    task_registry_rows = (
        read_csv_rows(repo_root, TASK_REGISTRY_PATH)
        if repo_path(repo_root, TASK_REGISTRY_PATH).is_file()
        else []
    )
    frontier_text = read_text_source(repo_root, CURRENT_FRONTIER_PATH)
    accepted_status_calibration_path = ""
    accepted_status_calibration = load_optional_control_yaml(repo_root, ACCEPTED_STATUS_CALIBRATION_V2_PATH)
    if accepted_status_calibration:
        accepted_status_calibration_path = ACCEPTED_STATUS_CALIBRATION_V2_PATH
    else:
        accepted_status_calibration = load_optional_control_yaml(repo_root, ACCEPTED_STATUS_CALIBRATION_V1_PATH)
        if accepted_status_calibration:
            accepted_status_calibration_path = ACCEPTED_STATUS_CALIBRATION_V1_PATH
    calibration = calibration_rows(accepted_status_calibration)
    selected_route = latest_handoff.get("selected_next_route")
    selected_route = selected_route if isinstance(selected_route, dict) else {}
    hard_blocks = latest_handoff.get("hard_blocks")
    hard_blocks = hard_blocks if isinstance(hard_blocks, list) else []
    current_status = text_value(program_state.get("current_status"))
    handoff_summary = text_value(latest_handoff.get("summary"))
    v15_completed = "v16_" in current_status or "v16 " in handoff_summary or "v16" in frontier_text
    v16_completed = bool_value(latest_handoff.get("v16_completed"))
    next_action = (
        text_value(latest_handoff.get("next_action"))
        or text_value(program_state.get("next_recommended_action"))
        or text_value(selected_route.get("route_id"))
    )

    high_risk_rows = [
        high_risk_row(row_by_burden(ledger_rows, burden_id), frontier_text, calibration)
        for burden_id in HIGH_RISK_BURDEN_IDS
        if row_by_burden(ledger_rows, burden_id)
    ]
    status_cards = high_risk_status_cards(ledger_rows, frontier_text, calibration)
    generated_from = [
        PROGRAM_STATE_PATH,
        latest_handoff_path,
        DISTANCE_LEDGER_PATH,
        METRIC_USE_LEDGER_PATH,
        CURRENT_FRONTIER_PATH,
        MARKDOWN_REGISTRY_PATH,
    ]
    if accepted_status_calibration_path:
        generated_from.append(accepted_status_calibration_path)
    if repo_path(repo_root, ACTIVE_STATE_BIFURCATION_POLICY_PATH).exists():
        generated_from.append(ACTIVE_STATE_BIFURCATION_POLICY_PATH)

    if repo_path(repo_root, TASK_REGISTRY_PATH).exists():
        generated_from.append(TASK_REGISTRY_PATH)
    generated_from = sorted(set(generated_from))
    source_hashes = {
        path: report_provenance.sha256_file(repo_root, path)
        for path in generated_from
    }
    if source_commit is None:
        existing = report_provenance.metadata_from_json_file(
            repo_root, DEFAULT_JSON_PATH
        )
        source_commit = report_provenance.source_commit_from_metadata(
            existing, report_provenance.git_head(repo_root)
        )
    strict = repo_root.resolve() == REPO_ROOT.resolve() if strict_provenance is None else strict_provenance
    generation_time = text_value(latest_handoff.get("created_at")) or text_value(
        latest_handoff.get("updated_at")
    )
    task_count = len(task_registry_rows)
    if not task_count:
        tasks_root = repo_path(repo_root, "research_control/tasks")
        task_count = sum(
            1 for path in tasks_root.glob("RT-*") if path.is_dir()
        ) if tasks_root.exists() else 0
    primary_source_paths = [
        PROGRAM_STATE_PATH,
        latest_handoff_path,
        DISTANCE_LEDGER_PATH,
        CURRENT_FRONTIER_PATH,
    ]
    if TASK_REGISTRY_PATH in source_hashes:
        primary_source_paths.append(TASK_REGISTRY_PATH)
    provenance = report_provenance.build_metadata(
        report_class="compact_current_frontier",
        source_commit=source_commit,
        source_hashes=source_hashes,
        primary_source_paths=primary_source_paths,
        generation_time=generation_time,
        task_count=task_count,
        renderer_path=RENDERER_PATH,
        renderer_sha256=RENDERER_SHA256,
        strict=strict,
    )

    return {
        "schema_id": SCHEMA_ID,
        "generated_from": generated_from,
        "report_provenance": provenance,
        "active_state": {
            "active_task_id": active_task_id,
            "latest_handoff_id": latest_handoff_id,
            "current_status": current_status,
            "v15_completed": v15_completed,
            "v16_completed": v16_completed,
            "v16_plan_registered": markdown_registry_has_object(markdown_rows, V16_PLAN_OBJECT_ID),
        },
        "active_state_bifurcation": active_state_bifurcation_state(
            active_task_id=active_task_id,
            latest_handoff_id=latest_handoff_id,
            next_action=next_action,
        ),
        "next_route": {
            "route_id": text_value(selected_route.get("route_id")),
            "role_family": text_value(selected_route.get("role_family")),
            "target_derivation_milestone": text_value(selected_route.get("target_derivation_milestone")),
            "milestone_burden": text_value(selected_route.get("milestone_burden")),
            "requires_human_gate": bool_value(selected_route.get("requires_human_gate")),
        },
        "claim_boundary": {
            "physics_claim_authority": False,
            "proof_authority": False,
            "blocked_claims": dedupe_ordered([*REQUIRED_BLOCKED_CLAIMS, *[text_value(item) for item in hard_blocks]]),
        },
        "high_risk_status_cards": status_cards,
        "scoped_positive_objects": scoped_positive_objects(ledger_rows, frontier_text),
        "scoped_evidence_preconditions": scoped_evidence_preconditions(ledger_rows, frontier_text),
        "blocked_physical_targets": blocked_physical_targets(ledger_rows, frontier_text),
        "distance_to_gr": {
            "delta": distance_delta(latest_handoff),
            "high_risk_rows": high_risk_rows,
        },
        "metric_use_ledger": metric_use_ledger_summary(metric_use_rows),
        "validation": {
            "latest_required_status": latest_required_status(latest_handoff),
            "pending_layers": pending_validation_layers(latest_handoff),
        },
        "authority_warning": {
            "snapshot_only_not_authority": True,
        },
    }


def validate_snapshot(snapshot: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if snapshot.get("schema_id") != SCHEMA_ID:
        errors.append("schema_id mismatch")
    provenance = snapshot.get("report_provenance")
    if not isinstance(provenance, dict):
        errors.append("report_provenance missing")
    elif provenance.get("report_class") != "compact_current_frontier":
        errors.append("report_provenance class mismatch")
    if snapshot.get("authority_warning", {}).get("snapshot_only_not_authority") is not True:
        errors.append("authority warning is missing or false")
    bifurcation = snapshot.get("active_state_bifurcation")
    if not isinstance(bifurcation, dict):
        errors.append("active_state_bifurcation missing")
    else:
        active_state = snapshot.get("active_state", {})
        if bifurcation.get("latest_research_task_id") != active_state.get("active_task_id"):
            errors.append("active_state_bifurcation latest_research_task_id mismatch")
        if bifurcation.get("latest_research_handoff_id") != active_state.get("latest_handoff_id"):
            errors.append("active_state_bifurcation latest_research_handoff_id mismatch")
        if not text_value(bifurcation.get("latest_research_next_action")):
            errors.append("active_state_bifurcation latest_research_next_action missing")
        if bifurcation.get("sidecar_supersedes_research_handoff") is not False:
            errors.append("active_state_bifurcation must not let sidecar supersede research handoff")
        if bifurcation.get("next_research_route_source") != "latest_research_handoff":
            errors.append("active_state_bifurcation next route source mismatch")
    boundary = snapshot.get("claim_boundary", {})
    if boundary.get("physics_claim_authority") is not False:
        errors.append("physics_claim_authority must be false")
    if boundary.get("proof_authority") is not False:
        errors.append("proof_authority must be false")
    blocked_claims = set(boundary.get("blocked_claims", []))
    for claim in REQUIRED_BLOCKED_CLAIMS:
        if claim not in blocked_claims:
            errors.append(f"missing blocked claim: {claim}")
    high_risk_ids = {
        row.get("burden_id")
        for row in snapshot.get("distance_to_gr", {}).get("high_risk_rows", [])
        if isinstance(row, dict)
    }
    for burden_id in HIGH_RISK_BURDEN_IDS:
        if burden_id not in high_risk_ids:
            errors.append(f"missing high-risk row: {burden_id}")
    for row in snapshot.get("distance_to_gr", {}).get("high_risk_rows", []):
        if not isinstance(row, dict):
            continue
        if row.get("burden_id") in HIGH_RISK_BURDEN_IDS and row.get("reader_facing_status") == "accepted":
            errors.append(f"bare accepted high-risk row: {row.get('burden_id')}")
        card = row.get("high_risk_status_card")
        if not isinstance(card, dict):
            errors.append(f"missing nested status card: {row.get('burden_id')}")
            continue
        if card.get("object_id") != row.get("burden_id"):
            errors.append(f"nested status card object mismatch: {row.get('burden_id')}")
    cards = snapshot.get("high_risk_status_cards")
    if not isinstance(cards, list):
        errors.append("high_risk_status_cards must be a list")
        cards = []
    cards_by_id = {
        card.get("object_id"): card
        for card in cards
        if isinstance(card, dict) and text_value(card.get("object_id"))
    }
    for burden_id in HIGH_RISK_BURDEN_IDS:
        card = cards_by_id.get(burden_id)
        if not isinstance(card, dict):
            errors.append(f"missing high-risk status card: {burden_id}")
            continue
        for field in ["positive_status", "exact_scope", "allowed_use", "next_burden", "public_summary"]:
            if not text_value(card.get(field)):
                errors.append(f"empty status card field {field}: {burden_id}")
        blocked = card.get("blocked_overread")
        if not isinstance(blocked, list) or not [item for item in blocked if text_value(item)]:
            errors.append(f"empty status card blocked_overread: {burden_id}")
        full_non_conclusions = card.get("full_control_non_conclusions")
        if (
            not isinstance(full_non_conclusions, list)
            or not [item for item in full_non_conclusions if text_value(item)]
        ):
            errors.append(f"empty status card full_control_non_conclusions: {burden_id}")
        if text_value(card.get("positive_status")).lower() == "accepted":
            errors.append(f"bare accepted status card: {burden_id}")
    metric_summary = snapshot.get("metric_use_ledger")
    if not isinstance(metric_summary, dict):
        errors.append("metric_use_ledger summary missing")
    else:
        if metric_summary.get("ledger_path") != METRIC_USE_LEDGER_PATH:
            errors.append("metric_use_ledger ledger_path mismatch")
        if int(metric_summary.get("total_row_count", 0)) <= 0:
            errors.append("metric_use_ledger total_row_count missing")
        if int(metric_summary.get("forbidden_or_import_row_count", 0)) <= 0:
            errors.append("metric_use_ledger forbidden_or_import_row_count missing")
    return errors


def markdown_list_cell(values: Any) -> str:
    if not isinstance(values, list):
        return text_value(values) if text_value(values) else "none"
    items = [text_value(item) for item in values if text_value(item)]
    return "<br>".join(items) if items else "none"


def status_cards_markdown_rows(cards: list[dict[str, Any]]) -> str:
    lines = [
        "| Object | Positive status | Scope | Allowed use | Blocked overread | Next burden |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for card in cards:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{card['object_id']}`",
                    card["positive_status"],
                    card["exact_scope"],
                    card["allowed_use"],
                    markdown_list_cell(card.get("blocked_overread", [])),
                    card.get("next_burden", ""),
                ]
            )
            + " |"
        )
    return "\n".join(lines) if len(lines) > 2 else "No high-risk status cards are available."


def render_markdown(snapshot: dict[str, Any], yaml_text: str, json_text: str) -> str:
    active = snapshot["active_state"]
    bifurcation = snapshot["active_state_bifurcation"]
    next_route = snapshot["next_route"]
    metric_use = snapshot["metric_use_ledger"]
    high_risk_rows = snapshot["distance_to_gr"]["high_risk_rows"]
    status_cards = snapshot.get("high_risk_status_cards", [])
    status_cards = status_cards if isinstance(status_cards, list) else []
    row_lines = [
        "| Burden ID | Reader-facing status | Control | Physical | Promotion |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in high_risk_rows:
        row_lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['burden_id']}`",
                    row["reader_facing_status"],
                    row["control_status"],
                    row["physical_status"],
                    row["promotion_status"],
                ]
            )
            + " |"
        )
    provenance_text = "\n".join(
        report_provenance.markdown_provenance_lines(snapshot["report_provenance"])
    )
    return (
        "<!-- authority: generated -->\n\n"
        "# Compact Current Frontier v16\n\n"
        "This generated index mirrors `output/compact_current_frontier_v16.yaml` "
        "and `output/compact_current_frontier_v16.json`. It is a snapshot-only "
        "reader aid. If it differs from tracked control state, tracked control "
        "state governs.\n\n"
        f"{provenance_text}\n"
        "## Active State\n\n"
        f"- Active task: `{active['active_task_id']}`\n"
        f"- Latest handoff: `{active['latest_handoff_id']}`\n"
        f"- Current status: `{active['current_status']}`\n"
        f"- V15 completed: `{str(active['v15_completed']).lower()}`\n"
        f"- V16 plan registered: `{str(active['v16_plan_registered']).lower()}`\n\n"
        "## Active-State Bifurcation\n\n"
        f"- Latest research task: `{bifurcation['latest_research_task_id']}`\n"
        f"- Latest research handoff: `{bifurcation['latest_research_handoff_id']}`\n"
        f"- Latest research next action: {bifurcation['latest_research_next_action']}\n"
        f"- Latest project-system task: `{bifurcation['latest_project_system_task_id']}`\n"
        f"- Latest project-system status: `{bifurcation['latest_project_system_status']}`\n"
        f"- Latest project-system sidecar task: `{bifurcation['latest_project_system_sidecar_task_id']}`\n"
        f"- Latest project-system sidecar status: `{bifurcation['latest_project_system_sidecar_status']}`\n"
        f"- Sidecar supersedes research handoff: `{str(bifurcation['sidecar_supersedes_research_handoff']).lower()}`\n"
        f"- Next research route source: `{bifurcation['next_research_route_source']}`\n\n"
        "## Next Route\n\n"
        f"- Route ID: `{next_route['route_id']}`\n"
        f"- Role family: `{next_route['role_family']}`\n"
        f"- Target milestone: `{next_route['target_derivation_milestone']}`\n"
        f"- Milestone burden: {next_route['milestone_burden']}\n"
        f"- Requires human gate: `{str(next_route['requires_human_gate']).lower()}`\n\n"
        "## High-Risk Rows\n\n"
        + "\n".join(row_lines)
        + "\n\n"
        "## Positive-First Status Cards\n\n"
        "These cards render high-risk rows in the required order: positive status, "
        "exact scope, allowed use, and blocked overread. They are operational "
        "calibration only and do not create physics proof authority.\n\n"
        f"{status_cards_markdown_rows(status_cards)}\n\n"
        "## Metric-Use Ledger\n\n"
        f"- Ledger path: `{metric_use['ledger_path']}`\n"
        f"- Total rows: `{metric_use['total_row_count']}`\n"
        f"- Forbidden/import guard rows: `{metric_use['forbidden_or_import_row_count']}`\n"
        f"- Blocked physical metric-use rows: `{metric_use['blocked_physical_metric_use_row_count']}`\n"
        "- Authority: project-control guard ledger only; no physics proof authority.\n\n"
        "## Snapshot Hashes\n\n"
        f"- YAML SHA-256: `{sha256_text(yaml_text)}`\n"
        f"- JSON SHA-256: `{sha256_text(json_text)}`\n\n"
        "## Authority Warning\n\n"
        "This compact current frontier is not physics authority, proof authority, "
        "Gate Chair authority, benchmark authority, or completed-derivation "
        "evidence.\n"
    )


def rendered_texts(snapshot: dict[str, Any]) -> tuple[str, str, str]:
    yaml_text = dump_compact_yaml(snapshot)
    json_text = json.dumps(snapshot, indent=2, sort_keys=False) + "\n"
    markdown_text = render_markdown(snapshot, yaml_text, json_text)
    return yaml_text, json_text, markdown_text


def dump_compact_yaml(data: dict[str, Any]) -> str:
    """Dump compact snapshot data in the repository's strict YAML subset."""

    lines: list[str] = []

    def emit_mapping_item(key: str, value: Any, indent: int) -> None:
        prefix = " " * indent
        rendered_key = key if key.replace("_", "").isalnum() else quote_scalar(key)
        if isinstance(value, dict):
            lines.append(f"{prefix}{rendered_key}:")
            for child_key, child_value in value.items():
                emit_mapping_item(child_key, child_value, indent + 2)
        elif isinstance(value, list):
            if not value:
                lines.append(f"{prefix}{rendered_key}: []")
                return
            lines.append(f"{prefix}{rendered_key}:")
            emit_list_items(value, indent + 2)
        else:
            lines.append(f"{prefix}{rendered_key}: {quote_scalar(value)}")

    def emit_list_items(values: list[Any], indent: int) -> None:
        prefix = " " * indent
        for item in values:
            if isinstance(item, dict):
                ordered = list(item.items())
                if not ordered:
                    lines.append(f"{prefix}- empty: true")
                    continue
                first_key, first_value = ordered[0]
                if isinstance(first_value, dict):
                    lines.append(f"{prefix}- {first_key}:")
                    for child_key, child_value in first_value.items():
                        emit_mapping_item(child_key, child_value, indent + 2)
                elif isinstance(first_value, list):
                    lines.append(f"{prefix}- {first_key}:")
                    emit_list_items(first_value, indent + 2)
                else:
                    lines.append(f"{prefix}- {first_key}: {quote_scalar(first_value)}")
                for child_key, child_value in ordered[1:]:
                    emit_mapping_item(child_key, child_value, indent + 2)
            else:
                lines.append(f"{prefix}- {quote_scalar(item)}")

    for key in YAML_FIELD_ORDER:
        if key in data:
            emit_mapping_item(key, data[key], 0)
    for key, value in data.items():
        if key not in YAML_FIELD_ORDER:
            emit_mapping_item(key, value, 0)
    return "\n".join(lines) + "\n"


def check_outputs(repo_root: Path, yaml_text: str, json_text: str, markdown_text: str) -> bool:
    expected = {
        DEFAULT_YAML_PATH: yaml_text,
        DEFAULT_JSON_PATH: json_text,
        DEFAULT_MARKDOWN_PATH: markdown_text,
    }
    return all(repo_path(repo_root, rel_path).exists() and repo_path(repo_root, rel_path).read_text(encoding="utf-8") == text for rel_path, text in expected.items())


def write_outputs(repo_root: Path, yaml_text: str, json_text: str, markdown_text: str) -> None:
    for rel_path, text in [
        (DEFAULT_YAML_PATH, yaml_text),
        (DEFAULT_JSON_PATH, json_text),
        (DEFAULT_MARKDOWN_PATH, markdown_text),
    ]:
        path = repo_path(repo_root, rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def status_payload(snapshot: dict[str, Any], status: str, errors: list[str]) -> dict[str, Any]:
    yaml_text, json_text, markdown_text = rendered_texts(snapshot)
    return {
        "schema_id": SCHEMA_ID,
        "status": status,
        "errors": errors,
        "active_task_id": snapshot["active_state"]["active_task_id"],
        "latest_handoff_id": snapshot["active_state"]["latest_handoff_id"],
        "next_route_id": snapshot["next_route"]["route_id"],
        "active_state_bifurcation": snapshot["active_state_bifurcation"],
        "yaml_path": DEFAULT_YAML_PATH,
        "json_path": DEFAULT_JSON_PATH,
        "markdown_path": DEFAULT_MARKDOWN_PATH,
        "yaml_sha256": sha256_text(yaml_text),
        "json_sha256": sha256_text(json_text),
        "markdown_sha256": sha256_text(markdown_text),
        "high_risk_row_count": len(snapshot["distance_to_gr"]["high_risk_rows"]),
        "high_risk_status_card_count": len(snapshot.get("high_risk_status_cards", [])),
        "metric_use_forbidden_or_import_row_count": int(
            snapshot["metric_use_ledger"]["forbidden_or_import_row_count"]
        ),
        "blocked_claim_count": len(snapshot["claim_boundary"]["blocked_claims"]),
        "snapshot_only_not_authority": snapshot["authority_warning"]["snapshot_only_not_authority"],
        "report_provenance": snapshot["report_provenance"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write compact YAML JSON and markdown outputs")
    mode.add_argument("--check", action="store_true", help="verify compact outputs are current and schema-valid")
    mode.add_argument("--json", action="store_true", help="emit compact snapshot JSON")
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    existing_metadata = report_provenance.metadata_from_json_file(
        repo_root, DEFAULT_JSON_PATH
    )
    source_commit = (
        report_provenance.git_head(repo_root)
        if args.write
        else report_provenance.source_commit_from_metadata(
            existing_metadata, report_provenance.git_head(repo_root)
        )
    )
    try:
        snapshot = build_snapshot(repo_root, source_commit=source_commit)
    except (CompactFrontierError, report_provenance.GeneratedReportProvenanceError) as exc:
        print(f"render_compact_current_frontier_v16: {exc}", file=sys.stderr)
        return 2

    errors = validate_snapshot(snapshot)
    provenance_validation = report_provenance.validate_metadata(
        repo_root=repo_root,
        observed=existing_metadata or {},
        expected=snapshot["report_provenance"],
        strict=repo_root == REPO_ROOT,
    )
    yaml_text, json_text, markdown_text = rendered_texts(snapshot)
    if args.write:
        if errors:
            print(json.dumps(status_payload(snapshot, "invalid", errors), indent=2, sort_keys=True))
            return 1
        write_outputs(repo_root, yaml_text, json_text, markdown_text)
        written_metadata = report_provenance.metadata_from_json_file(
            repo_root, DEFAULT_JSON_PATH
        ) or {}
        provenance_validation = report_provenance.validate_metadata(
            repo_root=repo_root,
            observed=written_metadata,
            expected=snapshot["report_provenance"],
            strict=repo_root == REPO_ROOT,
        )
        payload = status_payload(snapshot, "written", [])
        payload["provenance_validation"] = provenance_validation
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    if args.check:
        current = check_outputs(repo_root, yaml_text, json_text, markdown_text)
        fresh = current and not errors and provenance_validation["status"] == "PASS"
        status = "pass" if fresh else "stale" if not errors else "invalid"
        payload = status_payload(snapshot, status, errors)
        payload["provenance_validation"] = provenance_validation
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if fresh else 1
    print(json_text, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
