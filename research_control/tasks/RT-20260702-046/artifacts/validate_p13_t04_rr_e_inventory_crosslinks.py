#!/usr/bin/env python3
"""Validate the bounded P13-T04 RR_E inventory crosslink packet."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260702-046"
INVENTORY = ROOT / "research_control" / "design" / "frontier_theorem_inventory.md"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260702-046-001.yaml"
HANDOFF = ROOT / "research_control" / "handoffs" / "handoff-0499.yaml"

SECTION_HEADERS = {
    "rr_e_transport": "### Item 10E: rr_e_transport_completeness_or_invariance_law_v1",
    "readiness": "### Item 10J: source_matter_semantics_adoption_readiness_law_v1",
    "positive_profile": "### Item 10L: positive_ms_profile_v1",
}

NEXT_SECTION = re.compile(r"^### Item \d+[A-Z]?: ", re.MULTILINE)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def section(text: str, header: str) -> str:
    start = text.find(header)
    if start == -1:
        return ""
    match = NEXT_SECTION.search(text, start + len(header))
    end = match.start() if match else len(text)
    return text[start:end]


def contains_all(haystack: str, needles: list[str]) -> list[str]:
    lower_haystack = haystack.lower()
    return [needle for needle in needles if needle.lower() not in lower_haystack]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    inventory_text = read_text(INVENTORY)
    completion_text = read_text(COMPLETION)
    handoff_text = read_text(HANDOFF)

    checks: list[dict[str, object]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    transport_section = section(inventory_text, SECTION_HEADERS["rr_e_transport"])
    readiness_section = section(inventory_text, SECTION_HEADERS["readiness"])
    profile_section = section(inventory_text, SECTION_HEADERS["positive_profile"])

    record("target_sections_present", all([transport_section, readiness_section, profile_section]), "required P13-T04 inventory sections found")

    transport_required = [
        "rr_e_boundary_crosslinks",
        "rr_e_underdetermination_obstruction",
        "rr_e_separation_obstruction_witness_v1",
        "rr_e_separation_boundary_control_note.md",
        "rr_e_allowed_identification_checklist.md",
        "certificate-indexed",
        "missing certificate data preserves separation or obstruction",
    ]
    transport_missing = contains_all(transport_section, transport_required)
    record("transport_row_links_obstruction_and_certificate_scope", not transport_missing, f"missing={transport_missing}")

    readiness_required = [
        "rr_e_non_collapse_pressure",
        "rr_e_separation_boundary_control_note.md",
        "rr_e_allowed_identification_checklist.md",
        "rr_e_transport_completeness_or_invariance_law_v1",
        "rr_e_underdetermination_obstruction",
        "rr_e_separation_obstruction_witness_v1",
        "fail-closed separation branch",
    ]
    readiness_missing = contains_all(readiness_section, readiness_required)
    record("readiness_row_links_non_collapse_pressure", not readiness_missing, f"missing={readiness_missing}")

    profile_required = [
        "rr_e_separation_transport_boundary",
        "PositiveMSProfile_v1",
        "RR_ETransportCompletenessOrInvarianceLaw_v1",
        "rr_e_separation_boundary_control_note.md",
        "rr_e_allowed_identification_checklist.md",
        "preserve separation or obstruction",
        "rr_e_underdetermination_obstruction",
        "rr_e_separation_obstruction_witness_v1",
    ]
    profile_missing = contains_all(profile_section, profile_required)
    record("positive_profile_links_separation_transport_boundary", not profile_missing, f"missing={profile_missing}")

    coverage_required = [
        "P13-T04 `RR_E` crosslink receipt",
        "PositiveMSProfile_v1",
        "SourceMatterSemanticsAdoptionReadinessLaw_v1",
        "RR_ETransportCompletenessOrInvarianceLaw_v1",
        "Missing certificate data preserves separation or obstruction",
    ]
    coverage_missing = contains_all(inventory_text, coverage_required)
    record("coverage_receipt_present", not coverage_missing, f"missing={coverage_missing}")

    forbidden_patterns = [
        r"\bRR_E irrelevance proved\b",
        r"\bunrestricted RR_E irrelevance proved\b",
        r"\bRR_E collapsed\b",
        r"\bRR_E removed as irrelevant\b",
        r"\bRR_E identified without source transport certificate\b",
        r"\bRR_E identified without source invariance certificate\b",
        r"\bRR_E identified without source factorization certificate\b",
        r"\bg_eff collapses RR_E\b",
        r"\bbenchmark behavior collapses RR_E\b",
        r"\bprocess authority collapses RR_E\b",
        r"\bsupport-only formalization collapses RR_E\b",
    ]
    forbidden_hits = [
        pattern
        for pattern in forbidden_patterns
        if re.search(pattern, inventory_text, flags=re.IGNORECASE)
    ]
    record("no_certificate_free_rr_e_overread_phrases", not forbidden_hits, f"forbidden_hits={forbidden_hits}")

    completion_required = [
        'related_plan_task_id: "P13-T04"',
        "rr_e_inventory_crosslinks:",
        "frontier_theorem_inventory.md",
        "v14_p13_t04_rr_e_inventory_crosslinks_completed_next_phase_validation",
    ]
    completion_missing = contains_all(completion_text, completion_required)
    record("completion_markers_present", not completion_missing, f"missing={completion_missing}")

    handoff_required = [
        'handoff_id: "handoff-0499"',
        "P13-T05",
        "RR_E separation phase validation",
    ]
    handoff_missing = contains_all(handoff_text, handoff_required)
    record("handoff_routes_to_p13_t05", not handoff_missing, f"missing={handoff_missing}")

    passed = all(check["status"] == "PASS" for check in checks)
    report = {
        "validator_id": "validate_p13_t04_rr_e_inventory_crosslinks",
        "task_id": "RT-20260702-046",
        "job_id": "AJ-RT-20260702-046-001",
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
