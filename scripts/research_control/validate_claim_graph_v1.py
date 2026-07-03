#!/usr/bin/env python3
"""Validate claim_graph_v1 against the v15 P12-T03 guard rules.

The validator is project-control evidence only. A PASS confirms that the graph
keeps the declared non-promotion and derivative-authority boundaries visible;
it does not establish any physics claim.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_GRAPH_PATH = "output/claim_graph_v1.json"
REPORT_SCHEMA_ID = "claim_graph_validation_report_v1"
VALIDATOR_NAME = "scripts/research_control/validate_claim_graph_v1.py"
VALIDATOR_VERSION = "v1"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    from generate_claim_graph_v1 import EDGE_TYPES, NODE_TYPES, PROMOTION_STATUSES
except Exception:  # pragma: no cover - defensive fallback for direct reuse.
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


REQUIRED_ENVELOPE_FIELDS = {
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
REQUIRED_NODE_FIELDS = {
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
}
REQUIRED_EDGE_FIELDS = {
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
}

HIGH_RISK_NODE_TYPES = {
    "source_object",
    "source_extension_object",
    "evidence_precondition",
    "theorem_candidate",
    "proved_theorem",
    "conditional_theorem",
}
NON_POSITIVE_NODE_TYPES = {
    "blocked_physical_target",
    "obstruction",
    "frozen_route",
    "generated_derivative",
    "validator_receipt",
}
BLOCKING_EDGE_TYPES = {
    "does_not_establish",
    "forbids_overread",
    "blocks",
    "requires_human_gate",
}
NEGATIVE_EDGE_TYPES = {
    "does_not_establish",
    "forbids_overread",
    "blocks",
}
SCOPED_EVIDENCE_PROMOTIONS = {
    "scoped_evidence_precondition",
    "scoped_source_object_only",
    "source_extension_data_only",
    "conditional_under_explicit_assumptions",
}
DOWNSTREAM_PHYSICAL_TERMS = {
    "matter coupling",
    "matter coupling derivation",
    "matter coupling adoption",
    "einstein equations",
    "benchmark promotion",
    "completed derivation",
}
REQUIRED_COMPLETED_DERIVATION_INTERMEDIATES = (
    "matter coupling",
    "einstein equations",
    "benchmark promotion",
)
DERIVATIVE_PREFIXES = ("wiki/", "output/", ".local/")
GATE_CHAIR_ALLOWED_REGISTRIES = {
    "registries/TEX_SOURCE_REGISTRY.csv",
    "registries/AGENT_JOB_REGISTRY.csv",
    "registries/DIRECTOR_DECISION_REGISTRY.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def flattened_text(value: Any) -> str:
    parts: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            parts.append(str(key))
            parts.append(flattened_text(item))
    elif isinstance(value, list):
        for item in value:
            parts.append(flattened_text(item))
    elif value is not None:
        parts.append(str(value))
    return " ".join(part for part in parts if part)


def text_contains_term(text: str, term: str) -> bool:
    return normalize(term) in normalize(text)


def references_any(text: str, terms: set[str] | tuple[str, ...]) -> bool:
    normalized = normalize(text)
    return any(normalize(term) in normalized for term in terms)


def add_error(
    errors: list[dict[str, Any]],
    code: str,
    message: str,
    **context: Any,
) -> None:
    entry: dict[str, Any] = {"code": code, "message": message}
    entry.update({key: value for key, value in context.items() if value not in (None, "", [])})
    errors.append(entry)


def load_graph(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    if not path.exists():
        add_error(errors, "graph_file_missing", "Claim graph JSON file is missing.", graph_path=str(path))
        return {}, errors
    try:
        return json.loads(path.read_text(encoding="utf-8")), errors
    except json.JSONDecodeError as exc:
        add_error(
            errors,
            "graph_json_parse_error",
            "Claim graph JSON could not be parsed.",
            graph_path=str(path),
            line=exc.lineno,
            column=exc.colno,
        )
        return {}, errors


def node_text(node: dict[str, Any]) -> str:
    return flattened_text(
        {
            "node_id": node.get("node_id", ""),
            "node_type": node.get("node_type", ""),
            "label": node.get("label", ""),
            "status": node.get("status", ""),
            "authority_path": node.get("authority_path", ""),
            "authority_registry": node.get("authority_registry", ""),
            "authority_object_id": node.get("authority_object_id", ""),
            "promotion_status": node.get("promotion_status", ""),
            "overread_guards": node.get("overread_guards", []),
            "metadata": node.get("metadata", {}),
        }
    )


def edge_text(edge: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]) -> str:
    source = nodes_by_id.get(str(edge.get("source_node_id", "")), {})
    target = nodes_by_id.get(str(edge.get("target_node_id", "")), {})
    return flattened_text(
        {
            "edge": edge,
            "source_label": source.get("label", ""),
            "source_type": source.get("node_type", ""),
            "target_label": target.get("label", ""),
            "target_type": target.get("node_type", ""),
        }
    )


def build_indexes(graph: dict[str, Any]) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
]:
    nodes_by_id = {
        str(node.get("node_id")): node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("node_id")
    }
    outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
    incoming: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        outgoing[str(edge.get("source_node_id", ""))].append(edge)
        incoming[str(edge.get("target_node_id", ""))].append(edge)
    return nodes_by_id, outgoing, incoming


def is_high_risk_positive_node(node: dict[str, Any]) -> bool:
    node_type = str(node.get("node_type", ""))
    if node_type in NON_POSITIVE_NODE_TYPES:
        return False
    promotion_status = normalize(node.get("promotion_status", ""))
    status = normalize(node.get("status", ""))
    if "blocked" in promotion_status or "frozen" in promotion_status:
        return False
    if "obstruction" in status:
        return False
    if node_type in HIGH_RISK_NODE_TYPES:
        return True
    text = node_text(node)
    return references_any(
        text,
        {
            "M_src",
            "g_eff",
            "Resp_lc",
            "PositiveMSProfile_v1",
            "RR_ETransportCompletenessOrInvarianceLaw_v1",
            "NarrowMSCertEq_v1",
            "matter coupling",
            "Einstein equations",
            "benchmark promotion",
        },
    )


def is_accepted_evidence_precondition(node: dict[str, Any]) -> bool:
    if node.get("node_type") == "evidence_precondition":
        return True
    status = normalize(node.get("status", ""))
    promotion_status = str(node.get("promotion_status", ""))
    return (
        "accepted as scoped evidence" in status
        or "accepted scoped evidence" in status
        or promotion_status == "scoped_evidence_precondition"
    )


def is_gate_chair_node(node: dict[str, Any]) -> bool:
    raw = flattened_text(
        {
            "node_id": node.get("node_id", ""),
            "node_type": node.get("node_type", ""),
            "label": node.get("label", ""),
            "status": node.get("status", ""),
            "authority_path": node.get("authority_path", ""),
        }
    ).lower()
    return (
        node.get("node_type") == "human_gated_decision"
        or "gate chair" in raw
        or "gate_chair" in raw
    )


def is_completed_derivation_node(node: dict[str, Any]) -> bool:
    return references_any(
        flattened_text(
            {
                "node_id": node.get("node_id", ""),
                "label": node.get("label", ""),
                "status": node.get("status", ""),
                "node_type": node.get("node_type", ""),
            }
        ),
        {"completed derivation", "completed_derivation"},
    )


def is_scoped_evidence_node(node: dict[str, Any]) -> bool:
    if node.get("promotion_status") in SCOPED_EVIDENCE_PROMOTIONS:
        return True
    return references_any(normalize(node.get("status", "")), {"scoped evidence", "scoped source"})


def validate_schema(
    graph: dict[str, Any],
    errors: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    missing_envelope = sorted(REQUIRED_ENVELOPE_FIELDS.difference(graph))
    if missing_envelope:
        add_error(
            errors,
            "missing_envelope_fields",
            "Claim graph envelope lacks required fields.",
            missing_fields=missing_envelope,
        )
    if graph.get("claim_graph_schema_id") != "claim_graph_schema_v1":
        add_error(
            errors,
            "unexpected_claim_graph_schema_id",
            "Claim graph schema id must be claim_graph_schema_v1.",
            actual=graph.get("claim_graph_schema_id"),
        )
    if not isinstance(graph.get("nodes", []), list):
        add_error(errors, "nodes_not_list", "Claim graph nodes must be a list.")
        graph["nodes"] = []
    if not isinstance(graph.get("edges", []), list):
        add_error(errors, "edges_not_list", "Claim graph edges must be a list.")
        graph["edges"] = []

    nodes_by_id, outgoing, incoming = build_indexes(graph)
    seen_node_ids: set[str] = set()
    for node in graph.get("nodes", []):
        if not isinstance(node, dict):
            add_error(errors, "node_not_object", "Claim graph node must be an object.")
            continue
        node_id = str(node.get("node_id", "<unknown>"))
        missing = sorted(REQUIRED_NODE_FIELDS.difference(node))
        if missing:
            add_error(
                errors,
                "node_missing_required_fields",
                "Claim graph node lacks required fields.",
                node_id=node_id,
                missing_fields=missing,
            )
        if node_id in seen_node_ids:
            add_error(errors, "duplicate_node_id", "Claim graph node id is duplicated.", node_id=node_id)
        seen_node_ids.add(node_id)
        if node.get("node_type") not in NODE_TYPES:
            add_error(
                errors,
                "unknown_node_type",
                "Claim graph node type is not in the schema vocabulary.",
                node_id=node_id,
                node_type=node.get("node_type"),
            )
        if node.get("promotion_status") not in PROMOTION_STATUSES:
            add_error(
                errors,
                "unknown_promotion_status",
                "Claim graph node promotion status is not in the schema vocabulary.",
                node_id=node_id,
                promotion_status=node.get("promotion_status"),
            )
        if node.get("validator_receipt_only") and node.get("scientific_proof_authority"):
            add_error(
                errors,
                "validator_receipt_claims_scientific_authority",
                "Validator receipt node cannot claim scientific proof authority.",
                node_id=node_id,
            )

    seen_edge_ids: set[str] = set()
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            add_error(errors, "edge_not_object", "Claim graph edge must be an object.")
            continue
        edge_id = str(edge.get("edge_id", "<unknown>"))
        missing = sorted(REQUIRED_EDGE_FIELDS.difference(edge))
        if missing:
            add_error(
                errors,
                "edge_missing_required_fields",
                "Claim graph edge lacks required fields.",
                edge_id=edge_id,
                missing_fields=missing,
            )
        if edge_id in seen_edge_ids:
            add_error(errors, "duplicate_edge_id", "Claim graph edge id is duplicated.", edge_id=edge_id)
        seen_edge_ids.add(edge_id)
        if edge.get("edge_type") not in EDGE_TYPES:
            add_error(
                errors,
                "unknown_edge_type",
                "Claim graph edge type is not in the schema vocabulary.",
                edge_id=edge_id,
                edge_type=edge.get("edge_type"),
            )
        if edge.get("source_node_id") not in nodes_by_id:
            add_error(
                errors,
                "edge_unknown_source_node",
                "Claim graph edge source node does not exist.",
                edge_id=edge_id,
                source_node_id=edge.get("source_node_id"),
            )
        if edge.get("target_node_id") not in nodes_by_id:
            add_error(
                errors,
                "edge_unknown_target_node",
                "Claim graph edge target node does not exist.",
                edge_id=edge_id,
                target_node_id=edge.get("target_node_id"),
            )
        if edge.get("edge_type") == "requires_human_gate" and edge.get("requires_human_gate") is not True:
            add_error(
                errors,
                "human_gate_edge_lacks_required_flag",
                "requires_human_gate edge must set requires_human_gate=true.",
                edge_id=edge_id,
            )

    boundary = graph.get("claim_boundary", {})
    if not isinstance(boundary, dict):
        add_error(errors, "claim_boundary_not_object", "Claim boundary must be an object.")
        boundary = {}
    for key in ("graph_is_proof_authority", "graph_changes_scientific_claims", "graph_promotes_status"):
        if boundary.get(key) is not False:
            add_error(
                errors,
                "claim_boundary_flag_not_false",
                "Claim boundary promotion/proof flags must remain false.",
                field=key,
                actual=boundary.get(key),
            )
    if boundary.get("no_physics_delta") is not True:
        add_error(
            errors,
            "claim_boundary_no_physics_delta_not_true",
            "Claim boundary must explicitly preserve no_physics_delta=true.",
            actual=boundary.get("no_physics_delta"),
        )

    source_authority = graph.get("source_authority", {})
    if isinstance(source_authority, dict) and source_authority.get("derivative_sources_allowed") is not False:
        add_error(
            errors,
            "derivative_sources_allowed_not_false",
            "Claim graph source authority must not allow derivative sources as independent authority.",
            actual=source_authority.get("derivative_sources_allowed"),
        )

    return nodes_by_id, outgoing, incoming


def validate_high_risk_positive_nodes(
    graph: dict[str, Any],
    outgoing: dict[str, list[dict[str, Any]]],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    checked: list[str] = []
    for node in graph.get("nodes", []):
        if not isinstance(node, dict) or not is_high_risk_positive_node(node):
            continue
        node_id = str(node.get("node_id", ""))
        checked.append(node_id)
        blocked_edges = [
            edge
            for edge in outgoing.get(node_id, [])
            if edge.get("edge_type") in BLOCKING_EDGE_TYPES
            or edge.get("does_not_establish")
            or edge.get("overread_guards")
        ]
        if not node.get("overread_guards") or not blocked_edges:
            add_error(
                errors,
                "high_risk_positive_node_lacks_blocked_overread_edges",
                "High-risk positive node must carry overread guards and at least one blocked-overread edge.",
                node_id=node_id,
                label=node.get("label"),
            )
    return {"checked_count": len(checked), "checked_node_ids": checked}


def downstream_non_establishment_edges(
    node: dict[str, Any],
    outgoing: dict[str, list[dict[str, Any]]],
    nodes_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for edge in outgoing.get(str(node.get("node_id", "")), []):
        if edge.get("edge_type") != "does_not_establish":
            continue
        if references_any(edge_text(edge, nodes_by_id), DOWNSTREAM_PHYSICAL_TERMS):
            edges.append(edge)
    return edges


def validate_accepted_evidence_preconditions(
    graph: dict[str, Any],
    outgoing: dict[str, list[dict[str, Any]]],
    nodes_by_id: dict[str, dict[str, Any]],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    checked: list[str] = []
    for node in graph.get("nodes", []):
        if not isinstance(node, dict) or not is_accepted_evidence_precondition(node):
            continue
        node_id = str(node.get("node_id", ""))
        checked.append(node_id)
        if not downstream_non_establishment_edges(node, outgoing, nodes_by_id):
            add_error(
                errors,
                "accepted_evidence_precondition_lacks_downstream_non_establishment",
                "Accepted evidence/precondition node must have does_not_establish edges to downstream physical targets.",
                node_id=node_id,
                label=node.get("label"),
            )
    return {"checked_count": len(checked), "checked_node_ids": checked}


def validate_generated_derivatives(
    graph: dict[str, Any],
    outgoing: dict[str, list[dict[str, Any]]],
    incoming: dict[str, list[dict[str, Any]]],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    checked: list[str] = []
    for node in graph.get("nodes", []):
        if not isinstance(node, dict) or node.get("node_type") != "generated_derivative":
            continue
        node_id = str(node.get("node_id", ""))
        checked.append(node_id)
        derivative_edges = [
            edge
            for edge in outgoing.get(node_id, []) + incoming.get(node_id, [])
            if edge.get("edge_type") == "is_derivative_of"
        ]
        if not derivative_edges:
            add_error(
                errors,
                "generated_derivative_lacks_is_derivative_of",
                "Generated derivative node must have an is_derivative_of edge.",
                node_id=node_id,
                label=node.get("label"),
            )
    return {"checked_count": len(checked), "checked_node_ids": checked}


def validate_gate_chair_authority_paths(
    graph: dict[str, Any],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    checked: list[str] = []
    for node in graph.get("nodes", []):
        if not isinstance(node, dict) or not is_gate_chair_node(node):
            continue
        node_id = str(node.get("node_id", ""))
        checked.append(node_id)
        authority_path = str(node.get("authority_path", ""))
        authority_registry = str(node.get("authority_registry", ""))
        authority_object_id = str(node.get("authority_object_id", ""))
        path = REPO_ROOT / authority_path
        invalid = (
            not authority_path.startswith("research_control/tasks/")
            or authority_path.startswith(DERIVATIVE_PREFIXES)
            or authority_registry not in GATE_CHAIR_ALLOWED_REGISTRIES
            or not authority_object_id
            or not path.exists()
        )
        if invalid:
            add_error(
                errors,
                "gate_chair_node_lacks_exact_authority_path",
                "Gate Chair node must point to an exact non-derivative task authority path and allowed authority registry.",
                node_id=node_id,
                authority_path=authority_path,
                authority_registry=authority_registry,
                authority_object_id=authority_object_id,
            )
    return {"checked_count": len(checked), "checked_node_ids": checked}


def edge_mentions_benchmark_promotion(edge: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]) -> bool:
    return references_any(edge_text(edge, nodes_by_id), {"benchmark promotion", "benchmark_promotion"})


def benchmark_edge_is_protected(edge: dict[str, Any]) -> bool:
    if edge.get("edge_type") in NEGATIVE_EDGE_TYPES:
        return True
    if references_any(flattened_text(edge.get("does_not_establish", [])), {"benchmark promotion", "benchmark_promotion"}):
        return True
    if edge.get("requires_human_gate") is True:
        return True
    if edge.get("edge_type") == "requires_human_gate":
        return edge.get("requires_human_gate") is True
    metadata = edge.get("metadata", {})
    if isinstance(metadata, dict):
        return bool(metadata.get("protected_authority_path") or metadata.get("protected_authority_id"))
    return False


def validate_benchmark_promotion_edges(
    graph: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    checked: list[str] = []
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict) or not edge_mentions_benchmark_promotion(edge, nodes_by_id):
            continue
        edge_id = str(edge.get("edge_id", ""))
        checked.append(edge_id)
        if not benchmark_edge_is_protected(edge):
            add_error(
                errors,
                "benchmark_promotion_edge_lacks_protected_authority",
                "Edge touching benchmark promotion must be negative/non-establishing or protected by human-gated authority.",
                edge_id=edge_id,
                edge_type=edge.get("edge_type"),
            )
    return {"checked_count": len(checked), "checked_edge_ids": checked}


def positive_adjacency(graph: dict[str, Any]) -> dict[str, list[str]]:
    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        if edge.get("edge_type") in NEGATIVE_EDGE_TYPES:
            continue
        if edge.get("does_not_establish"):
            continue
        adjacency[str(edge.get("source_node_id", ""))].append(str(edge.get("target_node_id", "")))
    return adjacency


def find_paths(adjacency: dict[str, list[str]], start: str, target: str, limit: int) -> list[list[str]]:
    paths: list[list[str]] = []
    stack: list[list[str]] = [[start]]
    while stack:
        path = stack.pop()
        current = path[-1]
        if current == target:
            paths.append(path)
            continue
        if len(path) >= limit:
            continue
        for next_node in adjacency.get(current, []):
            if next_node in path:
                continue
            stack.append(path + [next_node])
    return paths


def validate_scoped_evidence_completed_derivation_paths(
    graph: dict[str, Any],
    nodes_by_id: dict[str, dict[str, Any]],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    scoped_nodes = [
        node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and is_scoped_evidence_node(node)
    ]
    completed_nodes = [
        node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and is_completed_derivation_node(node)
    ]
    adjacency = positive_adjacency(graph)
    checked_paths = 0
    max_depth = max(1, len(nodes_by_id))
    for scoped_node in scoped_nodes:
        start = str(scoped_node.get("node_id", ""))
        for completed_node in completed_nodes:
            target = str(completed_node.get("node_id", ""))
            for path in find_paths(adjacency, start, target, max_depth):
                checked_paths += 1
                path_text = flattened_text([nodes_by_id.get(node_id, {}) for node_id in path])
                missing = [
                    term
                    for term in REQUIRED_COMPLETED_DERIVATION_INTERMEDIATES
                    if not text_contains_term(path_text, term)
                ]
                if missing:
                    add_error(
                        errors,
                        "scoped_evidence_path_to_completed_derivation_lacks_required_intermediate_nodes",
                        "Scoped evidence must not reach completed derivation without matter-coupling, Einstein-equation, and benchmark-promotion intermediates.",
                        source_node_id=start,
                        target_node_id=target,
                        path=path,
                        missing_intermediate_terms=missing,
                    )
    return {
        "checked_source_count": len(scoped_nodes),
        "completed_derivation_target_count": len(completed_nodes),
        "checked_path_count": checked_paths,
    }


def status_for(errors: list[dict[str, Any]], codes: set[str]) -> str:
    return "FAIL" if any(error["code"] in codes for error in errors) else "PASS"


def validate_claim_graph_payload(
    graph: dict[str, Any],
    *,
    graph_path: Path | None = None,
    initial_errors: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    errors = list(initial_errors or [])
    nodes_by_id, outgoing, incoming = validate_schema(graph, errors)
    high_risk = validate_high_risk_positive_nodes(graph, outgoing, errors)
    evidence = validate_accepted_evidence_preconditions(graph, outgoing, nodes_by_id, errors)
    derivatives = validate_generated_derivatives(graph, outgoing, incoming, errors)
    gate_chair = validate_gate_chair_authority_paths(graph, errors)
    benchmark = validate_benchmark_promotion_edges(graph, nodes_by_id, errors)
    scoped_paths = validate_scoped_evidence_completed_derivation_paths(graph, nodes_by_id, errors)

    rule_results = {
        "schema_and_boundary": {
            "status": status_for(
                errors,
                {
                    "missing_envelope_fields",
                    "unexpected_claim_graph_schema_id",
                    "nodes_not_list",
                    "edges_not_list",
                    "node_not_object",
                    "node_missing_required_fields",
                    "duplicate_node_id",
                    "unknown_node_type",
                    "unknown_promotion_status",
                    "validator_receipt_claims_scientific_authority",
                    "edge_not_object",
                    "edge_missing_required_fields",
                    "duplicate_edge_id",
                    "unknown_edge_type",
                    "edge_unknown_source_node",
                    "edge_unknown_target_node",
                    "human_gate_edge_lacks_required_flag",
                    "claim_boundary_not_object",
                    "claim_boundary_flag_not_false",
                    "claim_boundary_no_physics_delta_not_true",
                    "derivative_sources_allowed_not_false",
                },
            )
        },
        "high_risk_positive_blocked_overread_edges": {
            "status": status_for(errors, {"high_risk_positive_node_lacks_blocked_overread_edges"}),
            **high_risk,
        },
        "accepted_evidence_preconditions_downstream_non_establishment": {
            "status": status_for(errors, {"accepted_evidence_precondition_lacks_downstream_non_establishment"}),
            **evidence,
        },
        "generated_derivatives_is_derivative_of": {
            "status": status_for(errors, {"generated_derivative_lacks_is_derivative_of"}),
            **derivatives,
        },
        "gate_chair_exact_authority_paths": {
            "status": status_for(errors, {"gate_chair_node_lacks_exact_authority_path"}),
            **gate_chair,
        },
        "benchmark_promotion_protected_authority": {
            "status": status_for(errors, {"benchmark_promotion_edge_lacks_protected_authority"}),
            **benchmark,
        },
        "scoped_evidence_to_completed_derivation_paths": {
            "status": status_for(
                errors,
                {"scoped_evidence_path_to_completed_derivation_lacks_required_intermediate_nodes"},
            ),
            **scoped_paths,
        },
    }
    return {
        "schema_id": REPORT_SCHEMA_ID,
        "validator_name": VALIDATOR_NAME,
        "validator_version": VALIDATOR_VERSION,
        "generated_at": utc_now(),
        "graph_path": str(graph_path) if graph_path else "",
        "graph_id": graph.get("graph_id", ""),
        "claim_graph_schema_id": graph.get("claim_graph_schema_id", ""),
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "rule_results": rule_results,
        "operational_receipt_only": True,
        "no_physics_delta": True,
        "physics_proof_authority": False,
        "distance_to_gr_delta": "none",
    }


def validate_claim_graph_path(graph_path: Path) -> dict[str, Any]:
    graph, initial_errors = load_graph(graph_path)
    return validate_claim_graph_payload(graph, graph_path=graph_path, initial_errors=initial_errors)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, default=REPO_ROOT / DEFAULT_GRAPH_PATH)
    parser.add_argument("--output", type=Path, help="Optional JSON validation report path.")
    parser.add_argument("--json", action="store_true", help="Print the JSON report to stdout.")
    parser.add_argument(
        "--expect-fail",
        action="store_true",
        help="Return success only when the graph fails validation. Intended for bad fixtures.",
    )
    return parser.parse_args(argv)


def write_report(report: dict[str, Any], output: Path | None) -> None:
    if not output:
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    graph_path = args.graph if args.graph.is_absolute() else REPO_ROOT / args.graph
    report = validate_claim_graph_path(graph_path)
    write_report(report, args.output)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    if args.expect_fail:
        return 0 if report["status"] == "FAIL" else 1
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
