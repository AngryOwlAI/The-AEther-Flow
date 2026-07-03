#!/usr/bin/env python3
"""Validate v15 P6-T01 source-extension classification checklist."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
CHECKLIST_PATH = REPO_ROOT / "research_control/design/source_extension_classification_checklist_v1.md"

REQUIRED_CLASSIFICATIONS = [
    "derived_from_current_ontology",
    "conservative_definitional_extension",
    "new_ontology_primitive_candidate",
    "forbidden_target_import",
    "status_boundary_evidence_only",
    "blocked_adoption_open_continuation",
]

REQUIRED_EVIDENCE_PHRASES = [
    "Required evidence",
    "relation to current ontology",
    "allowed conclusion language",
    "forbidden conclusion language",
    "downstream promotion status",
    "Missing classification records fail closed",
]

REQUIRED_FORBIDDEN_PHRASES = [
    "source law is adopted",
    "matter semantics are adopted",
    "detector semantics are adopted",
    "coupling law is adopted",
    "matter coupling is derived",
    "MetricData(E)",
    "g_eff",
    "Einstein equations are derived",
    "exact-GR benchmark is promoted",
    "derivation is complete",
    "future source-extension is impossible",
    "program is globally refuted",
]

REQUIRED_NON_CONCLUSIONS = [
    "source-law adoption",
    "ontology adoption",
    "matter-semantics adoption",
    "detector-semantics adoption",
    "coupling-law adoption",
    "matter-coupling derivation",
    "Einstein-equation derivation",
    "benchmark promotion",
    "completed derivation",
]


def make_check(check_id: str, passed: bool, detail: str) -> dict[str, object]:
    return {"id": check_id, "passed": passed, "detail": detail}


def build_report() -> dict[str, object]:
    text = CHECKLIST_PATH.read_text(encoding="utf-8")
    checks = [
        make_check(
            "all_required_classifications_present",
            all(item in text for item in REQUIRED_CLASSIFICATIONS),
            "Checklist contains all six v15 P6-T01 classification labels.",
        ),
        make_check(
            "evidence_requirements_present",
            all(phrase in text for phrase in REQUIRED_EVIDENCE_PHRASES),
            "Checklist names required evidence, relation to ontology, conclusion language, downstream status, and fail-closed behavior.",
        ),
        make_check(
            "forbidden_language_present",
            all(phrase in text for phrase in REQUIRED_FORBIDDEN_PHRASES),
            "Checklist includes forbidden conclusion language for high-risk downstream overreads.",
        ),
        make_check(
            "non_conclusions_present",
            all(phrase in text for phrase in REQUIRED_NON_CONCLUSIONS),
            "Checklist states that passing classification is not physics promotion or proof authority.",
        ),
        make_check(
            "machine_readable_schema_present",
            "source_extension_classification_checklist_v1" in text
            and "missing_classification_fails_closed: true" in text
            and "physics_promotion_authorized: false" in text
            and "proof_authority: false" in text,
            "Machine-readable checklist records fail-closed classification and no proof authority.",
        ),
    ]
    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "status": status,
        "check_count": len(checks),
        "failed_check_count": sum(1 for check in checks if not check["passed"]),
        "checks": checks,
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "matter_coupling_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Optional JSON report output path.")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout.")
    args = parser.parse_args()

    report = build_report()
    if args.output:
        output_path = REPO_ROOT / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
