#!/usr/bin/env python3
"""Execute an explicit validated v19 plan from tracked adapter bindings."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import signal
import sys
import threading
from typing import Mapping


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.validation.executor import (  # noqa: E402
    AdapterResult,
    ExecutionContext,
    ExecutorError,
    SubprocessAdapter,
    ValidationAdapter,
    execute_plan,
)
from scripts.validation.plan import ValidationPlan, load_manifest  # noqa: E402


DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
DEFAULT_BINDINGS = (
    REPO_ROOT / "research_control/design/validation_adapter_bindings_v1.json"
)
DEFAULT_RECEIPT_ROOT = REPO_ROOT / ".local/validation-receipts"
BINDING_TOP_LEVEL_FIELDS = {
    "schema_id",
    "schema_version",
    "binding_id",
    "manifest_id",
    "gate_catalog_sha256",
    "scope",
    "status",
    "authority",
    "bindings",
}
BINDING_FIELDS = {
    "gate_id",
    "adapter_id",
    "kind",
    "command",
    "child_gate_ids",
}
BINDING_AUTHORITY = {
    "operational_validation_only": True,
    "source_authoritative": False,
    "physics_claim_authority": False,
    "ontology_authority": False,
    "benchmark_authority": False,
    "proof_authority": False,
    "gate_chair_authority": False,
}


@dataclass(frozen=True, slots=True)
class DependencyAggregateAdapter:
    """Record a dependency aggregate without re-executing its child gates."""

    child_gate_ids: tuple[str, ...]

    def run(self, _context: ExecutionContext) -> AdapterResult:
        return AdapterResult(child_gates=self.child_gate_ids)


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ExecutorError(f"duplicate adapter binding key: {key}")
        result[key] = value
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--adapter-bindings", type=Path, default=DEFAULT_BINDINGS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--receipt-root", type=Path, default=DEFAULT_RECEIPT_ROOT)
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--mutation-root", type=Path)
    parser.add_argument("--allow-mutation-glob", action="append", default=[])
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
    if document["schema_id"] != "validation_plan_v1":
        raise ExecutorError("unsupported plan document")
    if document["execution_authority"] not in {"legacy", "manifest_planner"}:
        raise ExecutorError("plan execution authority is unsupported")
    planner_authoritative = document["execution_authority"] == "manifest_planner"
    if document["planner_executes_commands"] is not planner_authoritative:
        raise ExecutorError("plan command authority is inconsistent")
    expected_authority = {
        "operational_validation_only": True,
        "legacy_result_authoritative": not planner_authoritative,
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


def _canonical_gate_catalog_sha256(manifest: Mapping[str, object]) -> str:
    gates = manifest.get("gates")
    if not isinstance(gates, list):
        raise ExecutorError("manifest gates must be an array")
    payload = json.dumps(
        gates,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_adapters(
    path: Path,
    manifest: Mapping[str, object],
) -> dict[str, ValidationAdapter]:
    try:
        document = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (OSError, json.JSONDecodeError) as error:
        raise ExecutorError(f"adapter binding load failed: {error}") from error
    if not isinstance(document, dict) or set(document) != BINDING_TOP_LEVEL_FIELDS:
        raise ExecutorError("adapter binding document fields are invalid")
    if (
        document["schema_id"] != "validation_adapter_bindings_v1"
        or document["schema_version"] != 1
        or isinstance(document["schema_version"], bool)
        or document["binding_id"] != "validation-adapter-bindings-v1"
        or document["manifest_id"] != manifest.get("manifest_id")
        or document["scope"] != "canonical_current_full_profile"
        or document["status"] != "active_candidate"
        or document["authority"] != BINDING_AUTHORITY
    ):
        raise ExecutorError("adapter binding document contract is invalid")
    if document["gate_catalog_sha256"] != _canonical_gate_catalog_sha256(manifest):
        raise ExecutorError("adapter bindings do not match the manifest gate catalog")
    raw_gates = manifest.get("gates")
    assert isinstance(raw_gates, list)
    gates = {
        str(gate["gate_id"]): gate
        for gate in raw_gates
        if isinstance(gate, dict) and isinstance(gate.get("gate_id"), str)
    }
    raw_bindings = document["bindings"]
    if not isinstance(raw_bindings, list) or not raw_bindings:
        raise ExecutorError("adapter bindings must be a nonempty array")
    adapters: dict[str, ValidationAdapter] = {}
    bound_gate_ids: set[str] = set()
    for index, raw_binding in enumerate(raw_bindings):
        if not isinstance(raw_binding, dict) or set(raw_binding) != BINDING_FIELDS:
            raise ExecutorError(f"adapter binding {index} fields are invalid")
        gate_id = raw_binding["gate_id"]
        adapter_id = raw_binding["adapter_id"]
        kind = raw_binding["kind"]
        command = raw_binding["command"]
        child_gate_ids = raw_binding["child_gate_ids"]
        if (
            not isinstance(gate_id, str)
            or gate_id not in gates
            or gate_id in bound_gate_ids
            or not isinstance(adapter_id, str)
            or not adapter_id
            or adapter_id in adapters
            or gates[gate_id].get("adapter") != adapter_id
            or kind not in {"subprocess", "dependency_aggregate"}
            or not isinstance(command, list)
            or not isinstance(child_gate_ids, list)
            or any(not isinstance(value, str) or not value for value in command)
            or any(not isinstance(value, str) or not value for value in child_gate_ids)
        ):
            raise ExecutorError(f"adapter binding {index} is invalid")
        bound_gate_ids.add(gate_id)
        if kind == "subprocess":
            if not command or child_gate_ids:
                raise ExecutorError(f"subprocess binding is incomplete: {gate_id}")
            adapters[adapter_id] = SubprocessAdapter(tuple(command), cwd=REPO_ROOT)
            continue
        prerequisites = gates[gate_id].get("prerequisites")
        if command or child_gate_ids != prerequisites:
            raise ExecutorError(f"aggregate binding differs from prerequisites: {gate_id}")
        adapters[adapter_id] = DependencyAggregateAdapter(tuple(child_gate_ids))
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
        manifest = load_manifest(args.manifest)
        outcome = execute_plan(
            load_plan(args.plan),
            manifest,
            load_adapters(args.adapter_bindings, manifest),
            receipt_root=args.receipt_root,
            max_workers=args.max_workers,
            cancellation=cancellation,
            mutation_root=args.mutation_root,
            allowed_mutation_globs=args.allow_mutation_glob,
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
