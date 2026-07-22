#!/usr/bin/env python3
"""Render the P10-T08 current burden view from tracked authority sources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


SCHEMA_ID = "v21_current_burden_status_v1"
RECEIPT_SCHEMA_ID = "v21_burden_status_migration_receipt_v1"
DEFINITIONS_PATH = (
    "research_control/tasks/RT-20260721-009/artifacts/"
    "v21_burden_definitions_v1.yaml"
)
OUTPUT_PATH = (
    "research_control/tasks/RT-20260721-009/artifacts/"
    "v21_current_burden_status.md"
)
RECEIPT_PATH = (
    "research_control/tasks/RT-20260721-009/artifacts/"
    "v21_burden_status_migration_receipt.json"
)
LEDGER_PATH = "registries/DISTANCE_TO_GR_LEDGER.csv"
PROGRAM_STATE_PATH = "research_control/program_state.yaml"
TASK_REGISTRY_PATH = "registries/RESEARCH_TASK_REGISTRY.csv"
BURDEN_MAP_PATH = "research_control/design/gr_derivation_burden_map.md"
REQUIRED_LEDGER_FIELDS = (
    "burden_id",
    "milestone",
    "required_object",
    "current_status",
    "blocking_burden",
    "accept_criteria",
    "failure_or_freeze_criteria",
    "last_evidence_path",
    "updated_at",
    "control_status",
    "mathematical_status",
    "physical_status",
    "promotion_status",
    "overread_guard",
)
REQUIRED_DEFINITION_FIELDS = (
    "milestone",
    "required_object",
    "depends_on",
    "route_kind",
    "blocking_burden_definition",
    "accept_criteria_definition",
    "failure_or_freeze_definition",
)
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class BurdenStatusError(RuntimeError):
    """Raised when a source or generated status violates the P10-T08 contract."""


def repo_path(repo_root: Path, rel_path: str) -> Path:
    return repo_root / rel_path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(repo_root: Path, rel_path: str) -> str:
    path = repo_path(repo_root, rel_path)
    if not path.is_file():
        raise BurdenStatusError(f"missing required source: {rel_path}")
    return sha256_bytes(path.read_bytes())


def text_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def load_yaml_mapping(repo_root: Path, rel_path: str) -> dict[str, Any]:
    path = repo_path(repo_root, rel_path)
    if not path.is_file():
        raise BurdenStatusError(f"missing required YAML source: {rel_path}")
    try:
        value = load_yaml(path)
    except StrictYamlError as exc:
        raise BurdenStatusError(f"invalid strict YAML {rel_path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BurdenStatusError(f"YAML source must be a mapping: {rel_path}")
    return value


def read_csv_rows(repo_root: Path, rel_path: str) -> list[dict[str, str]]:
    path = repo_path(repo_root, rel_path)
    if not path.is_file():
        raise BurdenStatusError(f"missing required CSV source: {rel_path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return [
            {str(key): text_value(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def validate_definition_graph(definitions: list[dict[str, Any]]) -> None:
    milestone_ids = [text_value(item.get("milestone")) for item in definitions]
    if any(not item for item in milestone_ids):
        raise BurdenStatusError("stable definition contains a blank milestone")
    if len(milestone_ids) != len(set(milestone_ids)):
        raise BurdenStatusError("stable definition milestones must be unique")

    known = set(milestone_ids)
    dependencies: dict[str, list[str]] = {}
    for item in definitions:
        missing = [field for field in REQUIRED_DEFINITION_FIELDS if field not in item]
        if missing:
            raise BurdenStatusError(
                f"definition {item.get('milestone', '<blank>')} missing fields: {missing}"
            )
        milestone = text_value(item["milestone"])
        raw_dependencies = item["depends_on"]
        if not isinstance(raw_dependencies, list):
            raise BurdenStatusError(f"definition {milestone} depends_on must be a list")
        dependency_ids = [text_value(value) for value in raw_dependencies]
        if any(not value for value in dependency_ids):
            raise BurdenStatusError(f"definition {milestone} has a blank dependency")
        unknown = sorted(set(dependency_ids) - known)
        if unknown:
            raise BurdenStatusError(
                f"definition {milestone} has unknown dependencies: {unknown}"
            )
        dependencies[milestone] = dependency_ids

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(milestone: str) -> None:
        if milestone in visiting:
            raise BurdenStatusError(f"stable definition dependency cycle at {milestone}")
        if milestone in visited:
            return
        visiting.add(milestone)
        for dependency in dependencies[milestone]:
            visit(dependency)
        visiting.remove(milestone)
        visited.add(milestone)

    for milestone in milestone_ids:
        visit(milestone)


def load_definitions(repo_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    document = load_yaml_mapping(repo_root, DEFINITIONS_PATH)
    if text_value(document.get("schema_id")) != "v21_stable_burden_definitions_v1":
        raise BurdenStatusError("unexpected stable-definition schema_id")
    if document.get("status_fields_are_forbidden") is not True:
        raise BurdenStatusError("stable definitions must forbid mutable status fields")
    definitions = document.get("definitions")
    if not isinstance(definitions, list) or not definitions:
        raise BurdenStatusError("stable definitions must be a nonempty list")
    normalized: list[dict[str, Any]] = []
    for item in definitions:
        if not isinstance(item, dict):
            raise BurdenStatusError("each stable definition must be a mapping")
        forbidden_keys = sorted(
            key for key in item if "status" in text_value(key).lower()
        )
        if forbidden_keys:
            raise BurdenStatusError(
                f"stable definition contains mutable status fields: {forbidden_keys}"
            )
        normalized.append(item)
    validate_definition_graph(normalized)
    return document, normalized


def validate_ledger(
    ledger_rows: list[dict[str, str]], definitions: list[dict[str, Any]]
) -> dict[str, list[dict[str, str]]]:
    if not ledger_rows:
        raise BurdenStatusError("Distance-to-GR ledger is empty")
    burden_ids = [row.get("burden_id", "") for row in ledger_rows]
    if any(not value for value in burden_ids):
        raise BurdenStatusError("Distance-to-GR ledger contains a blank burden_id")
    if len(burden_ids) != len(set(burden_ids)):
        raise BurdenStatusError("Distance-to-GR ledger contains duplicate burden_id values")
    definition_milestones = {text_value(item["milestone"]) for item in definitions}
    grouped: dict[str, list[dict[str, str]]] = {
        milestone: [] for milestone in definition_milestones
    }
    for row in ledger_rows:
        missing = [field for field in REQUIRED_LEDGER_FIELDS if not row.get(field, "")]
        if missing:
            raise BurdenStatusError(
                f"ledger burden {row.get('burden_id', '<blank>')} has blank fields: {missing}"
            )
        milestone = row["milestone"]
        if milestone not in grouped:
            raise BurdenStatusError(
                f"ledger burden {row['burden_id']} has unmapped milestone {milestone}"
            )
        grouped[milestone].append(row)
    empty_definitions = sorted(
        milestone for milestone, rows in grouped.items() if not rows
    )
    if empty_definitions:
        raise BurdenStatusError(
            f"stable definitions have no ledger rows: {empty_definitions}"
        )
    for rows in grouped.values():
        rows.sort(key=lambda row: row["burden_id"])
    return grouped


def marker_value(map_text: str, marker: str) -> str:
    match = re.search(rf"<!-- {re.escape(marker)}: ([0-9a-f]+) -->", map_text)
    if not match:
        raise BurdenStatusError(f"burden map is missing marker {marker}")
    return match.group(1)


def git_head(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    value = result.stdout.strip()
    if not HEX40.fullmatch(value):
        raise BurdenStatusError("Git HEAD is not a full lowercase commit hash")
    return value


def build_snapshot(repo_root: Path, *, source_commit: str) -> dict[str, Any]:
    if not HEX40.fullmatch(source_commit):
        raise BurdenStatusError("source_commit must be a full lowercase Git hash")

    definition_document, definitions = load_definitions(repo_root)
    ledger_rows = read_csv_rows(repo_root, LEDGER_PATH)
    grouped = validate_ledger(ledger_rows, definitions)
    program_state = load_yaml_mapping(repo_root, PROGRAM_STATE_PATH)
    latest_handoff_id = text_value(program_state.get("latest_handoff_id"))
    if not latest_handoff_id:
        raise BurdenStatusError("program state has no latest_handoff_id")
    handoff_rel_path = f"research_control/handoffs/{latest_handoff_id}.yaml"
    handoff = load_yaml_mapping(repo_root, handoff_rel_path)
    if text_value(handoff.get("handoff_id")) != latest_handoff_id:
        raise BurdenStatusError("program-state and handoff identities disagree")
    program_next_action = text_value(program_state.get("next_recommended_action"))
    handoff_next_action = text_value(handoff.get("next_action"))
    if program_next_action != handoff_next_action:
        raise BurdenStatusError("program-state and handoff next actions disagree")

    active_task_id = text_value(program_state.get("active_task_id"))
    current_status = text_value(program_state.get("current_status"))
    if not active_task_id or not current_status or not program_next_action:
        raise BurdenStatusError("program state is missing active task status or next action")
    p10_state = program_state.get("p10_t08_current_burden_status_generation")
    if not isinstance(p10_state, dict):
        raise BurdenStatusError("program state is missing the P10-T08 control block")
    if p10_state.get("generated_status_is_authority") is not False:
        raise BurdenStatusError("generated status must remain non-authoritative")
    if p10_state.get("ledger_mutation_authorized") is not False:
        raise BurdenStatusError("P10-T08 must not authorize ledger mutation")
    if p10_state.get("scientific_claims_changed") is not False:
        raise BurdenStatusError("P10-T08 cannot record a scientific-claim delta")

    map_text = repo_path(repo_root, BURDEN_MAP_PATH).read_text(encoding="utf-8")
    definitions_sha256 = sha256_file(repo_root, DEFINITIONS_PATH)
    marker_sha256 = marker_value(map_text, "stable-burden-definitions-sha256")
    if marker_sha256 != definitions_sha256:
        raise BurdenStatusError("burden-map stable-definition hash is stale")
    historical_commit = marker_value(map_text, "historical-map-source-commit")
    historical_sha256 = marker_value(map_text, "historical-map-sha256")
    if not HEX40.fullmatch(historical_commit) or not HEX64.fullmatch(historical_sha256):
        raise BurdenStatusError("burden-map historical provenance markers are invalid")

    task_rows = read_csv_rows(repo_root, TASK_REGISTRY_PATH)
    if not task_rows:
        raise BurdenStatusError("research task registry is empty")
    task_ids = [row.get("task_id", "") for row in task_rows]
    if active_task_id not in task_ids:
        raise BurdenStatusError("active task is absent from the task registry")
    generation_time = text_value(handoff.get("created_at"))
    if not generation_time:
        raise BurdenStatusError("latest handoff has no created_at generation time")

    source_paths = [
        DEFINITIONS_PATH,
        LEDGER_PATH,
        PROGRAM_STATE_PATH,
        handoff_rel_path,
        TASK_REGISTRY_PATH,
        BURDEN_MAP_PATH,
    ]
    source_hashes = {path: sha256_file(repo_root, path) for path in source_paths}
    rendered_definitions: list[dict[str, Any]] = []
    for definition in definitions:
        milestone = text_value(definition["milestone"])
        rendered_definitions.append(
            {
                "milestone": milestone,
                "required_object": text_value(definition["required_object"]),
                "depends_on": [text_value(item) for item in definition["depends_on"]],
                "route_kind": text_value(definition["route_kind"]),
                "blocking_burden_definition": text_value(
                    definition["blocking_burden_definition"]
                ),
                "accept_criteria_definition": text_value(
                    definition["accept_criteria_definition"]
                ),
                "failure_or_freeze_definition": text_value(
                    definition["failure_or_freeze_definition"]
                ),
                "current_rows": grouped[milestone],
            }
        )

    return {
        "schema_id": SCHEMA_ID,
        "status": "PASS",
        "source_commit": source_commit,
        "status_generation_time": generation_time,
        "task_count": len(task_rows),
        "burden_count": len(ledger_rows),
        "definition_count": len(definitions),
        "active_task_id": active_task_id,
        "latest_handoff_id": latest_handoff_id,
        "current_status": current_status,
        "next_recommended_action": program_next_action,
        "source_hashes": source_hashes,
        "historical_map_source_commit": historical_commit,
        "historical_map_sha256": historical_sha256,
        "definitions": rendered_definitions,
        "forbidden_conclusions": definition_document.get("forbidden_conclusions", []),
        "authority": {
            "distance_to_gr_ledger_is_authority": True,
            "program_state_is_live_state_authority": True,
            "latest_handoff_is_routing_authority": True,
            "generated_status_is_independent_authority": False,
            "scientific_claims_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }


def md_cell(value: Any) -> str:
    return text_value(value).replace("\n", " ").replace("|", r"\|")


def code_list(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "none"


def render_markdown(snapshot: dict[str, Any]) -> str:
    lines = [
        "<!-- authority: generated_noncanonical -->",
        "",
        "# Generated Current GR Derivation Burden Status",
        "",
        "This file is generated from tracked authority sources. It is a",
        "freshness-checked reader view, not independent scientific, ontology,",
        "Gate Chair, benchmark, proof, publication, or completed-derivation",
        "authority. If it conflicts with the Distance-to-GR ledger, program",
        "state, or latest handoff, those sources govern and this file is stale.",
        "",
        "## Provenance",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Schema | `{snapshot['schema_id']}` |",
        f"| Source commit at generation | `{snapshot['source_commit']}` |",
        f"| Status generation time | `{snapshot['status_generation_time']}` |",
        f"| Tracked task count | {snapshot['task_count']} |",
        f"| Stable definition count | {snapshot['definition_count']} |",
        f"| Distance-to-GR burden count | {snapshot['burden_count']} |",
        f"| Historical authored-map commit | `{snapshot['historical_map_source_commit']}` |",
        f"| Historical authored-map SHA-256 | `{snapshot['historical_map_sha256']}` |",
        "",
        "### Exact source hashes",
        "",
    ]
    for path, digest in sorted(snapshot["source_hashes"].items()):
        lines.append(f"- `{path}`: `{digest}`")
    lines.extend(
        [
            "",
            "## Live control state",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Active task | `{snapshot['active_task_id']}` |",
            f"| Latest handoff | `{snapshot['latest_handoff_id']}` |",
            f"| Current status | `{snapshot['current_status']}` |",
            f"| Next recommended action | {md_cell(snapshot['next_recommended_action'])} |",
            "",
            "## Authored stable definitions with generated current values",
            "",
        ]
    )
    for definition in snapshot["definitions"]:
        lines.extend(
            [
                f"### `{definition['milestone']}`",
                "",
                f"- Required object: {definition['required_object']}",
                f"- Authored dependencies: {code_list(definition['depends_on'])}",
                f"- Route kind: `{definition['route_kind']}`",
                f"- Stable blocking-burden definition: {definition['blocking_burden_definition']}",
                f"- Stable accept-criteria definition: {definition['accept_criteria_definition']}",
                f"- Stable failure/freeze definition: {definition['failure_or_freeze_definition']}",
                "",
                "| Burden ID | Required object | Current status | Control status | Mathematical status | Physical status | Promotion status | Updated at |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in definition["current_rows"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{md_cell(row['burden_id'])}`",
                        md_cell(row["required_object"]),
                        f"`{md_cell(row['current_status'])}`",
                        f"`{md_cell(row['control_status'])}`",
                        f"`{md_cell(row['mathematical_status'])}`",
                        f"`{md_cell(row['physical_status'])}`",
                        f"`{md_cell(row['promotion_status'])}`",
                        f"`{md_cell(row['updated_at'])}`",
                    ]
                )
                + " |"
            )
        lines.append("")
        for row in definition["current_rows"]:
            lines.extend(
                [
                    f"#### `{row['burden_id']}` generated detail",
                    "",
                    f"- Current blocking burden: {row['blocking_burden']}",
                    f"- Current next evidence or action: {row['accept_criteria']}",
                    f"- Current failure/freeze criterion: {row['failure_or_freeze_criteria']}",
                    f"- Current evidence: `{row['last_evidence_path']}`",
                    f"- Exact overread guard: `{row['overread_guard']}`",
                    "",
                ]
            )
    lines.extend(["## Forbidden conclusions", ""])
    for conclusion in snapshot["forbidden_conclusions"]:
        lines.append(f"- {text_value(conclusion)}")
    lines.extend(
        [
            "",
            "Renderer PASS is operational freshness evidence only. It does not",
            "change any ledger row or create scientific or protected authority.",
            "",
        ]
    )
    return "\n".join(lines)


def build_bundle(repo_root: Path, *, source_commit: str) -> tuple[dict[str, Any], str, dict[str, Any]]:
    snapshot = build_snapshot(repo_root, source_commit=source_commit)
    markdown = render_markdown(snapshot)
    receipt = {
        "schema_id": RECEIPT_SCHEMA_ID,
        "status": "PASS",
        "source_commit": snapshot["source_commit"],
        "status_generation_time": snapshot["status_generation_time"],
        "task_count": snapshot["task_count"],
        "definition_count": snapshot["definition_count"],
        "burden_count": snapshot["burden_count"],
        "active_task_id": snapshot["active_task_id"],
        "latest_handoff_id": snapshot["latest_handoff_id"],
        "source_hashes": snapshot["source_hashes"],
        "historical_map_source_commit": snapshot["historical_map_source_commit"],
        "historical_map_sha256": snapshot["historical_map_sha256"],
        "generated_output_path": OUTPUT_PATH,
        "generated_output_sha256": sha256_bytes(markdown.encode("utf-8")),
        "checks": {
            "stable_definition_schema": "PASS",
            "definition_dependency_acyclic": "PASS",
            "ledger_definition_coverage": "PASS",
            "ledger_burden_uniqueness": "PASS",
            "program_state_handoff_identity": "PASS",
            "program_state_handoff_next_action": "PASS",
            "source_hash_freshness": "PASS",
            "historical_map_provenance": "PASS",
            "generated_view_non_authority": "PASS",
        },
        "migration": {
            "legacy_inline_current_status_removed": True,
            "stable_definitions_remain_authored": True,
            "current_values_are_generated": True,
            "historical_map_preserved_by_git_identity": True,
            "ledger_rows_mutated": 0,
            "scientific_statuses_reinterpreted": 0,
        },
        "authority": snapshot["authority"],
    }
    return snapshot, markdown, receipt


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def existing_receipt_source_commit(repo_root: Path) -> str | None:
    path = repo_path(repo_root, RECEIPT_PATH)
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    source_commit = text_value(value.get("source_commit")) if isinstance(value, dict) else ""
    return source_commit if HEX40.fullmatch(source_commit) else None


def write_outputs(repo_root: Path, markdown: str, receipt: dict[str, Any]) -> None:
    output_path = repo_path(repo_root, OUTPUT_PATH)
    receipt_path = repo_path(repo_root, RECEIPT_PATH)
    output_path.write_text(markdown, encoding="utf-8")
    receipt_path.write_text(canonical_json(receipt), encoding="utf-8")


def drift_paths(repo_root: Path, markdown: str, receipt: dict[str, Any]) -> list[str]:
    expected = {
        OUTPUT_PATH: markdown,
        RECEIPT_PATH: canonical_json(receipt),
    }
    drift: list[str] = []
    for rel_path, expected_text in expected.items():
        path = repo_path(repo_root, rel_path)
        if not path.is_file() or path.read_text(encoding="utf-8") != expected_text:
            drift.append(rel_path)
    return drift


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--source-commit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    source_commit = args.source_commit
    if not source_commit and args.check:
        source_commit = existing_receipt_source_commit(repo_root)
    if not source_commit:
        source_commit = git_head(repo_root)
    try:
        snapshot, markdown, receipt = build_bundle(
            repo_root, source_commit=source_commit
        )
        if args.write:
            write_outputs(repo_root, markdown, receipt)
        drift = drift_paths(repo_root, markdown, receipt)
        result = {
            "schema_id": SCHEMA_ID,
            "status": "PASS" if not drift else "STALE",
            "mode": "write" if args.write else "check",
            "source_commit": source_commit,
            "status_generation_time": snapshot["status_generation_time"],
            "task_count": snapshot["task_count"],
            "definition_count": snapshot["definition_count"],
            "burden_count": snapshot["burden_count"],
            "active_task_id": snapshot["active_task_id"],
            "latest_handoff_id": snapshot["latest_handoff_id"],
            "generated_output_path": OUTPUT_PATH,
            "generated_output_sha256": receipt["generated_output_sha256"],
            "drift_paths": drift,
            "generated_status_is_independent_authority": False,
            "scientific_claims_changed": False,
            "physics_promotion_authorized": False,
        }
    except (BurdenStatusError, subprocess.CalledProcessError) as exc:
        result = {
            "schema_id": SCHEMA_ID,
            "status": "FAIL",
            "mode": "write" if args.write else "check",
            "error": str(exc),
        }
        if args.json:
            print(canonical_json(result), end="")
        else:
            print(f"FAIL: {exc}")
        return 1
    if args.json:
        print(canonical_json(result), end="")
    else:
        print(result["status"])
    return 0 if not drift else 1


if __name__ == "__main__":
    raise SystemExit(main())
