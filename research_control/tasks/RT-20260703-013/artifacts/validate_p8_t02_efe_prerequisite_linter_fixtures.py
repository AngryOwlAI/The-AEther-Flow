#!/usr/bin/env python3
"""Validate v15 P8-T02 EFE prerequisite claim-language linter fixtures."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
CLASS_ID = "premature_efe_prerequisite_overclaim"


BAD_PHRASES = [
    "g_eff implies Einstein equations",
    "matter-sector evidence implies stress-energy tensor",
    "no-target certificate implies matter action",
    "coupling-law candidate evidence implies matter coupling",
    "benchmark promotion follows from scoped evidence",
    "validator PASS proves EFE",
]

PASSING_PHRASES = [
    "Einstein equations remain not started.",
    "EFE route blocked by dynamics/action/variation.",
    "bounded prerequisite theorem packet allowed.",
    "exact-GR benchmark promotion requires protected authority.",
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
    plan_path = REPO_ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v15.md"
    moratorium_path = REPO_ROOT / "research_control/design/einstein_equation_route_moratorium_v1.md"
    bad_fixture_path = REPO_ROOT / "tests/fixtures/claim_language/efe_prerequisite_overread.md"
    valid_fixture_path = REPO_ROOT / "tests/fixtures/claim_language/efe_prerequisite_valid.md"
    test_path = REPO_ROOT / "tests/test_validate_claim_language.py"

    taxonomy_text = taxonomy_path.read_text(encoding="utf-8")
    contexts_text = contexts_path.read_text(encoding="utf-8")
    plan_text = plan_path.read_text(encoding="utf-8")
    plan_plain_text = plan_text.replace("`", "")
    moratorium_text = moratorium_path.read_text(encoding="utf-8")
    bad_fixture_text = bad_fixture_path.read_text(encoding="utf-8")
    valid_fixture_text = valid_fixture_path.read_text(encoding="utf-8")
    test_text = test_path.read_text(encoding="utf-8")

    bad_report = scan_text(linter, "research_control/current_frontier.md", bad_fixture_text)
    valid_report = scan_text(linter, "research_control/current_frontier.md", valid_fixture_text)
    current_frontier_report = linter.validate_paths(paths=["research_control/current_frontier.md"])
    plan_report = linter.validate_paths(paths=["implementations_plans/recommendations_implementation_plan_continue_task-v15.md"])
    taxonomy = linter.load_taxonomy()
    class_ids = {
        str(item.get("class_id"))
        for item in taxonomy.get("phrase_classes", [])
        if isinstance(item, dict)
    }
    efe_findings = class_findings(bad_report, CLASS_ID)
    plan_efe_hard_failures = [
        finding
        for finding in plan_report.get("findings", [])
        if finding.get("class_id") == CLASS_ID and str(finding.get("severity", "")).startswith("hard_fail_")
    ]
    coverage_pairs = [
        f'phrase: "{phrase}"' in taxonomy_text and f'class_id: "{CLASS_ID}"' in taxonomy_text
        for phrase in BAD_PHRASES
    ]

    checks = [
        {
            "id": "taxonomy_class_present",
            "passed": CLASS_ID in class_ids,
            "detail": "Taxonomy defines the premature EFE prerequisite overclaim class.",
        },
        {
            "id": "taxonomy_contains_required_bad_phrases",
            "passed": all(phrase in taxonomy_text for phrase in BAD_PHRASES) and all(coverage_pairs),
            "detail": "Taxonomy maps every P8-T02 bad phrase to the EFE prerequisite class.",
        },
        {
            "id": "bad_fixture_contains_required_phrases",
            "passed": all(phrase in bad_fixture_text for phrase in BAD_PHRASES),
            "detail": "Bad fixture contains every required P8-T02 premature EFE phrase.",
        },
        {
            "id": "bad_fixture_hard_fails_as_current_control",
            "passed": bad_report["status"] == "FAIL"
            and bad_report["hard_fail_count"] == len(BAD_PHRASES)
            and len(efe_findings) == len(BAD_PHRASES),
            "detail": "Bad fixture hard-fails when scanned as a current control surface.",
        },
        {
            "id": "passing_fixture_contains_scoped_wording",
            "passed": all(phrase in valid_fixture_text for phrase in PASSING_PHRASES),
            "detail": "Passing fixture contains the P8-T02 public-safe wording.",
        },
        {
            "id": "passing_fixture_passes",
            "passed": valid_report["status"] == "PASS" and valid_report["finding_count"] == 0,
            "detail": "Public-safe P8-T02 wording produces no linter findings.",
        },
        {
            "id": "unit_tests_include_efe_prerequisite_cases",
            "passed": "test_efe_prerequisite_overread_fixture_fails" in test_text
            and "test_efe_prerequisite_scoped_wording_fixture_passes" in test_text,
            "detail": "Unit tests exercise the bad and passing EFE prerequisite fixtures.",
        },
        {
            "id": "reviewed_contexts_cover_plan_bad_examples",
            "passed": "ALLOW-V15-P8-EFE-PREREQUISITE-PLAN-ROUTE-CONTEXT" in contexts_text
            and CLASS_ID in contexts_text
            and not plan_efe_hard_failures,
            "detail": "Reviewed context downgrades only the v15 plan's P8-T02 bad-example quotations.",
        },
        {
            "id": "plan_p8_t02_examples_implemented",
            "passed": all(phrase in plan_plain_text for phrase in BAD_PHRASES)
            and all(phrase in plan_plain_text for phrase in [item.rstrip(".") for item in PASSING_PHRASES]),
            "detail": "The P8-T02 plan examples are represented by implemented fixtures.",
        },
        {
            "id": "p8_t01_moratorium_remains_scoped",
            "passed": "direct EFE route from scoped evidence/precondition alone is blocked" in moratorium_text
            and "bounded prerequisite work allowed" in moratorium_text,
            "detail": "The P8-T01 moratorium source remains the scoped route-control basis.",
        },
        {
            "id": "current_frontier_no_hard_failures",
            "passed": current_frontier_report["status"] == "PASS"
            and current_frontier_report["hard_fail_count"] == 0,
            "detail": "Current frontier has no P8-T02 claim-language hard failures.",
        },
    ]

    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "status": status,
        "task_id": "RT-20260703-013",
        "checks": checks,
        "bad_fixture_hard_fail_count": bad_report["hard_fail_count"],
        "bad_fixture_efe_prerequisite_finding_count": len(efe_findings),
        "passing_fixture_finding_count": valid_report["finding_count"],
        "current_frontier_hard_fail_count": current_frontier_report["hard_fail_count"],
        "plan_efe_prerequisite_hard_fail_count": len(plan_efe_hard_failures),
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "matter_semantics_adoption_authorized": False,
            "detector_semantics_adoption_authorized": False,
            "coupling_law_adoption_authorized": False,
            "matter_coupling_authorized": False,
            "stress_energy_semantics_authorized": False,
            "stress_energy_tensor_authorized": False,
            "matter_action_authorized": False,
            "variation_principle_authorized": False,
            "einstein_equations_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
            "proof_authority": False,
        },
    }


def write_receipt(report: dict[str, Any]) -> None:
    if report["status"] != "PASS":
        return
    receipt_path = (
        REPO_ROOT
        / "research_control/tasks/RT-20260703-013/artifacts/p8_t02_efe_prerequisite_linter_fixtures_receipt.md"
    )
    receipt_path.write_text(
        "\n".join(
            [
                "<!-- authority: control -->",
                "",
                "# P8-T02 EFE Prerequisite Linter Fixtures Receipt",
                "",
                "## Status",
                "",
                "PASS.",
                "",
                "## Scope",
                "",
                "This receipt validates deterministic claim-language fixtures for premature EFE prerequisite overreads. It does not authorize source-law adoption, matter semantics, detector semantics, coupling-law adoption, matter coupling, stress-energy semantics, a stress-energy tensor, a matter action, a variation principle, Einstein equations, benchmark promotion, or completed derivation.",
                "",
                "## Evidence",
                "",
                f"- Bad fixture hard failures: {report['bad_fixture_hard_fail_count']}.",
                f"- Bad fixture EFE-prerequisite finding count: {report['bad_fixture_efe_prerequisite_finding_count']}.",
                f"- Passing fixture finding count: {report['passing_fixture_finding_count']}.",
                f"- Current frontier hard failures: {report['current_frontier_hard_fail_count']}.",
                f"- v15 plan P8-T02 hard failures after reviewed-context override: {report['plan_efe_prerequisite_hard_fail_count']}.",
                "",
                "## Claim Boundary",
                "",
                "The validator pass is a project-control receipt only. It is not proof authority and does not establish Einstein equations, benchmark promotion, or downstream GR derivation.",
                "",
            ]
        ),
        encoding="utf-8",
    )


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
    write_receipt(report)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
