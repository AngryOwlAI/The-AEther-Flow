#!/usr/bin/env python3
"""Render research_control/current_frontier.md from tracked control state."""

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

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402
import generated_report_provenance as report_provenance  # noqa: E402
import task_taxonomy  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ID = "current_frontier_state_v1"
DEFAULT_FRONTIER_PATH = "research_control/current_frontier.md"
TASK_REGISTRY_PATH = "registries/RESEARCH_TASK_REGISTRY.csv"
RENDERER_PATH = "scripts/research_control/render_current_frontier.py"
RENDERER_SHA256 = report_provenance.sha256_file(REPO_ROOT, RENDERER_PATH)
LEDGER_PATH = "registries/DISTANCE_TO_GR_LEDGER.csv"
METRIC_USE_LEDGER_PATH = "registries/METRIC_USE_LEDGER.csv"
STATUS_ALIAS_PATH = "research_control/design/distance_to_gr_status_aliases.yaml"
ACCEPTED_STATUS_CALIBRATION_V1_PATH = "research_control/design/accepted_status_calibration_v1.yaml"
ACCEPTED_STATUS_CALIBRATION_V2_PATH = "research_control/design/accepted_status_calibration_v2.yaml"
ACCEPTED_STATUS_CALIBRATION_PATH = ACCEPTED_STATUS_CALIBRATION_V2_PATH
ACTIVE_STATE_BIFURCATION_POLICY_PATH = "research_control/design/active_state_bifurcation_policy_v1.md"
HIGH_RISK_STATUS_CARD_IDS = [
    "m_src",
    "g_eff",
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
]
VALIDATION_LAYER_ORDER = [
    "pre_execution",
    "completion_internal",
    "post_write",
    "post_checkpoint",
    "renderer",
    "memory_bootstrap",
    "claim_language_linter",
]
AUTHORIZATION_LAYER_ORDER = [
    "protected_scoped_gate_review_authorized",
    "protected_scoped_gate_review_scope",
    "protected_scoped_gate_review_authority_source_path",
    "downstream_physics_promotion_authorized",
    "downstream_physics_promotion_authority_source_path",
    "benchmark_promotion_authorized",
    "benchmark_promotion_authority_source_path",
    "completed_derivation_authorized",
    "completed_derivation_authority_source_path",
]
VALIDATION_STATUS_ORDER = [
    "PASS",
    "PASS_WITH_WARNINGS",
    "PENDING",
    "FAIL",
    "NOT_RUN",
    "NOT_APPLICABLE",
    "UNSPECIFIED",
]
VALIDATION_STATUS_MEANINGS = {
    "PASS": "receipt complete",
    "PASS_WITH_WARNINGS": "receipt complete with stated warnings",
    "PENDING": "open item; evidence must explain why",
    "FAIL": "blocking failure",
    "NOT_RUN": "not run for this packet",
    "NOT_APPLICABLE": "not applicable to this packet",
    "UNSPECIFIED": "missing status; inspect source",
}
AUTHORIZATION_BOOLEAN_FIELDS = {
    "protected_scoped_gate_review_authorized",
    "downstream_physics_promotion_authorized",
    "benchmark_promotion_authorized",
    "completed_derivation_authorized",
}
AUTHORIZATION_LAYER_MEANINGS = {
    "protected_scoped_gate_review_authorized": "scoped review authority only",
    "protected_scoped_gate_review_scope": "exact scope of protected review authority",
    "protected_scoped_gate_review_authority_source_path": "tracked source for scoped review authority",
    "downstream_physics_promotion_authorized": "authorizes downstream physics promotion only when true",
    "downstream_physics_promotion_authority_source_path": "tracked source for downstream promotion authority",
    "benchmark_promotion_authorized": "authorizes benchmark promotion only when true",
    "benchmark_promotion_authority_source_path": "tracked source for benchmark authority",
    "completed_derivation_authorized": "authorizes completed-derivation claim only when true",
    "completed_derivation_authority_source_path": "tracked source for completed-derivation authority",
}

BLOCKED_CLAIMS = [
    "canonical ontology edit",
    "source-law adoption",
    "`MetricData(E)` adoption",
    "`g_eff` adoption or scope expansion",
    "unscoped or target coupling-law adoption",
    "matter-coupling derivation",
    "target matter-coupling adoption",
    "target stress-energy semantics",
    "target stress-energy tensor",
    "target matter action",
    "target detector semantics",
    "Einstein equations",
    "exact-GR benchmark promotion",
    "benchmark closure without protected authority",
    "completed derivation",
    "future source-extension impossibility",
    "program-wide no-go conclusion",
    "this snapshot as independent authority",
    "generated graph, checker, registry, validator, local cache, role, handoff, approval, or commit status as scientific proof",
]


class FrontierRenderError(RuntimeError):
    """Raised when authoritative inputs needed for rendering are absent."""


def repo_path(repo_root: Path, rel_path: str) -> Path:
    return repo_root / rel_path


