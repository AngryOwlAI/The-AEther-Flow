#!/usr/bin/env python3
"""Validate the bounded P10-T03 literature comparison packet."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control" / "tasks" / "RT-20260702-031"
ARTIFACT = TASK_DIR / "artifacts" / "p10_t03_literature_comparison_packet.md"
COMPLETION = TASK_DIR / "jobs" / "completions" / "AJC-AJ-RT-20260702-031-001.yaml"
HANDOFF = ROOT / "research_control" / "handoffs" / "handoff-0484.yaml"


REQUIRED_HEADINGS = [
    "## Literature Source List",
    "## Neighboring Program Summary",
    "## Relevant Reconstruction Constraints",
    "## No-Go Constraints",
    "## Similarities To AEther-Flow",
    "## Differences From AEther-Flow",
    "## Risks To M_src",
    "## Risks To Scoped g_eff",
    "## Risks To Positive Matter Semantics",
    "## Risks To RR_E Transport/Invariance",
    "## Implications For No-Target Certificate Hygiene",
    "## Implications For Stress-Energy/Action Route",
    "## Implications For Einstein-Equation Route",
    "## No Claim-Promotion Statement",
    "## Recommendations For Selector",
]

RISK_TERMS = [
    "M_src",
    "g_eff",
    "Positive Matter Semantics",
    "RR_E",
    "No-Target",
    "Stress-Energy/Action",
    "Einstein-Equation",
]

NO_PROMOTION_PHRASES = [
    "does not validate",
    "does not adopt",
    "does not derive",
    "does not promote",
]

COMPLETION_MARKERS = [
    'related_plan_task_id: "P10-T03"',
    'target_derivation_milestone: "einstein_equations"',
    "distance_to_gr_status:",
    "new_mathematical_payload:",
    "parent_child_synthesis:",
    "comparison_only_no_distance_delta",
]

HANDOFF_MARKERS = [
    'task_type: "v14_p10_t04_literature_findings_route_selector"',
    'role_id: "theoretical-continuation-selector"',
    "P10-T04",
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    artifact_text = read_text(ARTIFACT)
    completion_text = read_text(COMPLETION)
    handoff_text = read_text(HANDOFF)

    checks: list[dict[str, object]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    missing_headings = [heading for heading in REQUIRED_HEADINGS if heading not in artifact_text]
    record("required_sections_present", not missing_headings, f"missing={missing_headings}")

    source_ids = sorted(set(re.findall(r"P10-SRC-\d{3}", artifact_text)))
    record("all_source_ids_referenced", len(source_ids) >= 14, f"source_id_count={len(source_ids)}")

    lower_artifact = artifact_text.lower()
    missing_no_promotion = [phrase for phrase in NO_PROMOTION_PHRASES if phrase not in lower_artifact]
    record("no_claim_promotion_statement", not missing_no_promotion, f"missing={missing_no_promotion}")

    missing_risks = [term for term in RISK_TERMS if term not in artifact_text]
    record("risk_surfaces_covered", not missing_risks, f"missing={missing_risks}")

    selector_terms = [
        "repair_needed",
        "red_team_needed",
        "theorem_target",
        "obstruction_candidate",
        "no_action",
        "public_boundary_update",
    ]
    missing_selector_terms = [term for term in selector_terms if term not in artifact_text]
    record("selector_classes_present", not missing_selector_terms, f"missing={missing_selector_terms}")

    missing_completion = [marker for marker in COMPLETION_MARKERS if marker not in completion_text]
    record("completion_markers_present", not missing_completion, f"missing={missing_completion}")

    missing_handoff = [marker for marker in HANDOFF_MARKERS if marker not in handoff_text]
    record("handoff_routes_to_p10_t04", not missing_handoff, f"missing={missing_handoff}")

    generated_texts = [
        read_text(TASK_DIR / "artifacts" / "child_phys_math_p10_t03_literature_comparison.yaml"),
        read_text(TASK_DIR / "artifacts" / "child_phys_phil_p10_t03_literature_comparison.yaml"),
        read_text(TASK_DIR / "artifacts" / "parent_conflict_review_p10_t03_literature_comparison.yaml"),
        read_text(TASK_DIR / "artifacts" / "parent_fusion_notes_p10_t03_literature_comparison.md"),
    ]
    record(
        "parent_child_synthesis_artifacts_present",
        all(text.strip() for text in generated_texts),
        "child math child phil conflict review and fusion notes checked",
    )

    passed = all(check["status"] == "PASS" for check in checks)
    report = {
        "validator_id": "validate_p10_t03_literature_comparison",
        "task_id": "RT-20260702-031",
        "job_id": "AJ-RT-20260702-031-001",
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
