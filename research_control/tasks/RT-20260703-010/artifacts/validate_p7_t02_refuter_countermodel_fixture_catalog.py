#!/usr/bin/env python3
"""Validate the P7-T02 Refuter countermodel fixture catalog."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
CATALOG_PATH = REPO_ROOT / "research_control/design/refuter_countermodel_fixture_catalog_v1.md"
FIXTURE_ROOT = REPO_ROOT / "tests/fixtures/research_control/refuter_countermodel"
LINTER_PATH = REPO_ROOT / "scripts/project_control/validate_claim_language.py"
TAXONOMY_PATH = REPO_ROOT / "research_control/design/claim_language_linter_taxonomy.yaml"

REQUIRED_CLASSES = {
    "finite_rr_e_separation_witness",
    "missing_certificate_witness",
    "malformed_certificate_witness",
    "detector_semantics_import_witness",
    "target_metric_import_witness",
    "finite_local_globalization_failure",
    "source_extension_as_derivation_overread",
    "scoped_evidence_as_adoption_overread",
}

REQUIRED_OBSTRUCTION_FIELDS = {
    "obstruction_id",
    "target_claim",
    "target_milestone",
    "failed_premise",
    "minimal_countermodel_available",
    "countermodel_path",
    "countermodel_scope",
    "certificate_gap",
    "source_extension_repair_possible",
    "global_no_go_claim_authorized",
    "future_source_extension_impossibility_authorized",
    "freeze_criteria_status",
    "route_cycle_control",
    "forbidden_conclusions",
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


def load_fixture(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pass_check(name: str, detail: str) -> dict[str, str]:
    return {"name": name, "status": "PASS", "detail": detail}


def fail_check(name: str, detail: str) -> dict[str, str]:
    return {"name": name, "status": "FAIL", "detail": detail}


def validate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    catalog = load_catalog()
    fixture_items = catalog.get("fixtures", [])
    catalog_classes = [item.get("fixture_class") for item in fixture_items]

    if set(catalog.get("required_fixture_classes", [])) == REQUIRED_CLASSES:
        checks.append(pass_check("required_fixture_classes_declared", "all P7-T02 classes declared"))
    else:
        checks.append(fail_check("required_fixture_classes_declared", "required class set mismatch"))

    if set(catalog_classes) == REQUIRED_CLASSES and len(catalog_classes) == len(set(catalog_classes)):
        checks.append(pass_check("catalog_fixture_classes_unique", "all fixture classes present once"))
    else:
        checks.append(fail_check("catalog_fixture_classes_unique", "fixture classes missing or duplicated"))

    linter = load_linter()
    taxonomy = linter.load_taxonomy(TAXONOMY_PATH)
    fixture_failures: list[str] = []
    linter_failures: list[str] = []

    for item in fixture_items:
        path_text = str(item.get("path", ""))
        path = REPO_ROOT / path_text
        if not path.is_file():
            fixture_failures.append(f"{path_text}: missing")
            continue
        fixture = load_fixture(path)
        if fixture.get("fixture_id") != item.get("fixture_id"):
            fixture_failures.append(f"{path_text}: fixture_id mismatch")
        if fixture.get("fixture_class") != item.get("fixture_class"):
            fixture_failures.append(f"{path_text}: fixture_class mismatch")
        record = fixture.get("refuter_obstruction_record", {})
        if set(record) != REQUIRED_OBSTRUCTION_FIELDS:
            fixture_failures.append(f"{path_text}: obstruction field set mismatch")
        if record.get("countermodel_path") != path_text:
            fixture_failures.append(f"{path_text}: countermodel_path mismatch")
        if record.get("global_no_go_claim_authorized") is not False:
            fixture_failures.append(f"{path_text}: global no-go flag not false")
        if record.get("future_source_extension_impossibility_authorized") is not False:
            fixture_failures.append(f"{path_text}: future source-extension impossibility flag not false")
        if not record.get("forbidden_conclusions"):
            fixture_failures.append(f"{path_text}: forbidden_conclusions empty")
        boundary = fixture.get("boundary", {})
        for field in (
            "proof_authority",
            "physics_promotion_authorized",
            "source_law_adopted",
            "matter_coupling_derived",
            "einstein_equations_derived",
            "completed_derivation_claimed",
        ):
            if boundary.get(field) is not False:
                fixture_failures.append(f"{path_text}: boundary {field} not false")

        linter_block = fixture.get("claim_language_linter", {})
        snippets = linter_block.get("negative_snippets", [])
        expected = set(linter_block.get("expected_class_ids", []))
        if not snippets or not expected:
            linter_failures.append(f"{path_text}: missing linter snippets or expected class ids")
            continue
        report = linter.report_dict(
            linter.scan_text_map(
                {
                    "tests/fixtures/claim_language/refuter_countermodel_fixture.md": "\n".join(
                        snippets
                    )
                },
                taxonomy=taxonomy,
                reviewed_contexts=[],
                active_handoffs=set(),
            ),
            scanned_paths=["tests/fixtures/claim_language/refuter_countermodel_fixture.md"],
        )
        observed = {finding["class_id"] for finding in report["findings"]}
        missing = expected - observed
        if missing:
            linter_failures.append(f"{path_text}: missing linter classes {sorted(missing)}")

    if fixture_failures:
        checks.append(fail_check("fixture_contracts", "; ".join(fixture_failures)))
    else:
        checks.append(pass_check("fixture_contracts", "all fixture records match catalog contract"))

    actual_paths = sorted(path.relative_to(REPO_ROOT).as_posix() for path in FIXTURE_ROOT.glob("*.json"))
    if len(actual_paths) == len(REQUIRED_CLASSES):
        checks.append(pass_check("fixture_file_count", "eight fixture JSON files present"))
    else:
        checks.append(fail_check("fixture_file_count", f"expected 8 fixture files, found {len(actual_paths)}"))

    if linter_failures:
        checks.append(fail_check("claim_language_linter_usability", "; ".join(linter_failures)))
    else:
        checks.append(
            pass_check(
                "claim_language_linter_usability",
                "current linter detects expected class IDs for all fixture snippets",
            )
        )

    failed = [check for check in checks if check["status"] != "PASS"]
    return {
        "validator_id": "p7_t02_refuter_countermodel_fixture_catalog_validator",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "catalog_path": CATALOG_PATH.relative_to(REPO_ROOT).as_posix(),
        "fixture_root": FIXTURE_ROOT.relative_to(REPO_ROOT).as_posix(),
        "checks": checks,
        "claim_boundary": {
            "proof_authority": False,
            "physics_promotion_authorized": False,
            "source_law_adopted": False,
            "matter_coupling_derived": False,
            "einstein_equations_derived": False,
            "completed_derivation_claimed": False,
            "global_no_go_claim_authorized": False,
            "future_source_extension_impossibility_authorized": False
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
