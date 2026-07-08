#!/usr/bin/env python3
"""Validate v18 P9-T05 public cognitive-load red-team outputs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.research_control import strict_yaml  # noqa: E402
from scripts.research_control.validate_red_team_review_artifact import (  # noqa: E402
    validate_review_file,
)


TASK_ID = "RT-20260708-036"
JOB_ID = "AJ-RT-20260708-036-001"
ARTIFACT = (
    ROOT
    / "research_control/tasks/RT-20260708-036/artifacts/"
    / "public_cognitive_load_red_team_review_v1.md"
)
REPORT = (
    ROOT
    / "research_control/tasks/RT-20260708-036/artifacts/"
    / "p9_t05_public_cognitive_load_red_team_report.json"
)
ALLOWED_RESULTS = {"pass", "repair_required", "fail_closed"}
REQUIRED_DONE_CRITERIA = {
    "review_result_allowed",
    "can_identify_what_exists",
    "can_identify_exact_scope",
    "can_identify_what_does_not_follow",
    "can_identify_next_burden",
    "avoids_public_overclaim",
    "caveat_fog_not_blocking",
    "generated_surfaces_not_authoritative",
    "pass_routes_to_p10_t01",
}
PUBLIC_FILES = [
    "README.md",
    "research_control/current_frontier.md",
    "wiki/indexes/compact_current_frontier_v16.md",
]
PUBLIC_DIRS = [
    "github-facing",
    "markdown/publication-briefs",
    "markdown/html-explainer-specs",
]
REQUIRED_SURFACE_PHRASES = {
    "README.md": ["Status-card v2 public reading", "Next burden", "generated noncanonical"],
    "github-facing/proof-state-dashboard-explainer.md": [
        "Next burden",
        "generated noncanonical reader surface",
    ],
    "github-facing/source-authority-explainer.md": [
        "Status-card v2 reduces cognitive load",
        "does not create a new authority",
        "layer",
    ],
    "wiki/indexes/compact_current_frontier_v16.md": [
        "snapshot-only reader aid",
        "not physics authority",
    ],
}


def _as_map(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def _as_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    return value if isinstance(value, list) else []


def _public_linter_paths() -> list[str]:
    paths = list(PUBLIC_FILES)
    for directory in PUBLIC_DIRS:
        root = ROOT / directory
        paths.extend(
            path.relative_to(ROOT).as_posix()
            for path in sorted(root.rglob("*"))
            if path.is_file() and path.suffix == ".md"
        )
    return paths


def _run_claim_language_linter(paths: list[str]) -> dict[str, Any]:
    command = [
        sys.executable,
        "scripts/project_control/validate_claim_language.py",
        "--paths",
        *paths,
        "--json",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {
            "status": "FAIL",
            "exit_code": completed.returncode,
            "error": f"invalid linter JSON: {exc}",
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    payload["exit_code"] = completed.returncode
    return payload


def _surface_phrase_report() -> dict[str, Any]:
    failures: list[str] = []
    checked: dict[str, list[str]] = {}
    for rel_path, phrases in REQUIRED_SURFACE_PHRASES.items():
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        checked[rel_path] = []
        for phrase in phrases:
            if phrase not in text:
                failures.append(f"{rel_path} missing phrase {phrase!r}")
            else:
                checked[rel_path].append(phrase)
    return {"failures": failures, "checked": checked}


def validate() -> dict[str, Any]:
    failures: list[str] = []
    schema_summary: dict[str, Any] = {}
    data: dict[str, Any] = {}

    if not ARTIFACT.exists():
        failures.append(f"missing artifact {ARTIFACT.relative_to(ROOT)}")
    else:
        try:
            schema_summary = validate_review_file(ARTIFACT)
        except Exception as exc:  # pragma: no cover - failure path reported as data
            failures.append(f"global red-team schema validation failed: {exc}")
        data = strict_yaml.load(ARTIFACT)

    if data.get("task_id") != TASK_ID:
        failures.append("task_id mismatch")
    if data.get("agent_job_id") != JOB_ID:
        failures.append("agent_job_id mismatch")
    if data.get("plan_task_id") != "P9-T05":
        failures.append("plan_task_id must be P9-T05")
    if data.get("p9_review_result") not in ALLOWED_RESULTS:
        failures.append("p9_review_result must be pass repair_required or fail_closed")
    if data.get("p9_review_result") != "pass":
        failures.append("P9-T05 expected pass for this packet")
    if data.get("verdict") != "no_blocking_defect_found_as_written":
        failures.append("global red-team verdict must be no_blocking_defect_found_as_written")
    if data.get("recommended_next_route") != "P10-T01":
        failures.append("recommended_next_route must be P10-T01 on pass")
    if data.get("physics_promotion_authorized") is not False:
        failures.append("physics_promotion_authorized must be exactly false")
    if data.get("repair_required") is not False:
        failures.append("repair_required must be exactly false")
    if data.get("fail_closed") is not False:
        failures.append("fail_closed must be exactly false")

    done = _as_map(data, "done_criteria_status")
    missing_done = sorted(REQUIRED_DONE_CRITERIA - set(done))
    if missing_done:
        failures.append(f"missing done criteria: {missing_done}")
    for field in REQUIRED_DONE_CRITERIA:
        if done.get(field) is not True:
            failures.append(f"done_criteria_status.{field} must be true")

    six = _as_map(data, "six_question_assessment")
    for question in (
        "what_exists",
        "exact_scope",
        "what_does_not_follow",
        "next_burden",
        "hype_and_caveat_fog",
        "generated_surface_authority_confusion",
    ):
        block = _as_map(six, question)
        if not block:
            failures.append(f"six_question_assessment.{question} missing")
        elif not block.get("status"):
            failures.append(f"six_question_assessment.{question}.status missing")
        elif not _as_list(block, "evidence"):
            failures.append(f"six_question_assessment.{question}.evidence missing")

    linter_paths = _public_linter_paths()
    linter = _run_claim_language_linter(linter_paths)
    if linter.get("status") != "PASS":
        failures.append("public claim-language linter must pass")
    if linter.get("hard_fail_count") != 0:
        failures.append("public claim-language linter hard_fail_count must be 0")
    if linter.get("config_errors"):
        failures.append(f"public claim-language linter config_errors: {linter.get('config_errors')}")
    if _as_map(data, "linter_result").get("warning_disposition") != "justified_nonblocking":
        failures.append("linter_result.warning_disposition must be justified_nonblocking")

    phrase_report = _surface_phrase_report()
    failures.extend(phrase_report["failures"])

    pressure_points = _as_list(data, "external_mathematical_pressure_points")
    if len(pressure_points) < 3:
        failures.append("external_mathematical_pressure_points must contain at least three items")
    if data.get("minimal_countermodel_attempt", {}).get("attempted") is not False:
        failures.append("minimal_countermodel_attempt.attempted must be false for review-only packet")

    claim_boundary = _as_map(data, "claim_boundary")
    forbidden_claims = " ".join(str(item) for item in _as_list(claim_boundary, "forbidden_claims"))
    for phrase in (
        "generated reader surface as source authority",
        "matter-coupling derivation",
        "Einstein-equation derivation",
        "completed derivation",
    ):
        if phrase not in forbidden_claims:
            failures.append(f"missing forbidden claim phrase: {phrase}")

    return {
        "schema_id": "p9_t05_public_cognitive_load_red_team_validator_v1",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "artifact_path": ARTIFACT.relative_to(ROOT).as_posix(),
        "global_schema_summary": schema_summary,
        "review_result": data.get("p9_review_result"),
        "verdict": data.get("verdict"),
        "recommended_next_route": data.get("recommended_next_route"),
        "done_criteria_status": done,
        "linter_path_count": len(linter_paths),
        "linter_summary": {
            "status": linter.get("status"),
            "hard_fail_count": linter.get("hard_fail_count"),
            "warning_count": linter.get("warning_count"),
            "underclaim_calibration_warning_count": linter.get(
                "underclaim_calibration_warning_count"
            ),
            "exit_code": linter.get("exit_code"),
        },
        "surface_phrase_report": phrase_report,
        "physics_promotion_authorized": data.get("physics_promotion_authorized"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.write_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
