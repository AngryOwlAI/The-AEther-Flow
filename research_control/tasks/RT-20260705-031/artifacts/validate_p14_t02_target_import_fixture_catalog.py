#!/usr/bin/env python3
"""Validate the P14-T02 target-import attack fixture catalog."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
CATALOG_PATH = REPO_ROOT / "research_control/design/target_import_attack_fixture_catalog_v16.md"
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"

REQUIRED_BAD_CLASSES = {
    "target_metric_used_as_source_certificate",
    "lorentzian_signature_used_as_certificate_validity",
    "proper_time_used_as_source_readout",
    "detector_calibration_treated_as_source_label",
    "stress_energy_tensor_used_to_prove_matter_semantics",
    "matter_action_used_to_prove_coupling_law",
    "einstein_equations_used_as_upstream_premise",
    "benchmark_fit_used_as_source_evidence",
    "gate_chair_scoped_evidence_used_as_source_law",
    "validator_pass_used_as_proof",
    "generated_wiki_note_used_as_authority",
    "finite_local_model_rendered_as_universal_matter_coupling",
}

REQUIRED_GOOD_CLASSES = {
    "source_transport_certificate_with_no_target_guard",
    "scoped_evidence_precondition_wording",
    "target_import_fail_closed_wording",
    "detector_semantics_blocked_wording",
    "einstein_equations_not_started_wording",
    "benchmark_promotion_protected_wording",
}

BOUNDARY_FIELDS = {
    "proof_authority",
    "physics_promotion_authorized",
    "source_law_adopted",
    "matter_coupling_derived",
    "einstein_equations_derived",
    "completed_derivation_claimed",
    "validator_behavior_changed",
}


def load_linter():
    spec = importlib.util.spec_from_file_location("validate_claim_language", LINTER_PATH)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("claim-language linter loader not available")
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_catalog() -> dict[str, Any]:
    text = CATALOG_PATH.read_text(encoding="utf-8")
    match = re.search(r"```json\n(.*?)\n```", text, flags=re.DOTALL)
    if not match:
        raise ValueError("catalog JSON block not found")
    return json.loads(match.group(1))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_snippets(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    snippets: dict[str, str] = {}
    pattern = re.compile(
        r"<!-- fixture: (?P<key>[-_a-zA-Z0-9]+) -->\n(?P<body>.*?)\n<!-- /fixture -->",
        flags=re.DOTALL,
    )
    for match in pattern.finditer(text):
        snippets[match.group("key")] = match.group("body").strip()
    return snippets


def pass_check(name: str, detail: str) -> dict[str, str]:
    return {"name": name, "status": "PASS", "detail": detail}


def fail_check(name: str, detail: str) -> dict[str, str]:
    return {"name": name, "status": "FAIL", "detail": detail}


def scan_snippet(linter, taxonomy: dict[str, Any], snippet: str) -> dict[str, Any]:
    scanned_path = "research_control/current_frontier.md"
    return linter.report_dict(
        linter.scan_text_map(
            {scanned_path: snippet},
            taxonomy=taxonomy,
            reviewed_contexts=[],
            active_handoffs=set(),
        ),
        scanned_paths=[scanned_path],
    )


def validate_fixture_set(
    *,
    linter,
    taxonomy: dict[str, Any],
    fixture_set: dict[str, Any],
    required_classes: set[str],
    expected_mode: str,
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    checks: list[dict[str, str]] = []
    reports: list[dict[str, Any]] = []
    fixture_path = REPO_ROOT / str(fixture_set["path"])
    fixture_data = load_json(fixture_path)
    snippets = load_snippets(REPO_ROOT / fixture_data["snippet_path"])
    fixtures = fixture_data.get("fixtures", [])
    classes = [fixture.get("fixture_class") for fixture in fixtures]

    if fixture_data.get("mode") == expected_mode:
        checks.append(pass_check(f"{expected_mode}_fixture_set_mode", "mode matches catalog"))
    else:
        checks.append(fail_check(f"{expected_mode}_fixture_set_mode", "mode mismatch"))

    if set(classes) == required_classes and len(classes) == len(set(classes)):
        checks.append(pass_check(f"{expected_mode}_fixture_classes", "required classes present once"))
    else:
        checks.append(fail_check(f"{expected_mode}_fixture_classes", "required class set mismatch"))

    fixture_failures: list[str] = []
    linter_failures: list[str] = []
    for fixture in fixtures:
        fixture_id = str(fixture.get("fixture_id"))
        snippet_key = str(fixture.get("snippet_key"))
        if snippet_key not in snippets:
            fixture_failures.append(f"{fixture_id}: snippet missing")
            continue
        boundary = fixture.get("boundary", {})
        for field in BOUNDARY_FIELDS:
            if boundary.get(field) is not False:
                fixture_failures.append(f"{fixture_id}: boundary {field} not false")

        report = scan_snippet(linter, taxonomy, snippets[snippet_key])
        observed = {finding["class_id"] for finding in report["findings"]}
        expected_classes = set(fixture.get("expected_current_linter_class_ids", []))
        reports.append(
            {
                "fixture_id": fixture_id,
                "fixture_class": fixture.get("fixture_class"),
                "expected_status": fixture.get("expected_status"),
                "observed_status": report["status"],
                "expected_current_linter_class_ids": sorted(expected_classes),
                "observed_current_linter_class_ids": sorted(observed),
                "finding_count": report["finding_count"],
            }
        )
        if expected_mode == "bad":
            if report["status"] != "FAIL":
                linter_failures.append(f"{fixture_id}: expected FAIL, observed {report['status']}")
            missing = expected_classes - observed
            if missing:
                linter_failures.append(f"{fixture_id}: missing linter classes {sorted(missing)}")
        else:
            if report["status"] != "PASS" or report["finding_count"] != 0:
                linter_failures.append(
                    f"{fixture_id}: expected clean PASS, observed {report['status']}"
                )

    if fixture_failures:
        checks.append(fail_check(f"{expected_mode}_fixture_contracts", "; ".join(fixture_failures)))
    else:
        checks.append(pass_check(f"{expected_mode}_fixture_contracts", "boundary contracts hold"))

    if linter_failures:
        checks.append(fail_check(f"{expected_mode}_linter_results", "; ".join(linter_failures)))
    else:
        checks.append(pass_check(f"{expected_mode}_linter_results", "linter expectations satisfied"))

    return checks, reports


def validate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    fixture_reports: list[dict[str, Any]] = []
    catalog = load_catalog()

    if set(catalog.get("required_bad_fixture_classes", [])) == REQUIRED_BAD_CLASSES:
        checks.append(pass_check("required_bad_fixture_classes_declared", "all bad classes declared"))
    else:
        checks.append(fail_check("required_bad_fixture_classes_declared", "bad class set mismatch"))

    if set(catalog.get("required_good_fixture_classes", [])) == REQUIRED_GOOD_CLASSES:
        checks.append(pass_check("required_good_fixture_classes_declared", "all good classes declared"))
    else:
        checks.append(fail_check("required_good_fixture_classes_declared", "good class set mismatch"))

    catalog_boundary = catalog.get("claim_boundary", {})
    boundary_failures = [
        field for field in BOUNDARY_FIELDS if catalog_boundary.get(field) is not False
    ]
    if boundary_failures:
        checks.append(fail_check("catalog_boundary", f"non-false fields: {boundary_failures}"))
    else:
        checks.append(pass_check("catalog_boundary", "catalog boundary denies promotion/change"))

    linter = load_linter()
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    sets_by_mode = {item["mode"]: item for item in catalog.get("fixture_sets", [])}
    for mode, required in (("bad", REQUIRED_BAD_CLASSES), ("good", REQUIRED_GOOD_CLASSES)):
        if mode not in sets_by_mode:
            checks.append(fail_check(f"{mode}_fixture_set_declared", "missing from catalog"))
            continue
        checks.append(pass_check(f"{mode}_fixture_set_declared", "fixture set declared"))
        set_checks, set_reports = validate_fixture_set(
            linter=linter,
            taxonomy=taxonomy,
            fixture_set=sets_by_mode[mode],
            required_classes=required,
            expected_mode=mode,
        )
        checks.extend(set_checks)
        fixture_reports.extend(set_reports)

    failed = [check for check in checks if check["status"] != "PASS"]
    return {
        "validator_id": "p14_t02_target_import_fixture_catalog_validator",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "catalog_path": CATALOG_PATH.relative_to(REPO_ROOT).as_posix(),
        "fixture_report_count": len(fixture_reports),
        "fixture_reports": fixture_reports,
        "checks": checks,
        "claim_boundary": {
            "proof_authority": False,
            "physics_promotion_authorized": False,
            "source_law_adopted": False,
            "matter_coupling_derived": False,
            "einstein_equations_derived": False,
            "completed_derivation_claimed": False,
            "validator_behavior_changed": False
        }
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON report path.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    args = parser.parse_args(argv)

    report = validate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['validator_id']}: {report['status']}")
        for check in report["checks"]:
            print(f"- {check['status']} {check['name']}: {check['detail']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

