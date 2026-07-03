#!/usr/bin/env python3
"""Validate the v15 P4-T02 populated matter-coupling dependency DAG."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DAG_PATH = Path("research_control/design/matter_coupling_dependency_dag_v1.md")

REQUIRED_NODES = [
    "mc_source_matter_semantics_objects",
    "mc_source_matter_semantics_equivalence_theorem",
    "mc_rr_e_certificate_boundary",
    "mc_detector_semantics_target",
    "mc_coupling_law_target",
    "mc_stress_energy_semantics_target",
    "mc_stress_energy_tensor_target",
    "mc_matter_action_target",
    "mc_universal_matter_coupling_derivation",
    "mc_einstein_equation_dependency",
    "mc_benchmark_promotion_dependency",
]

REQUIRED_NODE_KINDS = [
    "evidence_precondition",
    "adopted_object",
    "theorem",
    "law",
    "obstruction",
    "physical_target",
]

REQUIRED_EDGES = [
    "mc_edge_objects_to_theorem",
    "mc_edge_rr_e_boundary_to_theorem",
    "mc_edge_theorem_to_coupling_law",
    "mc_edge_detector_to_universal",
    "mc_edge_coupling_law_to_universal",
    "mc_edge_stress_semantics_to_tensor",
    "mc_edge_tensor_to_action",
    "mc_edge_action_to_einstein",
    "mc_edge_universal_to_einstein",
    "mc_edge_einstein_to_benchmark",
]

BLOCKED_NODES = [
    "mc_detector_semantics_target",
    "mc_coupling_law_target",
    "mc_stress_energy_semantics_target",
    "mc_stress_energy_tensor_target",
    "mc_matter_action_target",
    "mc_universal_matter_coupling_derivation",
    "mc_einstein_equation_dependency",
    "mc_benchmark_promotion_dependency",
]

REQUIRED_INPUT_MARKERS = [
    "registries/DISTANCE_TO_GR_LEDGER.csv",
    "research_control/current_frontier.md",
    "source_side_matter_semantics_object_certificate_manifest_v1.tex",
    "narrow_source_side_matter_semantics_equivalence_theorem_v1.tex",
    "matter_semantics_equivalence_theorem_refuter_stress_v1.tex",
    "narrow_ms_cert_eq_gate_chair_review_v1.tex",
    "source_certificate_operation_laws_v1.tex",
    "no_target_import_guard_map.md",
]

FORBIDDEN_BARE_ACCEPTED_PATTERNS = [
    "| `accepted` |",
    "| accepted |",
    "status: accepted\n",
]

FORBIDDEN_CONCLUSIONS = [
    "not matter-semantics adoption",
    "not detector-semantics adoption",
    "not coupling-law adoption",
    "not matter-coupling derivation",
    "not stress-energy semantics",
    "not a matter action",
    "not Einstein equations",
    "not benchmark promotion",
    "not a completed derivation",
]


def add_check(checks: list[dict[str, object]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"id": check_id, "passed": passed, "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    text = DAG_PATH.read_text(encoding="utf-8")
    checks: list[dict[str, object]] = []

    add_check(checks, "dag_file_exists", DAG_PATH.exists(), f"{DAG_PATH} exists.")

    for kind in REQUIRED_NODE_KINDS:
      marker = f"`{kind}`"
      add_check(checks, f"node_kind_{kind}", marker in text, f"Node kind {marker} appears in DAG.")

    for node_id in REQUIRED_NODES:
        marker = f"| `{node_id}` |"
        add_check(checks, f"required_node_{node_id}", marker in text, f"Required node `{node_id}` is populated.")

    for edge_id in REQUIRED_EDGES:
        marker = f"| `{edge_id}` |"
        add_check(checks, f"required_edge_{edge_id}", marker in text, f"Required edge `{edge_id}` is populated.")

    for node_id in BLOCKED_NODES:
        burden_marker = f"| `{node_id}` |"
        missing_burden = burden_marker in text and "Missing burden:" in text
        summary_row = f"| `{node_id}` |" in text
        add_check(
            checks,
            f"blocked_node_missing_burden_{node_id}",
            missing_burden and summary_row,
            f"Blocked node `{node_id}` has an exact missing-burden statement.",
        )

    for marker in REQUIRED_INPUT_MARKERS:
        add_check(
            checks,
            f"input_marker_{marker.replace('/', '_').replace('.', '_')}",
            marker in text,
            f"Required input marker `{marker}` appears.",
        )

    edge_section = text.split("## Populated Edges", 1)[1].split("## Blocked Node Burden Summary", 1)[0]
    edge_rows = [line for line in edge_section.splitlines() if line.startswith("| `mc_edge_")]
    for index, row in enumerate(edge_rows, start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        source_path = cells[4] if len(cells) > 4 else ""
        passed = "/" in source_path or source_path == "`registries/DISTANCE_TO_GR_LEDGER.csv`"
        add_check(checks, f"edge_{index}_has_source_path", passed, f"Edge row {index} has source evidence path `{source_path}`.")

    for pattern in FORBIDDEN_BARE_ACCEPTED_PATTERNS:
        add_check(
            checks,
            f"no_bare_accepted_{pattern.strip().replace(' ', '_')}",
            pattern not in text,
            f"Forbidden bare accepted pattern `{pattern}` is absent.",
        )

    for phrase in FORBIDDEN_CONCLUSIONS:
        add_check(
            checks,
            f"forbidden_conclusion_phrase_{phrase.replace(' ', '_').replace('-', '_')}",
            phrase in text,
            f"Boundary phrase `{phrase}` appears.",
        )

    claim_boundary = {
        "physics_claim_authority": False,
        "source_law_adopted": False,
        "matter_semantics_adopted": False,
        "detector_semantics_adopted": False,
        "coupling_law_adopted": False,
        "matter_coupling_derived": False,
        "stress_energy_semantics_adopted": False,
        "einstein_equations_derived": False,
        "benchmark_promoted": False,
        "completed_derivation_claimed": False,
    }
    failed = [check for check in checks if not check["passed"]]
    report = {
        "status": "PASS" if not failed else "FAIL",
        "dag_path": str(DAG_PATH),
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
        "edge_count": len(edge_rows),
        "claim_boundary": claim_boundary,
    }
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
