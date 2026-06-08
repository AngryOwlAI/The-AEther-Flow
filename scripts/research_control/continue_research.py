#!/usr/bin/env python3
"""Deterministic entry point for research-control continuation setup.

This bootstrap version validates state and reports the next executable boundary.
It does not perform open-ended research reasoning; Codex/Director reasoning must
author DDRs and execute AgentJobs under the tracked contracts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from resolve_latest_handoff import resolve_latest
    from strict_yaml import StrictYamlError, load as load_yaml
    from validate_research_control import validate_all
except ImportError:  # pragma: no cover
    from scripts.research_control.resolve_latest_handoff import resolve_latest
    from scripts.research_control.strict_yaml import StrictYamlError, load as load_yaml
    from scripts.research_control.validate_research_control import validate_all


REPO_ROOT = Path(__file__).resolve().parents[2]
PROGRAM_STATE_PATH = REPO_ROOT / "research_control" / "program_state.yaml"


def continuation_status() -> dict[str, object]:
    report = validate_all()
    if not report.ok():
        return {
            "status": "blocked",
            "reason": "research-control validation failed",
            "errors": report.errors,
        }
    try:
        program_state = load_yaml(PROGRAM_STATE_PATH)
    except StrictYamlError as exc:
        return {"status": "blocked", "reason": f"program_state parse failed: {exc}"}
    latest = resolve_latest()
    return {
        "status": "ready",
        "active_task_id": program_state.get("active_task_id", ""),
        "current_status": program_state.get("current_status", ""),
        "latest_handoff": latest,
        "next_action": latest.get("next_action", ""),
        "execution_boundary": "one bounded AgentJob per invocation",
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    status = continuation_status()
    if args.json:
        print(json.dumps(status, indent=2))
    else:
        print(f"Status: {status['status']}")
        print(f"Current status: {status.get('current_status', '')}")
        print(f"Next action: {status.get('next_action', '')}")
        if status["status"] == "blocked":
            for error in status.get("errors", []):
                print(f"- {error}")
    return 0 if status["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
