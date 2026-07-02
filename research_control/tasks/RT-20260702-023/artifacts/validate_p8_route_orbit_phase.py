#!/usr/bin/env python3
"""Validate the v14 P8 route-orbit hardening phase."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = REPO_ROOT / "scripts" / "research_control"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from extract_route_history import SIGNATURE_SCHEMA_ID, build_route_history  # noqa: E402
from validate_route_orbits import VALIDATOR_SCHEMA_ID, validate_route_history  # noqa: E402


REQUIRED_LABELS = [
    "RR_E_UNRESTRICTED_IRRELEVANCE_UNDERDETERMINATION",
    "RR_E_TRANSPORT_INVARIANCE_MISSING_SOURCE_LAW",
    "MATTER_SEMANTICS_EVIDENCE_AS_ADOPTION_OVERREAD",
    "NO_TARGET_CERTIFICATE_POSITIVE_SEMANTICS_OVERREAD",
    "SCOPED_GATE_RESULT_WITHOUT_BOUNDARY_SYNC",
    "REPEATED_FORMALIZE_AUDIT_STRESS_GATE_NO_NEW_PAYLOAD",
]

REQUIRED_PATHS = {
    "p8_t01_route_signature_definition": "research_control/design/route_signature_definition.md",
    "p8_t01_receipt": "research_control/tasks/RT-20260702-018/artifacts/p8_t01_route_signature_definition_receipt.md",
    "p8_t02_extractor": "scripts/research_control/extract_route_history.py",
    "p8_t02_receipt": "research_control/tasks/RT-20260702-019/artifacts/p8_t02_route_history_extractor_receipt.md",
    "p8_t02_sample": "research_control/tasks/RT-20260702-019/artifacts/p8_t02_route_history_sample.json",
    "p8_t03_validator": "scripts/research_control/validate_route_orbits.py",
    "p8_t03_tests": "tests/test_route_orbit_validator.py",
    "p8_t03_receipt": "research_control/tasks/RT-20260702-020/artifacts/p8_t03_route_orbit_validator_receipt.md",
    "p8_t03_sample": "research_control/tasks/RT-20260702-020/artifacts/p8_t03_route_orbit_validator_sample.json",
    "p8_t04_pilot_report": "research_control/tasks/RT-20260702-021/artifacts/p8_t04_route_orbit_pilot_report.json",
    "p8_t04_pilot_receipt": "research_control/tasks/RT-20260702-021/artifacts/p8_t04_route_orbit_pilot_receipt.md",
    "p8_t05_freeze_taxonomy": "research_control/design/obstruction_and_freeze_control.md",
    "p8_t05_receipt": "research_control/tasks/RT-20260702-022/artifacts/p8_t05_freeze_taxonomy_receipt.md",
    "handoff_0475": "research_control/handoffs/handoff-0475.yaml",
    "v14_plan": "implementations_plans/recommendations_implementation_plan_continue_task-v14.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_required_paths(repo_root: Path) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for key, rel_path in REQUIRED_PATHS.items():
        path = repo_root / rel_path
        checks.append(
            {
                "id": key,
                "path": rel_path,
                "exists": path.exists(),
                "sha256": sha256(path) if path.exists() and path.is_file() else "",
                "status": "PASS" if path.exists() else "FAIL",
            }
        )
    return checks


def check_pilot_report(repo_root: Path) -> dict[str, Any]:
    path = repo_root / REQUIRED_PATHS["p8_t04_pilot_report"]
    report = load_json(path)
    acceptance = report.get("acceptance", {})
    combined = report.get("combined_recent_chain_validation", {})
    replay = report.get("no_payload_replay_control", {})
    chain_reports = report.get("chain_reports", [])
    return {
        "status": "PASS"
        if (
            report.get("status") == "PASS"
            and all(acceptance.get(key) is True for key in acceptance)
            and combined.get("status") == "PASS"
            and combined.get("hard_failure_count") == 0
            and replay.get("flagged") is True
            and replay.get("hard_failure_count", 0) > 0
            and all(chain.get("source_evidence_complete") is True for chain in chain_reports)
        )
        else "FAIL",
        "report_status": report.get("status"),
        "acceptance": acceptance,
        "combined_recent_chain_validation": {
            "status": combined.get("status"),
            "signature_count": combined.get("signature_count"),
            "hard_failure_count": combined.get("hard_failure_count"),
            "warning_count": combined.get("warning_count"),
        },
        "no_payload_replay_control": {
            "flagged": replay.get("flagged"),
            "hard_failure_count": replay.get("hard_failure_count"),
            "control_id": replay.get("control_id"),
        },
        "chain_count": len(chain_reports),
        "source_evidence_complete": all(chain.get("source_evidence_complete") is True for chain in chain_reports),
    }


def check_freeze_labels(repo_root: Path) -> dict[str, Any]:
    text = (repo_root / REQUIRED_PATHS["p8_t05_freeze_taxonomy"]).read_text(encoding="utf-8")
    missing = [label for label in REQUIRED_LABELS if label not in text]
    return {
        "status": "PASS" if not missing else "FAIL",
        "required_label_count": len(REQUIRED_LABELS),
        "missing_labels": missing,
        "present_labels": [label for label in REQUIRED_LABELS if label in text],
    }


def check_route_tools(repo_root: Path) -> dict[str, Any]:
    history = build_route_history(repo_root=repo_root, task_ids=[], sample="recent-matter-rr-e", limit=0)
    validation = validate_route_history(history)
    return {
        "status": "PASS"
        if (
            history.get("schema_id") == "route_history_extractor_v1"
            and history.get("signature_schema_id") == SIGNATURE_SCHEMA_ID
            and history.get("extraction_errors") == []
            and validation.get("schema_id") == VALIDATOR_SCHEMA_ID
            and validation.get("status") == "PASS"
            and validation.get("hard_failure_count") == 0
        )
        else "FAIL",
        "history_schema_id": history.get("schema_id"),
        "signature_schema_id": history.get("signature_schema_id"),
        "signature_count": history.get("signature_count"),
        "task_count": history.get("task_count"),
        "extraction_error_count": len(history.get("extraction_errors", [])),
        "validator_schema_id": validation.get("schema_id"),
        "validator_status": validation.get("status"),
        "hard_failure_count": validation.get("hard_failure_count"),
        "warning_count": validation.get("warning_count"),
    }


def check_handoff_boundary(repo_root: Path) -> dict[str, Any]:
    text = (repo_root / REQUIRED_PATHS["handoff_0475"]).read_text(encoding="utf-8")
    required = [
        "v14_p8_t06_route_orbit_phase_validation",
        "P9 external red-team mode",
        "downstream_physics_promotion_authorized: false",
        "benchmark_promotion_authorized: false",
        "completed_derivation_authorized: false",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    return {
        "status": "PASS" if not missing else "FAIL",
        "missing_fragments": missing,
        "next_route_fragment_present": "P9 external red-team mode" in text,
    }


def build_report(repo_root: Path) -> dict[str, Any]:
    path_checks = check_required_paths(repo_root)
    pilot_check = check_pilot_report(repo_root)
    label_check = check_freeze_labels(repo_root)
    route_tool_check = check_route_tools(repo_root)
    handoff_check = check_handoff_boundary(repo_root)
    checks = {
        "required_paths": "PASS" if all(check["status"] == "PASS" for check in path_checks) else "FAIL",
        "route_tools": route_tool_check["status"],
        "pilot_report": pilot_check["status"],
        "freeze_taxonomy": label_check["status"],
        "handoff_boundary": handoff_check["status"],
    }
    return {
        "schema_id": "p8_t06_route_orbit_phase_validation_report_v1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": "PASS" if all(value == "PASS" for value in checks.values()) else "FAIL",
        "checks": checks,
        "required_paths": path_checks,
        "route_tool_check": route_tool_check,
        "pilot_report_check": pilot_check,
        "freeze_taxonomy_check": label_check,
        "handoff_boundary_check": handoff_check,
        "claim_boundary": {
            "physics_promotion_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
            "phase_validation_is_physics_evidence": False,
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(argv or sys.argv[1:]))
    repo_root = args.repo_root.resolve()
    report = build_report(repo_root)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        output_path = args.output if args.output.is_absolute() else repo_root / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")
    if args.json or args.output is None:
        print(payload, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
