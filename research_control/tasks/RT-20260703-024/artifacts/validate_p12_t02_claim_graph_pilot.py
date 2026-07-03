#!/usr/bin/env python3
"""Validate the v15 P12-T02 claim graph generator pilot outputs."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = REPO_ROOT / "scripts" / "research_control" / "generate_claim_graph_v1.py"
DEFAULT_JSON_PATH = REPO_ROOT / "output" / "claim_graph_v1.json"
DEFAULT_DOT_PATH = REPO_ROOT / "output" / "claim_graph_v1.dot"
DEFAULT_MARKDOWN_PATH = REPO_ROOT / "wiki" / "indexes" / "claim_graph_v1.md"

REQUIRED_LABELS = [
    "M_src",
    "g_eff",
    "Resp_lc",
    "matter_coupling",
    "PositiveMSProfile_v1",
    "RR_ETransportCompletenessOrInvarianceLaw_v1",
    "RR_E separation obstruction",
    "Einstein equations",
    "benchmark promotion",
    "NarrowMSCertEq_v1",
]

REQUIRED_NEGATIVE_TARGETS = [
    "matter_coupling",
    "Einstein equations",
    "benchmark promotion",
]


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_claim_graph_v1", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def validate_outputs(json_path: Path, dot_path: Path, markdown_path: Path) -> dict[str, object]:
    generator = load_generator()
    errors: list[str] = []
    warnings: list[str] = []

    expected_graph = generator.build_claim_graph(REPO_ROOT)
    expected_json = json.dumps(expected_graph, indent=2, sort_keys=True) + "\n"
    expected_dot = generator.render_dot(expected_graph)
    expected_markdown = generator.render_markdown(expected_graph)

    for path in (json_path, dot_path, markdown_path):
        if not path.exists():
            errors.append(f"missing output: {rel(path)}")

    actual_graph: dict[str, object] = {}
    if json_path.exists():
        try:
            actual_text = json_path.read_text(encoding="utf-8")
            actual_graph = json.loads(actual_text)
            if actual_text != expected_json:
                errors.append(f"stale or nondeterministic JSON output: {rel(json_path)}")
        except json.JSONDecodeError as exc:
            errors.append(f"JSON output is not parseable: {exc}")

    if dot_path.exists() and dot_path.read_text(encoding="utf-8") != expected_dot:
        errors.append(f"stale DOT output: {rel(dot_path)}")

    if markdown_path.exists() and markdown_path.read_text(encoding="utf-8") != expected_markdown:
        errors.append(f"stale Markdown output: {rel(markdown_path)}")

    graph = actual_graph or expected_graph
    labels_by_id = {node["node_id"]: node["label"] for node in graph.get("nodes", [])}
    labels = set(labels_by_id.values())
    for label in REQUIRED_LABELS:
        if label not in labels:
            errors.append(f"missing required pilot node label: {label}")

    boundary = graph.get("claim_boundary", {})
    for field in (
        "graph_is_proof_authority",
        "graph_changes_scientific_claims",
        "graph_promotes_status",
    ):
        if boundary.get(field) is not False:
            errors.append(f"claim boundary field must be false: {field}")

    for node in graph.get("nodes", []):
        if node.get("scientific_proof_authority") is True:
            errors.append(f"node claims scientific proof authority: {node.get('node_id')}")
        if node.get("node_type") in {
            "source_object",
            "source_extension_object",
            "evidence_precondition",
            "conditional_theorem",
        } and not node.get("overread_guards"):
            errors.append(f"support-like node lacks overread guards: {node.get('node_id')}")

    negative_targets_seen: set[str] = set()
    for edge in graph.get("edges", []):
        target_label = labels_by_id.get(edge.get("target_node_id", ""))
        if edge.get("edge_type") in {"does_not_establish", "blocks", "requires_human_gate"}:
            if target_label in REQUIRED_NEGATIVE_TARGETS:
                negative_targets_seen.add(target_label)
        if edge.get("edge_type") in {"supports", "depends_on", "does_not_establish"}:
            if not edge.get("does_not_establish"):
                errors.append(f"guarded edge lacks does_not_establish: {edge.get('edge_id')}")

    missing_negative_targets = sorted(set(REQUIRED_NEGATIVE_TARGETS).difference(negative_targets_seen))
    if missing_negative_targets:
        errors.append(f"missing negative or blocking edge to targets: {missing_negative_targets}")

    sources = set(graph.get("source_authority", {}).get("canonical_sources", []))
    for required_source in (
        "registries/DISTANCE_TO_GR_LEDGER.csv",
        "research_control/design/frontier_theorem_inventory.md",
        "research_control/design/claim_graph_schema_v1.md",
    ):
        if required_source not in sources:
            errors.append(f"missing canonical source authority: {required_source}")

    return {
        "schema_id": "claim_graph_schema_v1",
        "task_id": "RT-20260703-024",
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
        "warnings": warnings,
        "json_path": rel(json_path),
        "dot_path": rel(dot_path),
        "markdown_path": rel(markdown_path),
        "required_node_labels_present": len(set(REQUIRED_LABELS).intersection(labels)),
        "required_node_labels_total": len(REQUIRED_LABELS),
        "negative_targets_seen": sorted(negative_targets_seen),
        "no_physics_delta": True,
        "next_route": "P12-T03 claim graph validation rules",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-path", default=str(DEFAULT_JSON_PATH))
    parser.add_argument("--dot-path", default=str(DEFAULT_DOT_PATH))
    parser.add_argument("--markdown-path", default=str(DEFAULT_MARKDOWN_PATH))
    parser.add_argument("--output", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate_outputs(
        Path(args.json_path),
        Path(args.dot_path),
        Path(args.markdown_path),
    )
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
