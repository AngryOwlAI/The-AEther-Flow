#!/usr/bin/env python3
"""Validate the bounded EqSrc family-closure source-law candidate packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEX = ROOT / "eqsrc_family_closure_source_law_candidate_v1.tex"
MATH_CHILD = ROOT / "child_phys_math_eqsrc_closure_law.yaml"
PHIL_CHILD = ROOT / "child_phys_phil_eqsrc_closure_law.yaml"
CONFLICT = ROOT / "parent_conflict_review_eqsrc_closure_law.yaml"
FUSION = ROOT / "parent_fusion_notes_eqsrc_closure_law.md"
RECEIPT = ROOT / "eqsrc_closure_source_law_receipt.md"
REPORT = ROOT / "eqsrc_closure_source_law_validation.json"


def require_markers(path: Path, markers: list[str], errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing file: {path.name}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"{path.name}: missing marker {marker!r}")


def validate() -> dict[str, object]:
    errors: list[str] = []
    require_markers(
        TEX,
        [
            "EqSrcClosureLaw",
            "proposal-only",
            "blocked_adoption_open_continuation",
            "identity token",
            "inverse-provenance",
            "composition-certificate",
            "Ledger congruence",
            "Missing-inverse",
            "Missing-composition",
            "Ledger-mismatch",
            "No general EqSrc discharge",
            "Smuggling Auditor",
        ],
        errors,
    )
    require_markers(
        MATH_CHILD,
        ["child_phys_math", "conditional_theorem_available", "fail_closed_branches_preserved"],
        errors,
    )
    require_markers(
        PHIL_CHILD,
        ["child_phys_phil", "current_ontology_underdetermined", "target_independence_required"],
        errors,
    )
    require_markers(CONFLICT, ["status: \"resolved\"", "unresolved_conflicts: []"], errors)
    require_markers(
        FUSION,
        ["proposal-only", "blocked_adoption_open_continuation", "Smuggling Auditor"],
        errors,
    )
    require_markers(
        RECEIPT,
        ["candidate_constructed_pending_audit", "no_distance_delta", "Smuggling Auditor"],
        errors,
    )
    return {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260718-015",
        "candidate_name": "EqSrcClosureLaw_src^cand",
        "candidate_status": "proposal-only",
        "adoption_status": "blocked_adoption_open_continuation",
        "physics_progress_status": "candidate_constructed_pending_audit",
        "distance_to_gr_effect": "no_distance_delta",
        "next_required_role": "smuggling-auditor@0.2.0",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
