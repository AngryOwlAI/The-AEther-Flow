#!/usr/bin/env python3
"""Validate the v15 P12-T01 claim graph schema control document."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCHEMA_PATH = REPO_ROOT / "research_control" / "design" / "claim_graph_schema_v1.md"

REQUIRED_NODE_TYPES = [
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
]

REQUIRED_EDGE_TYPES = [
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
]

REQUIRED_TERMS = [
    "claim_graph_schema_v1",
    "promotion_status",
    "overread_guards",
    "validator_receipt_only",
    "scientific_proof_authority",
    "does_not_establish",
    "not proof authority",
    "not a physics source",
    "generated_derivative",
    "is_derivative_of",
    "next_route",
    "P12-T02",
    "Validator Receipts Versus Scientific Proof",
    "Generated Derivative Rule",
]

FORBIDDEN_PHRASES = [
    "validator receipt proves",
    "schema authorizes source-law adoption",
    "schema authorizes benchmark promotion",
    "graph is proof authority",
    "graph promotes status",
]


def validate_schema(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.exists():
        return {
            "schema_id": "claim_graph_schema_v1",
            "status": "FAIL",
            "errors": [f"missing schema path: {path.relative_to(REPO_ROOT)}"],
            "warnings": warnings,
            "required_node_types_present": 0,
            "required_edge_types_present": 0,
        }

    text = path.read_text(encoding="utf-8")
    lower_text = text.lower()

    for node_type in REQUIRED_NODE_TYPES:
        if f"`{node_type}`" not in text:
            errors.append(f"missing required node type: {node_type}")

    for edge_type in REQUIRED_EDGE_TYPES:
        if f"`{edge_type}`" not in text:
            errors.append(f"missing required edge type: {edge_type}")

    for term in REQUIRED_TERMS:
        if term.lower() not in lower_text:
            errors.append(f"missing required schema term: {term}")

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            errors.append(f"forbidden overclaim phrase present: {phrase}")

    if "validator_receipt_only: true" not in text:
        errors.append("validator receipt example must set validator_receipt_only: true")
    if "scientific_proof_authority: false" not in text:
        errors.append("schema must explicitly set scientific_proof_authority: false")
    if "graph_is_proof_authority: false" not in text:
        errors.append("graph envelope must set graph_is_proof_authority: false")
    if "graph_promotes_status: false" not in text:
        errors.append("graph envelope must set graph_promotes_status: false")
    if "Source Materials" not in text:
        errors.append("schema must include APA-style source materials")

    if len(text.splitlines()) < 200:
        warnings.append("schema is unusually short for the required boundary contract")

    return {
        "schema_id": "claim_graph_schema_v1",
        "schema_path": str(path.relative_to(REPO_ROOT)),
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
        "warnings": warnings,
        "required_node_types_present": sum(
            1 for node_type in REQUIRED_NODE_TYPES if f"`{node_type}`" in text
        ),
        "required_edge_types_present": sum(
            1 for edge_type in REQUIRED_EDGE_TYPES if f"`{edge_type}`" in text
        ),
        "required_node_types_total": len(REQUIRED_NODE_TYPES),
        "required_edge_types_total": len(REQUIRED_EDGE_TYPES),
        "validator_receipt_boundary_present": (
            "validator_receipt_only: true" in text
            and "scientific_proof_authority: false" in text
        ),
        "generated_derivative_boundary_present": (
            "generated_derivative" in text and "is_derivative_of" in text
        ),
        "promotion_status_boundary_present": "promotion_status" in text,
        "overread_guard_boundary_present": "overread_guards" in text,
        "next_route": "P12-T02 claim graph generator pilot",
        "no_physics_delta": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", default=str(SCHEMA_PATH))
    parser.add_argument("--output", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate_schema(Path(args.schema))
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
