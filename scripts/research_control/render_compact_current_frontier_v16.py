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


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ID = "compact_current_frontier_v16"
PROGRAM_STATE_PATH = "research_control/program_state.yaml"
DISTANCE_LEDGER_PATH = "registries/DISTANCE_TO_GR_LEDGER.csv"
CURRENT_FRONTIER_PATH = "research_control/current_frontier.md"
MARKDOWN_REGISTRY_PATH = "registries/MARKDOWN_SOURCE_REGISTRY.csv"
DEFAULT_YAML_PATH = "output/compact_current_frontier_v16.yaml"
DEFAULT_JSON_PATH = "output/compact_current_frontier_v16.json"
DEFAULT_MARKDOWN_PATH = "wiki/indexes/compact_current_frontier_v16.md"
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
    "active_state",
    "next_route",
    "claim_boundary",
    "scoped_positive_objects",
    "scoped_evidence_preconditions",
    "blocked_physical_targets",
    "distance_to_gr",
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


def high_risk_row(row: dict[str, str], frontier_text: str) -> dict[str, Any]:
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


def build_snapshot(repo_root: Path) -> dict[str, Any]:
    program_state = load_control_yaml(repo_root, PROGRAM_STATE_PATH)
    active_task_id = text_value(program_state.get("active_task_id"))
    latest_handoff_id = text_value(program_state.get("latest_handoff_id"))
    if not active_task_id or not latest_handoff_id:
        raise CompactFrontierError("program_state.yaml must name active_task_id and latest_handoff_id")

    latest_handoff_path = handoff_path(latest_handoff_id)
    latest_handoff = load_control_yaml(repo_root, latest_handoff_path)
    ledger_rows = read_csv_rows(repo_root, DISTANCE_LEDGER_PATH)
    markdown_rows = read_csv_rows(repo_root, MARKDOWN_REGISTRY_PATH)
    frontier_text = read_text_source(repo_root, CURRENT_FRONTIER_PATH)
    selected_route = latest_handoff.get("selected_next_route")
    selected_route = selected_route if isinstance(selected_route, dict) else {}
    hard_blocks = latest_handoff.get("hard_blocks")
    hard_blocks = hard_blocks if isinstance(hard_blocks, list) else []
    current_status = text_value(program_state.get("current_status"))
    handoff_summary = text_value(latest_handoff.get("summary"))
    v15_completed = "v16_" in current_status or "v16 " in handoff_summary or "v16" in frontier_text
    v16_completed = bool_value(latest_handoff.get("v16_completed"))

    high_risk_rows = [
        high_risk_row(row_by_burden(ledger_rows, burden_id), frontier_text)
        for burden_id in HIGH_RISK_BURDEN_IDS
        if row_by_burden(ledger_rows, burden_id)
    ]

    return {
        "schema_id": SCHEMA_ID,
        "generated_from": [
            PROGRAM_STATE_PATH,
            latest_handoff_path,
            DISTANCE_LEDGER_PATH,
            CURRENT_FRONTIER_PATH,
            MARKDOWN_REGISTRY_PATH,
        ],
        "active_state": {
            "active_task_id": active_task_id,
            "latest_handoff_id": latest_handoff_id,
            "current_status": current_status,
            "v15_completed": v15_completed,
            "v16_completed": v16_completed,
            "v16_plan_registered": markdown_registry_has_object(markdown_rows, V16_PLAN_OBJECT_ID),
        },
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
        "scoped_positive_objects": scoped_positive_objects(ledger_rows, frontier_text),
        "scoped_evidence_preconditions": scoped_evidence_preconditions(ledger_rows, frontier_text),
        "blocked_physical_targets": blocked_physical_targets(ledger_rows, frontier_text),
        "distance_to_gr": {
            "delta": distance_delta(latest_handoff),
            "high_risk_rows": high_risk_rows,
        },
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
    if snapshot.get("authority_warning", {}).get("snapshot_only_not_authority") is not True:
        errors.append("authority warning is missing or false")
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
    return errors


def render_markdown(snapshot: dict[str, Any], yaml_text: str, json_text: str) -> str:
    active = snapshot["active_state"]
    next_route = snapshot["next_route"]
    high_risk_rows = snapshot["distance_to_gr"]["high_risk_rows"]
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
    return (
        "<!-- authority: generated -->\n\n"
        "# Compact Current Frontier v16\n\n"
        "This generated index mirrors `output/compact_current_frontier_v16.yaml` "
        "and `output/compact_current_frontier_v16.json`. It is a snapshot-only "
        "reader aid. If it differs from tracked control state, tracked control "
        "state governs.\n\n"
        "## Active State\n\n"
        f"- Active task: `{active['active_task_id']}`\n"
        f"- Latest handoff: `{active['latest_handoff_id']}`\n"
        f"- Current status: `{active['current_status']}`\n"
        f"- V15 completed: `{str(active['v15_completed']).lower()}`\n"
        f"- V16 plan registered: `{str(active['v16_plan_registered']).lower()}`\n\n"
        "## Next Route\n\n"
        f"- Route ID: `{next_route['route_id']}`\n"
        f"- Role family: `{next_route['role_family']}`\n"
        f"- Target milestone: `{next_route['target_derivation_milestone']}`\n"
        f"- Milestone burden: {next_route['milestone_burden']}\n"
        f"- Requires human gate: `{str(next_route['requires_human_gate']).lower()}`\n\n"
        "## High-Risk Rows\n\n"
        + "\n".join(row_lines)
        + "\n\n"
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
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            for child_key, child_value in value.items():
                emit_mapping_item(child_key, child_value, indent + 2)
        elif isinstance(value, list):
            if not value:
                lines.append(f"{prefix}{key}: []")
                return
            lines.append(f"{prefix}{key}:")
            emit_list_items(value, indent + 2)
        else:
            lines.append(f"{prefix}{key}: {quote_scalar(value)}")

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
        "yaml_path": DEFAULT_YAML_PATH,
        "json_path": DEFAULT_JSON_PATH,
        "markdown_path": DEFAULT_MARKDOWN_PATH,
        "yaml_sha256": sha256_text(yaml_text),
        "json_sha256": sha256_text(json_text),
        "markdown_sha256": sha256_text(markdown_text),
        "high_risk_row_count": len(snapshot["distance_to_gr"]["high_risk_rows"]),
        "blocked_claim_count": len(snapshot["claim_boundary"]["blocked_claims"]),
        "snapshot_only_not_authority": snapshot["authority_warning"]["snapshot_only_not_authority"],
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
    try:
        snapshot = build_snapshot(repo_root)
    except CompactFrontierError as exc:
        print(f"render_compact_current_frontier_v16: {exc}", file=sys.stderr)
        return 2

    errors = validate_snapshot(snapshot)
    yaml_text, json_text, markdown_text = rendered_texts(snapshot)
    if args.write:
        if errors:
            print(json.dumps(status_payload(snapshot, "invalid", errors), indent=2, sort_keys=True))
            return 1
        write_outputs(repo_root, yaml_text, json_text, markdown_text)
        print(json.dumps(status_payload(snapshot, "written", []), indent=2, sort_keys=True))
        return 0
    if args.check:
        current = check_outputs(repo_root, yaml_text, json_text, markdown_text)
        status = "pass" if current and not errors else "stale" if not errors else "invalid"
        print(json.dumps(status_payload(snapshot, status, errors), indent=2, sort_keys=True))
        return 0 if current and not errors else 1
    print(json_text, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
