#!/usr/bin/env python3
"""Validate the v15 P9-T03 physics-progress metrics integration packet."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = REPO_ROOT / "scripts" / "research_control" / "report_physics_progress_metrics.py"
SAMPLE_JSON_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260703-016"
    / "artifacts"
    / "p9_t03_physics_progress_metrics_sample.json"
)
SAMPLE_MARKDOWN_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260703-016"
    / "artifacts"
    / "p9_t03_physics_progress_metrics_sample.md"
)
RECEIPT_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260703-016"
    / "artifacts"
    / "p9_t03_physics_progress_metrics_integration_receipt.md"
)


def load_reporter() -> Any:
    script_dir = SCRIPT_PATH.parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
    spec = importlib.util.spec_from_file_location("report_physics_progress_metrics", SCRIPT_PATH)
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
    metrics = report["metrics"]
    integration = metrics.get("physics_progress_integration_metrics", {})
    separate_counts = integration.get("separate_packet_counts", {})
    payload_summary = integration.get("payload_density_summary", {})

    checks = [
        check(SCRIPT_PATH.exists(), "script_exists", "Metrics report script exists."),
        check(
            isinstance(integration, dict) and integration.get("status") == "pass",
            "integration_section_present",
            "Report exposes a passing physics-progress integration section.",
        ),
        check(
            isinstance(integration.get("distance_delta"), dict)
            and isinstance(integration["distance_delta"].get("effect_counts"), dict),
            "distance_delta_integrated",
            "Integration section includes distance-delta effect counts.",
        ),
        check(
            all(
                isinstance(separate_counts.get(key), int)
                for key in (
                    "candidate_packet_count",
                    "obstruction_packet_count",
                    "freeze_packet_count",
                    "theorem_packet_count",
                    "process_only_packet_count",
                )
            ),
            "separate_packet_counts",
            "Integration section counts candidates obstructions freezes theorem packets and process-only packets separately.",
        ),
        check(
            isinstance(payload_summary, dict)
            and "payload_density" in payload_summary
            and "process_only_task_count" in payload_summary,
            "payload_density_integrated",
            "Integration section includes payload-density summary fields.",
        ),
        check(
            integration.get("not_physics_proof") is True
            and integration.get("physics_claim_promotion_authorized") is False,
            "integration_boundary",
            "Integration section states it is not physics proof or promotion authority.",
        ),
        check(
            report["authority_boundary"].get("metrics_report_not_physics_proof") is True
            and report["authority_boundary"].get("physics_claim_promotion_authorized") is False,
            "report_boundary",
            "Report-level authority boundary blocks physics-proof overread.",
        ),
        check(
            metrics["metric_separation_guard"]["status"] == "pass",
            "metric_separation_guard",
            "Operational integration did not contaminate scientific_progress_metrics.",
        ),
    ]
    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    sample = {
        "schema_id": "p9_t03_physics_progress_metrics_integration_sample_v1",
        "authority_boundary": report["authority_boundary"],
        "physics_progress_integration_metrics": integration,
        "metric_separation_guard": metrics["metric_separation_guard"],
    }
    SAMPLE_JSON_PATH.write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    SAMPLE_MARKDOWN_PATH.write_text(reporter.render_markdown(report), encoding="utf-8")

    return {
        "validator_id": "p9_t03_physics_progress_metrics_integration_validator",
        "status": status,
        "checks": checks,
        "sample_json_path": str(SAMPLE_JSON_PATH.relative_to(repo_root)),
        "sample_markdown_path": str(SAMPLE_MARKDOWN_PATH.relative_to(repo_root)),
        "integration_summary": integration,
    }


def render_receipt(result: dict[str, Any]) -> str:
    lines = [
        "# P9-T03 Physics-Progress Metrics Integration Receipt",
        "",
        f"Status: `{result['status']}`",
        "",
        "The integrated metrics are operational diagnostics only. They are not physics proof, source-law adoption, benchmark promotion, or completed-derivation authority.",
        "",
        "## Checks",
        "",
    ]
    for item in result["checks"]:
        lines.append(f"- `{item['check_id']}`: `{item['status']}` - {item['message']}")
    lines.extend(
        [
            "",
            "## Samples",
            "",
            f"- JSON: `{result['sample_json_path']}`",
            f"- Markdown: `{result['sample_markdown_path']}`",
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
    RECEIPT_PATH.write_text(render_receipt(result), encoding="utf-8")
    if args.json:
        print(json.dumps({"status": result["status"], "checks": len(result["checks"])}))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
