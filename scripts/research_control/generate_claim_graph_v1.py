#!/usr/bin/env python3
"""Generate the v15 P12-T02 claim graph pilot from tracked source authority."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]

SCHEMA_ID = "claim_graph_schema_v1"
GRAPH_ID = "claim_graph_v1"
GENERATOR_NAME = "scripts/research_control/generate_claim_graph_v1.py"
GENERATOR_VERSION = "v1"

DEFAULT_JSON_PATH = "output/claim_graph_v1.json"
DEFAULT_DOT_PATH = "output/claim_graph_v1.dot"
DEFAULT_MARKDOWN_PATH = "wiki/indexes/claim_graph_v1.md"

LEDGER_PATH = "registries/DISTANCE_TO_GR_LEDGER.csv"
INVENTORY_PATH = "research_control/design/frontier_theorem_inventory.md"
SCHEMA_PATH = "research_control/design/claim_graph_schema_v1.md"
CURRENT_FRONTIER_PATH = "research_control/current_frontier.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v15.md"
TASK_PATH = "research_control/tasks/RT-20260703-024/00_TASK.yaml"
HANDOFF_SOURCE_PATH = "research_control/handoffs/handoff-0542.yaml"
NARROW_MS_GATE_PATH = (
    "research_control/tasks/RT-20260702-062/artifacts/"
    "narrow_ms_cert_eq_gate_chair_review_v1.tex"
)

MARKDOWN_REGISTRY = "registries/MARKDOWN_SOURCE_REGISTRY.csv"
TEX_REGISTRY = "registries/TEX_SOURCE_REGISTRY.csv"

NODE_TYPES = {
    "source_object",
    "source_extension_object",
    "evidence_precondition",
    "theorem_target",
    "theorem_candidate",
    "proved_theorem",
    "conditional_theorem",
    "obstruction",
    "frozen_route",
    "human_gated_decision",
    "blocked_physical_target",
    "generated_derivative",
    "validator_receipt",
}

EDGE_TYPES = {
    "supports",
    "depends_on",
    "blocks",
    "forbids_overread",
    "requires_certificate",
    "requires_human_gate",
    "supersedes",
    "is_derivative_of",
    "does_not_establish",
    "next_route",
}

PROMOTION_STATUSES = {
    "not_promoted",
    "none",
    "draft_control",
    "scoped_evidence_precondition",
    "scoped_source_object_only",
    "source_extension_data_only",
    "conditional_under_explicit_assumptions",
    "proved_under_declared_assumptions",
    "human_gated",
    "blocked",
    "frozen",
    "generated_only",
    "validator_receipt_only",
}

DOWNSTREAM_NON_CONCLUSIONS = [
    "source-law adoption",
    "RR_ETransportCompletenessOrInvarianceLaw_v1 adoption",
    "PositiveMSProfile_v1 adoption",
    "matter-semantics adoption",
    "detector-semantics adoption",
    "coupling-law adoption",
    "matter-coupling derivation or adoption",
    "stress-energy semantics",
    "matter action",
    "Einstein equations",
    "benchmark promotion",
    "completed derivation",
]


class ClaimGraphError(RuntimeError):
    """Raised when the generated graph violates the P12 schema contract."""


def repo_path(path_text: str) -> Path:
    return REPO_ROOT / path_text


def file_hash(path_text: str) -> str:
    path = repo_path(path_text)
    if not path.exists() or not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_text(path_text: str) -> str:
    path = repo_path(path_text)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_csv_rows(path_text: str) -> list[dict[str, str]]:
    path = repo_path(path_text)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def registry_rows_by_path(registry_path: str) -> dict[str, dict[str, str]]:
    return {
        row["path"]: row
        for row in read_csv_rows(registry_path)
        if row.get("path")
    }


def first_yaml_scalar(path_text: str, key: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:\s*\"?([^\"\n]+)\"?\s*$")
    for line in read_text(path_text).splitlines():
        match = pattern.match(line.strip())
        if match:
            return match.group(1).strip()
    return ""


def generated_at_hint() -> str:
    return (
        first_yaml_scalar(TASK_PATH, "created_at")
        or first_yaml_scalar(HANDOFF_SOURCE_PATH, "created_at")
        or "1970-01-01T00:00:00Z"
    )


def ledger_by_burden_id() -> dict[str, dict[str, str]]:
    return {
        row["burden_id"]: row
        for row in read_csv_rows(LEDGER_PATH)
        if row.get("burden_id")
    }


def parse_inventory_sections() -> dict[str, dict[str, Any]]:
    text = read_text(INVENTORY_PATH)
    sections: dict[str, dict[str, Any]] = {}
    current_id = ""
    current_start = 0
    current_lines: list[str] = []

    def flush() -> None:
        if current_id:
            sections[current_id] = {
                "frontier_item_id": current_id,
                "start_line": current_start,
                "body": "\n".join(current_lines).strip(),
            }

    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^### Item [^:]+:\s*(\S+)\s*$", line)
        if match:
            flush()
            current_id = match.group(1)
            current_start = line_number
            current_lines = [line]
        elif current_id:
            current_lines.append(line)
    flush()
    return sections


def extract_markdown_field(body: str, field: str) -> str:
    lines = body.splitlines()
    captured: list[str] = []
    capture = False
    field_prefix = f"- `{field}`:"
    for line in lines:
        if line.startswith("- `") and not line.startswith(field_prefix):
            if capture:
                break
        if line.startswith(field_prefix):
            capture = True
            captured.append(line.split(":", 1)[1].strip())
            continue
        if capture:
            captured.append(line.strip())
    return " ".join(part for part in captured if part).strip()


def clean_markdown_value(value: str) -> str:
    value = value.replace("`", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" ;")


def split_guards(value: str) -> list[str]:
    clean = clean_markdown_value(value)
    if not clean:
        return []
    parts = re.split(r";", clean)
    return [part.strip() for part in parts if part.strip()]


def item_status(section: dict[str, Any], key: str, fallback: str) -> str:
    body = str(section.get("body", ""))
    match = re.search(rf"- `{re.escape(key)}`:\s*`([^`]+)`", body)
    return clean_markdown_value(match.group(1)) if match else fallback


def source_artifacts(section: dict[str, Any]) -> list[str]:
    text = extract_markdown_field(str(section.get("body", "")), "source_artifact_path")
    return re.findall(r"research_control/[A-Za-z0-9_./-]+", text)


def authority_object_for_path(path_text: str, registry_path: str) -> str:
    return registry_rows_by_path(registry_path).get(path_text, {}).get("object_id", "")


def source_record(path_text: str) -> dict[str, str]:
    return {"path": path_text, "source_hash": file_hash(path_text)}


def guard_list(*values: str, extras: list[str] | None = None) -> list[str]:
    guards: list[str] = []
    for value in values:
        guards.extend(split_guards(value))
    if extras:
        guards.extend(extras)
    deduped: list[str] = []
    seen: set[str] = set()
    for guard in guards:
        if guard and guard not in seen:
            deduped.append(guard)
            seen.add(guard)
    return deduped


def node(
    *,
    node_id: str,
    node_type: str,
    label: str,
    status: str,
    authority_path: str,
    authority_registry: str,
    authority_object_id: str,
    promotion_status: str,
    overread_guards: list[str],
    metadata: dict[str, Any] | None = None,
    validator_receipt_only: bool = False,
    scientific_proof_authority: bool = False,
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "node_type": node_type,
        "label": label,
        "status": status,
        "authority_path": authority_path,
        "authority_registry": authority_registry,
        "authority_object_id": authority_object_id,
        "promotion_status": promotion_status,
        "overread_guards": overread_guards,
        "validator_receipt_only": validator_receipt_only,
        "scientific_proof_authority": scientific_proof_authority,
        "source_hash": file_hash(authority_path),
        "metadata": metadata or {},
    }


def edge(
    *,
    edge_id: str,
    edge_type: str,
    source_node_id: str,
    target_node_id: str,
    authority_path: str,
    authority_registry: str,
    authority_object_id: str,
    does_not_establish: list[str] | None = None,
    overread_guards: list[str] | None = None,
    requires_human_gate: bool = False,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "edge_id": edge_id,
        "edge_type": edge_type,
        "source_node_id": source_node_id,
        "target_node_id": target_node_id,
        "authority_path": authority_path,
        "authority_registry": authority_registry,
        "authority_object_id": authority_object_id,
        "does_not_establish": does_not_establish or [],
        "overread_guards": overread_guards or [],
        "requires_human_gate": requires_human_gate,
        "metadata": metadata or {},
    }


def ledger_node(
    ledger: dict[str, dict[str, str]],
    burden_id: str,
    *,
    node_id: str,
    node_type: str,
    label: str,
    status: str | None = None,
    promotion_status: str | None = None,
    extra_guards: list[str] | None = None,
) -> dict[str, Any]:
    row = ledger[burden_id]
    guards = guard_list(row.get("overread_guard", ""), extras=extra_guards)
    return node(
        node_id=node_id,
        node_type=node_type,
        label=label,
        status=status or row.get("control_status") or row.get("current_status") or "active",
        authority_path=LEDGER_PATH,
        authority_registry=LEDGER_PATH,
        authority_object_id=burden_id,
        promotion_status=promotion_status or row.get("promotion_status") or "not_promoted",
        overread_guards=guards,
        metadata={
            "ledger_burden_id": burden_id,
            "milestone": row.get("milestone", ""),
            "required_object": row.get("required_object", ""),
            "current_status": row.get("current_status", ""),
            "physical_status": row.get("physical_status", ""),
            "last_evidence_path": row.get("last_evidence_path", ""),
            "updated_at": row.get("updated_at", ""),
        },
    )


def inventory_node(
    sections: dict[str, dict[str, Any]],
    item_id: str,
    *,
    node_id: str,
    node_type: str,
    label: str,
    status: str | None = None,
    promotion_status: str | None = None,
    extra_guards: list[str] | None = None,
) -> dict[str, Any]:
    section = sections[item_id]
    body = str(section.get("body", ""))
    guards = guard_list(
        extract_markdown_field(body, "overread_guard"),
        extras=extra_guards,
    )
    return node(
        node_id=node_id,
        node_type=node_type,
        label=label,
        status=status or item_status(section, "control_status", "active"),
        authority_path=INVENTORY_PATH,
        authority_registry=MARKDOWN_REGISTRY,
        authority_object_id=item_id,
        promotion_status=promotion_status or item_status(section, "promotion_status", "not_promoted"),
        overread_guards=guards,
        metadata={
            "frontier_item_id": item_id,
            "frontier_start_line": section.get("start_line", 0),
            "source_artifact_paths": source_artifacts(section),
            "physical_status": item_status(section, "physical_status", ""),
            "mathematical_status": item_status(section, "mathematical_status", ""),
        },
    )


def build_nodes() -> list[dict[str, Any]]:
    ledger = ledger_by_burden_id()
    sections = parse_inventory_sections()
    required_ledger = {
        "resp_lc",
        "m_src",
        "g_eff",
        "matter_coupling",
        "einstein_equations",
        "benchmark_promotion",
    }
    required_inventory = {
        "positive_ms_profile_v1",
        "rr_e_transport_completeness_or_invariance_law_v1",
        "rr_e_separation_obstruction_witness_v1",
    }
    missing_ledger = sorted(required_ledger.difference(ledger))
    missing_inventory = sorted(required_inventory.difference(sections))
    if missing_ledger or missing_inventory:
        raise ClaimGraphError(
            "missing graph source items: "
            f"ledger={missing_ledger} inventory={missing_inventory}"
        )

    common_guard = [
        "Graph node is project-control metadata only.",
        "Graph node does not promote the cited source beyond its authority.",
    ]
    physical_target_guard = [
        "Physical target remains blocked unless a future protected source proves it.",
        "Graph visibility does not establish the target.",
    ]

    nodes = [
        ledger_node(
            ledger,
            "resp_lc",
            node_id="source-extension-resp-lc",
            node_type="source_extension_object",
            label="Resp_lc",
            extra_guards=common_guard,
        ),
        ledger_node(
            ledger,
            "m_src",
            node_id="source-object-m-src",
            node_type="source_object",
            label="M_src",
            extra_guards=common_guard,
        ),
        ledger_node(
            ledger,
            "g_eff",
            node_id="source-extension-g-eff",
            node_type="source_extension_object",
            label="g_eff",
            extra_guards=common_guard,
        ),
        ledger_node(
            ledger,
            "matter_coupling",
            node_id="blocked-target-matter-coupling",
            node_type="blocked_physical_target",
            label="matter_coupling",
            status="blocked",
            promotion_status="blocked",
            extra_guards=physical_target_guard,
        ),
        inventory_node(
            sections,
            "positive_ms_profile_v1",
            node_id="evidence-positive-ms-profile-v1",
            node_type="evidence_precondition",
            label="PositiveMSProfile_v1",
            promotion_status="scoped_evidence_precondition",
            extra_guards=common_guard,
        ),
        inventory_node(
            sections,
            "rr_e_transport_completeness_or_invariance_law_v1",
            node_id="evidence-rr-e-transport-completeness-or-invariance-law-v1",
            node_type="evidence_precondition",
            label="RR_ETransportCompletenessOrInvarianceLaw_v1",
            promotion_status="scoped_evidence_precondition",
            extra_guards=common_guard,
        ),
        inventory_node(
            sections,
            "rr_e_separation_obstruction_witness_v1",
            node_id="obstruction-rr-e-separation",
            node_type="obstruction",
            label="RR_E separation obstruction",
            status="obstruction_recorded",
            promotion_status="blocked",
            extra_guards=[
                "Scoped obstruction does not establish future source-extension impossibility.",
                "Scoped obstruction does not establish program-wide no-go.",
            ],
        ),
        ledger_node(
            ledger,
            "einstein_equations",
            node_id="blocked-target-einstein-equations",
            node_type="blocked_physical_target",
            label="Einstein equations",
            status="blocked",
            promotion_status="blocked",
            extra_guards=physical_target_guard,
        ),
        ledger_node(
            ledger,
            "benchmark_promotion",
            node_id="blocked-target-benchmark-promotion",
            node_type="blocked_physical_target",
            label="benchmark promotion",
            status="blocked",
            promotion_status="blocked",
            extra_guards=physical_target_guard,
        ),
        node(
            node_id="conditional-theorem-narrow-ms-cert-eq-v1",
            node_type="conditional_theorem",
            label="NarrowMSCertEq_v1",
            status="accepted_as_scoped_evidence_status",
            authority_path=NARROW_MS_GATE_PATH,
            authority_registry=TEX_REGISTRY,
            authority_object_id=authority_object_for_path(NARROW_MS_GATE_PATH, TEX_REGISTRY),
            promotion_status="scoped_evidence_precondition",
            overread_guards=guard_list(
                "no_source_law_adoption;no_matter_semantics_adoption;"
                "no_detector_semantics_adoption;no_coupling_law_adoption;"
                "no_matter_coupling_derivation;no_einstein_equations;"
                "no_benchmark_promotion;no_completed_derivation",
                extras=[
                    "Conditional theorem remains under explicit certificates.",
                    "Gate Chair evidence-status review is scoped evidence only.",
                ],
            ),
            metadata={
                "ledger_burden_id": "matter_coupling",
                "source_role": "P2 theorem output if present",
                "source_registry_object": authority_object_for_path(NARROW_MS_GATE_PATH, TEX_REGISTRY),
            },
        ),
    ]
    return sorted(nodes, key=lambda item: item["node_id"])


def guarded_edge(
    edge_id: str,
    edge_type: str,
    source_node_id: str,
    target_node_id: str,
    authority_object_id: str,
    note: str,
    *,
    authority_path: str = LEDGER_PATH,
    authority_registry: str = LEDGER_PATH,
    does_not_establish: list[str] | None = None,
    overread_guards: list[str] | None = None,
    requires_human_gate: bool = False,
) -> dict[str, Any]:
    return edge(
        edge_id=edge_id,
        edge_type=edge_type,
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        authority_path=authority_path,
        authority_registry=authority_registry,
        authority_object_id=authority_object_id,
        does_not_establish=does_not_establish,
        overread_guards=overread_guards,
        requires_human_gate=requires_human_gate,
        metadata={"pilot_relation_note": note},
    )


def build_edges() -> list[dict[str, Any]]:
    common_does_not_establish = [
        "matter-coupling derivation or adoption",
        "Einstein equations",
        "benchmark promotion",
        "completed derivation",
    ]
    support_guard = [
        "Support relation is scoped to source-side control status.",
        "Support relation is not physics promotion.",
    ]
    obstruction_guard = [
        "Same-milestone continuation remains open.",
        "The obstruction is not a program-wide no-go conclusion.",
    ]

    edges = [
        guarded_edge(
            "edge-resp-lc-supports-m-src",
            "supports",
            "source-extension-resp-lc",
            "source-object-m-src",
            "resp_lc",
            "Resp_lc may be cited only within scoped source-extension status.",
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-m-src-supports-g-eff",
            "supports",
            "source-object-m-src",
            "source-extension-g-eff",
            "m_src",
            "M_src is a scoped source object and does not expand g_eff scope.",
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-g-eff-does-not-establish-matter-coupling",
            "does_not_establish",
            "source-extension-g-eff",
            "blocked-target-matter-coupling",
            "g_eff",
            "Scoped g_eff is not matter coupling.",
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-positive-profile-does-not-establish-matter-coupling",
            "does_not_establish",
            "evidence-positive-ms-profile-v1",
            "blocked-target-matter-coupling",
            "positive_ms_profile_v1",
            "PositiveMSProfile_v1 is scoped evidence/precondition only.",
            authority_path=INVENTORY_PATH,
            authority_registry=MARKDOWN_REGISTRY,
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-rr-e-transport-does-not-establish-matter-coupling",
            "does_not_establish",
            "evidence-rr-e-transport-completeness-or-invariance-law-v1",
            "blocked-target-matter-coupling",
            "rr_e_transport_completeness_or_invariance_law_v1",
            "RR_E transport evidence is not source-law or matter-coupling adoption.",
            authority_path=INVENTORY_PATH,
            authority_registry=MARKDOWN_REGISTRY,
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-narrow-ms-cert-eq-does-not-establish-matter-coupling",
            "does_not_establish",
            "conditional-theorem-narrow-ms-cert-eq-v1",
            "blocked-target-matter-coupling",
            "TEX-V15-NARROW-MS-CERT-EQ-GATE-CHAIR-REVIEW",
            "NarrowMSCertEq_v1 is scoped evidence-status under explicit certificates.",
            authority_path=NARROW_MS_GATE_PATH,
            authority_registry=TEX_REGISTRY,
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-rr-e-separation-blocks-matter-coupling-overread",
            "blocks",
            "obstruction-rr-e-separation",
            "blocked-target-matter-coupling",
            "rr_e_separation_obstruction_witness_v1",
            "RR_E separation obstruction blocks unrestricted overread under current premises.",
            authority_path=INVENTORY_PATH,
            authority_registry=MARKDOWN_REGISTRY,
            does_not_establish=[
                "future source-extension impossibility",
                "program-wide no-go conclusion",
            ],
            overread_guards=obstruction_guard,
        ),
        guarded_edge(
            "edge-matter-coupling-depends-on-g-eff",
            "depends_on",
            "blocked-target-matter-coupling",
            "source-extension-g-eff",
            "matter_coupling",
            "Matter-coupling target depends on prior scoped source objects.",
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-matter-coupling-depends-on-positive-profile",
            "depends_on",
            "blocked-target-matter-coupling",
            "evidence-positive-ms-profile-v1",
            "matter_coupling",
            "Matter-coupling target depends on profile evidence as precondition only.",
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-matter-coupling-depends-on-rr-e-transport",
            "depends_on",
            "blocked-target-matter-coupling",
            "evidence-rr-e-transport-completeness-or-invariance-law-v1",
            "matter_coupling",
            "Matter-coupling target depends on RR_E transport evidence as precondition only.",
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-matter-coupling-depends-on-narrow-ms",
            "depends_on",
            "blocked-target-matter-coupling",
            "conditional-theorem-narrow-ms-cert-eq-v1",
            "matter_coupling",
            "Matter-coupling target depends on scoped P2 theorem output as precondition only.",
            does_not_establish=common_does_not_establish,
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-matter-coupling-does-not-establish-einstein-equations",
            "does_not_establish",
            "blocked-target-matter-coupling",
            "blocked-target-einstein-equations",
            "matter_coupling",
            "Current matter-coupling evidence is not an Einstein-equation premise.",
            does_not_establish=[
                "Einstein equations",
                "benchmark promotion",
                "completed derivation",
            ],
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-einstein-equations-depends-on-matter-coupling",
            "depends_on",
            "blocked-target-einstein-equations",
            "blocked-target-matter-coupling",
            "einstein_equations",
            "Einstein equations remain blocked by missing matter-coupling and dynamics burdens.",
            does_not_establish=[
                "Einstein equations",
                "benchmark promotion",
                "completed derivation",
            ],
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-einstein-equations-does-not-establish-benchmark-promotion",
            "does_not_establish",
            "blocked-target-einstein-equations",
            "blocked-target-benchmark-promotion",
            "einstein_equations",
            "No Einstein-equation derivation or benchmark promotion is established.",
            does_not_establish=[
                "benchmark promotion",
                "completed derivation",
            ],
            overread_guards=support_guard,
        ),
        guarded_edge(
            "edge-benchmark-promotion-requires-human-gate",
            "requires_human_gate",
            "blocked-target-benchmark-promotion",
            "blocked-target-einstein-equations",
            "benchmark_promotion",
            "Benchmark promotion remains human-gated after required derivation evidence.",
            does_not_establish=[
                "benchmark promotion",
                "completed derivation",
            ],
            overread_guards=[
                "Graph relation does not issue a Gate Chair or benchmark verdict.",
            ],
            requires_human_gate=True,
        ),
    ]
    return sorted(edges, key=lambda item: item["edge_id"])


def validate_graph(graph: dict[str, Any]) -> None:
    errors: list[str] = []
    required_envelope = {
        "claim_graph_schema_id",
        "graph_id",
        "generated_at",
        "generator",
        "source_authority",
        "nodes",
        "edges",
        "validation",
        "claim_boundary",
    }
    missing_envelope = required_envelope.difference(graph)
    if missing_envelope:
        errors.append(f"missing envelope fields: {sorted(missing_envelope)}")

    node_ids: set[str] = set()
    for item in graph.get("nodes", []):
        for field in (
            "node_id",
            "node_type",
            "label",
            "status",
            "authority_path",
            "authority_registry",
            "authority_object_id",
            "promotion_status",
            "overread_guards",
            "validator_receipt_only",
            "scientific_proof_authority",
            "source_hash",
            "metadata",
        ):
            if field not in item:
                errors.append(f"node lacks field {field}: {item.get('node_id', '<unknown>')}")
        if item.get("node_id") in node_ids:
            errors.append(f"duplicate node id: {item.get('node_id')}")
        node_ids.add(item.get("node_id", ""))
        if item.get("node_type") not in NODE_TYPES:
            errors.append(f"unknown node_type: {item.get('node_type')}")
        if item.get("promotion_status") not in PROMOTION_STATUSES:
            errors.append(f"unknown promotion_status: {item.get('promotion_status')}")
        if item.get("validator_receipt_only") and item.get("scientific_proof_authority"):
            errors.append(f"validator receipt claims proof authority: {item.get('node_id')}")
        if item.get("node_type") in {
            "source_object",
            "source_extension_object",
            "evidence_precondition",
            "conditional_theorem",
        } and not item.get("overread_guards"):
            errors.append(f"support-like node lacks overread guards: {item.get('node_id')}")

    edge_ids: set[str] = set()
    for item in graph.get("edges", []):
        for field in (
            "edge_id",
            "edge_type",
            "source_node_id",
            "target_node_id",
            "authority_path",
            "authority_registry",
            "authority_object_id",
            "does_not_establish",
            "overread_guards",
            "requires_human_gate",
            "metadata",
        ):
            if field not in item:
                errors.append(f"edge lacks field {field}: {item.get('edge_id', '<unknown>')}")
        if item.get("edge_id") in edge_ids:
            errors.append(f"duplicate edge id: {item.get('edge_id')}")
        edge_ids.add(item.get("edge_id", ""))
        if item.get("edge_type") not in EDGE_TYPES:
            errors.append(f"unknown edge_type: {item.get('edge_type')}")
        if item.get("source_node_id") not in node_ids:
            errors.append(f"edge has unknown source node: {item.get('edge_id')}")
        if item.get("target_node_id") not in node_ids:
            errors.append(f"edge has unknown target node: {item.get('edge_id')}")
        if item.get("edge_type") in {"supports", "depends_on", "does_not_establish"}:
            if not item.get("does_not_establish"):
                errors.append(f"guarded edge lacks does_not_establish: {item.get('edge_id')}")
        if item.get("edge_type") == "requires_human_gate" and not item.get("requires_human_gate"):
            errors.append(f"human-gate edge lacks requires_human_gate=true: {item.get('edge_id')}")

    boundary = graph.get("claim_boundary", {})
    if boundary.get("graph_is_proof_authority") is not False:
        errors.append("claim_boundary.graph_is_proof_authority must be false")
    if boundary.get("graph_changes_scientific_claims") is not False:
        errors.append("claim_boundary.graph_changes_scientific_claims must be false")
    if boundary.get("graph_promotes_status") is not False:
        errors.append("claim_boundary.graph_promotes_status must be false")

    if errors:
        raise ClaimGraphError("; ".join(errors[:20]))


def build_claim_graph(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    global REPO_ROOT
    previous_root = REPO_ROOT
    REPO_ROOT = repo_root
    try:
        nodes = build_nodes()
        edges = build_edges()
        sources = [
            source_record(LEDGER_PATH),
            source_record(INVENTORY_PATH),
            source_record(SCHEMA_PATH),
            source_record(CURRENT_FRONTIER_PATH),
            source_record(PLAN_PATH),
        ]
        graph = {
            "claim_graph_schema_id": SCHEMA_ID,
            "graph_id": GRAPH_ID,
            "generated_at": generated_at_hint(),
            "generator": {
                "name": GENERATOR_NAME,
                "version": GENERATOR_VERSION,
            },
            "source_authority": {
                "canonical_sources": [source["path"] for source in sources],
                "source_hashes": sources,
                "derivative_sources_allowed": False,
            },
            "outputs": {
                "json": DEFAULT_JSON_PATH,
                "dot": DEFAULT_DOT_PATH,
                "markdown": DEFAULT_MARKDOWN_PATH,
            },
            "nodes": nodes,
            "edges": edges,
            "validation": {
                "validator_name": GENERATOR_NAME,
                "validator_version": GENERATOR_VERSION,
                "status": "PASS",
            },
            "claim_boundary": {
                "graph_is_proof_authority": False,
                "graph_changes_scientific_claims": False,
                "graph_promotes_status": False,
                "no_physics_delta": True,
                "forbidden_conclusions": DOWNSTREAM_NON_CONCLUSIONS,
            },
        }
        validate_graph(graph)
        return graph
    finally:
        REPO_ROOT = previous_root


def dot_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def render_dot(graph: dict[str, Any]) -> str:
    lines = [
        "digraph claim_graph_v1 {",
        '  graph [label="claim_graph_v1: project-control metadata only", labelloc=t];',
        "  rankdir=LR;",
        '  node [shape=box, style="rounded"];',
    ]
    for item in graph["nodes"]:
        label = f"{item['label']}\\n{item['node_type']}\\n{item['promotion_status']}"
        lines.append(f'  "{dot_escape(item["node_id"])}" [label="{dot_escape(label)}"];')
    for item in graph["edges"]:
        edge_label = item["edge_type"]
        if item.get("does_not_establish"):
            edge_label += "\\nnon-establishing"
        if item.get("requires_human_gate"):
            edge_label += "\\nhuman-gated"
        lines.append(
            f'  "{dot_escape(item["source_node_id"])}" -> '
            f'"{dot_escape(item["target_node_id"])}" '
            f'[label="{dot_escape(edge_label)}"];'
        )
    lines.append("}")
    return "\n".join(lines) + "\n"


def render_markdown(graph: dict[str, Any]) -> str:
    labels = {item["node_id"]: item["label"] for item in graph["nodes"]}
    lines = [
        "<!-- generated: claim_graph_v1; authority: derivative -->",
        "",
        "# Claim Graph v1",
        "",
        "This index is generated project-control metadata. It is not proof authority, "
        "not physics source authority, and not authority to promote any claim.",
        "",
        f"- Schema: `{graph['claim_graph_schema_id']}`",
        f"- Generated from tracked state as of: `{graph['generated_at']}`",
        f"- Nodes: `{len(graph['nodes'])}`",
        f"- Edges: `{len(graph['edges'])}`",
        "- Claim boundary: `no physics delta; no promotion; no proof authority`",
        "",
        "## Required Pilot Nodes",
        "",
        "| Label | Type | Status | Promotion status | Authority |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in graph["nodes"]:
        lines.append(
            f"| `{item['label']}` | `{item['node_type']}` | `{item['status']}` | "
            f"`{item['promotion_status']}` | `{item['authority_path']}` |"
        )

    lines.extend(
        [
            "",
            "## High-Risk Non-Establishment Edges",
            "",
            "| Source | Relation | Target | Does not establish |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in graph["edges"]:
        if item["edge_type"] in {"does_not_establish", "blocks", "requires_human_gate"}:
            does_not = "; ".join(item["does_not_establish"]) or "stronger downstream claim"
            lines.append(
                f"| `{labels[item['source_node_id']]}` | `{item['edge_type']}` | "
                f"`{labels[item['target_node_id']]}` | {does_not} |"
            )

    lines.extend(
        [
            "",
            "## Source Materials",
            "",
            "The AEther-Flow Research Project. (2026a). *Distance-to-GR ledger* "
            "[Research-control registry]. `registries/DISTANCE_TO_GR_LEDGER.csv`.",
            "",
            "The AEther-Flow Research Project. (2026b). *Frontier theorem inventory* "
            "[Internal control inventory]. "
            "`research_control/design/frontier_theorem_inventory.md`.",
            "",
            "The AEther-Flow Research Project. (2026c). *Claim graph schema v1* "
            "[Project-control schema]. `research_control/design/claim_graph_schema_v1.md`.",
            "",
            "The AEther-Flow Research Project. (2026d). *Recommendations "
            "implementation plan continue task v15* [Implementation plan]. "
            "`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_if_changed(path_text: str, content: str) -> None:
    path = repo_path(path_text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def compare_existing(path_text: str, expected: str) -> str:
    path = repo_path(path_text)
    if not path.exists():
        return f"missing: {path_text}"
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        return f"stale: {path_text}"
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path", default=DEFAULT_JSON_PATH)
    parser.add_argument("--dot", dest="dot_path", default=DEFAULT_DOT_PATH)
    parser.add_argument("--markdown", dest="markdown_path", default=DEFAULT_MARKDOWN_PATH)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    graph = build_claim_graph(REPO_ROOT)
    json_text = json.dumps(graph, indent=2, sort_keys=True) + "\n"
    dot_text = render_dot(graph)
    markdown_text = render_markdown(graph)

    if args.check:
        failures = [
            failure
            for failure in (
                compare_existing(args.json_path, json_text),
                compare_existing(args.dot_path, dot_text),
                compare_existing(args.markdown_path, markdown_text),
            )
            if failure
        ]
        if failures:
            print("\n".join(failures), file=sys.stderr)
            return 1
        print("claim graph outputs are fresh")
        return 0

    write_if_changed(args.json_path, json_text)
    write_if_changed(args.dot_path, dot_text)
    write_if_changed(args.markdown_path, markdown_text)
    print(json.dumps({"status": "PASS", "graph_id": GRAPH_ID, "nodes": len(graph["nodes"]), "edges": len(graph["edges"])}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
