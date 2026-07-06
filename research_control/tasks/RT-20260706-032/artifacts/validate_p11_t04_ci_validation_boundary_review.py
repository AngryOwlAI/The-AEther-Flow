"""Validate the v17 P11-T04 CI validation boundary red-team review."""

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


TASK_DIR = Path("research_control/tasks/RT-20260706-032")
ARTIFACT = TASK_DIR / "artifacts/ci_validation_boundary_review_v1.md"
REPORT = TASK_DIR / "artifacts/p11_t04_ci_validation_boundary_review_report.json"


def build_report() -> dict[str, object]:
    global_result = validate_review_file(ARTIFACT)
    data = strict_yaml.load(ARTIFACT)
    issues: list[str] = []

    if data.get("p11_review_result") != "pass_no_repair_required":
        issues.append("p11_review_result must be pass_no_repair_required")
    if data.get("repair_required") is not False:
        issues.append("repair_required must be false")
    if data.get("recommended_next_route") != "v17_p12_t01_ai_research_agent_metrics_taxonomy":
        issues.append("recommended_next_route must point to P12-T01")
    if data.get("physics_promotion_authorized") is not False:
        issues.append("physics_promotion_authorized must be false")

    required_sources = {
        "CONTRIBUTING.md",
        ".github/workflows/project-control-validation.yml",
        "output/validation_summary.md",
        "output/validation_summary.json",
        "scripts/research_control/collect_validation_artifacts.py",
    }
    reviewed_sources = set(data.get("reviewed_source_paths", []))
    missing_sources = sorted(required_sources - reviewed_sources)
    if missing_sources:
        issues.append(f"missing required reviewed sources: {missing_sources}")

    done = data.get("done_criteria_status", {})
    if not isinstance(done, dict):
        issues.append("done_criteria_status must be a map")
    else:
        if done.get("ci_docs_say_validation_not_physics_proof") is not True:
            issues.append("CI docs proof-boundary done criterion must be true")
        if done.get("validation_artifacts_do_not_claim_proof_authority") is not True:
            issues.append("validation artifact proof-authority done criterion must be true")
        if done.get("blocking_repair_required") is not False:
            issues.append("blocking_repair_required must be false")

    statuses = [
        item.get("status")
        for item in data.get("review_questions", [])
        if isinstance(item, dict)
    ]
    if not statuses or not all(str(status).startswith("pass") for status in statuses):
        issues.append("all review questions must pass or pass_with_advisory")

    surfaces = data.get("per_surface_findings", [])
    if not isinstance(surfaces, list) or len(surfaces) < 5:
        issues.append("per_surface_findings must include CONTRIBUTING workflow validation summaries and collector")
    else:
        for surface in surfaces:
            if not isinstance(surface, dict):
                issues.append("each per_surface_finding must be a map")
                continue
            if surface.get("overclaim_found") is not False:
                issues.append(f"{surface.get('surface_id')} overclaim_found must be false")
            if surface.get("proof_authority_claim_found") is not False:
                issues.append(f"{surface.get('surface_id')} proof_authority_claim_found must be false")

    if data.get("workflow_success_disregarded_as_evidence") is not True:
        issues.append("workflow_success_disregarded_as_evidence must be true")
    if data.get("validator_success_disregarded_as_evidence") is not True:
        issues.append("validator_success_disregarded_as_evidence must be true")
    if data.get("registry_status_disregarded_as_proof") is not True:
        issues.append("registry_status_disregarded_as_proof must be true")

    status = "PASS" if not issues else "FAIL"
    return {
        "task_id": "RT-20260706-032",
        "plan_task_id": "P11-T04",
        "status": status,
        "artifact_path": ARTIFACT.as_posix(),
        "global_red_team_validator": global_result,
        "issues": issues,
        "review_result": data.get("p11_review_result"),
        "repair_required": data.get("repair_required"),
        "recommended_next_route": data.get("recommended_next_route"),
        "done_criteria_status": data.get("done_criteria_status"),
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

