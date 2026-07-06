"""Validate the v17 P9-T04 proof-state dashboard red-team review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.research_control import strict_yaml
from scripts.research_control.validate_red_team_review_artifact import validate_review_file


TASK_DIR = Path("research_control/tasks/RT-20260706-024")
ARTIFACT = TASK_DIR / "artifacts/proof_state_dashboard_red_team_review_v1.md"
REPORT = TASK_DIR / "artifacts/p9_t04_proof_state_dashboard_red_team_review_report.json"


def build_report() -> dict[str, object]:
    global_result = validate_review_file(ARTIFACT)
    data = strict_yaml.load(ARTIFACT)
    issues: list[str] = []

    if data.get("p9_review_result") != "pass_no_repair_required":
        issues.append("p9_review_result must be pass_no_repair_required")
    if data.get("repair_required") is not False:
        issues.append("repair_required must be false")
    if data.get("recommended_next_route") != "v17_p10_t01_research_control_task_index_schema":
        issues.append("recommended_next_route must point to P10-T01")
    if data.get("physics_promotion_authorized") is not False:
        issues.append("physics_promotion_authorized must be false")

    required_sources = {
        "github-facing/proof-state-dashboard-explainer.md",
        "html/proof-state-dashboard-explainer.html",
        "markdown/html-explainer-specs/proof-state-dashboard-explainer.spec.md",
        "markdown/publication-briefs/proof-state-dashboard.publication-brief.md",
        "README.md",
    }
    reviewed_sources = set(data.get("reviewed_source_paths", []))
    missing_sources = sorted(required_sources - reviewed_sources)
    if missing_sources:
        issues.append(f"missing required reviewed sources: {missing_sources}")

    statuses = [
        item.get("status")
        for item in data.get("review_questions", [])
        if isinstance(item, dict)
    ]
    if not statuses or not all(str(status).startswith("pass") for status in statuses):
        issues.append("all review questions must pass or pass_with_advisory")

    surfaces = data.get("per_surface_findings", [])
    if not isinstance(surfaces, list) or len(surfaces) < 3:
        issues.append("per_surface_findings must include dashboard Markdown HTML and README")
    else:
        for surface in surfaces:
            if not isinstance(surface, dict):
                issues.append("each per_surface_finding must be a map")
                continue
            if surface.get("overclaim_found") is not False:
                issues.append(f"{surface.get('surface_id')} overclaim_found must be false")
            if surface.get("underclaim_found") is not False:
                issues.append(f"{surface.get('surface_id')} underclaim_found must be false")

    status = "PASS" if not issues else "FAIL"
    return {
        "task_id": "RT-20260706-024",
        "plan_task_id": "P9-T04",
        "status": status,
        "artifact_path": ARTIFACT.as_posix(),
        "global_red_team_validator": global_result,
        "issues": issues,
        "review_result": data.get("p9_review_result"),
        "repair_required": data.get("repair_required"),
        "recommended_next_route": data.get("recommended_next_route"),
        "physics_promotion_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
