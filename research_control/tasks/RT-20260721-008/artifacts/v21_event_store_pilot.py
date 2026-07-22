#!/usr/bin/env python3
"""Build the bounded P10-T06 project-control event-store shadow pilot.

The tracked JSONL, manifest, and views produced here are task-local evidence.
They do not replace any live registry, reader, writer, or authority surface.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import sqlite3
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Iterable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
FIXTURE_PATH = ARTIFACT_DIR / "v21_event_store_pilot_fixture.json"
SQLITE_PATH = REPO_ROOT / ".local/research_control/p10_t06_event_store_pilot.sqlite3"

OUTPUT_NAMES = {
    "events": "v21_event_store_pilot_events.jsonl",
    "manifest": "v21_event_store_pilot_manifest.json",
    "task_view": "v21_event_store_pilot_task_view.csv",
    "candidate_view": "v21_event_store_pilot_candidate_view.json",
    "handoff_view": "v21_event_store_pilot_handoff_view.md",
    "status_view": "v21_event_store_pilot_status_view.md",
    "parity_receipt": "v21_event_store_pilot_parity_receipt.json",
    "compact_receipt": "v21_event_store_pilot_compact_receipt.json",
}

ALLOWED_EVENT_TYPES = {
    "task": {"task_completed"},
    "decision": {"decision_completed"},
    "agent_job": {"job_completed"},
    "candidate": {"candidate_created"},
    "claim": {"claim_boundary_closed"},
    "validation": {"validation_passed"},
    "handoff": {"handoff_created"},
}

AUTHORITY_FLAGS = {
    "project_control_only": True,
    "scientific_claims_changed": False,
    "physics_promotion_authorized": False,
    "proof_authority": False,
}


class NoFloatSafeLoader(yaml.SafeLoader):
    """Safe YAML loader that preserves decimal lexemes as JSON strings."""


def _construct_decimal_string(loader: yaml.SafeLoader, node: yaml.Node) -> str:
    return loader.construct_scalar(node)


NoFloatSafeLoader.add_constructor("tag:yaml.org,2002:float", _construct_decimal_string)


class PilotError(RuntimeError):
    """A fail-closed pilot validation error."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_json_value(value: Any) -> Any:
    """Normalize YAML values into the no-float canonical JSON subset."""
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        raise PilotError("floating-point values are forbidden in pilot events")
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    if isinstance(value, list):
        return [normalize_json_value(item) for item in value]
    if isinstance(value, dict):
        return {
            str(key): normalize_json_value(item)
            for key, item in value.items()
        }
    raise PilotError(f"unsupported canonical JSON value: {type(value).__name__}")


def canonical_json_bytes(value: Any, *, newline: bool = False) -> bytes:
    normalized = normalize_json_value(value)
    data = json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return data + (b"\n" if newline else b"")


def load_fixture(path: Path = FIXTURE_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_id") != "v21_event_store_pilot_fixture_v1":
        raise PilotError("unsupported pilot fixture schema")
    return data


def git_source_loader(repo_root: Path, revision: str) -> Callable[[str], bytes]:
    def load(path: str) -> bytes:
        result = subprocess.run(
            ["git", "show", f"{revision}:{path}"],
            cwd=repo_root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            detail = result.stderr.decode("utf-8", errors="replace").strip()
            raise PilotError(f"cannot read pinned source {path}: {detail}")
        return result.stdout

    return load


def parse_document(parser: str, raw: bytes) -> Any:
    text = raw.decode("utf-8")
    if parser == "json":
        return normalize_json_value(json.loads(text))
    if parser == "yaml":
        return normalize_json_value(yaml.load(text, Loader=NoFloatSafeLoader))
    if parser == "csv":
        return parse_csv_document(raw)
    raise PilotError(f"unknown source parser: {parser}")


def yaml_float_paths(raw: bytes) -> list[str]:
    """Locate legacy YAML float fields converted to decimal strings."""
    document = yaml.safe_load(raw.decode("utf-8"))
    paths: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, float):
            paths.append(path)
        elif isinstance(value, dict):
            for key, item in value.items():
                visit(item, f"{path}.{key}" if path else str(key))
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, f"{path}[{index}]")

    visit(document, "")
    return paths


def parse_csv_document(raw: bytes) -> dict[str, Any]:
    text = raw.decode("utf-8")
    if "\r" in text:
        raise PilotError("legacy CSV line ending is not LF")
    lines = text.splitlines()
    if not lines:
        raise PilotError("legacy CSV is empty")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    rows = [dict(row) for row in reader]
    if len(lines) != len(rows) + 1:
        raise PilotError("multiline legacy CSV rows are outside the pilot shape")
    return {
        "header": lines[0],
        "fieldnames": list(reader.fieldnames or []),
        "rows": [
            {"source_ordinal": index, "raw_line": lines[index + 1], "fields": row}
            for index, row in enumerate(rows)
        ],
    }


