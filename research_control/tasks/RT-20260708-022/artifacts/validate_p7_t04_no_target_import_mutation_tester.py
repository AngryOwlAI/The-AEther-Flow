#!/usr/bin/env python3
"""Validate the v18 P7-T04 no-target import mutation tester artifacts."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = (
    REPO_ROOT
    / "scripts/research_control/support_formalization/no_target_import_mutation_tester.py"
)
TEST_PATH = REPO_ROOT / "tests/test_no_target_import_mutation_tester.py"
TASK_DIR = REPO_ROOT / "research_control/tasks/RT-20260708-022"
ARTIFACT_DIR = TASK_DIR / "artifacts"
SPEC_PATH = ARTIFACT_DIR / "no_target_import_mutation_tester_spec_v1.md"
REPORT_PATH = ARTIFACT_DIR / "no_target_import_mutation_tester_report.json"
VALIDATION_REPORT_PATH = ARTIFACT_DIR / "p7_t04_no_target_import_mutation_tester_report.json"


def load_tester() -> Any:
    spec = importlib.util.spec_from_file_location(
        "no_target_import_mutation_tester", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import tester from {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check(checks: list[dict[str, str]], check_id: str, condition: bool, message: str) -> None:
    checks.append(
        {
            "check_id": check_id,
            "message": message,
            "status": "PASS" if condition else "FAIL",
        }
    )


def validate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    for path in (SCRIPT_PATH, TEST_PATH, SPEC_PATH, REPORT_PATH):
        check(checks, f"exists:{path.name}", path.exists(), f"{path} exists")

    tester = load_tester()
    generated = tester.generate_report()
    stored = json.loads(REPORT_PATH.read_text(encoding="utf-8")) if REPORT_PATH.exists() else {}
    spec_text = SPEC_PATH.read_text(encoding="utf-8") if SPEC_PATH.exists() else ""

    check(
        checks,
        "deterministic_report",
        stored == generated,
        "stored report matches tester output",
    )
    check(checks, "report_status", stored.get("status") == "PASS", "report status is PASS")
    check(checks, "support_only", stored.get("support_only") is True, "report is support-only")
    check(
        checks,
        "proof_authority_false",
        stored.get("proof_authority") is False,
        "proof_authority is false",
    )
    check(
        checks,
        "physics_promotion_false",
        stored.get("physics_promotion_authorized") is False,
        "physics promotion is not authorized",
    )
    check(
        checks,
        "source_law_adopted_false",
        stored.get("source_law_adopted") is False,
        "source_law_adopted is false",
    )
    check(
        checks,
        "validator_behavior_unchanged",
        stored.get("validator_behavior_changed") is False,
        "tester does not modify validator behavior",
    )
    check(
        checks,
        "base_safe_text_passes",
        stored.get("base_safe_text_status") == "PASS",
        "base safe text passes before mutation",
    )
    check(
        checks,
        "configured_mutations",
        tuple(stored.get("configured_mutations", [])) == tester.MUTATION_IDS,
        "configured mutations match the v18 P7-T04 plan",
    )

    mutation_results = stored.get("mutation_results", [])
    check(
        checks,
        "mutation_count",
        len(mutation_results) == len(tester.MUTATIONS),
        "one result exists per configured mutation",
    )
    for result in mutation_results:
        mutation_id = result.get("mutation_id", "unknown")
        check(
            checks,
            f"mutation_fail_closed:{mutation_id}",
            result.get("fail_closed") is True and result.get("observed_status") == "FAIL",
            f"{mutation_id} fails closed",
        )
        check(
            checks,
            f"mutation_expected_classes:{mutation_id}",
            result.get("missing_expected_linter_class_ids") == [],
            f"{mutation_id} has no missing expected linter classes",
        )
        check(
            checks,
            f"mutation_boundary:{mutation_id}",
            result.get("support_only") is True
            and result.get("proof_authority") is False
            and result.get("physics_promotion_authorized") is False,
            f"{mutation_id} preserves support-only boundary",
        )

    check(
        checks,
        "spec_support_only",
        "support-only validator tooling" in spec_text,
        "spec states support-only validator boundary",
    )
    check(
        checks,
        "spec_next_route",
        "P7-T05" in spec_text
        and "metric_use_ledger_tex_validator_support_only" in spec_text,
        "spec routes to P7-T05",
    )

    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "checks": checks,
        "failed_check_count": len(failed),
        "mutation_count": len(mutation_results),
        "physics_promotion_authorized": stored.get("physics_promotion_authorized"),
        "proof_authority": stored.get("proof_authority"),
        "status": "PASS" if not failed else "FAIL",
        "support_only": stored.get("support_only"),
        "tester_id": stored.get("tester_id"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate()
    if args.write_report:
        VALIDATION_REPORT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
