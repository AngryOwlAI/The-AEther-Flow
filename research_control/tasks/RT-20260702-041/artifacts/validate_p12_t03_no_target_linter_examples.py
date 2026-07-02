#!/usr/bin/env python3
"""Validate P12-T03 no-target linter and examples integration."""

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


def no_target_findings(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        finding
        for finding in report.get("findings", [])
        if finding.get("class_id") == "no_target_certificate_as_positive_semantics"
    ]


def build_report() -> dict[str, Any]:
    linter = load_linter()
    fixture_path = REPO_ROOT / "tests/fixtures/claim_language/no_target_certificate_overread.md"
    examples_path = REPO_ROOT / "research_control/design/scoped_claim_language_examples.md"
    taxonomy_path = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"

    fixture_text = fixture_path.read_text(encoding="utf-8")
    fixture_report = scan_text(linter, "research_control/current_frontier.md", fixture_text)
    corrected_text = (
        "The certificate is source_hygiene_certificate_only under the stated checker "
        "scope; it is not positive matter semantics, detector semantics, "
        "stress-energy semantics, matter action, benchmark recovery, or proof authority.\n"
    )
    corrected_report = scan_text(linter, "research_control/current_frontier.md", corrected_text)

    examples_text = examples_path.read_text(encoding="utf-8")
    taxonomy_text = taxonomy_path.read_text(encoding="utf-8")
    required_example_phrases = [
        "The no-target certificate proves positive matter semantics.",
        "The no-target certificate supplies detector semantics.",
        "The no-target certificate supplies stress-energy semantics.",
        "The no-target certificate provides proof authority.",
        "source_hygiene_certificate_only",
        "it is not positive matter semantics",
    ]
    required_taxonomy_phrases = [
        "no-target certificate proves positive matter semantics",
        "no-target certificate supplies detector semantics",
        "no-target certificate supplies stress-energy semantics",
        "no-target certificate supplies matter action",
        "no-target certificate provides proof authority",
    ]

    public_paths = []
    for pattern in (
        "README.md",
        "github-facing/*.md",
        "github-facing/**/*.md",
        "research_control/current_frontier.md",
        "markdown/publication-briefs/*.md",
        "markdown/html-explainer-specs/*.md",
    ):
        for candidate in REPO_ROOT.glob(pattern):
            if candidate.is_file():
                public_paths.append(candidate.relative_to(REPO_ROOT).as_posix())
    public_paths = sorted(set(public_paths))
    public_report = linter.validate_paths(paths=public_paths)
    public_no_target_hard_failures = [
        finding
        for finding in no_target_findings(public_report)
        if str(finding.get("severity", "")).startswith("hard_fail_")
    ]

    checks = [
        {
            "id": "fixture_hard_fails",
            "passed": fixture_report["status"] == "FAIL"
            and len(no_target_findings(fixture_report)) >= 5,
            "detail": "No-target overread fixture produces no-target hard failures on a current control surface.",
        },
        {
            "id": "corrected_wording_passes",
            "passed": corrected_report["status"] == "PASS"
            and not no_target_findings(corrected_report),
            "detail": "Corrected hygiene wording produces no no-target findings.",
        },
        {
            "id": "examples_pack_contains_before_after",
            "passed": all(phrase in examples_text for phrase in required_example_phrases),
            "detail": "Examples pack contains no-target bad wording and corrected wording.",
        },
        {
            "id": "taxonomy_contains_required_patterns",
            "passed": all(phrase in taxonomy_text for phrase in required_taxonomy_phrases),
            "detail": "Taxonomy stores P12-T03 no-target overread patterns.",
        },
        {
            "id": "public_surfaces_no_no_target_hard_failures",
            "passed": not public_no_target_hard_failures,
            "detail": "Current public surfaces do not hard-fail on no-target overread.",
        },
    ]
    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "status": status,
        "checks": checks,
        "fixture_no_target_finding_count": len(no_target_findings(fixture_report)),
        "fixture_hard_fail_count": fixture_report["hard_fail_count"],
        "corrected_finding_count": corrected_report["finding_count"],
        "public_paths_scanned": public_paths,
        "public_no_target_hard_failures": public_no_target_hard_failures,
        "claim_boundary": {
            "physics_promotion_authorized": False,
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