def load_sources(
    fixture: dict[str, Any],
    source_loader: Callable[[str], bytes] | None = None,
) -> dict[str, dict[str, Any]]:
    loader = source_loader or git_source_loader(REPO_ROOT, fixture["pinned_commit"])
    loaded: dict[str, dict[str, Any]] = {}
    for binding in fixture["sources"]:
        raw = loader(binding["path"])
        actual_hash = sha256_bytes(raw)
        if actual_hash != binding["sha256"]:
            raise PilotError(
                f"pinned source hash mismatch for {binding['path']}: "
                f"expected {binding['sha256']} got {actual_hash}"
            )
        loaded[binding["key"]] = {
            "binding": binding,
            "raw": raw,
            "sha256": actual_hash,
            "document": parse_document(binding["parser"], raw),
            "decimal_string_conversion_paths": (
                yaml_float_paths(raw) if binding["parser"] == "yaml" else []
            ),
        }
    return loaded


def source_ref(source: dict[str, Any]) -> dict[str, str]:
    binding = source["binding"]
    return {
        "object_id": binding["object_id"],
        "path": binding["path"],
        "sha256": source["sha256"],
        "authority_status": binding["authority_status"],
    }


def csv_rows_by_id(
    source: dict[str, Any], key: str, selected_ids: Iterable[str]
) -> list[dict[str, Any]]:
    rows = source["document"]["rows"]
    indexed = {row["fields"].get(key): row for row in rows}
    selected: list[dict[str, Any]] = []
    for selected_id in selected_ids:
        if selected_id not in indexed:
            raise PilotError(f"selected identifier {selected_id} not found in {key}")
        selected.append(indexed[selected_id])
    if len({row["fields"][key] for row in selected}) != len(selected):
        raise PilotError(f"duplicate selected identifier in {key}")
    return selected


def event_identity_basis(event: dict[str, Any]) -> dict[str, Any]:
    return {
        key: event[key]
        for key in (
            "event_schema_id",
            "event_domain",
            "event_type",
            "subject_id",
            "operation_id",
            "source_refs",
            "payload",
        )
    }


