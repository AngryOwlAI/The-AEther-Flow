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


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ID = "current_frontier_state_v1"
DEFAULT_FRONTIER_PATH = "research_control/current_frontier.md"
LEDGER_PATH = "registries/DISTANCE_TO_GR_LEDGER.csv"

BLOCKED_CLAIMS = [
    "canonical ontology edit",
    "source-law adoption",
    "`MetricData(E)` adoption",
    "`g_eff` adoption or scope expansion",
    "coupling-law adoption",
    "matter-coupling derivation",
    "matter-coupling adoption",
    "stress-energy semantics",
    "stress-energy tensor",
    "matter action",
    "detector semantics",
    "Einstein equations",
    "exact-GR benchmark promotion",
    "benchmark Gate Chair closure",
    "completed derivation",
    "future source-extension impossibility",
    "global theory rejection",
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


def guard_cell(value: Any) -> str:
    tokens = split_tokens(value)
    if not tokens:
        return "none"
    return "<br>".join(md_cell(token) for token in tokens)


def sentence_fragment(value: Any, fallback: str) -> str:
    text = text_value(value).rstrip(".")
    return text if text else fallback


def ledger_rows_for_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "| Burden ID | Milestone | Current status | Control status | Mathematical status | Physical status | Promotion status | Overread guard | Last evidence |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    code_value(row.get("burden_id", "")),
                    code_value(row.get("milestone", "")),
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


def layered_boundary_line(row: dict[str, str]) -> str:
    burden = row.get("burden_id", "")
    return (
        f"- `{md_cell(burden)}`: control `{md_cell(row.get('control_status', ''))}`; "
        f"mathematical `{md_cell(row.get('mathematical_status', ''))}`; "
        f"physical `{md_cell(row.get('physical_status', ''))}`; "
        f"promotion `{md_cell(row.get('promotion_status', ''))}`; "
        f"guards: {guard_cell(row.get('overread_guard', ''))}."
    )


def layered_boundary_notes(rows: list[dict[str, str]]) -> str:
    focus_ids = ["matter_coupling", "g_eff", "einstein_equations", "benchmark_promotion"]
    lines = []
    for burden_id in focus_ids:
        row = row_by_burden(rows, burden_id)
        if row:
            lines.append(layered_boundary_line(row))
    return "\n".join(lines)


def route_family_text(handoff: dict[str, Any], task: dict[str, Any]) -> str:
    task_type = text_value(task.get("task_type"))
    loop_route = text_value(handoff.get("loop_risk_route"))
    if task_type == "p1_generated_current_state_report":
        return "P1 active-state repair: deterministic current-frontier renderer completed; final P8 validation remains required"
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
        "This ledger status must not be read as coupling-law adoption, universal "
        "matter-coupling derivation, matter-coupling adoption, stress-energy "
        "semantics, stress-energy tensor, matter action, detector semantics, "
        "Einstein equations, benchmark promotion, or completed derivation."
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
    next_action = text_value(latest_handoff.get("next_action")) or text_value(
        program_state.get("next_recommended_action")
    )

    return {
        "schema_id": SCHEMA_ID,
        "active_task_id": active_task_id,
        "latest_handoff_id": latest_handoff_id,
        "current_status": text_value(program_state.get("current_status")),
        "next_recommended_action": next_action,
        "program_state_path": "research_control/program_state.yaml",
        "latest_handoff_path": handoff_path(latest_handoff_id),
        "active_task_path": active_task_path(active_task_id),
        "ledger_path": LEDGER_PATH,
        "active_task": active_task,
        "latest_handoff": latest_handoff,
        "distance_to_gr_rows": ledger_rows,
        "route_family": route_family_text(latest_handoff, active_task),
        "target_derivation_milestone": target_milestone_text(latest_handoff),
        "current_burden": current_burden_text(latest_handoff),
        "required_next_authority": required_next_authority_text(latest_handoff),
    }


def render_markdown(state: dict[str, Any]) -> str:
    task = state["active_task"]
    handoff = state["latest_handoff"]
    ledger_rows = state["distance_to_gr_rows"]
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

    body = f"""<!-- authority: control -->

# Current Research Frontier

This control snapshot records the active research-control frontier after
{code_value(state['active_task_id'])} and {code_value(state['latest_handoff_id'])}.
It is generated from tracked control state. It is a synchronized reader-facing
snapshot, not independent routing authority and not a physics proof surface.
If this file ever contradicts `research_control/program_state.yaml`, the
handoff named by that file, or `registries/DISTANCE_TO_GR_LEDGER.csv`, those
tracked authority files govern.

## Active Research State

| Field | Value |
| --- | --- |
| Active task ID | {code_value(state['active_task_id'])} |
| Latest handoff ID | {code_value(state['latest_handoff_id'])} |
| Current status | {code_value(state['current_status'])} |
| Current route family | {md_cell(state['route_family'])} |
| Target derivation milestone | {md_cell(state['target_derivation_milestone'])} |
| Current burden | {md_cell(state['current_burden'])} |
| Required next authority | {md_cell(state['required_next_authority'])} |
| Next recommended action | {md_cell(state['next_recommended_action'])} |

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

## Matter-Coupling Boundary

{matter_coupling_boundary(ledger_rows)}

Universal matter coupling and downstream GR promotion remain blocked until a
separate tracked route and the required protected authorities establish them.

## Layered Distance-To-GR Boundary Notes

The legacy `current_status` column is retained for continuity. The layered
columns below are the reader-facing anti-overread boundary:

- `control_status` records workflow or gate-review state.
- `mathematical_status` records the source-side mathematical object state.
- `physical_status` records what must not be inferred physically.
- `promotion_status` records whether any downstream promotion is authorized.
- `overread_guard` records exact blocked readings that must remain visible.

High-risk rows:

{layered_boundary_notes(ledger_rows)}

## Exact Blocked Claims

{line_list(BLOCKED_CLAIMS)}

## Distance-To-GR Table

This table summarizes the layered fields in
`registries/DISTANCE_TO_GR_LEDGER.csv`; the ledger remains the authoritative
source if this summary drifts.

{ledger_rows_for_markdown(ledger_rows)}

## Exact Next Route

The immediate next route is:

```text
{text_value(state['next_recommended_action'])}
```

The next route must be executed through tracked continue-research state. This
snapshot does not create physics authority, Gate Chair authority, benchmark
authority, or completed-derivation authority.

## Validation Status

Latest tracked state records:

{chr(10).join(validation_lines)}

## Retrieval Warning Status

This renderer reads only tracked control sources:

- `research_control/program_state.yaml`
- `{md_cell(state['latest_handoff_path'])}`
- `{md_cell(state['active_task_path'])}`
- `registries/DISTANCE_TO_GR_LEDGER.csv`

Memory, wiki notes, semantic extracts, Obsidian notes, PDFs, generated HTML,
SQLite indexes, and `.local/` caches remain retrieval or reader layers only.
They are not scientific authority and are not inputs to this rendered state.

## Source Materials

The AEther-Flow Research Project. (2026, June 17). *GR derivation burden map*
[Internal control note].

The AEther-Flow Research Project. (2026, June 28). *Current research frontier*
[Generated internal control snapshot].

The AEther-Flow Research Project. (2026, June 28). *Handoff {state['latest_handoff_id'].replace('handoff-', '')}*
[Internal research-control handoff].

The AEther-Flow Research Project. (2026, June 29). *Recommendations
implementation plan continue task v12* [Internal implementation plan].
"""
    return body.strip() + "\n"


def render_payload(repo_root: Path) -> tuple[dict[str, Any], str]:
    state = build_state(repo_root)
    markdown = render_markdown(state)
    payload = {
        "schema_id": SCHEMA_ID,
        "active_task_id": state["active_task_id"],
        "latest_handoff_id": state["latest_handoff_id"],
        "current_status": state["current_status"],
        "next_recommended_action": state["next_recommended_action"],
        "route_family": state["route_family"],
        "target_derivation_milestone": state["target_derivation_milestone"],
        "current_burden": state["current_burden"],
        "required_next_authority": state["required_next_authority"],
        "source_paths": [
            state["program_state_path"],
            state["latest_handoff_path"],
            state["active_task_path"],
            state["ledger_path"],
        ],
        "frontier_path": DEFAULT_FRONTIER_PATH,
        "rendered_hash": sha256_text(markdown),
        "distance_to_gr_row_count": len(state["distance_to_gr_rows"]),
        "layered_status_fields": [
            "control_status",
            "mathematical_status",
            "physical_status",
            "promotion_status",
            "overread_guard",
        ],
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
    try:
        payload, markdown = render_payload(repo_root)
    except FrontierRenderError as exc:
        print(f"render_current_frontier: {exc}", file=sys.stderr)
        return 2

    frontier_path = repo_path(repo_root, DEFAULT_FRONTIER_PATH)
    if args.write:
        frontier_path.parent.mkdir(parents=True, exist_ok=True)
        frontier_path.write_text(markdown, encoding="utf-8")
        print(json.dumps({**payload, "status": "written"}, indent=2, sort_keys=True))
        return 0
    if args.check:
        current = check_frontier(repo_root, markdown)
        status = "pass" if current else "stale"
        print(json.dumps({**payload, "status": status}, indent=2, sort_keys=True))
        return 0 if current else 1
    print(json.dumps({**payload, "status": "rendered"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
