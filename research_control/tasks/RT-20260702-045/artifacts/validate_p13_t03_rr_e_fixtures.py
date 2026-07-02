#!/usr/bin/env python3
"""Validate the bounded P13-T03 RR_E overread fixture packet."""

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


def build_report() -> dict[str, Any]:
    linter = load_linter()
    fixture_path = REPO_ROOT / "tests/fixtures/claim_language/rr_e_overread.md"
    examples_path = REPO_ROOT / "research_control/design/scoped_claim_language_examples.md"
    taxonomy_path = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"

    fixture_text = fixture_path.read_text(encoding="utf-8")
    fixture_report = scan_text(linter, "research_control/current_frontier.md", fixture_text)
    class_ids = [finding["class_id"] for finding in fixture_report.get("findings", [])]
    corrected_text = (
        "RR_E records R0 and R1 remain separated unless an explicit source transport, "
        "source invariance, or source factorization certificate for declared object F "
        "identifies them. A transported pair with certificate is scoped source-side "
        "evidence/precondition only; it is not source-law adoption, not unrestricted "
        "RR_E irrelevance, not detector semantics, not g_eff scope expansion, and not "
        "benchmark promotion.\n"
    )
    corrected_report = scan_text(linter, "research_control/current_frontier.md", corrected_text)

    examples_text = examples_path.read_text(encoding="utf-8")
    taxonomy_text = taxonomy_path.read_text(encoding="utf-8")
    required_fixture_phrases = [
        "same-support different-RR_E records identified without certificate",
        "RR_E identified without source transport certificate",
        "RR_E identified without source invariance certificate",
        "RR_E identified without source factorization certificate",
        "RR_E collapses by detector semantics",
        "g_eff collapses RR_E",
        "benchmark behavior collapses RR_E",
        "process authority collapses RR_E",
        "support-only formalization collapses RR_E",
        "RR_ETransportCompletenessOrInvarianceLaw_v1 adopted",
        "scoped RR_E evidence/precondition adopts source law",
        "RR_E support formalization proves source law adoption",
    ]
    required_examples_phrases = [
        "Support-Formalization And Certificate Collapse Overread",
        "same-support different-RR_E records identified without certificate",
        "transported pair with certificate is scoped source-side",
        "fails closed to separation or obstruction",
    ]
    required_taxonomy_phrases = [
        "same-support different-RR_E records identified without certificate",
        "RR_E identified without source transport certificate",
        "RR_E identified without source invariance certificate",
        "RR_E identified without source factorization certificate",
        "g_eff collapses RR_E",
        "benchmark behavior collapses RR_E",
        "process authority collapses RR_E",
        "support-only formalization collapses RR_E",
        "scoped RR_E evidence/precondition adopts source law",
        "RR_E support formalization proves source law adoption",
    ]

    checks = [
        {
            "id": "fixture_contains_required_overreads",
            "passed": all(phrase in fixture_text for phrase in required_fixture_phrases),
            "detail": "RR_E fixture contains every P13-T03 required overread case.",
        },
        {
            "id": "fixture_hard_fails",
            "passed": fixture_report["status"] == "FAIL"
            and fixture_report["hard_fail_count"] >= 12
            and class_ids.count("unrestricted_rr_e_irrelevance_overclaim") >= 9
            and class_ids.count("rr_e_transport_source_law_overclaim") >= 3,
            "detail": "RR_E overread fixture produces hard failures on a current control surface.",
        },
        {
            "id": "certificate_scoped_wording_passes",
            "passed": corrected_report["status"] == "PASS" and corrected_report["finding_count"] == 0,
            "detail": "Certificate-scoped RR_E wording produces no claim-language findings.",
        },
        {
            "id": "examples_pack_contains_before_after",
            "passed": all(phrase in examples_text for phrase in required_examples_phrases),
            "detail": "Examples pack contains RR_E bad wording and corrected wording.",
        },
        {
            "id": "taxonomy_contains_required_patterns",
            "passed": all(phrase in taxonomy_text for phrase in required_taxonomy_phrases),
            "detail": "Taxonomy stores P13-T03 RR_E overread patterns.",
        },
    ]
    status = "PASS" if all(check["passed"] for check in checks) else "FAIL"
    return {
        "status": status,
        "task_id": "RT-20260702-045",
        "checks": checks,
        "fixture_hard_fail_count": fixture_report["hard_fail_count"],
        "fixture_finding_classes": class_ids,
        "corrected_finding_count": corrected_report["finding_count"],
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "rr_e_transport_law_adoption_authorized": False,
            "unrestricted_rr_e_irrelevance_authorized": False,
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