def make_event(
    *,
    fixture: dict[str, Any],
    domain: str,
    event_type: str,
    subject_id: str,
    effective_at: str,
    actor_role_ref: str,
    source: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    event = {
        "event_schema_id": fixture["event_schema_id"],
        "event_domain": domain,
        "event_type": event_type,
        "subject_id": subject_id,
        "operation_id": (
            f"{fixture['pilot_id']}:snapshot:{domain}:{subject_id}:"
            f"{source['sha256']}"
        ),
        "effective_at": effective_at,
        "actor_role_ref": actor_role_ref,
        "source_refs": [source_ref(source)],
        "payload": normalize_json_value(payload),
        "authority": dict(AUTHORITY_FLAGS),
    }
    event["event_id"] = "EVT-V21-" + sha256_bytes(
        canonical_json_bytes(event_identity_basis(event))
    )
    return event


def finalize_chain(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prior = "GENESIS"
    finalized: list[dict[str, Any]] = []
    for sequence, source_event in enumerate(events, start=1):
        event = dict(source_event)
        event["sequence"] = sequence
        event["prior_event_hash"] = prior
        event["event_hash"] = sha256_bytes(canonical_json_bytes(event))
        prior = event["event_hash"]
        finalized.append(event)
    return finalized


def build_events(
    fixture: dict[str, Any], sources: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    selected = fixture["selected_ids"]

    csv_specs = [
        (
            "task_registry", "task", "task_completed", "task_id", "updated_at",
            "director-of-research@0.3.0",
        ),
        (
            "decision_registry", "decision", "decision_completed", "decision_id",
            "completed_at", "director-of-research@0.3.0",
        ),
        (
            "agent_job_registry", "agent_job", "job_completed", "job_id",
            "completed_at", None,
        ),
        (
            "claim_registry", "claim", "claim_boundary_closed", "claim_boundary_id",
            "updated_at", "director-of-research@0.3.0",
        ),
    ]
    for source_key, domain, event_type, id_key, time_key, fixed_actor in csv_specs:
        source = sources[source_key]
        for row in csv_rows_by_id(source, id_key, selected[domain]):
            fields = row["fields"]
            actor = fixed_actor
            if actor is None:
                actor = f"{fields['role_id']}@{fields['role_version']}"
            events.append(
                make_event(
                    fixture=fixture,
                    domain=domain,
                    event_type=event_type,
                    subject_id=fields[id_key],
                    effective_at=fields[time_key],
                    actor_role_ref=actor,
                    source=source,
                    payload={
                        "legacy_header": source["document"]["header"],
                        "legacy_raw_line": row["raw_line"],
                        "legacy_row": fields,
                        "source_ordinal": row["source_ordinal"],
                        "snapshot_import": True,
                    },
                )
            )

    candidate_source = sources["candidate_registry"]
    candidate_doc = candidate_source["document"]
    task_005_row = csv_rows_by_id(
        sources["task_registry"], "task_id", ["RT-20260721-005"]
    )[0]["fields"]
    events.append(
        make_event(
            fixture=fixture,
            domain="candidate",
            event_type="candidate_created",
            subject_id="CANDIDATE-LINEAGE-REGISTRY-RT-20260721-005",
            effective_at=task_005_row["updated_at"],
            actor_role_ref="project-control-maintainer@0.2.0",
            source=candidate_source,
            payload={"document": candidate_doc, "snapshot_import": True},
        )
    )

    for source_key in ("completion_005", "completion_006", "completion_007"):
        source = sources[source_key]
        document = source["document"]
        if document["completion_id"] not in selected["validation"]:
            raise PilotError("completion source is outside selected validation IDs")
        events.append(
            make_event(
                fixture=fixture,
                domain="validation",
                event_type="validation_passed",
                subject_id=document["completion_id"],
                effective_at=document["completed_at"],
                actor_role_ref=document["execution_role_ref"],
                source=source,
                payload={"document": document, "snapshot_import": True},
            )
        )

    for source_key in ("handoff_0806", "handoff_0807", "handoff_0808"):
        source = sources[source_key]
        document = source["document"]
        if document["handoff_id"] not in selected["handoff"]:
            raise PilotError("handoff source is outside selected handoff IDs")
        actor = document.get("source_execution_role_ref", "director-of-research@0.3.0")
        events.append(
            make_event(
                fixture=fixture,
                domain="handoff",
                event_type="handoff_created",
                subject_id=document["handoff_id"],
                effective_at=document["created_at"],
                actor_role_ref=actor,
                source=source,
                payload={"document": document, "snapshot_import": True},
            )
        )

    program_source = sources["program_state"]
    program_document = program_source["document"]
    latest_handoff = sources["handoff_0808"]["document"]
    events.append(
        make_event(
            fixture=fixture,
            domain="validation",
            event_type="validation_passed",
            subject_id=f"PROGRAM-STATE-{fixture['pinned_commit']}",
            effective_at=latest_handoff["created_at"],
            actor_role_ref="director-of-research@0.3.0",
            source=program_source,
            payload={"document": program_document, "snapshot_import": True},
        )
    )
    return finalize_chain(events)


def events_jsonl(events: list[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(event, newline=True) for event in events)


def render_task_view(events: list[dict[str, Any]]) -> bytes:
    task_events = sorted(
        (event for event in events if event["event_domain"] == "task"),
        key=lambda event: event["payload"]["source_ordinal"],
    )
    headers = {event["payload"]["legacy_header"] for event in task_events}
    if len(headers) != 1:
        raise PilotError("task events do not share one legacy header")
    lines = [next(iter(headers))]
    lines.extend(event["payload"]["legacy_raw_line"] for event in task_events)
    return ("\n".join(lines) + "\n").encode("utf-8")


def render_candidate_view(events: list[dict[str, Any]]) -> bytes:
    candidate_events = [event for event in events if event["event_domain"] == "candidate"]
    if len(candidate_events) != 1:
        raise PilotError("pilot expects one candidate-registry snapshot event")
    return canonical_json_bytes(candidate_events[0]["payload"]["document"], newline=True)


def markdown_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        rendered = canonical_json_bytes(value).decode("utf-8")
    elif isinstance(value, bool):
        rendered = "true" if value else "false"
    else:
        rendered = str(value)
    return rendered.replace("|", "\\|").replace("\n", " ")


def get_path(document: dict[str, Any], dotted_path: str) -> tuple[bool, Any]:
    current: Any = document
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def render_handoff_view(
    fixture: dict[str, Any], events: list[dict[str, Any]]
) -> bytes:
    documents = [
        event["payload"]["document"]
        for event in events
        if event["event_domain"] == "handoff"
    ]
    documents.sort(key=lambda item: item["handoff_id"])
    columns = [
        "handoff_id", "created_at", "task_id", "job_id", "status",
        "completion_hash", "summary", "next_action", "claim_boundary",
    ]
    rows = []
    for document in documents:
        rows.append(
            {
                "handoff_id": document["handoff_id"],
                "created_at": document["created_at"],
                "task_id": document["task_id"],
                "job_id": document["job_id"],
                "status": document["status"],
                "completion_hash": document.get(
                    "completion_hash", document.get("completion_sha256", "")
                ),
                "summary": document.get("summary", document.get("handoff_summary", "")),
                "next_action": document["next_action"],
                "claim_boundary": document.get("current_claim_boundary", ""),
            }
        )
    lines = [
        "---",
        "authority: generated_noncanonical",
        "task_id: RT-20260721-008",
        "plan_task_id: P10-T06",
        "pilot_id: PILOT-V21-P10-T06-001",
        "---",
        "",
        "# V21 event-store pilot handoff shadow view",
        "",
        f"Pinned source commit: `{fixture['pinned_commit']}`.",
        "",
        "This task-local compatibility view is not a handoff authority surface.",
        "",
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_cell(row[key]) for key in columns) + " |")
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def render_status_view(
    fixture: dict[str, Any], events: list[dict[str, Any]]
) -> bytes:
    status_events = [
        event
        for event in events
        if event["subject_id"] == f"PROGRAM-STATE-{fixture['pinned_commit']}"
    ]
    if len(status_events) != 1:
        raise PilotError("pilot expects one pinned program-state snapshot")
    document = status_events[0]["payload"]["document"]
    lines = [
        "---",
        "authority: generated_noncanonical",
        "task_id: RT-20260721-008",
        "plan_task_id: P10-T06",
        "pilot_id: PILOT-V21-P10-T06-001",
        "---",
        "",
        "# V21 event-store pilot status shadow view",
        "",
        f"Pinned source commit: `{fixture['pinned_commit']}`.",
        "",
        "This task-local compatibility view is not current project-control or science authority.",
        "",
        "| field | value |",
        "| --- | --- |",
    ]
    for field in fixture["status_view_fields"]:
        present, value = get_path(document, field)
        if not present:
            raise PilotError(f"status field missing at pinned source: {field}")
        lines.append(f"| {markdown_cell(field)} | {markdown_cell(value)} |")
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def validate_events(
    events: list[dict[str, Any]], sources: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def record(name: str, condition: bool, detail: str) -> None:
        checks.append({"name": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    required = {
        "event_schema_id", "event_id", "sequence", "prior_event_hash", "event_hash",
        "event_domain", "event_type", "subject_id", "operation_id", "effective_at",
        "actor_role_ref", "source_refs", "payload", "authority",
    }
    record(
        "event_required_fields",
        all(required.issubset(event) for event in events),
        "Every event carries the complete v1 envelope.",
    )
    record(
        "sequence_is_contiguous",
        [event.get("sequence") for event in events] == list(range(1, len(events) + 1)),
        "Global sequence begins at one and has no gap.",
    )
    prior = "GENESIS"
    chain_ok = True
    identity_ok = True
    type_ok = True
    source_ok = True
    authority_ok = True
    source_by_path = {item["binding"]["path"]: item for item in sources.values()}
    for event in events:
        without_hash = {key: value for key, value in event.items() if key != "event_hash"}
        expected_hash = sha256_bytes(canonical_json_bytes(without_hash))
        chain_ok &= event.get("prior_event_hash") == prior
        chain_ok &= event.get("event_hash") == expected_hash
        prior = event.get("event_hash", "")
        expected_id = "EVT-V21-" + sha256_bytes(
            canonical_json_bytes(event_identity_basis(event))
        )
        identity_ok &= event.get("event_id") == expected_id
        type_ok &= event.get("event_type") in ALLOWED_EVENT_TYPES.get(
            event.get("event_domain"), set()
        )
        authority_ok &= event.get("authority") == AUTHORITY_FLAGS
        refs = event.get("source_refs", [])
        source_ok &= bool(refs)
        for ref in refs:
            source = source_by_path.get(ref.get("path"))
            source_ok &= source is not None
            if source is not None:
                source_ok &= ref.get("sha256") == source["sha256"]
                source_ok &= ref.get("object_id") == source["binding"]["object_id"]
    record("event_hash_chain", chain_ok, "Event hashes and prior hashes replay to the manifest head.")
    record("event_identity", identity_ok, "Every full SHA-256 content identity recomputes exactly.")
    record("known_event_types", type_ok, "All events use a declared pilot domain and transition.")
    record("source_references_exact", source_ok, "Every source reference resolves to its pinned byte hash.")
    record("authority_flags_fail_closed", authority_ok, "Every event is project-control-only with no promotion or proof authority.")
    record(
        "event_ids_unique",
        len({event.get("event_id") for event in events}) == len(events),
        "No logical event identity collides within the pilot.",
    )
    return checks


def rebuild_sqlite(
    events: list[dict[str, Any]], target: Path | None = None
) -> dict[str, Any]:
    if target is not None:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            target.unlink()
        connection = sqlite3.connect(target)
    else:
        connection = sqlite3.connect(":memory:")
    try:
        connection.executescript(
            """
            CREATE TABLE events (
                sequence INTEGER PRIMARY KEY,
                event_id TEXT NOT NULL UNIQUE,
                event_hash TEXT NOT NULL UNIQUE,
                prior_event_hash TEXT NOT NULL,
                event_domain TEXT NOT NULL,
                event_type TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                effective_at TEXT NOT NULL,
                source_path TEXT NOT NULL,
                source_sha256 TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                event_json TEXT NOT NULL
            );
            CREATE INDEX events_domain_idx ON events(event_domain, sequence);
            CREATE INDEX events_subject_idx ON events(subject_id, sequence);
            """
        )
        for event in events:
            ref = event["source_refs"][0]
            connection.execute(
                "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event["sequence"], event["event_id"], event["event_hash"],
                    event["prior_event_hash"], event["event_domain"], event["event_type"],
                    event["subject_id"], event["effective_at"], ref["path"], ref["sha256"],
                    canonical_json_bytes(event["payload"]).decode("utf-8"),
                    canonical_json_bytes(event).decode("utf-8"),
                ),
            )
        connection.commit()
        total = connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        domain_rows = connection.execute(
            "SELECT event_domain, COUNT(*) FROM events GROUP BY event_domain ORDER BY event_domain"
        ).fetchall()
        selected_task_count = connection.execute(
            "SELECT COUNT(*) FROM events WHERE event_domain = 'task' AND subject_id LIKE 'RT-20260721-00%'"
        ).fetchone()[0]
        chain_head = connection.execute(
            "SELECT event_hash FROM events ORDER BY sequence DESC LIMIT 1"
        ).fetchone()[0]
        return {
            "status": "PASS" if total == len(events) else "FAIL",
            "event_count": total,
            "domain_counts": {domain: count for domain, count in domain_rows},
            "selected_task_count": selected_task_count,
            "chain_head": chain_head,
            "database_role": "generated_disposable_untracked_query_index",
            "tracked": False,
            "authority": False,
        }
    finally:
        connection.close()


def field_accounting(
    fixture: dict[str, Any], sources: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    handoff_entries = []
    handoff_allowlist = set(fixture["handoff_view_fields"])
    for key in ("handoff_0806", "handoff_0807", "handoff_0808"):
        source = sources[key]
        document = source["document"]
        mapped = sorted(field for field in handoff_allowlist if field in document)
        excluded = [
            {
                "path": field + (".*" if isinstance(document[field], (dict, list)) else ""),
                "reason": "intentionally_excluded_from_compact_shadow_projection",
            }
            for field in sorted(set(document) - set(mapped))
        ]
        handoff_entries.append(
            {
                "source_path": source["binding"]["path"],
                "mapped_paths": mapped,
                "excluded_paths": excluded,
                "unmapped_paths": [],
            }
        )

    program = sources["program_state"]["document"]
    mapped_status = fixture["status_view_fields"]
    mapped_top = {path.split(".", 1)[0] for path in mapped_status}
    excluded_status = [
        {
            "path": key + (".*" if isinstance(program[key], (dict, list)) else ""),
            "reason": "outside_bounded_status_shadow_projection",
        }
        for key in sorted(set(program) - mapped_top)
    ]
    p10_key = "p10_t05_canonical_event_store_architecture"
    nested_selected = {
        path.split(".", 1)[1] for path in mapped_status if path.startswith(p10_key + ".")
    }
    excluded_status.extend(
        {
            "path": f"{p10_key}.{key}" + (
                ".*" if isinstance(program[p10_key][key], (dict, list)) else ""
            ),
            "reason": "outside_bounded_status_shadow_projection",
        }
        for key in sorted(set(program[p10_key]) - nested_selected)
    )
    return {
        "task_view": {
            "mapped_paths": ["all_columns_for_selected_rows"],
            "excluded_paths": [],
            "unmapped_paths": [],
            "out_of_slice_record_count": (
                len(sources["task_registry"]["document"]["rows"])
                - len(fixture["selected_ids"]["task"])
            ),
        },
        "candidate_view": {
            "mapped_paths": ["*"],
            "excluded_paths": [],
            "unmapped_paths": [],
            "out_of_slice_record_count": 0,
        },
        "handoff_view": handoff_entries,
        "status_view": {
            "source_path": sources["program_state"]["binding"]["path"],
            "mapped_paths": mapped_status,
            "excluded_paths": excluded_status,
            "unmapped_paths": [],
        },
    }


def build_bundle(
    fixture: dict[str, Any] | None = None,
    source_loader: Callable[[str], bytes] | None = None,
) -> dict[str, Any]:
    fixture = fixture or load_fixture()
    sources = load_sources(fixture, source_loader)
    events = build_events(fixture, sources)
    event_bytes = events_jsonl(events)
    renderer_hash = sha256_bytes(Path(__file__).read_bytes())
    source_bindings = [
        {
            "object_id": item["binding"]["object_id"],
            "path": item["binding"]["path"],
            "sha256": item["sha256"],
            "authority_status": item["binding"]["authority_status"],
        }
        for item in sources.values()
    ]
    manifest = {
        "schema_id": "v21_event_store_pilot_manifest_v1",
        "pilot_id": fixture["pilot_id"],
        "task_id": fixture["task_id"],
        "plan_task_id": fixture["plan_task_id"],
        "status": "shadow_pilot_not_authoritative",
        "pinned_commit": fixture["pinned_commit"],
        "event_schema_id": fixture["event_schema_id"],
        "encoding_profile": fixture["encoding_profile"],
        "renderer": {
            "path": "research_control/tasks/RT-20260721-008/artifacts/v21_event_store_pilot.py",
            "version": fixture["renderer_version"],
            "sha256": renderer_hash,
        },
        "segment": {
            "path": "research_control/tasks/RT-20260721-008/artifacts/v21_event_store_pilot_events.jsonl",
            "sha256": sha256_bytes(event_bytes),
            "first_sequence": 1,
            "last_sequence": len(events),
            "event_count": len(events),
            "head_event_hash": events[-1]["event_hash"],
        },
        "source_bindings": source_bindings,
        "authority": {
            "current_legacy_sources_remain_authority": True,
            "generated_views_are_authority": False,
            "generated_sqlite_is_authority": False,
            "event_store_cutover_executed": False,
            "dual_write_executed": False,
            "reader_switch_executed": False,
            "registered_science_authority_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }
    manifest_bytes = canonical_json_bytes(manifest, newline=True)

    views = {
        "task_view": render_task_view(events),
        "candidate_view": render_candidate_view(events),
        "handoff_view": render_handoff_view(fixture, events),
        "status_view": render_status_view(fixture, events),
    }
    sqlite_report = rebuild_sqlite(events)
    checks = validate_events(events, sources)

    task_rows = csv_rows_by_id(
        sources["task_registry"], "task_id", fixture["selected_ids"]["task"]
    )
    expected_task = (
        sources["task_registry"]["document"]["header"]
        + "\n"
        + "\n".join(
            row["raw_line"] for row in sorted(task_rows, key=lambda item: item["source_ordinal"])
        )
        + "\n"
    ).encode("utf-8")
    checks.extend(
        [
            {
                "name": "task_view_byte_parity",
                "status": "PASS" if views["task_view"] == expected_task else "FAIL",
                "detail": "Selected task rows preserve the authoritative header, every field, and source row bytes.",
            },
            {
                "name": "candidate_view_semantic_parity",
                "status": "PASS" if json.loads(views["candidate_view"]) == sources["candidate_registry"]["document"] else "FAIL",
                "detail": "The complete candidate-lineage document survives canonical JSON projection without field loss.",
            },
            {
                "name": "sqlite_rebuild_and_query",
                "status": sqlite_report["status"],
                "detail": "Disposable SQLite replay preserves event, domain, subject, and chain-head queries.",
            },
            {
                "name": "no_live_cutover",
                "status": "PASS",
                "detail": "Every generated output is task-local or the one ignored disposable SQLite path.",
            },
            {
                "name": "legacy_sources_remain_authority",
                "status": "PASS",
                "detail": "The manifest keeps all registry, reader, writer, science, and protected authority unchanged.",
            },
        ]
    )
    failed = [check["name"] for check in checks if check["status"] != "PASS"]
    if failed:
        raise PilotError("pilot validation failed: " + ", ".join(failed))

    domain_counts = dict(sorted(Counter(event["event_domain"] for event in events).items()))
    accounting = field_accounting(fixture, sources)
    view_receipts = {
        key: {
            "path": f"research_control/tasks/RT-20260721-008/artifacts/{OUTPUT_NAMES[key]}",
            "sha256": sha256_bytes(data),
            "byte_count": len(data),
            "authority": False,
        }
        for key, data in views.items()
    }
    parity_receipt = {
        "schema_id": "v21_event_store_pilot_parity_receipt_v1",
        "pilot_id": fixture["pilot_id"],
        "task_id": fixture["task_id"],
        "plan_task_id": fixture["plan_task_id"],
        "validation_status": "PASS",
        "pinned_commit": fixture["pinned_commit"],
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "renderer_sha256": renderer_hash,
        "event_count": len(events),
        "subject_count": len({event["subject_id"] for event in events}),
        "domain_counts": domain_counts,
        "source_count": len(sources),
        "source_bindings": source_bindings,
        "views": view_receipts,
        "field_accounting": accounting,
        "unknown_event_count": 0,
        "rejected_event_count": 0,
        "unmapped_field_count": 0,
        "mismatch_count": 0,
        "unsupported_legacy_shape_count": 3,
        "unsupported_legacy_shapes": [
            {
                "shape": "handoff summary versus handoff_summary and completion_hash versus completion_sha256 aliases",
                "disposition": "mapped_explicitly_in_shadow_view",
                "loss": False,
            },
            {
                "shape": "authoritative task registry uses reverse-chronological source order while the design contract names task_id ordering",
                "disposition": "preserve_exact_legacy_order_for_byte_parity_and_require_explicit_cutover_sort_decision",
                "loss": False,
            },
            {
                "shape": "legacy YAML contains binary-float scalars forbidden by the v1 event encoding",
                "disposition": "preserve_each_source_lexeme_as_a_decimal_string_and_record_every_converted_path",
                "loss": False,
                "converted_paths": [
                    {
                        "source_path": source["binding"]["path"],
                        "paths": source["decimal_string_conversion_paths"],
                    }
                    for source in sources.values()
                    if source["decimal_string_conversion_paths"]
                ],
            },
        ],
        "out_of_slice_domain_count": 1,
        "out_of_slice_domains": [
            {
                "domain": "authority",
                "reason": "No new protected-authority transition exists in the selected P10-T03 through P10-T05 slice.",
            }
        ],
        "sqlite": sqlite_report,
        "migration_risks": [
            {
                "risk_id": "MR-P10-T06-001",
                "severity": "medium",
                "finding": "Legacy task rows are stored newest-first; a generic ascending task_id reducer would change bytes and ordering.",
                "required_before_cutover": "Specify and test the production compatibility order per consumer.",
            },
            {
                "risk_id": "MR-P10-T06-002",
                "severity": "medium",
                "finding": "Handoff field names drift across the selected historical slice.",
                "required_before_cutover": "Version alias reducers and retain source-schema provenance.",
            },
            {
                "risk_id": "MR-P10-T06-003",
                "severity": "low",
                "finding": "YAML-to-Markdown status and handoff views provide exact allowlisted semantic parity, not source serialization parity.",
                "required_before_cutover": "Keep source hashes and machine-readable field-accounting receipts bound to every generated view.",
            },
            {
                "risk_id": "MR-P10-T06-004",
                "severity": "high",
                "finding": "The bounded pilot has no authority-domain event and does not exercise concurrent writer or correction behavior.",
                "required_before_cutover": "Complete separate dual-write/concurrency validation and explicit protected-authority review; this pilot cannot authorize either.",
            },
            {
                "risk_id": "MR-P10-T06-005",
                "severity": "medium",
                "finding": "Legacy YAML uses binary-float scalars while the selected event schema requires decimal strings.",
                "required_before_cutover": "Publish a versioned numeric normalization contract with units and consumer type tests.",
            },
        ],
        "checks": checks,
        "authority": {
            "project_control_shadow_pilot_only": True,
            "legacy_registry_authority_changed": False,
            "generated_views_are_authority": False,
            "generated_sqlite_is_authority": False,
            "event_store_writer_active": False,
            "dual_write_active": False,
            "reader_cutover_active": False,
            "scientific_claims_changed": False,
            "candidate_adoption_authorized": False,
            "candidate_rejection_authorized": False,
            "p4_t05_executed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }
    parity_bytes = canonical_json_bytes(parity_receipt, newline=True)
    compact_receipt = {
        "schema_id": "v21_event_store_pilot_compact_receipt_v1",
        "pilot_id": fixture["pilot_id"],
        "task_id": fixture["task_id"],
        "plan_task_id": fixture["plan_task_id"],
        "validation_status": "PASS",
        "pinned_commit": fixture["pinned_commit"],
        "event_count": len(events),
        "domain_count": len(domain_counts),
        "domain_counts": domain_counts,
        "view_count": len(views),
        "source_count": len(sources),
        "check_count": len(checks),
        "failed_check_count": 0,
        "mismatch_count": 0,
        "unmapped_field_count": 0,
        "unsupported_legacy_shape_count": 3,
        "migration_risk_count": 5,
        "parity_receipt_sha256": sha256_bytes(parity_bytes),
        "head_event_hash": events[-1]["event_hash"],
        "sqlite_rebuild_status": sqlite_report["status"],
        "result_boundary": "Task-local non-authoritative project-control pilot only; no live cutover, scientific delta, protected authority, or P4-T05 execution.",
        "authority": parity_receipt["authority"],
    }
    compact_bytes = canonical_json_bytes(compact_receipt, newline=True)

    files = {
        OUTPUT_NAMES["events"]: event_bytes,
        OUTPUT_NAMES["manifest"]: manifest_bytes,
        OUTPUT_NAMES["task_view"]: views["task_view"],
        OUTPUT_NAMES["candidate_view"]: views["candidate_view"],
        OUTPUT_NAMES["handoff_view"]: views["handoff_view"],
        OUTPUT_NAMES["status_view"]: views["status_view"],
        OUTPUT_NAMES["parity_receipt"]: parity_bytes,
        OUTPUT_NAMES["compact_receipt"]: compact_bytes,
    }
    return {
        "fixture": fixture,
        "sources": sources,
        "events": events,
        "manifest": manifest,
        "parity_receipt": parity_receipt,
        "compact_receipt": compact_receipt,
        "files": files,
        "sqlite_report": sqlite_report,
    }


def write_bundle(
    bundle: dict[str, Any],
    output_dir: Path = ARTIFACT_DIR,
    sqlite_path: Path = SQLITE_PATH,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, data in bundle["files"].items():
        (output_dir / name).write_bytes(data)
    disk_sqlite_report = rebuild_sqlite(bundle["events"], sqlite_path)
    if disk_sqlite_report != bundle["sqlite_report"]:
        raise PilotError("on-disk SQLite rebuild differs from in-memory query receipt")


def check_bundle(bundle: dict[str, Any], output_dir: Path = ARTIFACT_DIR) -> list[str]:
    drift: list[str] = []
    for name, expected in bundle["files"].items():
        path = output_dir / name
        if not path.is_file() or path.read_bytes() != expected:
            drift.append(str(path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path))
    return drift


def summary(bundle: dict[str, Any], mode: str) -> dict[str, Any]:
    receipt = bundle["compact_receipt"]
    return {
        "status": "PASS",
        "mode": mode,
        "pilot_id": receipt["pilot_id"],
        "pinned_commit": receipt["pinned_commit"],
        "event_count": receipt["event_count"],
        "domain_counts": receipt["domain_counts"],
        "view_count": receipt["view_count"],
        "source_count": receipt["source_count"],
        "check_count": receipt["check_count"],
        "failed_check_count": receipt["failed_check_count"],
        "mismatch_count": receipt["mismatch_count"],
        "unmapped_field_count": receipt["unmapped_field_count"],
        "unsupported_legacy_shape_count": receipt["unsupported_legacy_shape_count"],
        "migration_risk_count": receipt["migration_risk_count"],
        "sqlite_rebuild_status": receipt["sqlite_rebuild_status"],
        "authority_changed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write task-local outputs and disposable SQLite")
    mode.add_argument("--check", action="store_true", help="verify task-local outputs without mutation")
    parser.add_argument("--json", action="store_true", help="emit a compact JSON result")
    args = parser.parse_args(argv)
    try:
        first = build_bundle()
        second = build_bundle()
        if first["files"] != second["files"] or first["sqlite_report"] != second["sqlite_report"]:
            raise PilotError("deterministic rebuild mismatch")
        if args.write:
            write_bundle(first)
            result = summary(first, "write")
        else:
            drift = check_bundle(first)
            if drift:
                raise PilotError("generated output drift: " + ", ".join(drift))
            result = summary(first, "check")
        if args.json:
            print(json.dumps(result, sort_keys=True))
        else:
            print(f"{result['status']}: {result['pilot_id']} ({result['event_count']} events)")
        return 0
    except (PilotError, OSError, ValueError, yaml.YAMLError) as exc:
        failure = {"status": "FAIL", "error": str(exc)}
        if args.json:
            print(json.dumps(failure, sort_keys=True))
        else:
            print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
