#!/usr/bin/env python3
"""Validate the v15 P6-T02 source-extension classification retrofit report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT = REPO_ROOT / "research_control/tasks/RT-20260703-007/artifacts/source_extension_classification_retrofit_report_v1.md"

REQUIRED_ITEMS = {
    "Resp_lc_XiR": "status_boundary_evidence_only",
    "M_src": "status_boundary_evidence_only",
    "g_eff": "status_boundary_evidence_only",
    "PositiveMSProfile_v1": "status_boundary_evidence_only",
    "RR_ETransportCompletenessOrInvarianceLaw_v1": "status_boundary_evidence_only",
    "MatterCouplingPreconditionAssembly_v1": "status_boundary_evidence_only",
    "SourceCouplingLawCandidate_cand_v1": "status_boundary_evidence_only",
    "MSStablePartitionPrecondition_v1": "status_boundary_evidence_only",
    "MSStableMatterSemanticsBridge_v1": "status_boundary_evidence_only",
    "SourceMatterSemanticsAdoptionReadinessLaw_v1": "status_boundary_evidence_only",
    "P2_theorem_output_NarrowMSCertEq_v1": "derived_from_current_ontology",
}

ALLOWED_CLASSIFICATIONS = {
    "derived_from_current_ontology",
    "conservative_definitional_extension",
    "new_ontology_primitive_candidate",
    "forbidden_target_import",
    "status_boundary_evidence_only",
    "blocked_adoption_open_continuation",
}

REQUIRED_PHRASES = [
    "This report implements v15 P6-T02",
    "This is a process-integrity retrofit.",
    "Every v15 P6-T02 required object has exactly one classification.",
    "No ambiguous object is promoted.",
    "P6-T03 source-extension classification validator integration",
    "physics_promotion_authorized: false",
    "downstream_promotion_authorized: false",
    "missing_classification_fails_closed: true",
    "ambiguous_item_count: 0",
]

FORBIDDEN_PHRASES = [
    "therefore matter coupling is derived",
    "therefore Einstein equations are derived",
    "therefore the derivation is complete",
    "benchmark is promoted",
    "program is globally refuted",
]


def extract_records(text: str) -> dict[str, str]:
    records: dict[str, str] = {}
    current_id: str | None = None
    for line in text.splitlines():
        item = re.match(r"\s*- item_id: \"([^\"]+)\"", line)
        if item:
            current_id = item.group(1)
            continue
        classification = re.match(r"\s*classification: \"([^\"]+)\"", line)
        if classification and current_id:
            records[current_id] = classification.group(1)
            current_id = None
    return records


def validate(text: str) -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def add_check(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    records = extract_records(text)
    missing = sorted(set(REQUIRED_ITEMS) - set(records))
    unexpected = sorted(set(records) - set(REQUIRED_ITEMS))
    wrong = {
        item: {"expected": expected, "actual": records.get(item)}
        for item, expected in REQUIRED_ITEMS.items()
        if records.get(item) != expected
    }

    add_check("all_required_items_present", not missing, f"missing={missing}")
    add_check("no_unexpected_items", not unexpected, f"unexpected={unexpected}")
    add_check("classification_count", len(records) == len(REQUIRED_ITEMS), f"count={len(records)}")
    add_check("expected_classifications", not wrong, f"wrong={wrong}")
    add_check(
        "allowed_classification_vocabulary",
        all(value in ALLOWED_CLASSIFICATIONS for value in records.values()),
        f"classifications={sorted(set(records.values()))}",
    )

    missing_phrases = [phrase for phrase in REQUIRED_PHRASES if phrase not in text]
    add_check("required_boundary_phrases", not missing_phrases, f"missing={missing_phrases}")

    present_forbidden = [phrase for phrase in FORBIDDEN_PHRASES if phrase in text]
    add_check("forbidden_overread_phrases_absent", not present_forbidden, f"present={present_forbidden}")

    evidence_count = text.count("evidence_paths:")
    add_check(
        "every_item_has_evidence_paths",
        evidence_count >= len(REQUIRED_ITEMS),
        f"evidence_paths_count={evidence_count}",
    )

    failed = [check for check in checks if not check["passed"]]
    return {
        "status": "PASS" if not failed else "FAIL",
        "report_path": str(REPORT.relative_to(REPO_ROOT)),
        "required_item_count": len(REQUIRED_ITEMS),
        "classification_count": len(records),
        "failed_check_count": len(failed),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    text = REPORT.read_text(encoding="utf-8")
    result = validate(text)

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
