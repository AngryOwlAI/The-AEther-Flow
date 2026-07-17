#!/usr/bin/env python3
"""Render a deterministic research dependency graph from tracked control state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dependency_graph_model import (  # noqa: E402
    GraphInputSnapshot,
    GraphInstrumentation,
    load_graph_input_snapshot,
)


SCHEMA_ID = "research_dependency_graph_v1"
AUTHORITY_NOTICE = (
    "This generated dependency graph is navigational support only. It is not "
    "physics authority, proof authority, claim-promotion authority, or a "
    "substitute for registered sources, completions, handoffs, gates, or "
    "control registries."
)
DEFAULT_JSON_PATH = "output/research_dependency_graph.json"
DEFAULT_MARKDOWN_PATH = "wiki/indexes/research_dependency_graph.md"
DEFAULT_DOT_PATH = "output/research_dependency_graph.dot"

NODE_CLASSES = {
    "accepted_scoped_object",
    "agent_job",
    "artifact",
    "blocked_burden",
    "claim_boundary",
    "draft_control_candidate",
    "frozen_negative",
    "gate_chair_verdict",
    "handoff",
    "human_gated_object",
    "ledger_row",
    "obstruction",
    "source_extension_evidence_precondition",
    "source_ontology_object",
    "task",
}
STATE_LABELS = {
    "accepted_scoped",
    "blocked",
    "canonical_source",
    "draft_control",
    "frozen_negative",
    "human_gated",
    "proposal_only",
    "rejected",
    "science_draft",
    "source_extension_evidence",
    "support_only",
}
EDGE_CLASSES = {
    "accepts_as_evidence",
    "adopts_scoped",
    "audits",
    "blocks",
    "constructs",
    "depends_on",
    "forbids_overread",
    "freezes",
    "handoffs_to",
    "rejects",
    "requires",
    "requires_human_gate",
    "selects_next",
    "stress_tests",
    "updates_ledger",
}

REGISTRY_SPECS = {
    "DISTANCE_TO_GR_LEDGER.csv": "distance_to_gr_ledger",
    "AGENT_JOB_REGISTRY.csv": "agent_job_registry",
    "RESEARCH_TASK_REGISTRY.csv": "research_task_registry",
    "CLAIM_BOUNDARY_REGISTRY.csv": "claim_boundary_registry",
    "DIRECTOR_DECISION_REGISTRY.csv": "director_decision_registry",
    "ROLE_EXECUTION_REGISTRY.csv": "role_execution_registry",
    "TEX_SOURCE_REGISTRY.csv": "tex_source_registry",
    "MARKDOWN_SOURCE_REGISTRY.csv": "markdown_source_registry",
    "FILE_OBJECT_REGISTRY.csv": "file_object_registry",
}

BLOCKED_CLAIM_PATTERNS = {
    "canonical ontology edit": "canonical ontology edit",
    "source-law adoption": "source-law adoption",
    "MetricData(E) adoption": "MetricData(E) adoption",
    "MetricData adoption": "MetricData(E) adoption",
    "g_eff adoption": "g_eff adoption or scope expansion",
    "g_eff scope": "g_eff adoption or scope expansion",
    "coupling-law adoption": "coupling-law adoption",
    "matter-coupling derivation": "matter-coupling derivation",
    "matter coupling": "matter-coupling derivation",
    "matter-coupling adoption": "matter-coupling adoption",
    "stress-energy semantics": "stress-energy semantics",
    "stress-energy tensor": "stress-energy tensor",
    "matter action": "matter action",
    "detector semantics": "detector semantics",
    "Einstein equations": "Einstein equations",
    "Einstein-equation": "Einstein equations",
    "benchmark promotion": "benchmark promotion",
    "benchmark fit": "benchmark promotion",
    "completed derivation": "completed derivation",
    "completed-derivation": "completed derivation",
    "downstream GR promotion": "downstream GR promotion",
    "graph output as physics evidence": "graph output as physics evidence",
    "graph data as physics authority": "graph data as physics authority",
}

FRONTIER_BURDEN_LABELS = {
    "matter_coupling": "matter-coupling burden",
    "einstein_equations": "Einstein-equations burden",
    "benchmark_promotion": "benchmark-promotion burden",
    "finite_toy_metric_response": "finite toy metric response",
}

FRONTIER_COMPLETION_ALIASES = [
    {
        "label": "B_E^{rec}",
        "needles": ("B_E^{rec}", "B_E_rec", "recovery-bridge"),
        "node_class": "source_extension_evidence_precondition",
        "state_label": "source_extension_evidence",
    },
    {
        "label": "BridgeCert",
        "needles": ("BridgeCert", "bridge certificate", "recovery-bridge"),
        "node_class": "source_extension_evidence_precondition",
        "state_label": "source_extension_evidence",
    },
    {
        "label": "SEI-MC criteria",
        "needles": ("SEI-MC", "stress-energy-interface criteria", "SEI criteria"),
        "node_class": "draft_control_candidate",
        "state_label": "draft_control",
    },
    {
        "label": "SEI_src^{cand}",
        "needles": ("SEI_src^{cand}", "SEI_src", "stress-energy-interface candidate"),
        "node_class": "draft_control_candidate",
        "state_label": "draft_control",
    },
]

ROLE_EDGE = {
    "candidate-constructor": "constructs",
    "documentation-curator": "constructs",
    "gate-chair": "accepts_as_evidence",
    "memory-system-maintainer": "constructs",
    "ontology-formalizer": "constructs",
    "process-integrity-auditor": "audits",
    "project-control-maintainer": "constructs",
    "project-system-director": "selects_next",
    "refuter": "stress_tests",
    "smuggling-auditor": "audits",
    "theoretical-continuation-selector": "selects_next",
    "validator-engineer": "audits",
}


class GraphError(RuntimeError):
    """Raised when the extracted graph violates its schema contract."""


def repo_path(path_text: str) -> Path:
    return REPO_ROOT / path_text


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def string_value(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def collect_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(collect_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(collect_text(item) for item in value)
    return string_value(value)


def scoped_positive_label_text(label: Any) -> str:
    text = string_value(label)
    if not text:
        return ""
    normalized = text.replace("_", "-")
    upper = normalized.upper()
    if "EVIDENCE-ACCEPTED" in upper:
        subject = normalized[: upper.index("EVIDENCE-ACCEPTED")].strip("-")
        subject = subject.lower().replace("-", " ")
        return f"{subject} scoped evidence/precondition status"
    if "ACCEPTED" in upper:
        return re.sub(r"(?i)\baccepted\b", "scoped evidence/precondition", normalized)
    return normalized


def freeze_criteria_summary(freeze: dict[str, Any], task_or_job_id: str) -> str:
    decision = string_value(freeze.get("freeze_decision") or freeze.get("decision")) or "recorded"
    active = scoped_positive_label_text(freeze.get("active_freeze_label")) or "not specified"
    candidate = scoped_positive_label_text(freeze.get("candidate_freeze_label")) or "not specified"
    next_route = string_value(freeze.get("next_allowed_route")) or "not specified"
    attempts = freeze.get("prior_attempts_considered")
    attempt_count = len(attempts) if isinstance(attempts, list) else 0
    return (
        f"Freeze evaluation for {task_or_job_id}: decision {decision}; "
        f"active status {active}; candidate status {candidate}; "
        f"prior attempts considered {attempt_count}; next allowed route {next_route}. "
        "Scoped evidence/precondition labels are routing labels only and do not "
        "adopt a source law, coupling law, matter coupling, Einstein equations, "
        "benchmark status, or completed derivation."
    )


def normalize_token(text: str) -> str:
    text = text.strip().lower()
    replacements = {
        "^": "_",
        "{": "_",
        "}": "_",
        "(": "_",
        ")": "_",
        "[": "_",
        "]": "_",
        "+": "plus",
        "-": "_",
        "/": "_",
        ";": "_",
        ":": "_",
        ",": "_",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^a-z0-9_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "unnamed"


def object_node_id(name: str) -> str:
    return f"object:{normalize_token(name)}"


def artifact_node_id(path_or_id: str) -> str:
    if path_or_id.startswith(("MD-", "TEX-", "WIKI-", "PDF-", "HTML-")):
        return f"artifact:{path_or_id}"
    return f"artifact:{normalize_token(path_or_id)}"


def blocked_claim_node_id(label: str) -> str:
    return f"blocked_claim:{normalize_token(label)}"


def obstruction_node_id(obstruction_id: str) -> str:
    return f"obstruction:{normalize_token(obstruction_id)}"


def state_from_text(*values: Any, default: str = "support_only") -> str:
    text = " ".join(string_value(value) for value in values).lower()
    if "support-only" in text or "support only" in text or "checker proof authority" in text:
        return "support_only"
    if "frozen negative" in text or "route_frozen" in text or "route frozen" in text:
        return "frozen_negative"
    if "reject" in text:
        return "rejected"
    if "human-gated" in text or "human gated" in text or "human gate" in text or "gate chair" in text:
        return "human_gated"
    if "proposal-only" in text or "proposal only" in text:
        return "proposal_only"
    if "draft/control" in text or "draft control" in text:
        return "draft_control"
    if "source-extension evidence" in text or "evidence/precondition" in text:
        return "source_extension_evidence"
    if "source-extension" in text and "accepted" not in text and "adopted" not in text:
        return "source_extension_evidence"
    if ("accepted" in text or "adopted" in text) and (
        "scoped" in text or "downstream" in text or "source-extension" in text
    ):
        return "accepted_scoped"
    if "blocked" in text or "not started" in text or "missing primitive" in text:
        return "blocked"
    if "draft object exists" in text or "constructive witness exists" in text or "science draft" in text:
        return "science_draft"
    if "canonical" in text:
        return "canonical_source"
    return default


def class_from_state(state_label: str, *, source_kind: str = "") -> str:
    if state_label == "accepted_scoped":
        return "accepted_scoped_object"
    if state_label == "source_extension_evidence":
        return "source_extension_evidence_precondition"
    if state_label in {"draft_control", "proposal_only", "science_draft"}:
        return "draft_control_candidate"
    if state_label == "human_gated":
        return "human_gated_object"
    if state_label == "frozen_negative":
        return "frozen_negative"
    if state_label == "blocked":
        return "blocked_burden"
    if state_label == "canonical_source" or source_kind == "tex_ontology":
        return "source_ontology_object"
    if state_label == "rejected":
        return "obstruction"
    return "artifact"


def ledger_state_from_row(row: dict[str, str]) -> str:
    status = row.get("current_status", "").strip().lower()
    if status == "accepted":
        return "accepted_scoped"
    if status == "frozen negative":
        return "frozen_negative"
    if status in {"human-gated", "human gated"}:
        return "human_gated"
    if status == "not started" or status.startswith("blocked"):
        return "blocked"
    if "draft" in status or "constructive witness" in status or "stress passed" in status:
        return "science_draft"
    return state_from_text(collect_text(row), default="blocked")


def role_state(role_id: str) -> str:
    if role_id in {
        "candidate-constructor",
        "ontology-formalizer",
        "refuter",
        "smuggling-auditor",
        "theoretical-continuation-selector",
    }:
        return "science_draft"
    if role_id == "gate-chair":
        return "human_gated"
    return "support_only"


def edge_id(source_id: str, edge_class: str, target_id: str, source_field: str) -> str:
    seed = f"{source_id}|{edge_class}|{target_id}|{source_field}"
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    return f"edge:{normalize_token(source_id)}:{edge_class}:{normalize_token(target_id)}:{digest}"


class GraphBuilder:
    def __init__(self, snapshot: GraphInputSnapshot) -> None:
        self.snapshot = snapshot
        self.sources: dict[str, dict[str, str]] = {}
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: dict[str, dict[str, Any]] = {}
        self.warnings: list[str] = []
        self.timestamps: list[str] = []
        self.generated_at_hint = ""

    def add_source(
        self,
        path_text: str,
        source_kind: str,
        *,
        registry_object_id: str = "",
        source_hash: str = "",
    ) -> None:
        if not path_text:
            return
        if not source_hash:
            source_hash = self.snapshot.source_hash(path_text)
        if path_text in self.sources:
            if registry_object_id and not self.sources[path_text].get("registry_object_id"):
                self.sources[path_text]["registry_object_id"] = registry_object_id
            return
        self.sources[path_text] = {
            "path": path_text,
            "source_kind": source_kind,
            "source_hash": source_hash,
            "registry_object_id": registry_object_id,
        }

    def note_timestamps(self, value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key and (
                    str(key).endswith("_at")
                    or key in {"created_at", "updated_at", "completed_at"}
                ):
                    text = string_value(item)
                    if text:
                        self.timestamps.append(text)
                self.note_timestamps(item)
        elif isinstance(value, list):
            for item in value:
                self.note_timestamps(item)

    def add_node(
        self,
        node_id: str,
        node_class: str,
        label: str,
        state_label: str,
        source_path: str,
        source_registry: str,
        source_field: str,
        authority_status: str,
        summary: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if node_class not in NODE_CLASSES:
            raise GraphError(f"unknown node_class {node_class!r} for {node_id}")
        if state_label not in STATE_LABELS:
            raise GraphError(f"unknown state_label {state_label!r} for {node_id}")
        if not source_path:
            raise GraphError(f"node {node_id} lacks source_path")
        existing = self.nodes.get(node_id)
        if existing:
            refs = existing.setdefault("metadata", {}).setdefault("source_refs", [])
            ref = {"source_path": source_path, "source_field": source_field}
            if ref not in refs:
                refs.append(ref)
            if len(summary) > len(string_value(existing.get("summary"))):
                existing["summary"] = summary
            return
        self.add_source(source_path, source_registry, registry_object_id=metadata.get("registry_object_id", "") if metadata else "")
        self.nodes[node_id] = {
            "node_id": node_id,
            "node_class": node_class,
            "label": label,
            "state_label": state_label,
            "source_path": source_path,
            "source_registry": source_registry,
            "source_field": source_field,
            "authority_status": authority_status,
            "summary": summary,
            "metadata": metadata or {},
        }

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_class: str,
        source_path: str,
        source_field: str,
        summary: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if edge_class not in EDGE_CLASSES:
            raise GraphError(f"unknown edge_class {edge_class!r} for {source_id}->{target_id}")
        if not source_path or not source_field:
            raise GraphError(f"edge {source_id}->{target_id} lacks source_path or source_field")
        eid = edge_id(source_id, edge_class, target_id, source_field)
        self.add_source(source_path, "edge_source")
        self.edges[eid] = {
            "edge_id": eid,
            "source_id": source_id,
            "target_id": target_id,
            "edge_class": edge_class,
            "source_path": source_path,
            "source_field": source_field,
            "summary": summary,
            "metadata": metadata or {},
        }

    def add_artifact_node(
        self,
        path_or_id: str,
        source_path: str,
        source_field: str,
        *,
        label: str | None = None,
        state_label: str | None = None,
        authority_status: str = "generated_noncanonical",
        registry_object_id: str = "",
    ) -> str:
        node_id = artifact_node_id(registry_object_id or path_or_id)
        label = label or path_or_id
        if state_label is None:
            state_label = state_from_text(path_or_id, authority_status)
        if "scripts/" in path_or_id or path_or_id.startswith("tests/") or "checker" in path_or_id:
            state_label = "support_only"
        node_class = class_from_state(state_label)
        if node_class not in {"source_ontology_object", "draft_control_candidate"}:
            node_class = "artifact"
        self.add_node(
            node_id,
            node_class,
            label,
            state_label,
            source_path,
            source_path.rsplit("/", 1)[-1],
            source_field,
            authority_status,
            f"Tracked artifact reference: {label}",
            metadata={"registry_object_id": registry_object_id} if registry_object_id else {},
        )
        return node_id

    def add_blocked_claims_from_text(
        self,
        text: str,
        source_id: str,
        source_path: str,
        source_field: str,
        *,
        edge_class: str = "blocks",
    ) -> None:
        lower = text.lower()
        for phrase, label in BLOCKED_CLAIM_PATTERNS.items():
            if phrase.lower() not in lower:
                continue
            node_id = blocked_claim_node_id(label)
            self.add_node(
                node_id,
                "blocked_burden",
                f"Blocked claim: {label}",
                "blocked",
                source_path,
                source_path.rsplit("/", 1)[-1],
                source_field,
                "project_control",
                f"Blocked downstream overread claim: {label}.",
                metadata={"claim_label": label},
            )
            self.add_edge(
                source_id,
                node_id,
                edge_class,
                source_path,
                source_field,
                f"Source text blocks overread as {label}.",
            )

    def validate(self) -> None:
        errors: list[str] = []
        for node in self.nodes.values():
            if not node.get("source_path"):
                errors.append(f"node {node['node_id']} lacks source_path")
            if node.get("node_class") not in NODE_CLASSES:
                errors.append(f"node {node['node_id']} uses unknown node_class")
            if node.get("state_label") not in STATE_LABELS:
                errors.append(f"node {node['node_id']} uses unknown state_label")
        for edge in self.edges.values():
            if edge["source_id"] not in self.nodes:
                errors.append(f"edge {edge['edge_id']} has missing source node {edge['source_id']}")
            if edge["target_id"] not in self.nodes:
                errors.append(f"edge {edge['edge_id']} has missing target node {edge['target_id']}")
            if not edge.get("source_path") or not edge.get("source_field"):
                errors.append(f"edge {edge['edge_id']} lacks source_path/source_field")
            if edge.get("edge_class") not in EDGE_CLASSES:
                errors.append(f"edge {edge['edge_id']} uses unknown edge_class")
        if errors:
            raise GraphError("; ".join(errors[:20]))

    def graph(self) -> dict[str, Any]:
        self.validate()
        timestamp = self.generated_at_hint or (max(self.timestamps) if self.timestamps else "1970-01-01T00:00:00Z")
        sources = sorted(self.sources.values(), key=lambda item: item["path"])
        source_fingerprint = hashlib.sha256(
            "\n".join(f"{item['path']}={item['source_hash']}" for item in sources).encode("utf-8")
        ).hexdigest()
        return {
            "schema_id": SCHEMA_ID,
            "generated_at": timestamp,
            "authority_notice": AUTHORITY_NOTICE,
            "authority_boundary": {
                "navigational_support_only": True,
                "physics_claim_authority": False,
                "proof_authority": False,
                "source_authority_required": True,
                "generated_graph_can_promote_claims": False,
            },
            "source_fingerprint": source_fingerprint,
            "sources": sources,
            "nodes": sorted(self.nodes.values(), key=lambda item: item["node_id"]),
            "edges": sorted(
                self.edges.values(),
                key=lambda item: (
                    item["source_id"],
                    item["edge_class"],
                    item["target_id"],
                    item["edge_id"],
                ),
            ),
            "warnings": sorted(set(self.warnings)),
        }


def add_registry_sources(
    builder: GraphBuilder,
    snapshot: GraphInputSnapshot,
) -> dict[str, list[dict[str, str]]]:
    registries: dict[str, list[dict[str, str]]] = {}
    for name, source_kind in REGISTRY_SPECS.items():
        path_text = f"registries/{name}"
        builder.add_source(path_text, source_kind)
        rows = snapshot.csv_rows(path_text)
        builder.note_timestamps(rows)
        registries[name] = rows
    builder.add_source("research_control/program_state.yaml", "program_state")
    builder.note_timestamps(snapshot.yaml_payload("research_control/program_state.yaml"))
    return registries


def add_ledger(builder: GraphBuilder, rows: list[dict[str, str]]) -> None:
    source_path = "registries/DISTANCE_TO_GR_LEDGER.csv"
    for row in rows:
        burden_id = row.get("burden_id", "")
        if not burden_id:
            continue
        ledger_id = f"ledger:{burden_id}"
        ledger_text = collect_text(row)
        ledger_state = ledger_state_from_row(row)
        builder.add_node(
            ledger_id,
            "ledger_row",
            burden_id,
            ledger_state,
            source_path,
            "DISTANCE_TO_GR_LEDGER.csv",
            "burden_id",
            "project_control",
            row.get("notes") or row.get("current_status", ""),
            metadata={"milestone": row.get("milestone", ""), "required_object": row.get("required_object", "")},
        )
        required_object = row.get("required_object", "")
        if required_object:
            object_state = ledger_state
            object_class = class_from_state(object_state)
            object_id = object_node_id(required_object)
            builder.add_node(
                object_id,
                object_class,
                required_object,
                object_state,
                source_path,
                "DISTANCE_TO_GR_LEDGER.csv",
                "required_object",
                "project_control",
                row.get("blocking_burden") or row.get("notes") or row.get("current_status", ""),
                metadata={"burden_id": burden_id, "milestone": row.get("milestone", "")},
            )
            builder.add_edge(
                ledger_id,
                object_id,
                "requires",
                source_path,
                "required_object",
                f"Ledger burden {burden_id} names required object {required_object}.",
            )
            evidence_path = row.get("last_evidence_path", "")
            if evidence_path:
                artifact_id = builder.add_artifact_node(
                    evidence_path,
                    source_path,
                    "last_evidence_path",
                    label=evidence_path,
                    state_label="support_only" if evidence_path.startswith(("scripts/", "tests/")) else None,
                    authority_status="project_control",
                )
                builder.add_edge(
                    artifact_id,
                    ledger_id,
                    "updates_ledger",
                    source_path,
                    "last_evidence_path",
                    f"Ledger row {burden_id} cites latest evidence path.",
                )
        if burden_id in FRONTIER_BURDEN_LABELS:
            label = FRONTIER_BURDEN_LABELS[burden_id]
            if burden_id == "benchmark_promotion":
                alias_state = "human_gated"
                alias_class = "human_gated_object"
            elif burden_id == "finite_toy_metric_response":
                alias_state = "frozen_negative"
                alias_class = "frozen_negative"
            elif burden_id == "einstein_equations":
                alias_state = "blocked"
                alias_class = "blocked_burden"
            else:
                alias_state = ledger_state
                alias_class = "ledger_row"
            alias_id = object_node_id(label)
            builder.add_node(
                alias_id,
                alias_class,
                label,
                alias_state,
                source_path,
                "DISTANCE_TO_GR_LEDGER.csv",
                "burden_id",
                "project_control",
                row.get("notes") or row.get("blocking_burden", ""),
                metadata={"burden_id": burden_id, "frontier_alias": True},
            )
            builder.add_edge(
                alias_id,
                ledger_id,
                "depends_on",
                source_path,
                "burden_id",
                f"Frontier alias {label} summarizes ledger burden {burden_id}.",
            )
        if "freeze" in ledger_text.lower() or ledger_state == "frozen_negative":
            builder.add_edge(
                ledger_id,
                ledger_id,
                "freezes",
                source_path,
                "failure_or_freeze_criteria",
                f"Ledger row {burden_id} carries freeze criteria or a frozen status.",
            )
        if "human gate" in ledger_text.lower() or "gate chair" in ledger_text.lower():
            builder.add_edge(
                ledger_id,
                ledger_id,
                "requires_human_gate",
                source_path,
                "failure_or_freeze_criteria",
                f"Ledger row {burden_id} requires protected human-gated authority.",
            )
        builder.add_blocked_claims_from_text(
            ledger_text,
            ledger_id,
            source_path,
            "notes",
        )


def add_tasks(builder: GraphBuilder, rows: list[dict[str, str]]) -> None:
    source_path = "registries/RESEARCH_TASK_REGISTRY.csv"
    for row in rows:
        task_id = row.get("task_id", "")
        if not task_id:
            continue
        node_id = f"task:{task_id}"
        state = "human_gated" if row.get("requires_human_gate") == "true" else "support_only"
        if "physics" in row.get("task_type", "") or "candidate" in row.get("task_type", ""):
            state = "science_draft"
        builder.add_node(
            node_id,
            "task",
            task_id,
            state,
            source_path,
            "RESEARCH_TASK_REGISTRY.csv",
            "task_id",
            "project_control",
            row.get("notes") or row.get("closure_status", ""),
            metadata={"task_type": row.get("task_type", ""), "status": row.get("status", "")},
        )
        parent = row.get("parent_task_id", "")
        if parent:
            parent_id = f"task:{parent}"
            builder.add_node(
                parent_id,
                "task",
                parent,
                "support_only",
                source_path,
                "RESEARCH_TASK_REGISTRY.csv",
                "parent_task_id",
                "project_control",
                "Parent task referenced by registry row.",
            )
            builder.add_edge(
                parent_id,
                node_id,
                "handoffs_to",
                source_path,
                "parent_task_id",
                f"Task {task_id} continues from parent {parent}.",
            )
        current_job = row.get("current_job_id", "")
        if current_job:
            job_id = f"job:{current_job}"
            builder.add_node(
                job_id,
                "agent_job",
                current_job,
                "support_only",
                source_path,
                "RESEARCH_TASK_REGISTRY.csv",
                "current_job_id",
                "project_control",
                "AgentJob referenced by task registry before job registry enrichment.",
            )
            builder.add_edge(
                node_id,
                job_id,
                "depends_on",
                source_path,
                "current_job_id",
                f"Task {task_id} records current job {current_job}.",
            )


def add_jobs(builder: GraphBuilder, rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    source_path = "registries/AGENT_JOB_REGISTRY.csv"
    jobs_by_id: dict[str, dict[str, str]] = {}
    for row in rows:
        job_id = row.get("job_id", "")
        if not job_id:
            continue
        jobs_by_id[job_id] = row
        node_id = f"job:{job_id}"
        role_id = row.get("role_id", "")
        state = role_state(role_id)
        builder.add_node(
            node_id,
            "agent_job",
            job_id,
            state,
            source_path,
            "AGENT_JOB_REGISTRY.csv",
            "job_id",
            "project_control",
            row.get("notes") or row.get("status", ""),
            metadata={"role_id": role_id, "role_version": row.get("role_version", "")},
        )
        task_id = row.get("task_id", "")
        if task_id:
            task_node = f"task:{task_id}"
            builder.add_node(
                task_node,
                "task",
                task_id,
                state,
                source_path,
                "AGENT_JOB_REGISTRY.csv",
                "task_id",
                "project_control",
                f"Task referenced by AgentJob {job_id}.",
            )
            builder.add_edge(
                node_id,
                task_node,
                "depends_on",
                source_path,
                "task_id",
                f"AgentJob {job_id} is attached to task {task_id}.",
            )
        edge_class = ROLE_EDGE.get(role_id, "constructs")
        for output_path in split_semicolon(row.get("output_paths", "")):
            artifact_id = builder.add_artifact_node(
                output_path,
                source_path,
                "output_paths",
                authority_status="project_control",
            )
            builder.add_edge(
                node_id,
                artifact_id,
                edge_class,
                source_path,
                "output_paths",
                f"AgentJob {job_id} {edge_class} output artifact {output_path}.",
            )
    return jobs_by_id


def add_claim_boundaries(builder: GraphBuilder, rows: list[dict[str, str]]) -> None:
    source_path = "registries/CLAIM_BOUNDARY_REGISTRY.csv"
    for row in rows:
        boundary_id = row.get("claim_boundary_id", "")
        if not boundary_id:
            continue
        node_id = f"claim_boundary:{boundary_id}"
        builder.add_node(
            node_id,
            "claim_boundary",
            boundary_id,
            "support_only",
            source_path,
            "CLAIM_BOUNDARY_REGISTRY.csv",
            "claim_boundary_id",
            "project_control",
            row.get("notes") or "Claim boundary constraining interpretation.",
            metadata={"scope": row.get("scope", ""), "applies_to_path": row.get("applies_to_path", "")},
        )
        for claim in split_semicolon(row.get("forbidden_claims", "")):
            claim_id = blocked_claim_node_id(claim)
            builder.add_node(
                claim_id,
                "blocked_burden",
                f"Blocked claim: {claim}",
                "blocked",
                source_path,
                "CLAIM_BOUNDARY_REGISTRY.csv",
                "forbidden_claims",
                "project_control",
                f"Claim boundary {boundary_id} forbids this overread.",
                metadata={"claim_boundary_id": boundary_id},
            )
            builder.add_edge(
                node_id,
                claim_id,
                "forbids_overread",
                source_path,
                "forbidden_claims",
                f"Claim boundary {boundary_id} forbids overread claim: {claim}.",
            )
        for claim in split_semicolon(row.get("requires_gate_for", "")):
            claim_id = blocked_claim_node_id(claim)
            builder.add_node(
                claim_id,
                "human_gated_object",
                f"Human-gated claim: {claim}",
                "human_gated",
                source_path,
                "CLAIM_BOUNDARY_REGISTRY.csv",
                "requires_gate_for",
                "project_control",
                f"Claim boundary {boundary_id} requires human gate for this claim.",
                metadata={"claim_boundary_id": boundary_id},
            )
            builder.add_edge(
                node_id,
                claim_id,
                "requires_human_gate",
                source_path,
                "requires_gate_for",
                f"Claim boundary {boundary_id} requires a human gate for {claim}.",
            )


def add_decisions(builder: GraphBuilder, rows: list[dict[str, str]]) -> None:
    source_path = "registries/DIRECTOR_DECISION_REGISTRY.csv"
    for row in rows:
        decision_id = row.get("decision_id", "")
        if not decision_id:
            continue
        decision_node = builder.add_artifact_node(
            decision_id,
            source_path,
            "decision_id",
            label=decision_id,
            state_label="support_only",
            authority_status="project_control",
        )
        task_id = row.get("task_id", "")
        job_id = row.get("agent_job_id", "")
        if task_id:
            builder.add_node(
                f"task:{task_id}",
                "task",
                task_id,
                "support_only",
                source_path,
                "DIRECTOR_DECISION_REGISTRY.csv",
                "task_id",
                "project_control",
                f"Task selected by Director decision {decision_id}.",
            )
            builder.add_edge(
                decision_node,
                f"task:{task_id}",
                "selects_next",
                source_path,
                "task_id",
                f"Director decision {decision_id} selects task context {task_id}.",
            )
        if job_id:
            builder.add_node(
                f"job:{job_id}",
                "agent_job",
                job_id,
                role_state(row.get("selected_role_id", "")),
                source_path,
                "DIRECTOR_DECISION_REGISTRY.csv",
                "agent_job_id",
                "project_control",
                f"AgentJob selected by Director decision {decision_id}.",
            )
            builder.add_edge(
                decision_node,
                f"job:{job_id}",
                "selects_next",
                source_path,
                "agent_job_id",
                f"Director decision {decision_id} selects AgentJob {job_id}.",
            )


def add_role_executions(builder: GraphBuilder, rows: list[dict[str, str]]) -> None:
    source_path = "registries/ROLE_EXECUTION_REGISTRY.csv"
    for row in rows:
        job_id = row.get("agent_job_id", "")
        ref = row.get("execution_role_ref", "")
        if not job_id or not ref:
            continue
        job_node = f"job:{job_id}"
        builder.add_node(
            job_node,
            "agent_job",
            job_id,
            role_state(row.get("base_role_id", "")),
            source_path,
            "ROLE_EXECUTION_REGISTRY.csv",
            "agent_job_id",
            "project_control",
            f"AgentJob constrained by execution role {ref}.",
            metadata={"execution_role_ref": ref, "base_role_id": row.get("base_role_id", "")},
        )
        for removed in split_semicolon(row.get("removed_permissions", "")):
            claim_id = blocked_claim_node_id(removed)
            builder.add_node(
                claim_id,
                "blocked_burden",
                f"Blocked permission: {removed}",
                "blocked",
                source_path,
                "ROLE_EXECUTION_REGISTRY.csv",
                "removed_permissions",
                "project_control",
                f"Execution role {ref} removes this permission.",
            )
            builder.add_edge(
                job_node,
                claim_id,
                "forbids_overread",
                source_path,
                "removed_permissions",
                f"Execution role {ref} forbids permission/claim overread: {removed}.",
            )


def add_source_registry_artifacts(builder: GraphBuilder, rows: Iterable[dict[str, str]], registry_name: str) -> None:
    source_path = f"registries/{registry_name}"
    for row in rows:
        object_id = row.get("object_id", "")
        path_text = row.get("path", "")
        if not object_id or not path_text:
            continue
        authority = row.get("authority_status", "")
        source_kind = "tex_ontology" if registry_name == "TEX_SOURCE_REGISTRY.csv" else ""
        state = state_from_text(
            authority,
            row.get("claim_status", ""),
            row.get("research_status", ""),
            row.get("ontology_promotion_status", ""),
            default="support_only",
        )
        node_class = class_from_state(state, source_kind=source_kind)
        if registry_name == "MARKDOWN_SOURCE_REGISTRY.csv":
            node_class = "artifact"
        builder.add_node(
            artifact_node_id(object_id),
            node_class,
            object_id,
            state,
            source_path,
            registry_name,
            "object_id",
            authority or "project_control",
            row.get("notes") or path_text,
            metadata={"registry_object_id": object_id, "path": path_text},
        )


def completion_payload_edge_class(role_id: str, payload: dict[str, Any]) -> str:
    text = collect_text(payload).lower()
    if "stress" in text or role_id == "refuter":
        return "stress_tests"
    if "audit" in text or role_id == "smuggling-auditor":
        return "audits"
    if "select" in text or role_id == "theoretical-continuation-selector":
        return "selects_next"
    if role_id == "gate-chair":
        return "accepts_as_evidence"
    return ROLE_EDGE.get(role_id, "constructs")


def add_completion_payloads(
    builder: GraphBuilder,
    completion_path: str,
    completion: dict[str, Any],
    job_row: dict[str, str],
) -> None:
    job_id = job_row.get("job_id", "")
    task_id = job_row.get("task_id", "")
    role_id = job_row.get("role_id", "")
    source_id = f"job:{job_id}" if job_id else f"task:{task_id}"
    source_node_class = "agent_job" if job_id else "task"
    builder.add_node(
        source_id,
        source_node_class,
        job_id or task_id,
        role_state(role_id),
        completion_path,
        "completion_yaml",
        "job_id",
        "project_control",
        f"Completion source for {job_id or task_id}.",
        metadata={"role_id": role_id},
    )
    manifest = completion.get("mathematical_payload_manifest")
    if isinstance(manifest, list):
        for index, payload in enumerate(manifest):
            if not isinstance(payload, dict):
                continue
            object_name = string_value(payload.get("object_name")) or string_value(payload.get("payload_id"))
            if not object_name:
                continue
            payload_text = collect_text(payload)
            state = state_from_text(payload.get("claim_status"), payload_text, default=role_state(role_id))
            node_class = class_from_state(state)
            object_id = object_node_id(object_name)
            builder.add_node(
                object_id,
                node_class,
                object_name,
                state,
                completion_path,
                "completion_yaml",
                f"mathematical_payload_manifest[{index}].object_name",
                "project_control",
                string_value(payload.get("summary")) or payload_text[:240],
                metadata={
                    "payload_id": string_value(payload.get("payload_id")),
                    "payload_type": string_value(payload.get("payload_type")),
                    "burden_effect": string_value(payload.get("burden_effect")),
                },
            )
            edge_class = completion_payload_edge_class(role_id, payload)
            builder.add_edge(
                source_id,
                object_id,
                edge_class,
                completion_path,
                f"mathematical_payload_manifest[{index}].object_name",
                f"Completion payload {edge_class} {object_name}.",
            )
            if state == "accepted_scoped":
                builder.add_edge(
                    source_id,
                    object_id,
                    "adopts_scoped",
                    completion_path,
                    f"mathematical_payload_manifest[{index}].claim_status",
                    f"Completion records scoped acceptance for {object_name}.",
                )
            if state == "source_extension_evidence":
                builder.add_edge(
                    source_id,
                    object_id,
                    "accepts_as_evidence",
                    completion_path,
                    f"mathematical_payload_manifest[{index}].claim_status",
                    f"Completion records source-extension evidence for {object_name}.",
                )
            builder.add_blocked_claims_from_text(
                payload_text,
                object_id,
                completion_path,
                f"mathematical_payload_manifest[{index}]",
                edge_class="forbids_overread",
            )

    obstruction = completion.get("obstruction_record")
    if isinstance(obstruction, dict) and string_value(obstruction.get("obstruction_id")):
        obstruction_id_text = string_value(obstruction.get("obstruction_id"))
        node_id = obstruction_node_id(obstruction_id_text)
        builder.add_node(
            node_id,
            "obstruction",
            obstruction_id_text,
            "blocked",
            completion_path,
            "completion_yaml",
            "obstruction_record.obstruction_id",
            "project_control",
            string_value(obstruction.get("summary")) or collect_text(obstruction),
            metadata={"task_id": task_id, "job_id": job_id},
        )
        builder.add_edge(
            source_id,
            node_id,
            "blocks",
            completion_path,
            "obstruction_record",
            f"Completion records obstruction {obstruction_id_text}.",
        )

    freeze = completion.get("freeze_criteria_status")
    if isinstance(freeze, dict) and "freeze" in collect_text(freeze).lower():
        freeze_id = f"freeze:{normalize_token(task_id or job_id)}"
        builder.add_node(
            freeze_id,
            "frozen_negative",
            f"Freeze status for {task_id or job_id}",
            "frozen_negative",
            completion_path,
            "completion_yaml",
            "freeze_criteria_status",
            "project_control",
            freeze_criteria_summary(freeze, task_id or job_id),
            metadata={"task_id": task_id, "job_id": job_id},
        )
        builder.add_edge(
            source_id,
            freeze_id,
            "freezes",
            completion_path,
            "freeze_criteria_status",
            f"Completion records freeze criteria for {task_id or job_id}.",
        )

    decision = completion.get("theoretical_decision_output")
    if isinstance(decision, dict) and collect_text(decision):
        selected = (
            string_value(decision.get("selected_next_packet_type"))
            or string_value(decision.get("selected_packet_type_for_validator"))
            or string_value(decision.get("selected_next_role"))
            or string_value(decision.get("selected_next_role_family"))
            or f"theoretical decision {task_id}"
        )
        decision_node = object_node_id(selected)
        builder.add_node(
            decision_node,
            "draft_control_candidate",
            selected,
            "draft_control",
            completion_path,
            "completion_yaml",
            "theoretical_decision_output",
            "project_control",
            collect_text(decision)[:240],
            metadata={"task_id": task_id, "job_id": job_id},
        )
        builder.add_edge(
            source_id,
            decision_node,
            "selects_next",
            completion_path,
            "theoretical_decision_output",
            f"Completion selects next route {selected}.",
        )

    forbidden_text = collect_text(completion.get("forbidden_conclusion_summary"))
    if forbidden_text:
        builder.add_blocked_claims_from_text(
            forbidden_text,
            source_id,
            completion_path,
            "forbidden_conclusion_summary",
            edge_class="forbids_overread",
        )

    if role_id == "gate-chair":
        verdict_id = f"gate_verdict:{task_id}"
        builder.add_node(
            verdict_id,
            "gate_chair_verdict",
            f"Gate Chair verdict {task_id}",
            "human_gated",
            completion_path,
            "completion_yaml",
            "role_id",
            "human_gated",
            string_value(completion.get("verdict")) or collect_text(completion)[:240],
            metadata={"task_id": task_id, "job_id": job_id},
        )
        builder.add_edge(
            source_id,
            verdict_id,
            "accepts_as_evidence",
            completion_path,
            "role_id",
            f"Gate Chair job {job_id} emits a human-gated verdict record.",
        )
        builder.add_blocked_claims_from_text(
            collect_text(completion),
            verdict_id,
            completion_path,
            "forbidden_conclusion_summary",
            edge_class="forbids_overread",
        )

    completion_text = collect_text(completion)
    completion_lower = completion_text.lower()
    for alias in FRONTIER_COMPLETION_ALIASES:
        if not any(needle.lower() in completion_lower for needle in alias["needles"]):
            continue
        alias_id = object_node_id(alias["label"])
        builder.add_node(
            alias_id,
            alias["node_class"],
            alias["label"],
            alias["state_label"],
            completion_path,
            "completion_yaml",
            "completion_text",
            "project_control",
            f"Required frontier object exposed in completion text: {alias['label']}.",
            metadata={"task_id": task_id, "job_id": job_id, "frontier_alias": True},
        )
        builder.add_edge(
            source_id,
            alias_id,
            completion_payload_edge_class(role_id, {"summary": completion_text}),
            completion_path,
            "completion_text",
            f"Completion text exposes required frontier object {alias['label']}.",
        )


def add_completions(
    builder: GraphBuilder,
    jobs_by_id: dict[str, dict[str, str]],
    snapshot: GraphInputSnapshot,
) -> None:
    for job_id, row in sorted(jobs_by_id.items()):
        completion_path = row.get("completion_path", "")
        if not completion_path:
            continue
        completion = snapshot.yaml_payload(completion_path)
        if not completion:
            builder.warnings.append(f"Skipped unreadable or empty completion: {completion_path}")
            continue
        builder.add_source(completion_path, "completion_yaml")
        builder.note_timestamps(completion)
        add_completion_payloads(builder, completion_path, completion, row)


def add_handoffs(
    builder: GraphBuilder,
    snapshot: GraphInputSnapshot,
) -> dict[str, Any]:
    latest: dict[str, Any] = {}
    for path_text in snapshot.handoff_paths:
        data = snapshot.yaml_payload(path_text)
        if not data:
            builder.warnings.append(f"Skipped unreadable handoff: {path_text}")
            continue
        builder.add_source(path_text, "handoff_yaml")
        builder.note_timestamps(data)
        handoff_id = string_value(data.get("handoff_id")) or Path(path_text).stem
        node_id = f"handoff:{handoff_id}"
        builder.add_node(
            node_id,
            "handoff",
            handoff_id,
            "support_only",
            path_text,
            "handoff_yaml",
            "handoff_id",
            "project_control",
            string_value(data.get("summary")) or string_value(data.get("next_action")),
            metadata={"next_action": string_value(data.get("next_action"))},
        )
        task_id = string_value(data.get("task_id"))
        job_id = string_value(data.get("job_id"))
        if task_id:
            builder.add_node(
                f"task:{task_id}",
                "task",
                task_id,
                "support_only",
                path_text,
                "handoff_yaml",
                "task_id",
                "project_control",
                f"Handoff {handoff_id} references task {task_id}.",
            )
            builder.add_edge(
                node_id,
                f"task:{task_id}",
                "depends_on",
                path_text,
                "task_id",
                f"Handoff {handoff_id} depends on task {task_id}.",
            )
        if job_id:
            builder.add_node(
                f"job:{job_id}",
                "agent_job",
                job_id,
                "support_only",
                path_text,
                "handoff_yaml",
                "job_id",
                "project_control",
                f"Handoff {handoff_id} references job {job_id}.",
            )
            builder.add_edge(
                f"job:{job_id}",
                node_id,
                "handoffs_to",
                path_text,
                "job_id",
                f"AgentJob {job_id} emits handoff {handoff_id}.",
            )
        required_packet = data.get("required_next_packet")
        if isinstance(required_packet, dict) and collect_text(required_packet):
            route_label = string_value(required_packet.get("route_label")) or string_value(
                required_packet.get("task_type")
            )
            if route_label:
                route_node = object_node_id(route_label)
                builder.add_node(
                    route_node,
                    "artifact",
                    f"Next route: {route_label}",
                    "support_only",
                    path_text,
                    "handoff_yaml",
                    "required_next_packet.route_label",
                    "project_control",
                    collect_text(required_packet)[:240],
                    metadata={"handoff_id": handoff_id},
                )
                builder.add_edge(
                    node_id,
                    route_node,
                    "selects_next",
                    path_text,
                    "required_next_packet",
                    f"Handoff {handoff_id} selects next route {route_label}.",
                )
        latest = {
            "handoff_id": handoff_id,
            "path": path_text,
            "task_id": task_id,
            "job_id": job_id,
            "next_action": string_value(data.get("next_action")),
        }
        builder.generated_at_hint = string_value(data.get("created_at"))
    return latest


def build_graph(
    repo_root: Path = REPO_ROOT,
    *,
    snapshot: GraphInputSnapshot | None = None,
    instrumentation: GraphInstrumentation | None = None,
) -> dict[str, Any]:
    snapshot = snapshot or load_graph_input_snapshot(
        repo_root,
        registry_paths=(f"registries/{name}" for name in REGISTRY_SPECS),
        instrumentation=instrumentation,
    )
    if snapshot.repo_root != repo_root.resolve():
        raise GraphError(
            f"snapshot root {snapshot.repo_root} does not match requested root {repo_root.resolve()}"
        )
    if instrumentation is not None:
        instrumentation.record_graph_build()
    builder = GraphBuilder(snapshot)
    registries = add_registry_sources(builder, snapshot)
    add_ledger(builder, registries["DISTANCE_TO_GR_LEDGER.csv"])
    add_tasks(builder, registries["RESEARCH_TASK_REGISTRY.csv"])
    jobs_by_id = add_jobs(builder, registries["AGENT_JOB_REGISTRY.csv"])
    add_claim_boundaries(builder, registries["CLAIM_BOUNDARY_REGISTRY.csv"])
    add_decisions(builder, registries["DIRECTOR_DECISION_REGISTRY.csv"])
    add_role_executions(builder, registries["ROLE_EXECUTION_REGISTRY.csv"])
    add_source_registry_artifacts(builder, registries["TEX_SOURCE_REGISTRY.csv"], "TEX_SOURCE_REGISTRY.csv")
    add_source_registry_artifacts(
        builder,
        registries["MARKDOWN_SOURCE_REGISTRY.csv"],
        "MARKDOWN_SOURCE_REGISTRY.csv",
    )
    add_completions(builder, jobs_by_id, snapshot)
    latest_handoff = add_handoffs(builder, snapshot)
    graph = builder.graph()
    program_state = snapshot.yaml_payload("research_control/program_state.yaml")
    graph["route_continuity"] = {
        "program_state_path": "research_control/program_state.yaml",
        "active_task_id": string_value(program_state.get("active_task_id")),
        "latest_handoff": latest_handoff,
        "authority_note": AUTHORITY_NOTICE,
    }
    return graph


def markdown_escape(value: Any) -> str:
    return string_value(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(
    graph: dict[str, Any],
    instrumentation: GraphInstrumentation | None = None,
) -> str:
    if instrumentation is not None:
        instrumentation.record_render("markdown")
    nodes = graph["nodes"]
    edges = graph["edges"]
    source_counts = Counter(source["source_kind"] for source in graph["sources"])
    node_counts = Counter((node["node_class"], node["state_label"]) for node in nodes)
    lines = [
        "<!-- generated: research_dependency_graph -->",
        "<!-- authority: generated_noncanonical -->",
        "",
        "# Research Dependency Graph",
        "",
        f"Authority notice: {AUTHORITY_NOTICE}",
        "",
        f"- Schema: `{graph['schema_id']}`",
        f"- Generated from tracked state as of: `{graph['generated_at']}`",
        f"- Source fingerprint: `{graph['source_fingerprint']}`",
        f"- Nodes: `{len(nodes)}`",
        f"- Edges: `{len(edges)}`",
        "",
        "## Source Counts",
        "",
        "| Source kind | Count |",
        "| --- | ---: |",
    ]
    for source_kind, count in sorted(source_counts.items()):
        lines.append(f"| `{markdown_escape(source_kind)}` | {count} |")
    lines.extend(
        [
            "",
            "## Node Summary",
            "",
            "| Node class | State label | Count |",
            "| --- | --- | ---: |",
        ]
    )
    for (node_class, state_label), count in sorted(node_counts.items()):
        lines.append(f"| `{node_class}` | `{state_label}` | {count} |")

    labels = {
        "Resp_lc": "Resp_lc",
        "M_src": "M_src",
        "scoped g_eff": "g_eff",
        "B_E^{rec}": "B_E^{rec}",
        "BridgeCert": "BridgeCert",
        "SEI-MC criteria": "SEI-MC",
        "SEI_src^{cand}": "SEI_src",
        "matter-coupling burden": "matter-coupling burden",
        "Einstein-equations burden": "Einstein-equations burden",
        "benchmark-promotion burden": "benchmark-promotion burden",
        "finite toy metric response frozen negative": "finite toy metric response",
    }
    lines.extend(
        [
            "",
            "## Frontier Table",
            "",
            "| Required item | Node | Class | State | Summary |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for required_label, needle in labels.items():
        found = find_node_by_label(nodes, needle)
        if found:
            lines.append(
                "| "
                f"{markdown_escape(required_label)} | `{found['node_id']}` | "
                f"`{found['node_class']}` | `{found['state_label']}` | "
                f"{markdown_escape(found['summary'][:160])} |"
            )
        else:
            lines.append(f"| {markdown_escape(required_label)} | missing | missing | missing | missing |")

    blocked_nodes = [
        node
        for node in nodes
        if node["state_label"] == "blocked" and node["label"].lower().startswith("blocked")
    ]
    lines.extend(
        [
            "",
            "## Blocked Downstream Claims",
            "",
            "| Claim node | Summary | Source |",
            "| --- | --- | --- |",
        ]
    )
    for node in sorted(blocked_nodes, key=lambda item: item["node_id"])[:80]:
        lines.append(
            f"| `{node['node_id']}` | {markdown_escape(node['label'])} | `{markdown_escape(node['source_path'])}` |"
        )

    route = graph.get("route_continuity", {})
    latest = route.get("latest_handoff", {}) if isinstance(route, dict) else {}
    lines.extend(
        [
            "",
            "## Route Continuity",
            "",
            f"- Active task: `{markdown_escape(route.get('active_task_id', ''))}`",
            f"- Latest handoff: `{markdown_escape(latest.get('handoff_id', ''))}`",
            f"- Handoff path: `{markdown_escape(latest.get('path', ''))}`",
            f"- Next action: {markdown_escape(latest.get('next_action', ''))}",
            "",
            "This graph is navigational support only; inspect the cited sources before using any claim.",
            "",
        ]
    )
    return "\n".join(lines)


def find_node_by_label(nodes: list[dict[str, Any]], needle: str) -> dict[str, Any] | None:
    normalized = normalize_token(needle)
    exact = [node for node in nodes if normalize_token(node["label"]) == normalized]
    if exact:
        return sorted(exact, key=lambda node: node["node_id"])[0]
    partial = [node for node in nodes if normalized in normalize_token(node["label"])]
    if partial:
        return sorted(partial, key=lambda node: (node["state_label"], node["node_id"]))[0]
    return None


def dot_quote(value: Any) -> str:
    return json.dumps(string_value(value), ensure_ascii=False)


def render_dot(
    graph: dict[str, Any],
    instrumentation: GraphInstrumentation | None = None,
) -> str:
    if instrumentation is not None:
        instrumentation.record_render("dot")
    lines = [
        "digraph research_dependency_graph {",
        "  graph [label=\"navigational_support_only\", labelloc=\"t\"];",
        "  node [shape=box];",
    ]
    for node in graph["nodes"]:
        label = f"{node['label']}\\n{node['node_class']}\\n{node['state_label']}"
        lines.append(
            "  "
            f"{dot_quote(node['node_id'])} "
            f"[label={dot_quote(label)}, node_class={dot_quote(node['node_class'])}, "
            f"state_label={dot_quote(node['state_label'])}];"
        )
    for edge in graph["edges"]:
        lines.append(
            "  "
            f"{dot_quote(edge['source_id'])} -> {dot_quote(edge['target_id'])} "
            f"[label={dot_quote(edge['edge_class'])}, edge_class={dot_quote(edge['edge_class'])}];"
        )
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_json(
    graph: dict[str, Any],
    instrumentation: GraphInstrumentation | None = None,
) -> str:
    if instrumentation is not None:
        instrumentation.record_render("json")
    return json.dumps(graph, indent=2, sort_keys=True) + "\n"


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_text(path_text: str, text: str) -> None:
    path = repo_path(path_text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(
    path_text: str,
    graph: dict[str, Any],
    instrumentation: GraphInstrumentation | None = None,
) -> None:
    path = repo_path(path_text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_json(graph, instrumentation), encoding="utf-8")


def compare_expected_text(path_text: str, expected_text: str) -> dict[str, Any]:
    path = repo_path(path_text)
    expected_hash = text_sha256(expected_text)
    if not path.exists():
        return {
            "path": path_text,
            "status": "missing",
            "fresh": False,
            "expected_hash": expected_hash,
            "actual_hash": "",
        }
    actual_text = path.read_text(encoding="utf-8")
    actual_hash = text_sha256(actual_text)
    fresh = actual_text == expected_text
    return {
        "path": path_text,
        "status": "fresh" if fresh else "stale",
        "fresh": fresh,
        "expected_hash": expected_hash,
        "actual_hash": actual_hash,
    }


def check_graph_artifacts(
    *,
    json_path: str = DEFAULT_JSON_PATH,
    markdown_path: str = DEFAULT_MARKDOWN_PATH,
    dot_path: str = DEFAULT_DOT_PATH,
    instrumentation: GraphInstrumentation | None = None,
) -> dict[str, Any]:
    snapshot = load_graph_input_snapshot(
        REPO_ROOT,
        registry_paths=(f"registries/{name}" for name in REGISTRY_SPECS),
        instrumentation=instrumentation,
    )
    graph = build_graph(REPO_ROOT, snapshot=snapshot, instrumentation=instrumentation)
    artifact_checks = {
        "json": compare_expected_text(json_path, render_json(graph, instrumentation)),
        "markdown": compare_expected_text(markdown_path, render_markdown(graph, instrumentation)),
        "dot": compare_expected_text(dot_path, render_dot(graph, instrumentation)),
    }
    fresh = all(item["fresh"] for item in artifact_checks.values())
    return {
        "status": "PASS" if fresh else "FAIL",
        "fresh": fresh,
        "schema_id": graph["schema_id"],
        "generated_at": graph["generated_at"],
        "source_fingerprint": graph["source_fingerprint"],
        "node_count": len(graph["nodes"]),
        "edge_count": len(graph["edges"]),
        "artifacts": artifact_checks,
        "authority_notice": AUTHORITY_NOTICE,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", dest="json_path", help="Write JSON graph to this path.")
    parser.add_argument("--markdown", dest="markdown_path", help="Write Markdown summary to this path.")
    parser.add_argument("--dot", dest="dot_path", help="Write DOT graph to this path.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if generated graph artifacts are stale relative to tracked state.",
    )
    parser.add_argument("--stdout", action="store_true", help="Print JSON graph to stdout.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    instrumentation = GraphInstrumentation()
    if args.check:
        try:
            report = check_graph_artifacts(
                json_path=args.json_path or DEFAULT_JSON_PATH,
                markdown_path=args.markdown_path or DEFAULT_MARKDOWN_PATH,
                dot_path=args.dot_path or DEFAULT_DOT_PATH,
                instrumentation=instrumentation,
            )
        except GraphError as exc:
            print(f"dependency graph freshness check failed: {exc}", file=sys.stderr)
            return 1
        if args.stdout:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print(f"dependency graph freshness check: {report['status']}")
            for format_name, item in report["artifacts"].items():
                print(
                    f"- {format_name}: {item['status']} "
                    f"path={item['path']} actual={item['actual_hash']} expected={item['expected_hash']}"
                )
        return 0 if report["fresh"] else 1
    try:
        snapshot = load_graph_input_snapshot(
            REPO_ROOT,
            registry_paths=(f"registries/{name}" for name in REGISTRY_SPECS),
            instrumentation=instrumentation,
        )
        graph = build_graph(REPO_ROOT, snapshot=snapshot, instrumentation=instrumentation)
    except GraphError as exc:
        print(f"dependency graph extraction failed: {exc}", file=sys.stderr)
        return 1
    if args.json_path:
        write_json(args.json_path, graph, instrumentation)
    if args.markdown_path:
        write_text(args.markdown_path, render_markdown(graph, instrumentation))
    if args.dot_path:
        write_text(args.dot_path, render_dot(graph, instrumentation))
    if args.stdout or not (args.json_path or args.markdown_path or args.dot_path):
        print(render_json(graph, instrumentation), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
