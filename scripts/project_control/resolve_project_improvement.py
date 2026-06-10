#!/usr/bin/env python3
"""Resolve the next bounded project-system improvement boundary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from classify_project_changes import changed_paths_from_git, classify_paths  # noqa: E402
from collect_project_improvement_signals import collect_signals  # noqa: E402
from project_signal_types import signal_type_role_map  # noqa: E402


SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
HIGH_PRIORITY_SEVERITIES = {"critical", "high"}


STOP_CONDITIONS = [
    "validation fails",
    "required write path is outside the AgentJob allowlist",
    "change would edit physics claims or generated derivatives by hand",
    "project-system action needs a human policy decision",
    "more than one AgentJob would be required",
]


def selected_signal(open_signals: list[dict[str, str]]) -> dict[str, str] | None:
    if not open_signals:
        return None
    return sorted(
        open_signals,
        key=lambda row: (
            SEVERITY_ORDER.get(row.get("severity", "low"), 9),
            row.get("created_at", ""),
            row.get("signal_id", ""),
        ),
    )[0]


def high_priority_signal(open_signals: list[dict[str, str]]) -> dict[str, str] | None:
    return selected_signal(
        [
            signal
            for signal in open_signals
            if signal.get("severity") in HIGH_PRIORITY_SEVERITIES
        ]
    )


def resolve_project_improvement(paths: list[str] | None = None) -> dict[str, object]:
    if paths is None:
        paths = changed_paths_from_git()
    classification = classify_paths(paths)
    signals = collect_signals()
    open_signals = signals["open_signals"]
    urgent_signal = high_priority_signal(open_signals)
    backlog_signal = selected_signal(open_signals)
    role_map = signal_type_role_map()
    chosen_signal: dict[str, str] | None = None

    boundary = "no_action"
    recommended_role = ""
    reason = "no open project-improvement signal and no current Git change requires action"

    if urgent_signal:
        chosen_signal = urgent_signal
        boundary = "project_improvement_signal_ready"
        recommended_role = chosen_signal.get("recommended_role") or role_map.get(
            chosen_signal.get("signal_type", ""), "project-system-director"
        )
        reason = (
            f"high-priority open signal {chosen_signal.get('signal_id', '')} "
            "requires one bounded AgentJob"
        )
    elif classification.get("docs_impact_required"):
        boundary = "documentation_curator_required"
        recommended_role = "documentation-curator"
        reason = "current Git change has documentation impact"
    elif classification.get("project_system_improvement_required"):
        boundary = "project_system_agent_job_required"
        recommended_role = classification.get("recommended_role", "validator-engineer")
        reason = "current Git change affects project-system machinery"
    elif backlog_signal:
        chosen_signal = backlog_signal
        boundary = "project_improvement_signal_ready"
        recommended_role = chosen_signal.get("recommended_role") or role_map.get(
            chosen_signal.get("signal_type", ""), "project-system-director"
        )
        reason = f"open backlog signal {chosen_signal.get('signal_id', '')} requires one bounded AgentJob"

    return {
        "status": "ready",
        "boundary": boundary,
        "reason": reason,
        "resolver_is_advisory": True,
        "hard_checkpoint_gate": False,
        "recommended_skill": "improve-project-system" if boundary != "no_action" else "",
        "recommended_role": recommended_role,
        "selected_signal": chosen_signal or {},
        "open_signals": open_signals,
        "change_classification": classification,
        "required_authority_surfaces": [
            "AGENTS.md",
            "research_control/AGENTS.md",
            "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv",
            "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv",
            "registries/AGENT_ROLE_REGISTRY.csv",
            ".agents/roles/research_ops/documentation-curator.v0.1.0.md",
            ".codex/skills/improve-project-system/SKILL.md",
        ],
        "stop_conditions": STOP_CONDITIONS,
        "checkpoint_required_after_execution": boundary != "no_action",
        "checkpoint_gate_source": "validators",
        "execution_boundary": "one bounded AgentJob per invocation",
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON. This is the default.")
    parser.add_argument("--paths", nargs="*", help="Resolve against explicit paths instead of Git state.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    print(json.dumps(resolve_project_improvement(args.paths), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
