#!/usr/bin/env python3
"""Validate P10-T02 literature source-acquisition coverage."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260702-030"
ARTIFACT = TASK_DIR / "artifacts/p10_t02_literature_source_acquisition.yaml"
COMPLETION = TASK_DIR / "jobs/completions/AJC-AJ-RT-20260702-030-001.yaml"
HANDOFF = ROOT / "research_control/handoffs/handoff-0483.yaml"

REQUIRED_FAMILIES = {
    "causal_order_to_geometry",
    "operational_spacetime_reconstruction",
    "universal_coupling_and_stress_energy_bootstrap",
    "variational_action_and_conservation_requirements",
    "thermodynamic_or_entropic_einstein_equation_derivations",
    "analogue_and_emergent_gravity_boundary_sources",
    "detector_operational_semantics",
}

REQUIRED_FIELDS = [
    "bibliographic_metadata:",
    "relevance_reason:",
    "aether_flow_burdens_may_constrain:",
    "source_access_notes:",
    "apa_7_citation_candidate:",
    "no_claim_promotion_statement:",
]


def expect(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return path.read_text()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    artifact = read(ARTIFACT)
    completion = read(COMPLETION)
    handoff = read(HANDOFF)

    source_ids = re.findall(r'source_id:\s+"(P10-SRC-\d+)"', artifact)
    families = set(re.findall(r'source_family:\s+"([^"]+)"', artifact))
    doi_count = len(re.findall(r'doi:\s+"10\.', artifact))
    apa_count = len(re.findall(r'apa_7_citation_candidate:', artifact))
    not_compared_count = len(re.findall(r'comparison_status:\s+"not_compared_in_p10_t02"', artifact))

    expect('artifact_type: "literature_source_acquisition_packet"' in artifact, errors, "artifact type mismatch")
    expect('selected_scope_id: "operational_causal_metric_universal_coupling_constraints_scope"' in artifact, errors, "selected scope missing")
    expect(len(source_ids) >= 12, errors, "at least 12 sources required")
    expect(len(set(source_ids)) == len(source_ids), errors, "source ids must be unique")
    expect(families >= REQUIRED_FAMILIES, errors, "not all required source families are covered")
    expect(doi_count >= 9, errors, "at least nine DOI-backed source records required")
    expect(apa_count == len(source_ids), errors, "every source must have an APA candidate")
    expect(not_compared_count == len(source_ids), errors, "every source must be marked not compared in P10-T02")
    for field in REQUIRED_FIELDS:
        expect(field in artifact, errors, f"required field missing: {field}")
    for phrase in (
        "does not compare",
        "does not validate",
        "does not promote",
        "does not derive",
    ):
        expect(phrase in artifact, errors, f"no-promotion statement missing phrase: {phrase}")
    expect('related_plan_task_id: "P10-T02"' in completion, errors, "completion must identify P10-T02")
    expect('source_acquisition_only_no_distance_delta' in completion, errors, "completion must preserve source-only status")
    expect('task_type: "v14_p10_t03_literature_comparison_packet"' in handoff, errors, "handoff must require P10-T03")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "validated_artifact": str(ARTIFACT.relative_to(ROOT)),
        "validated_completion": str(COMPLETION.relative_to(ROOT)),
        "source_count": len(source_ids),
        "source_family_count": len(families),
        "doi_backed_source_count": doi_count,
        "apa_candidate_count": apa_count,
        "claim_promotion_authorized": False,
    }
    Path(args.output).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
