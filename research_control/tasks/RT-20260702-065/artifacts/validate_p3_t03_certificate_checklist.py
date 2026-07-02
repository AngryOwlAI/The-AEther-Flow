#!/usr/bin/env python3
"""Validate v15 P3-T03 certificate checklist and linter fixture integration."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"


def load_linter() -> Any:
    spec = importlib.util.spec_from_file_location("validate_claim_language", LINTER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def scan_text(linter: Any, path: str, text: str) -> dict[str, Any]:
    taxonomy = linter.load_taxonomy()
    findings = linter.scan_text_map(
        {path: text},
        taxonomy=taxonomy,
        reviewed_contexts=linter.load_reviewed_contexts(),
        active_handoffs=linter.latest_handoff_rel(REPO_ROOT),
    )
    return linter.report_dict(findings, scanned_paths=[path])


def class_findings(report: dict[str, Any], class_id: str) -> list[dict[str, Any]]:
    return [
        finding
        for finding in report.get("findings", [])
        if finding.get("class_id") == class_id
    ]


def build_report() -> dict[str, Any]:
    linter = load_linter()
    checklist_path = REPO_ROOT / "research_control/design/source_certificate_algebra_checklist.md"
    taxonomy_path = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"
    template_path = REPO_ROOT / "research_control/design/narrow_theorem_task_template.md"
    overread_fixture_path = REPO_ROOT / "tests/fixtures/claim_language/source_certificate_overread.md"
    valid_fixture_path = REPO_ROOT / "tests/fixtures/claim_language/source_certificate_valid.md"

    overread_text = overread_fixture_path.read_text(encoding="utf-8")
    valid_text = valid_fixture_path.read_text(encoding="utf-8")
    overread_report = scan_text(linter, "research_control/current_frontier.md", overread_text)
    valid_report = scan_text(linter, "research_control/current_frontier.md", valid_text)

    checklist_text = checklist_path.read_text(encoding="utf-8")
    taxonomy_text = taxonomy_path.read_text(encoding="utf-8")
    template_text = template_path.read_text(encoding="utf-8")

    required_checklist_phrases = [
        "Missing certificate",
        "Malformed certificate",
        "Detector-semantics certificate",
        "Target-metric certificate",
        "Benchmark-behavior certificate",
        "Source transport certificate",
        "Source invariance certificate",
        "Source factorization certificate",
        "source_certificate_algebra_checklist_v1",
    ]
    required_taxonomy_phrases = [
        "missing certificate proves declared-object equivalence",
        "missing certificate identifies RR_E",
        "malformed certificate proves declared-object equivalence",
        "malformed certificate proves matter semantics",
        "detector-semantics certificate supplies source certificate validity",
        "target-metric certificate supplies source certificate validity",
        "benchmark-behavior certificate supplies source certificate validity",
    ]

    source_certificate_findings = class_findings(overread_report, "source_certificate_overread")
    no_target_findings = class_findings(overread_report, "no_target_certificate_as_positive_semantics")
    valid_source_certificate_findings = class_findings(valid_report, "source_certificate_overread")

    checks = [
        {
            "id": "checklist_contains_all_required_rows",
            "passed": all(phrase in checklist_text for phrase in required_checklist_phrases),
            "detail": "Checklist names missing, malformed, detector, target, benchmark, and valid source certificate rows.",
        },
        {
            "id": "taxonomy_contains_required_patterns",
            "passed": all(phrase in taxonomy_text for phrase in required_taxonomy_phrases),
            "detail": "Taxonomy stores P3-T03 certificate overread patterns.",
        },
        {
            "id": "overread_fixture_hard_fails",
            "passed": overread_report["status"] == "FAIL"
            and len(source_certificate_findings) >= 7
            and overread_report["hard_fail_count"] >= 7,
            "detail": "Overread fixture produces current-control hard failures.",
        },
        {
            "id": "valid_source_certificate_fixture_passes",
            "passed": valid_report["status"] == "PASS"
            and not valid_source_certificate_findings
            and not no_target_findings,
            "detail": "Valid source transport, invariance, and factorization wording produces no certificate findings.",
        },
        {
            "id": "template_requires_checklist_receipt",
            "passed": "Source Certificate Checklist Receipt" in template_text
            and "source_certificate_algebra_checklist.md" in template_text,
            "detail": "Narrow theorem template requires certificate checklist receipt for certificate-bearing packets.",
        },
    ]

    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "status": status,
        "checks": checks,
        "overread_hard_fail_count": overread_report["hard_fail_count"],
        "overread_source_certificate_finding_count": len(source_certificate_findings),
        "valid_fixture_finding_count": valid_report["finding_count"],
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
