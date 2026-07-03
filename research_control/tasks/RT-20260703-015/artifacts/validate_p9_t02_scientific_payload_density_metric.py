#!/usr/bin/env python3
"""Validate the v15 P9-T02 scientific payload density metric transaction."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = REPO_ROOT / "scripts" / "research_control" / "report_scientific_payload_density.py"
SPEC_PATH = REPO_ROOT / "research_control" / "tasks" / "RT-20260703-015" / "artifacts" / "scientific_payload_density_metric_spec_v1.md"
TEST_PATH = REPO_ROOT / "tests" / "test_report_scientific_payload_density.py"


def load_reporter() -> Any:
    script_dir = SCRIPT_PATH.parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
    spec = importlib.util.spec_from_file_location("report_scientific_payload_density", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check(condition: bool, check_id: str, message: str) -> dict[str, Any]:
    return {"check_id": check_id, "status": "PASS" if condition else "FAIL", "message": message}


def validate(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    reporter = load_reporter()
    report = reporter.build_report(repo_root)
    spec_text = SPEC_PATH.read_text(encoding="utf-8") if SPEC_PATH.exists() else ""

    checks = [
        check(SPEC_PATH.exists(), "spec_exists", "Required metric specification exists."),
        check(SCRIPT_PATH.exists(), "script_exists", "Dedicated metric report script exists."),
        check(TEST_PATH.exists(), "focused_tests_exist", "Focused unit test module exists."),
        check(
            "operational diagnostics only" in spec_text,
            "spec_boundary",
            "Specification states operational diagnostics only.",
        ),
        check(
            all(label in spec_text for label in reporter.PAYLOAD_CLASS_LABELS.values()),
            "spec_payload_classes",
            "Specification lists every required payload class label.",
        ),
        check(
            report["authority_boundary"]["metrics_are_operational_diagnostics_only"] is True
            and report["authority_boundary"]["physics_claim_promotion_authorized"] is False,
            "report_boundary",
            "Report declares non-promotional operational authority boundary.",
        ),
        check(
            report["metric_can_report_by"] == ["phase", "task_family", "role", "milestone"],
            "report_dimensions",
            "Report exposes phase task-family role and milestone groupings.",
        ),
        check(
            all(key in report for key in ("by_phase", "by_task_family", "by_role", "by_milestone")),
            "grouping_outputs",
            "Report includes all required grouping outputs.",
        ),
        check(
            report["overall"]["task_count"] > 0,
            "tracked_records_read",
            "Report reads at least one tracked completed AgentJob.",
        ),
    ]
    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    return {
        "validator_id": "p9_t02_scientific_payload_density_metric_validator",
        "status": status,
        "checks": checks,
        "metric_summary": {
            "task_count": report["overall"]["task_count"],
            "mathematical_payload_item_count": report["overall"]["mathematical_payload_item_count"],
            "process_only_item_count": report["overall"]["process_only_item_count"],
            "payload_density": report["overall"]["payload_density"],
            "task_payload_density": report["overall"]["task_payload_density"],
        },
        "authority_boundary": report["authority_boundary"],
    }


def render_receipt(result: dict[str, Any]) -> str:
    lines = [
        "# P9-T02 Scientific Payload Density Metric Receipt",
        "",
        f"Status: `{result['status']}`",
        "",
        "The metric is operational diagnostics only. It is not physics proof, source-law adoption, benchmark promotion, or completed-derivation authority.",
        "",
        "## Checks",
        "",
    ]
    for item in result["checks"]:
        lines.append(f"- `{item['check_id']}`: `{item['status']}` - {item['message']}")
    lines.extend(
        [
            "",
            "## Metric Summary",
            "",
            f"- Tasks read: `{result['metric_summary']['task_count']}`",
            f"- Mathematical payload items: `{result['metric_summary']['mathematical_payload_item_count']}`",
            f"- Process-only items: `{result['metric_summary']['process_only_item_count']}`",
            f"- Payload density: `{result['metric_summary']['payload_density']}`",
            f"- Task payload density: `{result['metric_summary']['task_payload_density']}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="JSON report output path.")
    parser.add_argument("--json", action="store_true", help="Print compact JSON summary.")
    args = parser.parse_args(argv)

    result = validate(REPO_ROOT)
    output_path = Path(args.output)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt_path = output_path.with_name("p9_t02_scientific_payload_density_metric_receipt.md")
    receipt_path.write_text(render_receipt(result), encoding="utf-8")
    if args.json:
        print(json.dumps({"status": result["status"], "checks": len(result["checks"])}))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
