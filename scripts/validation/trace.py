#!/usr/bin/env python3
"""Optional local tracing for validation gate invocations.

Trace files are operational diagnostics under ``.local/validation-traces``.
They are not validation receipts, scientific evidence, or authority to skip a
gate.  Tracing is disabled unless ``AETHER_VALIDATION_TRACE`` is truthy or a
caller explicitly enables a :class:`TraceSession`.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence, TextIO


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TRACE_DIR = REPO_ROOT / ".local" / "validation-traces"
TRACE_SCHEMA_ID = "validation_invocation_trace_v1"
TRACE_REPORT_SCHEMA_ID = "validation_invocation_trace_report_v1"
TRACE_ENV = "AETHER_VALIDATION_TRACE"
TRACE_DIR_ENV = "AETHER_VALIDATION_TRACE_DIR"
TRACE_ID_ENV = "AETHER_VALIDATION_TRACE_ID"
TRACE_RAW_PATH_ENV = "AETHER_VALIDATION_TRACE_RAW_PATH"
TRACE_HOOK_DIR_ENV = "AETHER_VALIDATION_TRACE_HOOK_DIR"
TRACE_PARENT_EVENT_ENV = "AETHER_VALIDATION_PARENT_EVENT_ID"
TRACE_PARENT_GATE_ENV = "AETHER_VALIDATION_PARENT_GATE_ID"
TRACE_SCOPE_ENV = "AETHER_VALIDATION_TRACE_SCOPE"
TRACE_TREE_ENV = "AETHER_VALIDATION_TRACE_TREE_HASH"
TRACE_CACHE_ENV = "AETHER_VALIDATION_TRACE_CACHE_STATE"
TRUTHY = {"1", "true", "yes", "on"}
_ORIGINAL_SUBPROCESS_RUN = subprocess.run
_TRACE_PATCH_MARKER = "_aether_validation_trace_wrapper"


def tracing_enabled(value: str | bool | None = None) -> bool:
    """Return whether tracing is enabled by an explicit value or environment."""

    if isinstance(value, bool):
        return value
    if value is None:
        value = os.environ.get(TRACE_ENV, "")
    return str(value).strip().lower() in TRUTHY


def _utc_timestamp(unix_ns: int) -> str:
    return datetime.fromtimestamp(unix_ns / 1_000_000_000, timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )


def _safe_token(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-.")
    return token or "trace"


def _output_bytes(*values: Any) -> int:
    total = 0
    for value in values:
        if value is None:
            continue
        if isinstance(value, bytes):
            total += len(value)
        else:
            total += len(str(value).encode("utf-8", errors="replace"))
    return total


def _command_list(command: Any) -> list[str]:
    if isinstance(command, (str, bytes)):
        return [command.decode() if isinstance(command, bytes) else command]
    try:
        return [str(part) for part in command]
    except TypeError:
        return [str(command)]


def canonical_gate_id(command: Any) -> str:
    """Map known legacy commands to the P1-T02 canonical gate IDs."""

    parts = _command_list(command)
    joined = " ".join(parts)
    mappings = (
        ("bootstrap_memory_system.py --validate-only", "memory_core"),
        ("bootstrap_memory_system.py", "memory_sync"),
        ("render_current_frontier.py", "current_frontier_freshness"),
        ("validate_compact_current_frontier_v16.py", "compact_frontier_freshness"),
        ("render_dependency_graph.py", "dependency_graph_freshness"),
        ("validate_task_index.py", "task_index_freshness"),
        ("validate_claim_graph_v1.py", "claim_graph_validation"),
        ("validate_claim_language.py", "claim_language_changed"),
        ("validate_documentation_impact.py", "documentation_impact"),
        ("collect_project_improvement_signals.py", "project_improvement_signals"),
        ("validate_research_control.py --check-diff", "research_control_diff"),
        ("validate_research_control.py", "research_control_core"),
        ("extract_route_signatures.py", "route_signature_diagnostic"),
        ("validate_route_orbits.py", "route_orbit_diagnostic"),
        ("git diff --check", "git_diff_check"),
    )
    for needle, gate_id in mappings:
        if needle in joined:
            return gate_id
    for part in reversed(parts):
        if part.endswith(".py"):
            return f"subprocess:{_safe_token(Path(part).stem)}"
    return f"subprocess:{_safe_token(Path(parts[0]).name if parts else 'unknown')}"


def _identity_key(event: Mapping[str, Any]) -> str:
    payload = {
        "gate_id": event["gate_id"],
        "scope": event["scope"],
        "tree_hash": event["tree_hash"],
        "cache_state": event["cache_state"],
        "command_digest": event.get("command_digest", ""),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


@dataclass
class GateSpan:
    """Mutable result fields for one active trace event."""

    event_id: str
    gate_id: str
    status: str = "PASS"
    output_bytes: int = 0

    def set_result(self, *, status: str, output_bytes: int = 0) -> None:
        self.status = status
        self.output_bytes = max(0, int(output_bytes))


class TraceSession:
    """Collect nested gate events without granting validation authority."""

    def __init__(
        self,
        *,
        trace_id: str | None = None,
        trace_dir: Path | str | None = None,
        raw_path: Path | str | None = None,
        enabled: bool | None = None,
        base_parent_event_id: str = "",
        base_parent_gate_id: str = "",
    ) -> None:
        self.enabled = tracing_enabled(enabled)
        self.trace_id = _safe_token(trace_id or uuid.uuid4().hex)
        self.trace_dir = Path(trace_dir or os.environ.get(TRACE_DIR_ENV, DEFAULT_TRACE_DIR))
        self.raw_path = Path(raw_path) if raw_path else self.trace_dir / f"{self.trace_id}.jsonl"
        self.report_path = self.trace_dir / f"{self.trace_id}.json"
        self.base_parent_event_id = base_parent_event_id
        self.base_parent_gate_id = base_parent_gate_id
        self._stack: list[GateSpan] = []

    @contextlib.contextmanager
    def gate(
        self,
        gate_id: str,
        *,
        scope: str,
        tree_hash: str,
        cache_state: str,
        command: Sequence[str] | None = None,
        parent_event_id: str = "",
        parent_gate_id: str = "",
    ) -> Iterator[GateSpan]:
        """Record one gate while preserving the wrapped operation's behavior."""

        if not self.enabled:
            yield GateSpan(event_id="", gate_id=gate_id)
            return

        active_parent = self._stack[-1] if self._stack else None
        span = GateSpan(event_id=uuid.uuid4().hex, gate_id=gate_id)
        resolved_parent_event = (
            parent_event_id
            or (active_parent.event_id if active_parent else "")
            or self.base_parent_event_id
        )
        resolved_parent_gate = (
            parent_gate_id
            or (active_parent.gate_id if active_parent else "")
            or self.base_parent_gate_id
        )
        start_unix_ns = time.time_ns()
        start_monotonic_ns = time.monotonic_ns()
        self._stack.append(span)
        try:
            yield span
        except BaseException:
            span.status = "FAIL"
            raise
        finally:
            self._stack.pop()
            end_unix_ns = time.time_ns()
            command_parts = list(command or [])
            event = {
                "schema_id": TRACE_SCHEMA_ID,
                "trace_id": self.trace_id,
                "event_id": span.event_id,
                "gate_id": gate_id,
                "scope": scope,
                "tree_hash": tree_hash,
                "parent_event_id": resolved_parent_event,
                "parent_gate_id": resolved_parent_gate,
                "start": _utc_timestamp(start_unix_ns),
                "end": _utc_timestamp(end_unix_ns),
                "start_unix_ns": start_unix_ns,
                "end_unix_ns": end_unix_ns,
                "duration_seconds": round(
                    (time.monotonic_ns() - start_monotonic_ns) / 1_000_000_000, 9
                ),
                "status": span.status,
                "output_bytes": span.output_bytes,
                "cache_state": cache_state,
                "command_executable": Path(command_parts[0]).name if command_parts else "",
                "command_digest": hashlib.sha256(
                    json.dumps(command_parts, separators=(",", ":")).encode("utf-8")
                ).hexdigest(),
                "local_non_authoritative": True,
            }
            event["identity_key"] = _identity_key(event)
            try:
                self._append_event(event)
            except OSError:
                # A caller may replace the writer, but tracing must still fail open.
                pass

    def _append_event(self, event: Mapping[str, Any]) -> None:
        try:
            self.raw_path.parent.mkdir(parents=True, exist_ok=True)
            line = json.dumps(dict(event), sort_keys=True, separators=(",", ":")) + "\n"
            descriptor = os.open(self.raw_path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
            try:
                os.write(descriptor, line.encode("utf-8"))
            finally:
                os.close(descriptor)
        except OSError:
            # Instrumentation failure must not change gate behavior or status.
            return

    def child_environment(
        self,
        span: GateSpan,
        *,
        scope: str,
        tree_hash: str,
        cache_state: str,
        base: Mapping[str, str] | None = None,
    ) -> dict[str, str]:
        environment = dict(base or os.environ)
        hook_dir = ensure_runtime_hook(self.trace_dir, self.trace_id)
        existing_pythonpath = environment.get("PYTHONPATH", "")
        environment.update(
            {
                TRACE_ENV: "1",
                TRACE_DIR_ENV: str(self.trace_dir),
                TRACE_ID_ENV: self.trace_id,
                TRACE_RAW_PATH_ENV: str(self.raw_path),
                TRACE_HOOK_DIR_ENV: str(hook_dir),
                TRACE_PARENT_EVENT_ENV: span.event_id,
                TRACE_PARENT_GATE_ENV: span.gate_id,
                TRACE_SCOPE_ENV: scope,
                TRACE_TREE_ENV: tree_hash,
                TRACE_CACHE_ENV: cache_state,
                "PYTHONPATH": os.pathsep.join(
                    item for item in (str(hook_dir), existing_pythonpath) if item
                ),
            }
        )
        return environment

    def run_subprocess(
        self,
        command: Any,
        *popenargs: Any,
        gate_id: str | None = None,
        scope: str,
        tree_hash: str,
        cache_state: str,
        **kwargs: Any,
    ) -> subprocess.CompletedProcess[Any]:
        """Run a subprocess with a trace event and unchanged subprocess semantics."""

        if not self.enabled:
            return _ORIGINAL_SUBPROCESS_RUN(command, *popenargs, **kwargs)
        resolved_gate_id = gate_id or canonical_gate_id(command)
        command_parts = _command_list(command)
        with self.gate(
            resolved_gate_id,
            scope=scope,
            tree_hash=tree_hash,
            cache_state=cache_state,
            command=command_parts,
        ) as span:
            child_kwargs = dict(kwargs)
            child_kwargs["env"] = self.child_environment(
                span,
                scope=scope,
                tree_hash=tree_hash,
                cache_state=cache_state,
                base=kwargs.get("env"),
            )
            try:
                completed = _ORIGINAL_SUBPROCESS_RUN(command, *popenargs, **child_kwargs)
            except subprocess.CalledProcessError as exc:
                span.set_result(
                    status="FAIL",
                    output_bytes=_output_bytes(exc.stdout, exc.stderr),
                )
                raise
            except BaseException:
                span.status = "FAIL"
                raise
            span.set_result(
                status="PASS" if completed.returncode == 0 else "FAIL",
                output_bytes=_output_bytes(completed.stdout, completed.stderr),
            )
            return completed

    def read_events(self) -> list[dict[str, Any]]:
        if not self.raw_path.exists():
            return []
        events: list[dict[str, Any]] = []
        for line in self.raw_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("trace_id") == self.trace_id:
                events.append(event)
        return events

    def finalize(self) -> dict[str, Any]:
        """Write a compact local report with duplicate identities annotated."""

        events = sorted(
            self.read_events(),
            key=lambda event: (int(event.get("start_unix_ns", 0)), event.get("event_id", "")),
        )
        first_by_identity: dict[str, str] = {}
        duplicates: list[dict[str, str]] = []
        for sequence, event in enumerate(events, start=1):
            event["sequence"] = sequence
            identity = str(event.get("identity_key", ""))
            duplicate_of = first_by_identity.get(identity, "")
            event["duplicate_identity"] = bool(duplicate_of)
            event["duplicate_of_event_id"] = duplicate_of
            if duplicate_of:
                duplicates.append(
                    {
                        "event_id": str(event.get("event_id", "")),
                        "duplicate_of_event_id": duplicate_of,
                        "identity_key": identity,
                    }
                )
            elif identity:
                first_by_identity[identity] = str(event.get("event_id", ""))
        status_counts: dict[str, int] = {}
        for event in events:
            status = str(event.get("status", "UNKNOWN"))
            status_counts[status] = status_counts.get(status, 0) + 1
        report = {
            "schema_id": TRACE_REPORT_SCHEMA_ID,
            "trace_id": self.trace_id,
            "status": "PASS" if not status_counts.get("FAIL", 0) else "FAIL",
            "event_count": len(events),
            "duplicate_identity_count": len(duplicates),
            "status_counts": status_counts,
            "duplicates": duplicates,
            "events": events,
            "raw_trace_path": str(self.raw_path),
            "local_non_authoritative": True,
            "trace_absence_is_not_pass_evidence": True,
        }
        try:
            self.report_path.parent.mkdir(parents=True, exist_ok=True)
            self.report_path.write_text(
                json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
        except OSError:
            pass
        return report


def normalized_events(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Normalize volatile IDs and timestamps for deterministic comparisons."""

    ordered = sorted(
        (dict(event) for event in events),
        key=lambda event: (int(event.get("sequence", 0)), int(event.get("start_unix_ns", 0))),
    )
    id_map = {
        str(event.get("event_id", "")): f"event-{index}"
        for index, event in enumerate(ordered, start=1)
        if event.get("event_id")
    }
    normalized: list[dict[str, Any]] = []
    for event in ordered:
        item = dict(event)
        item["trace_id"] = "TRACE"
        item["event_id"] = id_map.get(str(item.get("event_id", "")), "")
        item["parent_event_id"] = id_map.get(str(item.get("parent_event_id", "")), "")
        item["duplicate_of_event_id"] = id_map.get(
            str(item.get("duplicate_of_event_id", "")), ""
        )
        item["start"] = "NORMALIZED"
        item["end"] = "NORMALIZED"
        item["start_unix_ns"] = 0
        item["end_unix_ns"] = 0
        item["duration_seconds"] = 0.0
        normalized.append(item)
    return normalized


def normalized_trace_json(events: Sequence[Mapping[str, Any]]) -> str:
    return json.dumps(normalized_events(events), sort_keys=True, separators=(",", ":"))


def ensure_runtime_hook(trace_dir: Path, trace_id: str) -> Path:
    """Create a local sitecustomize hook so nested Python launches are traced."""

    hook_dir = trace_dir / "runtime" / _safe_token(trace_id)
    hook_path = hook_dir / "sitecustomize.py"
    if hook_path.exists():
        return hook_dir
    try:
        hook_dir.mkdir(parents=True, exist_ok=True)
        module_path = Path(__file__).resolve()
        hook_path.write_text(
            "from importlib.util import module_from_spec, spec_from_file_location\n"
            "import sys\n"
            f"_spec = spec_from_file_location('aether_validation_trace_runtime', {str(module_path)!r})\n"
            "if _spec is not None and _spec.loader is not None:\n"
            "    _module = module_from_spec(_spec)\n"
            "    sys.modules[_spec.name] = _module\n"
            "    _spec.loader.exec_module(_module)\n"
            "    _module.install_subprocess_tracing_from_environment()\n",
            encoding="utf-8",
        )
    except OSError:
        return hook_dir
    return hook_dir


def _traced_run_wrapper(session: TraceSession, *, scope: str, tree_hash: str, cache_state: str):
    def wrapper(command: Any, *args: Any, **kwargs: Any):
        return session.run_subprocess(
            command,
            *args,
            scope=scope,
            tree_hash=tree_hash,
            cache_state=cache_state,
            **kwargs,
        )

    setattr(wrapper, _TRACE_PATCH_MARKER, True)
    return wrapper


@contextlib.contextmanager
def intercept_subprocesses(
    session: TraceSession,
    *,
    scope: str,
    tree_hash: str,
    cache_state: str,
) -> Iterator[None]:
    """Trace subprocess.run calls made within the current Python process."""

    if not session.enabled:
        yield
        return
    previous = subprocess.run
    subprocess.run = _traced_run_wrapper(  # type: ignore[assignment]
        session,
        scope=scope,
        tree_hash=tree_hash,
        cache_state=cache_state,
    )
    try:
        yield
    finally:
        subprocess.run = previous  # type: ignore[assignment]


def install_subprocess_tracing_from_environment() -> None:
    """Install recursive tracing in Python children launched by a trace session."""

    if not tracing_enabled() or getattr(subprocess.run, _TRACE_PATCH_MARKER, False):
        return
    raw_path = os.environ.get(TRACE_RAW_PATH_ENV, "")
    trace_id = os.environ.get(TRACE_ID_ENV, "")
    if not raw_path or not trace_id:
        return
    session = TraceSession(
        trace_id=trace_id,
        trace_dir=os.environ.get(TRACE_DIR_ENV, DEFAULT_TRACE_DIR),
        raw_path=raw_path,
        enabled=True,
        base_parent_event_id=os.environ.get(TRACE_PARENT_EVENT_ENV, ""),
        base_parent_gate_id=os.environ.get(TRACE_PARENT_GATE_ENV, ""),
    )
    subprocess.run = _traced_run_wrapper(  # type: ignore[assignment]
        session,
        scope=os.environ.get(TRACE_SCOPE_ENV, "unspecified"),
        tree_hash=os.environ.get(TRACE_TREE_ENV, "unspecified"),
        cache_state=os.environ.get(TRACE_CACHE_ENV, "unspecified"),
    )


class CountingTextIO:
    """Transparent text stream proxy that counts forwarded UTF-8 bytes."""

    def __init__(self, stream: TextIO) -> None:
        self.stream = stream
        self.byte_count = 0

    def write(self, text: str) -> int:
        self.byte_count += len(text.encode("utf-8", errors="replace"))
        return self.stream.write(text)

    def flush(self) -> None:
        self.stream.flush()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.stream, name)


def _run_python_script(script: Path, argv: Sequence[str]) -> int:
    old_argv = sys.argv
    sys.argv = [str(script), *argv]
    try:
        spec = importlib.util.spec_from_file_location("__main__", script)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"could not load {script}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return 0
    except SystemExit as exc:
        if exc.code is None:
            return 0
        if isinstance(exc.code, int):
            return exc.code
        return 1
    finally:
        sys.argv = old_argv


def run_python_script_with_trace(
    script: Path,
    argv: Sequence[str],
    *,
    session: TraceSession,
    gate_id: str,
    scope: str,
    tree_hash: str,
    cache_state: str,
) -> int:
    """Run a Python entry point in-process so nested launches are observable."""

    if not session.enabled:
        return _run_python_script(script, argv)
    stdout_counter = CountingTextIO(sys.stdout)
    stderr_counter = CountingTextIO(sys.stderr)
    returncode = 1
    with session.gate(
        gate_id,
        scope=scope,
        tree_hash=tree_hash,
        cache_state=cache_state,
        command=[sys.executable, str(script), *argv],
    ) as span:
        with intercept_subprocesses(
            session,
            scope=scope,
            tree_hash=tree_hash,
            cache_state=cache_state,
        ):
            with contextlib.redirect_stdout(stdout_counter), contextlib.redirect_stderr(
                stderr_counter
            ):
                returncode = _run_python_script(script, argv)
        span.set_result(
            status="PASS" if returncode == 0 else "FAIL",
            output_bytes=stdout_counter.byte_count + stderr_counter.byte_count,
        )
    session.finalize()
    return returncode


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate-id", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--tree-hash", required=True)
    parser.add_argument("--cache-state", default="disabled")
    parser.add_argument("--trace-id")
    parser.add_argument("--trace-dir", type=Path, default=DEFAULT_TRACE_DIR)
    parser.add_argument("--python-script", type=Path, required=True)
    parser.add_argument("script_args", nargs=argparse.REMAINDER)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    script_args = list(args.script_args)
    if script_args[:1] == ["--"]:
        script_args = script_args[1:]
    session = TraceSession(
        trace_id=args.trace_id,
        trace_dir=args.trace_dir,
        enabled=None,
    )
    return run_python_script_with_trace(
        args.python_script.resolve(),
        script_args,
        session=session,
        gate_id=args.gate_id,
        scope=args.scope,
        tree_hash=args.tree_hash,
        cache_state=args.cache_state,
    )


if __name__ == "__main__":
    raise SystemExit(main())
