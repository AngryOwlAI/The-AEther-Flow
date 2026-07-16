#!/usr/bin/env python3
"""Execute an explicit validated read-only v19 plan in shadow mode."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import signal
import sys
import threading


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.validation.executor import (  # noqa: E402
    ExecutorError,
    SubprocessAdapter,
    execute_plan,
)
from scripts.validation.plan import ValidationPlan, load_manifest  # noqa: E402


DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
DEFAULT_RECEIPT_ROOT = REPO_ROOT / ".local/validation-receipts"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--adapter-commands", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--receipt-root", type=Path, default=DEFAULT_RECEIPT_ROOT)
    parser.add_argument("--max-workers", type=int, default=4)
    return parser.parse_args(argv)


def load_plan(path: Path) -> ValidationPlan:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ExecutorError(f"plan load failed: {error}") from error
    expected = {
        "schema_id", "manifest_id", "manifest_hash", "requested_profile",
        "effective_profile", "scopes", "changed_paths", "blocked_paths",
        "path_tags", "role_obligations", "ordered_gate_ids", "selected_gate_ids",
        "superseded_gate_ids", "skipped_gate_ids", "unknown_paths", "entries",
        "execution_authority", "status", "planner_executes_commands", "authority",
    }
    if not isinstance(document, dict) or set(document) != expected:
        raise ExecutorError("plan document fields differ from validation_plan_v1")
    if document["schema_id"] != "validation_plan_v1" or document["planner_executes_commands"] is not False:
        raise ExecutorError("unsupported or command-authorizing plan document")
    expected_authority = {
        "operational_validation_only": True,
        "legacy_result_authoritative": True,
        "physics_claim_authority": False,
        "ontology_authority": False,
        "benchmark_authority": False,
        "gate_chair_authority": False,
    }
    if document["authority"] != expected_authority:
        raise ExecutorError("plan authority boundary is invalid")
    try:
        return ValidationPlan(
            manifest_id=document["manifest_id"],
            manifest_hash=document["manifest_hash"],
            requested_profile=document["requested_profile"],
            effective_profile=document["effective_profile"],
            scopes=tuple(document["scopes"]),
            changed_paths=tuple(document["changed_paths"]),
            blocked_paths=tuple(document["blocked_paths"]),
            path_tags=tuple(document["path_tags"]),
            role_obligations=tuple(document["role_obligations"]),
            ordered_gate_ids=tuple(document["ordered_gate_ids"]),
            selected_gate_ids=tuple(document["selected_gate_ids"]),
            superseded_gate_ids=tuple(document["superseded_gate_ids"]),
            skipped_gate_ids=tuple(document["skipped_gate_ids"]),
            unknown_paths=tuple(document["unknown_paths"]),
            entries=tuple(document["entries"]),
            execution_authority=document["execution_authority"],
            status=document["status"],
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ExecutorError(f"invalid plan document: {error}") from error


def load_adapters(path: Path) -> dict[str, SubprocessAdapter]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ExecutorError(f"adapter command map load failed: {error}") from error
    if not isinstance(document, dict):
        raise ExecutorError("adapter command map must be an object")
    adapters: dict[str, SubprocessAdapter] = {}
    for adapter_id, command in document.items():
        if (
            not isinstance(adapter_id, str)
            or not adapter_id
            or not isinstance(command, list)
            or not command
            or any(not isinstance(argument, str) or not argument for argument in command)
        ):
            raise ExecutorError("adapter command map contains an invalid binding")
        adapters[adapter_id] = SubprocessAdapter(tuple(command), cwd=REPO_ROOT)
    return adapters


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    cancellation = threading.Event()

    def request_cancellation(_signal_number, _frame) -> None:
        cancellation.set()

    previous_handlers = {}
    for signal_number in (signal.SIGINT, signal.SIGTERM):
        previous_handlers[signal_number] = signal.signal(signal_number, request_cancellation)
    try:
        outcome = execute_plan(
            load_plan(args.plan),
            load_manifest(args.manifest),
            load_adapters(args.adapter_commands),
            receipt_root=args.receipt_root,
            max_workers=args.max_workers,
            cancellation=cancellation,
        )
    except (ExecutorError, OSError) as error:
        print(f"BLOCKED_CONFIGURATION: {error}", file=sys.stderr)
        return 2
    finally:
        for signal_number, handler in previous_handlers.items():
            signal.signal(signal_number, handler)

    counts = outcome.receipt["counts"]
    receipt = str(outcome.receipt_path) if outcome.receipt_path is not None else "unavailable"
    print(
        f"{outcome.status} gates={counts['gate_count']} pass={counts['pass_count']} "
        f"warn={counts['warn_count']} fail={counts['fail_count']} "
        f"blocked={counts['blocked_count']} receipt={receipt}"
    )
    if outcome.error:
        print(outcome.error, file=sys.stderr)
    return outcome.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