def load_control_yaml(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        raise FrontierRenderError(f"missing required YAML source: {rel_path}")
    try:
        data = load_yaml(path)
    except StrictYamlError as exc:
        raise FrontierRenderError(f"invalid YAML source {rel_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise FrontierRenderError(f"YAML source is not a mapping: {rel_path}")
    return data


def read_csv_rows(repo_root: Path, rel_path: str) -> list[dict[str, str]]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        raise FrontierRenderError(f"missing required CSV source: {rel_path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def load_optional_control_yaml(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_path(repo_root, rel_path)
    if not path.exists():
        return {}
    try:
        data = load_yaml(path)
    except StrictYamlError as exc:
        raise FrontierRenderError(f"invalid YAML source {rel_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise FrontierRenderError(f"YAML source is not a mapping: {rel_path}")
    return data


def text_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def md_cell(value: Any) -> str:
    text = text_value(value).replace("\n", " ")
    return text.replace("|", r"\|")


def code_value(value: Any) -> str:
    text = text_value(value)
    return f"`{text}`" if text else "none"


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return text_value(value).lower() == "true"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def handoff_path(handoff_id: str) -> str:
    return f"research_control/handoffs/{handoff_id}.yaml"


def active_task_path(task_id: str) -> str:
    return f"research_control/tasks/{task_id}/00_TASK.yaml"


def line_list(items: list[str]) -> str:
    return "\n".join(f"- [ ] {item}" for item in items)


def split_tokens(value: Any) -> list[str]:
    return [item.strip() for item in text_value(value).split(";") if item.strip()]


def count_by_field(rows: list[dict[str, str]], field_name: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = text_value(row.get(field_name)) or "unspecified"
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


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
        "total_row_count": len(rows),
        "forbidden_or_import_row_count": len(forbidden_or_import_rows),
        "blocked_physical_metric_use_row_count": sum(
            1 for row in rows if text_value(row.get("use_category")) == "blocked_physical_metric_use"
        ),
        "audited_clean_row_count": sum(1 for row in rows if text_value(row.get("audit_status")) == "audited_clean"),
        "blocked_by_scope_row_count": sum(1 for row in rows if text_value(row.get("audit_status")) == "blocked_by_scope"),
        "use_category_counts": count_by_field(rows, "use_category"),
        "audit_status_counts": count_by_field(rows, "audit_status"),
        "stress_status_counts": count_by_field(rows, "stress_status"),
    }


def inline_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return "; ".join(f"`{md_cell(key)}`: {value}" for key, value in counts.items())


def metric_use_ledger_markdown(summary: dict[str, Any]) -> str:
    return f"""`{METRIC_USE_LEDGER_PATH}` is a project-control guard ledger for
metric-adjacent wording. It records allowed scope and blocked interpretations
only. It does not adopt `MetricData(E)`, expand `g_eff`, authorize a physical
metric, import matter dynamics, promote benchmark status, or prove any
downstream GR claim.

| Field | Value |
| --- | --- |
| Ledger path | `{md_cell(summary.get('ledger_path'))}` |
| Total rows | {int(summary.get('total_row_count', 0))} |
| Forbidden/import guard rows | {int(summary.get('forbidden_or_import_row_count', 0))} |
| Blocked physical metric-use rows | {int(summary.get('blocked_physical_metric_use_row_count', 0))} |
| Audited-clean rows | {int(summary.get('audited_clean_row_count', 0))} |
| Blocked-by-scope rows | {int(summary.get('blocked_by_scope_row_count', 0))} |
| Use categories | {inline_counts(summary.get('use_category_counts', {}))} |
| Audit statuses | {inline_counts(summary.get('audit_status_counts', {}))} |"""


def guard_cell(value: Any) -> str:
    tokens = split_tokens(value)
    if not tokens:
        return "none"
    return "<br>".join(md_cell(token) for token in tokens)


def sentence_fragment(value: Any, fallback: str) -> str:
    text = text_value(value).rstrip(".")
    return text if text else fallback


def status_alias_rows(status_aliases: dict[str, Any]) -> dict[str, dict[str, Any]]:
    aliases = status_aliases.get("row_aliases")
    if not isinstance(aliases, dict):
        return {}
    return {str(key): value for key, value in aliases.items() if isinstance(value, dict)}


def status_alias_for_row(row: dict[str, str], aliases: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return aliases.get(row.get("burden_id", ""), {})


def reader_facing_status(row: dict[str, str], aliases: dict[str, dict[str, Any]]) -> str:
    alias = status_alias_for_row(row, aliases)
    display = text_value(alias.get("display_status"))
    if display:
        return display
    return text_value(row.get("current_status"))


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
    pieces = [
        f"control status {text_value(row.get('control_status')) or 'unspecified'}",
        f"mathematical status {text_value(row.get('mathematical_status')) or 'unspecified'}",
        f"physical status {text_value(row.get('physical_status')) or 'unspecified'}",
    ]
    return "The status is limited to " + ", ".join(pieces) + "."


def fallback_allowed_use_sentence(row: dict[str, str]) -> str:
    burden_id = text_value(row.get("burden_id"))
    if burden_id in {"einstein_equations", "benchmark_promotion"}:
        return "Later bounded packets may use this row only as a blocked-target boundary condition."
    return "Later bounded packets may use this row only under the listed scope and overread guards."


def fallback_blocked_overread_items(row: dict[str, str]) -> list[str]:
    tokens = split_tokens(row.get("overread_guard", ""))
    sentences = [sentence_from_guard_token(token) for token in tokens]
    return [sentence for sentence in sentences if sentence]


def status_card_for_row(
    row: dict[str, str],
    aliases: dict[str, dict[str, Any]],
    calibration: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    burden_id = text_value(row.get("burden_id"))
    card_source = calibration.get(burden_id, {})
    v2_card = card_source.get("status_card_v2") if isinstance(card_source, dict) else {}
    if isinstance(v2_card, dict) and v2_card:
        alias = aliases.get(burden_id, {})
        blocked_items = v2_card.get("blocked_overread")
        blocked_overread = [
            text_value(item)
            for item in blocked_items
            if text_value(item)
        ] if isinstance(blocked_items, list) else []
        blocked_overread_sentence = (
            text_value(v2_card.get("blocked_overread_sentence"))
            or text_value(alias.get("required_blocked_phrase"))
            or "; ".join(blocked_overread)
        )
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
            "blocked_overread_sentence": blocked_overread_sentence,
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
    blocked_items = fallback_blocked_overread_items(row)
    non_conclusions = split_tokens(row.get("overread_guard", ""))
    return {
        "object_id": burden_id,
        "positive_status": reader_facing_status(row, aliases),
        "exact_scope": fallback_scope_sentence(row),
        "allowed_use": fallback_allowed_use_sentence(row),
        "blocked_overread": blocked_items,
        "blocked_overread_sentence": " ".join(blocked_items),
        "next_burden": f"Address the current blocking burden before any downstream promotion: {text_value(row.get('blocking_burden')) or 'unspecified'}.",
        "next_lawful_route": "one bounded continue-research packet authorized by the latest tracked handoff",
        "public_summary": reader_facing_status(row, aliases),
        "full_control_non_conclusions": non_conclusions,
        "evidence_source": text_value(row.get("last_evidence_path")),
        "status_card_version": "fallback",
    }


def high_risk_status_cards(
    rows: list[dict[str, str]],
    aliases: dict[str, dict[str, Any]],
    calibration: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for burden_id in HIGH_RISK_STATUS_CARD_IDS:
        row = row_by_burden(rows, burden_id)
        if row:
            cards.append(status_card_for_row(row, aliases, calibration))
    return cards


def status_cards_markdown(cards: list[dict[str, Any]]) -> str:
    if not cards:
        return "No high-risk status cards are available."
    sections: list[str] = []
    for card in cards:
        blocked = text_value(card.get("blocked_overread_sentence"))
        if not blocked:
            blocked_items = card.get("blocked_overread")
            if isinstance(blocked_items, list):
                blocked = " ".join(text_value(item) for item in blocked_items if text_value(item))
        sections.append(
            "\n".join(
                [
                    f"### `{md_cell(card.get('object_id', ''))}`",
                    "",
                    f"**Positive status:** {md_cell(card.get('positive_status', ''))}",
                    "",
                    f"**Scope:** {md_cell(card.get('exact_scope', ''))}",
                    "",
                    f"**Allowed use:** {md_cell(card.get('allowed_use', ''))}",
                    "",
                    f"**Blocked overread:** {md_cell(blocked)}",
                    "",
                    f"**Next burden:** {md_cell(card.get('next_burden', ''))}",
                ]
            )
        )
    return "\n\n".join(sections)


def ledger_rows_for_markdown(rows: list[dict[str, str]], aliases: dict[str, dict[str, Any]]) -> str:
    lines = [
        "| Burden ID | Milestone | Reader-facing status | Legacy status | Control status | Mathematical status | Physical status | Promotion status | Overread guard | Last evidence |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    code_value(row.get("burden_id", "")),
                    code_value(row.get("milestone", "")),
                    md_cell(reader_facing_status(row, aliases)),
                    md_cell(row.get("current_status", "")),
                    md_cell(row.get("control_status", "")),
                    md_cell(row.get("mathematical_status", "")),
                    md_cell(row.get("physical_status", "")),
                    md_cell(row.get("promotion_status", "")),
                    guard_cell(row.get("overread_guard", "")),
                    code_value(row.get("last_evidence_path", "")),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def row_by_burden(rows: list[dict[str, str]], burden_id: str) -> dict[str, str]:
    return next((item for item in rows if item.get("burden_id") == burden_id), {})


def layered_boundary_line(row: dict[str, str], aliases: dict[str, dict[str, Any]]) -> str:
    burden = row.get("burden_id", "")
    alias = status_alias_for_row(row, aliases)
    alias_text = text_value(alias.get("display_status"))
    alias_part = f" reader-facing `{md_cell(alias_text)}`;" if alias_text else ""
    return (
        f"- `{md_cell(burden)}`:{alias_part} control `{md_cell(row.get('control_status', ''))}`; "
        f"mathematical `{md_cell(row.get('mathematical_status', ''))}`; "
        f"physical `{md_cell(row.get('physical_status', ''))}`; "
        f"promotion `{md_cell(row.get('promotion_status', ''))}`; "
        f"guards: {guard_cell(row.get('overread_guard', ''))}."
    )


def layered_boundary_notes(rows: list[dict[str, str]], aliases: dict[str, dict[str, Any]]) -> str:
    focus_ids = ["m_src", "g_eff", "matter_coupling", "einstein_equations", "benchmark_promotion"]
    lines = []
    for burden_id in focus_ids:
        row = row_by_burden(rows, burden_id)
        if row:
            lines.append(layered_boundary_line(row, aliases))
    return "\n".join(lines)


def alias_table_rows(aliases: dict[str, dict[str, Any]], focus_ids: list[str]) -> str:
    lines = [
        "| Object | Reader-facing status | Required qualifier | Required blocked phrase |",
        "| --- | --- | --- | --- |",
    ]
    for key in focus_ids:
        alias = aliases.get(key, {})
        if not alias:
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    code_value(key),
                    md_cell(alias.get("display_status", "")),
                    md_cell(alias.get("required_qualifier", "")),
                    md_cell(alias.get("required_blocked_phrase", "")),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def object_alias_table_rows(aliases: dict[str, dict[str, Any]], burden_id: str) -> str:
    parent = aliases.get(burden_id, {})
    object_aliases = parent.get("object_aliases") if isinstance(parent, dict) else {}
    if not isinstance(object_aliases, dict) or not object_aliases:
        return "No object aliases are registered for this burden."
    lines = [
        "| Object | Reader-facing status | Required qualifier |",
        "| --- | --- | --- |",
    ]
    for key, alias in object_aliases.items():
        if not isinstance(alias, dict):
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    code_value(key),
                    md_cell(alias.get("display_status", "")),
                    md_cell(alias.get("required_qualifier", "")),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def ordered_mapping_keys(mapping: dict[str, Any], preferred_order: list[str]) -> list[str]:
    ordered = [key for key in preferred_order if key in mapping]
    ordered.extend(sorted(key for key in mapping if key not in preferred_order))
    return ordered


def evidence_cell(value: Any) -> str:
    if isinstance(value, list):
        items = [md_cell(item) for item in value if text_value(item)]
        return "<br>".join(items) if items else "none"
    return md_cell(value) if text_value(value) else "none"


def validation_status_meaning(status: Any) -> str:
    return VALIDATION_STATUS_MEANINGS.get(
        text_value(status),
        "extension status; inspect evidence",
    )


def validation_layer_status_counts(handoff: dict[str, Any]) -> dict[str, int]:
    layers = handoff.get("validation_layers")
    if not isinstance(layers, dict) or not layers:
        return {}
    counts: dict[str, int] = {}
    for layer in layers.values():
        if not isinstance(layer, dict):
            continue
        status = text_value(layer.get("status")) or "UNSPECIFIED"
        counts[status] = counts.get(status, 0) + 1
    ordered: dict[str, int] = {}
    for status in VALIDATION_STATUS_ORDER:
        if status in counts:
            ordered[status] = counts.pop(status)
    for status in sorted(counts):
        ordered[status] = counts[status]
    return ordered


def validation_status_summary_table(handoff: dict[str, Any]) -> str:
    counts = validation_layer_status_counts(handoff)
    if not counts:
        return "No validation-layer status summary is available."
    lines = [
        "| Status | Count | Meaning |",
        "| --- | --- | --- |",
    ]
    for status, count in counts.items():
        lines.append(
            "| "
            + " | ".join(
                [
                    code_value(status),
                    str(count),
                    md_cell(validation_status_meaning(status)),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def validation_layer_table(handoff: dict[str, Any]) -> str:
    layers = handoff.get("validation_layers")
    if not isinstance(layers, dict) or not layers:
        return "No validation-layer split is recorded in the latest handoff."
    lines = [
        "| Validation layer | Status | Meaning | Evidence |",
        "| --- | --- | --- | --- |",
    ]
    for layer_name in ordered_mapping_keys(layers, VALIDATION_LAYER_ORDER):
        layer = layers.get(layer_name)
        if not isinstance(layer, dict):
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    code_value(layer_name),
                    md_cell(layer.get("status", "")),
                    md_cell(validation_status_meaning(layer.get("status", ""))),
                    evidence_cell(layer.get("evidence", [])),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def authorization_value_cell(field_name: str, value: Any) -> str:
    if field_name in AUTHORIZATION_BOOLEAN_FIELDS:
        return "true (authorized)" if bool_value(value) else "false (not authorized)"
    if field_name.endswith("_source_path") and not text_value(value):
        return "none"
    return md_cell(value) if text_value(value) else "none"


def authorization_layer_table(handoff: dict[str, Any]) -> str:
    layers = handoff.get("authorization_layers")
    if not isinstance(layers, dict) or not layers:
        return "No authorization-layer split is recorded in the latest handoff."
    lines = [
        "| Authorization field | Value | Meaning |",
        "| --- | --- | --- |",
    ]
    for field_name in ordered_mapping_keys(layers, AUTHORIZATION_LAYER_ORDER):
        lines.append(
            "| "
            + " | ".join(
                [
                    code_value(field_name),
                    authorization_value_cell(field_name, layers.get(field_name, "")),
                    md_cell(AUTHORIZATION_LAYER_MEANINGS.get(field_name, "extension authorization field")),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def authorization_layer_summary(handoff: dict[str, Any]) -> dict[str, list[str]]:
    layers = handoff.get("authorization_layers")
    if not isinstance(layers, dict) or not layers:
        return {"authorized": [], "not_authorized": []}
    authorized = [
        field_name
        for field_name in AUTHORIZATION_LAYER_ORDER
        if field_name in AUTHORIZATION_BOOLEAN_FIELDS and bool_value(layers.get(field_name))
    ]
    not_authorized = [
        field_name
        for field_name in AUTHORIZATION_LAYER_ORDER
        if field_name in AUTHORIZATION_BOOLEAN_FIELDS and not bool_value(layers.get(field_name))
    ]
    return {"authorized": authorized, "not_authorized": not_authorized}


def list_cell(value: Any) -> str:
    if isinstance(value, list):
        items = [md_cell(item) for item in value if text_value(item)]
        return "<br>".join(items) if items else "none"
    return md_cell(value) if text_value(value) else "none"


def bool_cell(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = text_value(value)
    return md_cell(text) if text else "false"


def default_adopted_objects(rows: list[dict[str, str]], aliases: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    display_names = {
        "m_src": "M_src",
        "g_eff": "g_eff",
        "matter_coupling": "P7SourceMatterPackage_v1",
    }
    for burden_id in ["m_src", "g_eff", "matter_coupling"]:
        row = row_by_burden(rows, burden_id)
        if not row:
            continue
        objects.append(
            {
                "object": display_names[burden_id],
                "status": reader_facing_status(row, aliases),
                "authority_path": row.get("last_evidence_path", ""),
                "scope_qualifier": row.get("physical_status", ""),
                "blocked_overread": split_tokens(row.get("overread_guard", "")),
                "downstream_promotion_authorized": row.get("promotion_status") not in {
                    "",
                    "none",
                    "scoped_source_object_only",
                    "scoped_source_evidence_only",
                    "scoped_source_postulate_adoption_only",
                },
            }
        )
    return objects


def default_evidence_preconditions(rows: list[dict[str, str]], aliases: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    row = row_by_burden(rows, "matter_coupling")
    if not row:
        return []
    return [
        {
            "object": "g_eff-dependent matter-coupling derivational burden",
            "status": "open after protected source-side postulate adoption",
            "authority_path": row.get("last_evidence_path", ""),
            "supports_target": "construction or precise obstruction of a source-to-target coupling bridge through derived g_eff",
            "does_not_establish": split_tokens(row.get("overread_guard", "")),
        }
    ]


def default_open_or_blocked_targets(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    for burden_id in ["matter_coupling", "einstein_equations", "benchmark_promotion"]:
        row = row_by_burden(rows, burden_id)
        if not row:
            continue
        targets.append(
            {
                "target": burden_id,
                "status": row.get("control_status") or row.get("current_status", ""),
                "missing_burden_or_authority": row.get("blocking_burden", ""),
                "evidence_not_to_overread": split_tokens(row.get("overread_guard", "")),
                "next_lawful_route": row.get("last_evidence_path", ""),
            }
        )
    return targets


def normalized_three_tier_summary(
    handoff: dict[str, Any],
    rows: list[dict[str, str]],
    aliases: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]] | list[str]]:
    summary = handoff.get("three_tier_claim_summary")
    summary = summary if isinstance(summary, dict) else {}
    adopted = summary.get("adopted_objects")
    accepted = summary.get("accepted_evidence_preconditions")
    open_targets = summary.get("open_or_blocked_physical_targets")
    forbidden = summary.get("forbidden_overread")
    return {
        "adopted_objects": adopted if isinstance(adopted, list) and adopted else default_adopted_objects(rows, aliases),
        "accepted_evidence_preconditions": (
            accepted if isinstance(accepted, list) and accepted else default_evidence_preconditions(rows, aliases)
        ),
        "open_or_blocked_physical_targets": (
            open_targets if isinstance(open_targets, list) and open_targets else default_open_or_blocked_targets(rows)
        ),
        "forbidden_overread": forbidden
        if isinstance(forbidden, list) and forbidden
        else [
            "three-tier summary as physics proof",
            "accepted evidence/preconditions as adopted objects",
            "current-frontier rendering as downstream promotion",
        ],
    }


def adopted_objects_table(items: list[Any]) -> str:
    lines = [
        "| Object | Status | Authority | Scope qualifier | Blocked overread | Downstream promotion authorized |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        if not isinstance(item, dict):
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(item.get("object", "")),
                    md_cell(item.get("status", "")),
                    code_value(item.get("authority_path", "")),
                    md_cell(item.get("scope_qualifier", "")),
                    list_cell(item.get("blocked_overread", [])),
                    bool_cell(item.get("downstream_promotion_authorized", False)),
                ]
            )
            + " |"
        )
    return "\n".join(lines) if len(lines) > 2 else "No adopted source-only or source-extension objects are listed."


def accepted_evidence_table(items: list[Any]) -> str:
    lines = [
        "| Evidence or precondition | Status | Supports target | Does not establish | Authority |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in items:
        if not isinstance(item, dict):
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(item.get("object", "")),
                    md_cell(item.get("status", "")),
                    md_cell(item.get("supports_target", "")),
                    list_cell(item.get("does_not_establish", [])),
                    code_value(item.get("authority_path", "")),
                ]
            )
            + " |"
        )
    return "\n".join(lines) if len(lines) > 2 else "No accepted evidence or precondition entries are listed."


def open_targets_table(items: list[Any]) -> str:
    lines = [
        "| Physical target | Status | Missing burden or authority | Evidence not to overread | Next lawful route or evidence |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in items:
        if not isinstance(item, dict):
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    md_cell(item.get("target", "")),
                    md_cell(item.get("status", "")),
                    md_cell(item.get("missing_burden_or_authority", "")),
                    list_cell(item.get("evidence_not_to_overread", [])),
                    md_cell(item.get("next_lawful_route", "")),
                ]
            )
            + " |"
        )
    return "\n".join(lines) if len(lines) > 2 else "No open or blocked physical target entries are listed."


def bullet_items(items: list[Any]) -> str:
    values = [text_value(item) for item in items if text_value(item)]
    if not values:
        return "- none"
    return "\n".join(f"- {md_cell(item)}" for item in values)


def three_tier_claim_summary_section(
    handoff: dict[str, Any],
    rows: list[dict[str, str]],
    aliases: dict[str, dict[str, Any]],
) -> str:
    summary = normalized_three_tier_summary(handoff, rows, aliases)
    return (
        "This pilot separates source-side object status from evidence/precondition "
        "status and from still-open physical targets. Evidence/precondition entries "
        "are intentionally not rendered as adopted objects unless tracked source "
        "authority independently records adoption.\n\n"
        "Adopted source-only or source-extension objects:\n\n"
        f"{adopted_objects_table(summary['adopted_objects'])}\n\n"
        "Scoped accepted evidence/preconditions:\n\n"
        f"{accepted_evidence_table(summary['accepted_evidence_preconditions'])}\n\n"
        "Open or blocked physical targets:\n\n"
        f"{open_targets_table(summary['open_or_blocked_physical_targets'])}\n\n"
        "Forbidden overreads:\n\n"
        f"{bullet_items(summary['forbidden_overread'])}"
    )


def scoped_alias_section(status_aliases: dict[str, Any]) -> str:
    aliases = status_alias_rows(status_aliases)
    if not aliases:
        return (
            "No status alias map is currently loaded. The renderer is falling back "
            "to layered ledger fields only."
        )
    focus_ids = [
        "m_src",
        "g_eff",
        "matter_coupling",
        "einstein_equations",
        "benchmark_promotion",
        "finite_toy_metric_response",
    ]
    rules = status_aliases.get("authority_rules")
    rules = rules if isinstance(rules, dict) else {}
    return (
        "The renderer consumes the subordinate status alias map at "
        f"`{STATUS_ALIAS_PATH}` for reader-facing wording only. The ledger "
        "continues to govern if an alias and ledger row ever conflict. Aliases "
        "are not physics proof, routing authority, benchmark authority, or "
        "claim-promotion authority.\n\n"
        f"- High-risk rows must not render bare `accepted`: {str(bool_value(rules.get('high_risk_rows_must_not_render_bare_accepted'))).lower()}.\n"
        f"- Aliases override the ledger: {str(not bool_value(rules.get('aliases_do_not_override_ledger'))).lower()}.\n"
        f"- Aliases are physics proof: {str(bool_value(rules.get('aliases_are_physics_proof'))).lower()}.\n\n"
        "High-risk burden aliases:\n\n"
        f"{alias_table_rows(aliases, focus_ids)}\n\n"
        "`matter_coupling` object aliases:\n\n"
        f"{object_alias_table_rows(aliases, 'matter_coupling')}"
    )


def route_family_text(handoff: dict[str, Any], task: dict[str, Any]) -> str:
    task_type = text_value(task.get("task_type"))
    loop_route = text_value(handoff.get("loop_risk_route"))
    if task_type == "p1_generated_current_state_report":
        return "P1 active-state repair: deterministic current-frontier renderer completed; final P8 validation remains required"
    if isinstance(task.get("task_taxonomy"), dict):
        normalized = task_taxonomy.classify_task(task)
        if not normalized["errors"]:
            work_kind = normalized["work_kind"].replace("_", " ")
            scope = normalized["scope"].replace("_", " ")
            return f"{work_kind} ({scope})"
    if loop_route:
        return loop_route.replace("_", " ")
    return text_value(task.get("task_type")) or "tracked continue-research route"


def current_burden_text(handoff: dict[str, Any]) -> str:
    distance = handoff.get("distance_to_gr") if isinstance(handoff.get("distance_to_gr"), dict) else {}
    burden_id = text_value(distance.get("burden_id"))
    status = text_value(distance.get("status"))
    if burden_id and burden_id != "none":
        suffix = f"; status: {status}" if status else ""
        return f"{code_value(burden_id)}{suffix}"
    next_packet = handoff.get("required_next_packet")
    if isinstance(next_packet, dict):
        task_type = text_value(next_packet.get("task_type"))
        if task_type:
            return f"none for physics derivation; live control burden is {task_type.replace('_', ' ')}"
    next_action = text_value(handoff.get("next_action"))
    if next_action:
        return f"none for physics derivation; live control burden follows the next action: {next_action}"
    return "none for physics derivation"


def target_milestone_text(handoff: dict[str, Any]) -> str:
    distance = handoff.get("distance_to_gr") if isinstance(handoff.get("distance_to_gr"), dict) else {}
    milestone = text_value(distance.get("milestone"))
    if milestone and milestone != "none":
        return code_value(milestone)
    return "none; this is project-control tooling work"


def required_next_authority_text(handoff: dict[str, Any]) -> str:
    boundary = handoff.get("claim_boundary") if isinstance(handoff.get("claim_boundary"), dict) else {}
    allowed = text_value(boundary.get("allowed_next_scope"))
    if allowed:
        return allowed
    next_action = text_value(handoff.get("next_action"))
    if next_action:
        return next_action
    return "tracked continue-research decision required"


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


def matter_coupling_boundary(rows: list[dict[str, str]]) -> str:
    row = row_by_burden(rows, "matter_coupling")
    status = row.get("current_status", "unknown")
    control_status = row.get("control_status", "unknown")
    mathematical_status = row.get("mathematical_status", "unknown")
    physical_status = row.get("physical_status", "unknown")
    promotion_status = row.get("promotion_status", "unknown")
    burden = row.get("blocking_burden", "matter-coupling derivation remains blocked")
    evidence = row.get("last_evidence_path", "registries/DISTANCE_TO_GR_LEDGER.csv")
    return (
        "The Distance-to-GR ledger currently records the `matter_coupling` burden row "
        f"with legacy status `{status}`, control status `{control_status}`, "
        f"mathematical status `{mathematical_status}`, physical status "
        f"`{physical_status}`, and promotion status `{promotion_status}`. Its "
        f"blocking burden is: {burden}. The last evidence path is `{evidence}`.\n\n"
        "The exact finite `P7SourceMatterPackage_v1` is adopted within its declared "
        "source-side scope by protected human constitutive postulate. That adoption "
        "includes the specifically authorized source-matter meanings, operational "
        "detector semantics, equipped-domain universal source coupling, source "
        "matter action, and source stress-energy input. It must not be read as a "
        "first-principles derivation, target-side matter coupling, target "
        "stress-energy tensor, coupling through a derived `g_eff`, an "
        "equivalence-principle result, Einstein equations, benchmark promotion, "
        "or completed derivation."
    )


def build_state(repo_root: Path) -> dict[str, Any]:
    program_state = load_control_yaml(repo_root, "research_control/program_state.yaml")
    active_task_id = text_value(program_state.get("active_task_id"))
    latest_handoff_id = text_value(program_state.get("latest_handoff_id"))
    if not active_task_id or not latest_handoff_id:
        raise FrontierRenderError("program_state.yaml must name active_task_id and latest_handoff_id")

    latest_handoff = load_control_yaml(repo_root, handoff_path(latest_handoff_id))
    active_task = load_control_yaml(repo_root, active_task_path(active_task_id))
    ledger_rows = read_csv_rows(repo_root, LEDGER_PATH)
    metric_use_rows = read_csv_rows(repo_root, METRIC_USE_LEDGER_PATH)
    task_registry_rows = (
        read_csv_rows(repo_root, TASK_REGISTRY_PATH)
        if repo_path(repo_root, TASK_REGISTRY_PATH).is_file()
        else []
    )
    status_aliases = load_optional_control_yaml(repo_root, STATUS_ALIAS_PATH)
    accepted_status_calibration_path = ""
    accepted_status_calibration = load_optional_control_yaml(repo_root, ACCEPTED_STATUS_CALIBRATION_V2_PATH)
    if accepted_status_calibration:
        accepted_status_calibration_path = ACCEPTED_STATUS_CALIBRATION_V2_PATH
    else:
        accepted_status_calibration = load_optional_control_yaml(repo_root, ACCEPTED_STATUS_CALIBRATION_V1_PATH)
        if accepted_status_calibration:
            accepted_status_calibration_path = ACCEPTED_STATUS_CALIBRATION_V1_PATH
    aliases = status_alias_rows(status_aliases)
    status_cards = high_risk_status_cards(
        ledger_rows,
        aliases,
        calibration_rows(accepted_status_calibration),
    )
    next_action = text_value(latest_handoff.get("next_action")) or text_value(
        program_state.get("next_recommended_action")
    )
    bifurcation = active_state_bifurcation_state(
        active_task_id=active_task_id,
        latest_handoff_id=latest_handoff_id,
        next_action=next_action,
    )

    return {
        "schema_id": SCHEMA_ID,
        "active_task_id": active_task_id,
        "latest_handoff_id": latest_handoff_id,
        "current_status": text_value(program_state.get("current_status")),
        "next_recommended_action": next_action,
        "active_state_bifurcation": bifurcation,
        "program_state_path": "research_control/program_state.yaml",
        "latest_handoff_path": handoff_path(latest_handoff_id),
        "active_task_path": active_task_path(active_task_id),
        "ledger_path": LEDGER_PATH,
        "metric_use_ledger_path": METRIC_USE_LEDGER_PATH,
        "active_task": active_task,
        "active_task_taxonomy": task_taxonomy.classify_task(active_task),
        "latest_handoff": latest_handoff,
        "v16_completed": bool_value(latest_handoff.get("v16_completed")),
        "distance_to_gr_rows": ledger_rows,
        "metric_use_rows": metric_use_rows,
        "task_registry_rows": task_registry_rows,
        "metric_use_ledger_summary": metric_use_ledger_summary(metric_use_rows),
        "status_aliases": status_aliases,
        "accepted_status_calibration": accepted_status_calibration,
        "accepted_status_calibration_path": accepted_status_calibration_path,
        "high_risk_status_cards": status_cards,
        "route_family": route_family_text(latest_handoff, active_task),
        "target_derivation_milestone": target_milestone_text(latest_handoff),
        "current_burden": current_burden_text(latest_handoff),
        "required_next_authority": required_next_authority_text(latest_handoff),
    }


def render_markdown(state: dict[str, Any]) -> str:
    task = state["active_task"]
    handoff = state["latest_handoff"]
    ledger_rows = state["distance_to_gr_rows"]
    status_aliases = state["status_aliases"]
    aliases = status_alias_rows(status_aliases)
    status_cards = state["high_risk_status_cards"]
    metric_use_summary = state["metric_use_ledger_summary"]
    task_objective = text_value(task.get("objective"))
    handoff_summary = text_value(handoff.get("summary"))
    validation = handoff.get("validation") if isinstance(handoff.get("validation"), dict) else {}
    validation_lines = [
        f"- active task: {code_value(state['active_task_id'])};",
        f"- latest handoff: {code_value(state['latest_handoff_id'])};",
        f"- current status: {code_value(state['current_status'])};",
        f"- renderer source: `scripts/research_control/render_current_frontier.py`;",
        "- renderer policy: tracked-state snapshot only, not authority;",
        "- claim boundary: no ontology edit, no source-law adoption, no `MetricData(E)` adoption, no `g_eff` scope expansion, no coupling-law adoption, no matter-coupling derivation or adoption, no stress-energy semantics, no Einstein equations, no benchmark promotion, no completed derivation, and no downstream GR promotion.",
    ]
    for key, value in sorted(validation.items()):
        validation_lines.append(f"- latest handoff validation `{md_cell(key)}`: {md_cell(value)};")
    legacy_validation_notes = "\n".join(validation_lines)
    validation_layers_table = validation_layer_table(handoff)
    validation_layers_summary_table = validation_status_summary_table(handoff)
    authorization_layers_table = authorization_layer_table(handoff)
    bifurcation = state["active_state_bifurcation"]
    provenance_section = "\n".join(
        report_provenance.markdown_provenance_lines(state["report_provenance"])
    )

    body = f"""<!-- authority: control -->

# Current Research Frontier

This control snapshot records the active research-control frontier after
{code_value(state['active_task_id'])} and {code_value(state['latest_handoff_id'])}.
It is generated from tracked control state. It is a synchronized reader-facing
snapshot, not independent routing authority and not a physics proof surface.
If this file ever contradicts `research_control/program_state.yaml`, the
handoff named by that file, or `registries/DISTANCE_TO_GR_LEDGER.csv`, those
tracked authority files govern.

{provenance_section}

## Active Research State

| Field | Value |
| --- | --- |
| Active task ID | {code_value(state['active_task_id'])} |
| Latest handoff ID | {code_value(state['latest_handoff_id'])} |
| Current status | {code_value(state['current_status'])} |
| V16 completed | {str(state['v16_completed']).lower()} |
| Current route family | {md_cell(state['route_family'])} |
| Target derivation milestone | {md_cell(state['target_derivation_milestone'])} |
| Current burden | {md_cell(state['current_burden'])} |
| Required next authority | {md_cell(state['required_next_authority'])} |
| Next recommended action | {md_cell(state['next_recommended_action'])} |

## Active-State Bifurcation

These fields separate ordinary research-continuation authority from any
project-system sidecar status. A sidecar may be evidence for project-system
repair, but it does not supersede the latest research handoff unless a later
tracked validator and handoff explicitly authorize that change.

| Field | Value |
| --- | --- |
| Latest research task ID | {code_value(bifurcation['latest_research_task_id'])} |
| Latest research handoff ID | {code_value(bifurcation['latest_research_handoff_id'])} |
| Latest research next action | {md_cell(bifurcation['latest_research_next_action'])} |
| Latest project-system task ID | {code_value(bifurcation['latest_project_system_task_id'])} |
| Latest project-system status | {code_value(bifurcation['latest_project_system_status'])} |
| Latest project-system sidecar task ID | {code_value(bifurcation['latest_project_system_sidecar_task_id'])} |
| Latest project-system sidecar status | {code_value(bifurcation['latest_project_system_sidecar_status'])} |
| Sidecar supersedes research handoff | {str(bifurcation['sidecar_supersedes_research_handoff']).lower()} |
| Next research route source | {code_value(bifurcation['next_research_route_source'])} |

## Active Boundary

`current_frontier.md` is a generated snapshot under the P1 active-state
authority invariant. The precedence order remains:

1. `research_control/program_state.yaml` is the compact live state pointer.
2. The latest handoff named by `program_state.yaml` is immediate routing
   authority.
3. `registries/DISTANCE_TO_GR_LEDGER.csv` is the persistent burden-state
   ledger.
4. Task records, DDRs, AgentJobs, completions, claim-boundary rows, and
   role-execution rows provide transaction provenance.
5. This file is a generated synchronized snapshot only.

The P1-T04 renderer check fails when this snapshot drifts from tracked
active-state authority. The renderer provides a deterministic repair command:

```zsh
.venv/bin/python scripts/research_control/render_current_frontier.py --write
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python scripts/research_control/render_current_frontier.py --json
```

## Current Route Evidence

- Active task path: `{md_cell(state['active_task_path'])}`.
- Active task objective: {md_cell(sentence_fragment(task_objective, "not recorded"))}.
- Latest handoff path: `{md_cell(state['latest_handoff_path'])}`.
- Latest handoff summary: {md_cell(sentence_fragment(handoff_summary, "not recorded"))}.
- Current route family: {md_cell(state['route_family'])}.
- Next recommended action: {md_cell(sentence_fragment(state['next_recommended_action'], "not recorded"))}.

## Three-Tier Claim Summary Pilot

{three_tier_claim_summary_section(handoff, ledger_rows, aliases)}

## Matter-Coupling Boundary

{matter_coupling_boundary(ledger_rows)}

Universal matter coupling and downstream GR promotion remain blocked until a
separate tracked route and the required protected authorities establish them.

## Metric-Use Ledger Warning

{metric_use_ledger_markdown(metric_use_summary)}

## Positive-First Status Cards

Every high-risk accepted or blocked row below is rendered with positive status
first, then exact scope, allowed use, and blocked overread. These cards are
reader-facing calibration only. They do not override the Distance-to-GR ledger
and do not create physics proof, Gate Chair authority, benchmark authority, or
completed-derivation authority.

{status_cards_markdown(status_cards)}

## Layered Distance-To-GR Boundary Notes

The legacy `current_status` column is retained for continuity. The layered
columns below are the reader-facing anti-overread boundary:

- `control_status` records workflow or gate-review state.
- `mathematical_status` records the source-side mathematical object state.
- `physical_status` records what must not be inferred physically.
- `promotion_status` records whether any downstream promotion is authorized.
- `overread_guard` records exact blocked readings that must remain visible.

High-risk rows:

{layered_boundary_notes(ledger_rows, aliases)}

## Exact Blocked Claims

{line_list(BLOCKED_CLAIMS)}

## Scoped-Positive Alias Pilot

{scoped_alias_section(status_aliases)}

## Distance-To-GR Table

This table summarizes the layered fields in
`registries/DISTANCE_TO_GR_LEDGER.csv`; the ledger remains the authoritative
source if this summary drifts. The `Reader-facing status` column is rendered
from `{STATUS_ALIAS_PATH}` when a row alias exists. The `Legacy status` column
preserves the raw ledger `current_status` field for continuity.

{ledger_rows_for_markdown(ledger_rows, aliases)}

## Exact Next Route

The immediate next route is:

```text
{text_value(state['next_recommended_action'])}
```

The next route must be executed through tracked continue-research state. This
snapshot does not create physics authority, Gate Chair authority, benchmark
authority, or completed-derivation authority.

## Validation And Authorization Layers

Validation receipts and protected authorization are separate. A layer-level
`PENDING` value must carry evidence explaining what remains pending; it does
not override a separate aggregate compatibility field unless the tracked
completion or handoff says so.

Layer status summary:

{validation_layers_summary_table}

Validation layers:

{validation_layers_table}

Authorization layers:

{authorization_layers_table}

Legacy compatibility records:

{legacy_validation_notes}

## Retrieval Warning Status

This renderer reads only tracked control sources:

- `research_control/program_state.yaml`
- `{md_cell(state['latest_handoff_path'])}`
- `{md_cell(state['active_task_path'])}`
- `registries/DISTANCE_TO_GR_LEDGER.csv`
- `{STATUS_ALIAS_PATH}` when present

Memory, wiki notes, semantic extracts, Obsidian notes, PDFs, generated HTML,
SQLite indexes, and `.local/` caches remain retrieval or reader layers only.
They are not scientific authority and are not inputs to this rendered state.

## Source Materials

The AEther-Flow Research Project. (2026, June 17). *GR derivation burden map*
[Internal control note].

The AEther-Flow Research Project. (2026, July 1). *Current research frontier*
[Generated internal control snapshot].

The AEther-Flow Research Project. (2026, July 1). *Handoff {state['latest_handoff_id'].replace('handoff-', '')}*
[Internal research-control handoff].

The AEther-Flow Research Project. (2026, July 1). *Recommendations
implementation plan continue task v14* [Internal implementation plan].
"""
    return body.strip() + "\n"


def render_payload(
    repo_root: Path,
    *,
    source_commit: str | None = None,
    strict_provenance: bool | None = None,
) -> tuple[dict[str, Any], str]:
    state = build_state(repo_root)
    source_paths = [
        state["program_state_path"],
        state["latest_handoff_path"],
        state["active_task_path"],
        state["ledger_path"],
        state["metric_use_ledger_path"],
    ]
    if state["status_aliases"]:
        source_paths.append(STATUS_ALIAS_PATH)
    if state["accepted_status_calibration_path"]:
        source_paths.append(state["accepted_status_calibration_path"])
    if repo_path(repo_root, ACTIVE_STATE_BIFURCATION_POLICY_PATH).exists():
        source_paths.append(ACTIVE_STATE_BIFURCATION_POLICY_PATH)
    if repo_path(repo_root, TASK_REGISTRY_PATH).exists():
        source_paths.append(TASK_REGISTRY_PATH)
    source_paths = sorted(set(source_paths))
    source_hashes = {
        path: report_provenance.sha256_file(repo_root, path)
        for path in source_paths
    }
    strict = repo_root.resolve() == REPO_ROOT.resolve() if strict_provenance is None else strict_provenance
    if source_commit is None:
        existing = report_provenance.metadata_from_markdown_file(
            repo_root, DEFAULT_FRONTIER_PATH
        )
        source_commit = report_provenance.source_commit_from_metadata(
            existing, report_provenance.git_head(repo_root)
        )
    generation_time = text_value(state["latest_handoff"].get("created_at")) or text_value(
        state["latest_handoff"].get("updated_at")
    )
    task_count = len(state["task_registry_rows"])
    if not task_count:
        tasks_root = repo_path(repo_root, "research_control/tasks")
        task_count = sum(
            1 for path in tasks_root.glob("RT-*") if path.is_dir()
        ) if tasks_root.exists() else 0
    primary_source_paths = [
        state["program_state_path"],
        state["latest_handoff_path"],
        state["ledger_path"],
    ]
    if TASK_REGISTRY_PATH in source_hashes:
        primary_source_paths.append(TASK_REGISTRY_PATH)
    state["report_provenance"] = report_provenance.build_metadata(
        report_class="current_frontier",
        source_commit=source_commit,
        source_hashes=source_hashes,
        primary_source_paths=primary_source_paths,
        generation_time=generation_time,
        task_count=task_count,
        renderer_path=RENDERER_PATH,
        renderer_sha256=RENDERER_SHA256,
        strict=strict,
    )
    markdown = render_markdown(state)
    payload = {
        "schema_id": SCHEMA_ID,
        "active_task_id": state["active_task_id"],
        "latest_handoff_id": state["latest_handoff_id"],
        "current_status": state["current_status"],
        "v16_completed": state["v16_completed"],
        "next_recommended_action": state["next_recommended_action"],
        "active_state_bifurcation": state["active_state_bifurcation"],
        "route_family": state["route_family"],
        "target_derivation_milestone": state["target_derivation_milestone"],
        "current_burden": state["current_burden"],
        "required_next_authority": state["required_next_authority"],
        "source_paths": source_paths,
        "report_provenance": state["report_provenance"],
        "frontier_path": DEFAULT_FRONTIER_PATH,
        "rendered_hash": sha256_text(markdown),
        "distance_to_gr_row_count": len(state["distance_to_gr_rows"]),
        "metric_use_ledger_path": state["metric_use_ledger_path"],
        "metric_use_ledger_summary": state["metric_use_ledger_summary"],
        "status_alias_path": STATUS_ALIAS_PATH if state["status_aliases"] else "",
        "status_alias_row_count": len(status_alias_rows(state["status_aliases"])),
        "status_alias_integration": "reader_facing_status_column",
        "accepted_status_calibration_path": (
            state["accepted_status_calibration_path"] if state["accepted_status_calibration"] else ""
        ),
        "status_card_version": (
            "v2"
            if state["accepted_status_calibration_path"] == ACCEPTED_STATUS_CALIBRATION_V2_PATH
            else "v1_compat" if state["accepted_status_calibration_path"] else "fallback"
        ),
        "high_risk_status_card_count": len(state["high_risk_status_cards"]),
        "high_risk_status_card_object_ids": [
            card["object_id"] for card in state["high_risk_status_cards"]
        ],
        "layered_status_fields": [
            "control_status",
            "mathematical_status",
            "physical_status",
            "promotion_status",
            "overread_guard",
        ],
        "validation_layer_fields": ordered_mapping_keys(
            state["latest_handoff"].get("validation_layers", {})
            if isinstance(state["latest_handoff"].get("validation_layers"), dict)
            else {},
            VALIDATION_LAYER_ORDER,
        ),
        "validation_layer_status_counts": validation_layer_status_counts(state["latest_handoff"]),
        "authorization_layer_fields": ordered_mapping_keys(
            state["latest_handoff"].get("authorization_layers", {})
            if isinstance(state["latest_handoff"].get("authorization_layers"), dict)
            else {},
            AUTHORIZATION_LAYER_ORDER,
        ),
        "authorization_layer_summary": authorization_layer_summary(state["latest_handoff"]),
        "snapshot_only_not_authority": True,
        "physics_claim_authority": False,
    }
    return payload, markdown


def check_frontier(repo_root: Path, markdown: str) -> bool:
    path = repo_path(repo_root, DEFAULT_FRONTIER_PATH)
    return path.exists() and path.read_text(encoding="utf-8") == markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write the rendered frontier snapshot")
    mode.add_argument("--check", action="store_true", help="verify the tracked frontier is current")
    mode.add_argument("--json", action="store_true", help="emit machine-readable rendered state")
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    existing_metadata = report_provenance.metadata_from_markdown_file(
        repo_root, DEFAULT_FRONTIER_PATH
    )
    source_commit = (
        report_provenance.git_head(repo_root)
        if args.write
        else report_provenance.source_commit_from_metadata(
            existing_metadata, report_provenance.git_head(repo_root)
        )
    )
    try:
        payload, markdown = render_payload(repo_root, source_commit=source_commit)
    except (FrontierRenderError, report_provenance.GeneratedReportProvenanceError) as exc:
        print(f"render_current_frontier: {exc}", file=sys.stderr)
        return 2

    observed_metadata = existing_metadata or {}
    provenance_validation = report_provenance.validate_metadata(
        repo_root=repo_root,
        observed=observed_metadata,
        expected=payload["report_provenance"],
        strict=repo_root == REPO_ROOT,
    )

    frontier_path = repo_path(repo_root, DEFAULT_FRONTIER_PATH)
    if args.write:
        frontier_path.parent.mkdir(parents=True, exist_ok=True)
        frontier_path.write_text(markdown, encoding="utf-8")
        written_metadata = report_provenance.metadata_from_markdown_file(
            repo_root, DEFAULT_FRONTIER_PATH
        ) or {}
        provenance_validation = report_provenance.validate_metadata(
            repo_root=repo_root,
            observed=written_metadata,
            expected=payload["report_provenance"],
            strict=repo_root == REPO_ROOT,
        )
        print(
            json.dumps(
                {**payload, "provenance_validation": provenance_validation, "status": "written"},
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    if args.check:
        current = check_frontier(repo_root, markdown)
        fresh = current and provenance_validation["status"] == "PASS"
        status = "pass" if fresh else "stale"
        print(
            json.dumps(
                {**payload, "provenance_validation": provenance_validation, "status": status},
                indent=2,
                sort_keys=True,
            )
        )
        return 0 if fresh else 1
    print(
        json.dumps(
            {**payload, "provenance_validation": provenance_validation, "status": "rendered"},
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
