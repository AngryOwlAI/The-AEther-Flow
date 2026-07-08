#!/usr/bin/env python3
"""Validate the v18 P7-T03 closure countermodel generator packet."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = (
    REPO_ROOT
    / "scripts"
    / "research_control"
    / "support_formalization"
    / "closure_countermodel_generator.py"
)
TEST_PATH = REPO_ROOT / "tests" / "test_closure_countermodel_generator.py"
TASK_ROOT = REPO_ROOT / "research_control" / "tasks" / "RT-20260708-021"
ARTIFACTS = TASK_ROOT / "artifacts"
SPEC_PATH = ARTIFACTS / "closure_countermodel_generator_spec_v1.md"
REPORT_PATH = ARTIFACTS / "closure_countermodel_generator_report.json"
OUTPUT_PATH = ARTIFACTS / "p7_t03_closure_countermodel_generator_report.json"


@dataclass(frozen=True)
class Check:
    check_id: str
    status: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "check_id": self.check_id,
            "message": self.message,
            "status": self.status,
        }


def load_generator():
    spec = importlib.util.spec_from_file_location("closure_countermodel_generator", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check(condition: bool, check_id: str, message: str) -> Check:
    return Check(check_id, "PASS" if condition else "FAIL", message)


def validate() -> dict[str, Any]:
    generator = load_generator()
    checks: list[Check] = []
    for path in (SCRIPT_PATH, TEST_PATH, SPEC_PATH, REPORT_PATH):
        checks.append(check(path.exists(), f"exists:{path.name}", f"{path} exists"))

    bundle = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    generated = generator.generate_bundle()
    checks.extend(
        [
            check(bundle == generated, "deterministic_report", "stored report matches generator output"),
            check(bundle["support_only"] is True, "support_only", "bundle is support-only"),
            check(bundle["proof_authority"] is False, "proof_authority_false", "proof_authority is false"),
            check(
                bundle["physics_promotion_authorized"] is False,
                "physics_promotion_false",
                "physics promotion is not authorized",
            ),
            check(
                set(bundle["configured_modes"]) == set(generator.MODES),
                "configured_modes",
                "all configured modes are present",
            ),
            check(
                bundle["case_count"] == len(generator.MODES),
                "case_count",
                "case count matches generator mode count",
            ),
        ]
    )

    case_modes = {case["mode"]: case for case in bundle["cases"]}
    for mode, expected_status in generator.EXPECTED_CHECKER_STATUS.items():
        case = case_modes.get(mode, {})
        report = generator.orbit_checker.check_fixture(case.get("record", {}))
        checks.append(
            check(
                report.status == expected_status,
                f"checker_status:{mode}",
                f"{mode} yields {expected_status}",
            )
        )
        checks.append(
            check(
                case.get("support_only") is True and case.get("proof_authority") is False,
                f"case_boundary:{mode}",
                f"{mode} case preserves support-only boundary",
            )
        )

    retainh = case_modes["RetainH_required"]["record"]["primitive_requirements"]
    genh = case_modes["GenH_required"]["record"]["primitive_requirements"]
    checks.extend(
        [
            check(
                retainh["retainh"]["status"] == "required"
                and retainh["retainh"]["adopted"] is False,
                "retainh_required_no_adoption",
                "RetainH mode requires RetainH without adoption",
            ),
            check(
                genh["genh"]["status"] == "required" and genh["genh"]["adopted"] is False,
                "genh_required_no_adoption",
                "GenH mode requires GenH without adoption",
            ),
        ]
    )

    spec_text = SPEC_PATH.read_text(encoding="utf-8")
    checks.extend(
        [
            check("support-only" in spec_text, "spec_support_only", "spec states support-only"),
            check("P7-T04" in spec_text, "spec_next_route", "spec routes to P7-T04"),
        ]
    )

    failed = [item for item in checks if item.status != "PASS"]
    return {
        "checks": [item.to_dict() for item in checks],
        "failed_check_count": len(failed),
        "generator_id": generator.GENERATOR_ID,
        "mode_count": len(generator.MODES),
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "status": "PASS" if not failed else "FAIL",
        "support_only": True,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args(argv)
    report = validate()
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.write_report:
        OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
