#!/usr/bin/env python3
"""Validate v15 P4-T04 semantic-layer claim-language linter fixtures."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"


BAD_PHRASES = [
    "source matter semantics as detector semantics",
    "source matter semantics as stress-energy",
    "no-target certificate as matter theory",
    "RR_E transport evidence as unrestricted theorem",
    "PositiveMSProfile_v1 as matter-semantics adoption",
    "g_eff as unscoped Lorentzian metric",
    "matter-sector evidence as coupling law",
    "scoped evidence as Einstein-equation premise",
    "source certificate supplies detector protocol",
    "stress-energy target supplies matter action",
]

PASSING_PHRASES = [
    "Source-side matter-semantics evidence remains inside declared source certificate scope.",
    "Detector semantics remain blocked unless separately derived or adopted by tracked authority.",
    "Stress-energy semantics and matter action remain blocked unless separately derived or adopted by tracked authority.",
    "No-target certificates are hygiene only and do not supply positive matter theory.",
    "Scoped evidence/precondition status supports later work without adopting matter semantics or coupling law.",
]


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
    taxonomy_path = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"
    contexts_path = REPO_ROOT / "research_control/design/claim_language_linter_reviewed_contexts.yaml"
    note_path = REPO_ROOT / "research_control/design/semantic_layer_separation_control_note.md"
    bad_fixture_path = REPO_ROOT / "tests/fixtures/claim_language/semantic_layer_collapse.md"
    valid_fixture_path = REPO_ROOT / "tests/fixtures/claim_language/semantic_layer_valid.md"
    test_path = REPO_ROOT / "tests/test_validate_claim_language.py"

    taxonomy_text = taxonomy_path.read_text(encoding="utf-8")
    contexts_text = contexts_path.read_text(encoding="utf-8")
    note_text = note_path.read_text(encoding="utf-8")
    bad_fixture_text = bad_fixture_path.read_text(encoding="utf-8")
    valid_fixture_text = valid_fixture_path.read_text(encoding="utf-8")
    test_text = test_path.read_text(encoding="utf-8")

    bad_report = scan_text(linter, "research_control/current_frontier.md", bad_fixture_text)
    valid_report = scan_text(linter, "research_control/current_frontier.md", valid_fixture_text)
    current_frontier_report = linter.validate_paths(paths=["research_control/current_frontier.md"])
    taxonomy = linter.load_taxonomy()
    class_ids = {
        str(item.get("class_id"))
        for item in taxonomy.get("phrase_classes", [])
        if isinstance(item, dict)
    }
    semantic_findings = class_findings(bad_report, "semantic_layer_collapse_overclaim")
    coverage_pairs = [
        f'phrase: "{phrase}"' in taxonomy_text
        and 'class_id: "semantic_layer_collapse_overclaim"' in taxonomy_text
        for phrase in BAD_PHRASES
    ]

    checks = [
        {
            "id": "taxonomy_class_present",
            "passed": "semantic_layer_collapse_overclaim" in class_ids,
            "detail": "Taxonomy defines the semantic-layer collapse overclaim class.",
        },
        {
            "id": "taxonomy_contains_required_bad_phrases",
            "passed": all(phrase in taxonomy_text for phrase in BAD_PHRASES) and all(coverage_pairs),
            "detail": "Taxonomy maps every P4-T04 bad phrase to the semantic-layer class.",
        },
        {
            "id": "bad_fixture_contains_required_phrases",
            "passed": all(phrase in bad_fixture_text for phrase in BAD_PHRASES),
            "detail": "Bad fixture contains every required P4-T04 collapse phrase.",
        },
        {
            "id": "bad_fixture_hard_fails_as_current_control",
            "passed": bad_report["status"] == "FAIL"
            and bad_report["hard_fail_count"] == len(BAD_PHRASES)
            and len(semantic_findings) == len(BAD_PHRASES),
            "detail": "Bad fixture hard-fails when scanned as a current control surface.",
        },
        {
            "id": "passing_fixture_contains_scoped_wording",
            "passed": all(phrase in valid_fixture_text for phrase in PASSING_PHRASES),
            "detail": "Passing fixture contains canonical scoped semantic-layer wording.",
        },
        {
            "id": "passing_fixture_passes",
            "passed": valid_report["status"] == "PASS" and valid_report["finding_count"] == 0,
            "detail": "Canonical scoped wording produces no linter findings.",
        },
        {
            "id": "unit_tests_include_semantic_layer_cases",
            "passed": "test_semantic_layer_collapse_fixture_fails" in test_text
            and "test_semantic_layer_scoped_wording_fixture_passes" in test_text,
            "detail": "Unit tests exercise the bad and passing semantic-layer fixtures.",
        },
        {
            "id": "reviewed_contexts_cover_deliberate_bad_examples",
            "passed": "ALLOW-V15-P4-SEMANTIC-LAYER-PLAN-ROUTE-CONTEXT" in contexts_text
            and "ALLOW-V15-P4-SEMANTIC-LAYER-NOTE-FIXTURE-PROPOSAL" in contexts_text,
            "detail": "Reviewed contexts downgrade the route-plan and P4-T03 proposal quotations only.",
        },
        {
            "id": "p4_t03_note_proposed_phrases_now_implemented",
            "passed": all(phrase in note_text for phrase in BAD_PHRASES),
            "detail": "The P4-T03 fixture proposal phrases are present and implemented by P4-T04.",
        },
        {
            "id": "current_frontier_no_hard_failures",
            "passed": current_frontier_report["status"] == "PASS"
            and current_frontier_report["hard_fail_count"] == 0,
            "detail": "Current frontier has no semantic-layer claim-language hard failures.",
        },
    ]

    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "status": status,
        "task_id": "RT-20260703-003",
        "checks": checks,
        "bad_fixture_hard_fail_count": bad_report["hard_fail_count"],
        "bad_fixture_semantic_layer_finding_count": len(semantic_findings),
        "passing_fixture_finding_count": valid_report["finding_count"],
        "current_frontier_hard_fail_count": current_frontier_report["hard_fail_count"],
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "matter_semantics_adoption_authorized": False,
            "detector_semantics_adoption_authorized": False,
            "stress_energy_semantics_authorized": False,
            "matter_coupling_authorized": False,
            "einstein_equations_authorized": False,
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
