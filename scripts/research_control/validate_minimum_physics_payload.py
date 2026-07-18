#!/usr/bin/env python3
"""Validate the v16 minimum-payload and route-orbit control contract.

This validator is project-control evidence only. A PASS/WARN/HARD_GATE result
does not prove or refute a physics claim, promote an ontology object, authorize
matter coupling, or establish a global no-go theorem.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from strict_yaml import StrictYamlError, load as load_yaml  # noqa: E402


VALIDATOR_SCHEMA_ID = "minimum_physics_payload_validator_v1"
POLICY_ID = "route_orbit_gating_policy_v16"
MINIMUM_PAYLOAD_SCHEMA_ID = "minimum_physics_payload_schema_v1"

PHYSICS_PAYLOAD_CLASSES = {
    "new_definition",
    "theorem_statement",
    "proof_attempt",
    "proved_conditional_theorem",
    "explicit_finite_witness",
    "minimal_countermodel",
    "obstruction_record",
    "source_model",
    "certificate_instance",
    "executable_support_spec",
    "attack_fixture",
}

EXCEPTION_PAYLOAD_CLASSES = {
    "selector_with_scored_route_matrix",
    "validation_repair",
    "freeze_review",
}

CONTROLLED_PAYLOAD_CLASSES = PHYSICS_PAYLOAD_CLASSES | EXCEPTION_PAYLOAD_CLASSES

PROCESS_RECEIPT_CLASSES = {
    "validator_pass",
    "unit_test_pass",
    "registry_row",
    "handoff_status",
    "approval_status",
    "generated_derivative",
    "generated_wiki_note",
    "commit_hash",
    "route_status",
    "evidence_status_restatement",
}

NON_PHYSICS_ROLES = {
    "documentation-curator",
    "process-integrity-auditor",
    "project-control-maintainer",
    "project-system-director",
    "validator-engineer",
    "memory-system-maintainer",
}

HARD_OVERREAD_KINDS = {
    "theorem_validator_pass_only",
    "evidence_status_restatement_as_payload",
    "generated_wiki_refresh_as_payload",
    "benchmark_promotion_by_route_status",
}

PROGRESS_PAYLOAD_CLASSES = PHYSICS_PAYLOAD_CLASSES | {"selector_with_scored_route_matrix"}


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1"}
    return bool(value)


def text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    result = str(value).strip()
    return result if result else default


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def payload_class(record: dict[str, Any]) -> str:
    payload = dict_value(record.get("minimum_payload"))
    return text(payload.get("payload_class") or record.get("payload_class"))


def payload_path(record: dict[str, Any]) -> str:
    payload = dict_value(record.get("minimum_payload"))
    return text(payload.get("payload_artifact_path") or record.get("payload_artifact_path"))


def payload_summary(record: dict[str, Any]) -> str:
    payload = dict_value(record.get("minimum_payload"))
    return text(payload.get("payload_summary") or record.get("payload_summary"))


def task_id(record: dict[str, Any]) -> str:
    return text(record.get("task_id"), "unknown")


def role_id(record: dict[str, Any]) -> str:
    return text(record.get("role_id"), "unknown")


def task_type(record: dict[str, Any]) -> str:
    return text(record.get("task_type"), "unknown")


def burden_key(record: dict[str, Any]) -> tuple[str, str]:
    return (
        text(record.get("target_derivation_milestone"), "none"),
        text(record.get("milestone_burden"), "none"),
    )


def is_selector(record: dict[str, Any]) -> bool:
    combined = f"{role_id(record)} {task_type(record)}".lower()
    return "selector" in combined


def is_validation_repair(record: dict[str, Any]) -> bool:
    combined = f"{role_id(record)} {task_type(record)} {payload_class(record)}".lower()
    return "validation_repair" in combined or "validator" in combined and "repair" in combined


def is_freeze_review(record: dict[str, Any]) -> bool:
    combined = f"{task_type(record)} {payload_class(record)}".lower()
    return "freeze" in combined


def is_non_physics_project_task(record: dict[str, Any]) -> bool:
    if truthy(record.get("non_physics_project_task")):
        return True
    if role_id(record) in NON_PHYSICS_ROLES:
        return True
    combined = f"{task_type(record)} {payload_class(record)}".lower()
    return "documentation" in combined or "publication" in combined


def is_physics_task(record: dict[str, Any]) -> bool:
    if "is_physics_task" in record:
        return truthy(record.get("is_physics_task"))
    milestone, burden = burden_key(record)
    if milestone == "none" or burden == "none":
        return False
    return not is_non_physics_project_task(record)


def has_payload_evidence(record: dict[str, Any]) -> bool:
    return bool(payload_path(record) or payload_summary(record) or list_value(record.get("payload_source_basis")))


def event(code: str, severity: str, records: list[dict[str, Any]], reason: str) -> dict[str, Any]:
    return {
        "code": code,
        "severity": severity,
        "task_ids": [task_id(record) for record in records],
        "reason": reason,
        "physics_claim_authority_created": False,
    }


def record_hard_events(record: dict[str, Any]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    pclass = payload_class(record)
    overread = text(record.get("overread_kind"))

    if overread in HARD_OVERREAD_KINDS:
        events.append(
            event(
                overread,
                "HARD_GATE",
                [record],
                "process status or route status is being counted as physics payload",
            )
        )

    if pclass in PROCESS_RECEIPT_CLASSES:
        events.append(
            event(
                "process_receipt_counted_as_payload",
                "HARD_GATE",
                [record],
                f"{pclass} is a process receipt and cannot satisfy minimum physics payload",
            )
        )

    if pclass and pclass not in CONTROLLED_PAYLOAD_CLASSES and is_physics_task(record):
        events.append(
            event(
                "unknown_payload_class",
                "HARD_GATE",
                [record],
                f"{pclass} is not a controlled minimum-payload class",
            )
        )

    if is_physics_task(record) and not pclass and not is_selector(record):
        events.append(
            event(
                "physics_task_missing_payload_class",
                "HARD_GATE",
                [record],
                "post-v15 physics task does not declare a minimum-payload class",
            )
        )

    if is_physics_task(record) and pclass in PHYSICS_PAYLOAD_CLASSES and not has_payload_evidence(record):
        events.append(
            event(
                "physics_payload_missing_artifact_or_summary",
                "HARD_GATE",
                [record],
                "payload-bearing physics task lacks an artifact path or inline payload summary",
            )
        )

    if pclass == "selector_with_scored_route_matrix" and not truthy(record.get("scored_route_matrix")):
        events.append(
            event(
                "selector_payload_missing_scored_matrix",
                "HARD_GATE",
                [record],
                "selector exception requires a scored route matrix",
            )
        )

    if pclass == "validation_repair" and truthy(record.get("physics_promotion_authorized")):
        events.append(
            event(
                "validation_repair_promotes_physics",
                "HARD_GATE",
                [record],
                "validation repair must not authorize physics promotion",
            )
        )

    return events


def no_route_progress(record: dict[str, Any]) -> bool:
    pclass = payload_class(record)
    if pclass in PROGRESS_PAYLOAD_CLASSES:
        return False
    progress_flags = [
        "has_new_mathematical_payload",
        "has_finite_local_witness",
        "has_countermodel",
        "has_source_model",
        "has_certificate_instance",
        "has_executable_support_spec",
        "validator_failure_requires_repair",
        "protected_gate_newly_required",
        "external_red_team_finding_requires_integration",
    ]
    return not any(truthy(record.get(flag)) for flag in progress_flags)


def weak_payload(record: dict[str, Any]) -> bool:
    if truthy(record.get("weak_payload")):
        return True
    pclass = payload_class(record)
    return not pclass or pclass in PROCESS_RECEIPT_CLASSES


def sequence_key(record: dict[str, Any]) -> tuple[int, str, str]:
    try:
        sequence = int(record.get("sequence", 0))
    except (TypeError, ValueError):
        sequence = 0
    return sequence, text(record.get("completed_at")), task_id(record)


def route_events(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    warnings: list[dict[str, Any]] = []
    hard_gates: list[dict[str, Any]] = []
    ordered = sorted(records, key=sequence_key)

    run: list[dict[str, Any]] = []
    previous_key: tuple[str, str] | None = None
    previous_record: dict[str, Any] | None = None
    for record in ordered:
        key = burden_key(record)
        if key == previous_key:
            run.append(record)
        else:
            run = [record]
            previous_key = key

        if len(run) == 2 and all(weak_payload(item) for item in run):
            warnings.append(
                event(
                    "two_same_burden_weak_payload",
                    "WARN",
                    list(run),
                    "two same-burden tasks have weak payload but have not reached the hard gate threshold",
                )
            )

        if len(run) >= 3 and all(no_route_progress(item) for item in run[-3:]):
            hard_gates.append(
                event(
                    "three_same_burden_no_payload_route_orbit",
                    "HARD_GATE",
                    list(run[-3:]),
                    "three consecutive same-burden tasks lack payload and all progress exceptions",
                )
            )

        if previous_record and is_physics_task(previous_record) and is_non_physics_project_task(record):
            warnings.append(
                event(
                    "documentation_or_project_task_after_physics",
                    "WARN",
                    [previous_record, record],
                    "non-physics project task follows physics task and should remain explicitly classified",
                )
            )
        previous_record = record

    return warnings, hard_gates


def evaluate_records(records: list[dict[str, Any]], sample: str = "") -> dict[str, Any]:
    hard_gates: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    passes: list[dict[str, Any]] = []

    for record in records:
        hard_gates.extend(record_hard_events(record))
        if not record_hard_events(record):
            passes.append(
                {
                    "task_id": task_id(record),
                    "payload_class": payload_class(record) or "none",
                    "physics_task": is_physics_task(record),
                }
            )

    route_warnings, route_hard_gates = route_events(records)
    warnings.extend(route_warnings)
    hard_gates.extend(route_hard_gates)

    status = "HARD_GATE" if hard_gates else "WARN" if warnings else "PASS"
    return {
        "schema_id": VALIDATOR_SCHEMA_ID,
        "minimum_payload_schema_id": MINIMUM_PAYLOAD_SCHEMA_ID,
        "route_orbit_policy_id": POLICY_ID,
        "sample": sample,
        "status": status,
        "record_count": len(records),
        "hard_gate_count": len(hard_gates),
        "warning_count": len(warnings),
        "hard_gates": hard_gates,
        "warnings": warnings,
        "passes": passes,
        "authority_boundary": {
            "validator_is_project_control_only": True,
            "physics_claim_authority_created": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
        },
    }


def load_yaml_file(path: Path) -> dict[str, Any]:
    try:
        payload = load_yaml(path)
    except StrictYamlError as exc:
        raise SystemExit(f"{path}: YAML parse error: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"{path}: expected YAML mapping")
    return payload


def load_fixture(path: Path) -> tuple[str, str, list[dict[str, Any]]]:
    payload = load_yaml_file(path)
    records = list_value(payload.get("records"))
    if not records:
        records = [dict_value(payload.get("record"))]
    normalized_records = [dict(record) for record in records if isinstance(record, dict)]
    return text(payload.get("fixture_id"), path.stem), text(payload.get("expected_status"), "PASS"), normalized_records


def evaluate_fixture_dir(path: Path) -> dict[str, Any]:
    fixture_results: list[dict[str, Any]] = []
    all_match = True
    for fixture_path in sorted(path.glob("*.yaml")):
        fixture_id, expected_status, records = load_fixture(fixture_path)
        report = evaluate_records(records, sample=fixture_id)
        actual_status = report["status"]
        matches = actual_status == expected_status
        all_match = all_match and matches
        fixture_results.append(
            {
                "fixture_id": fixture_id,
                "path": str(fixture_path),
                "expected_status": expected_status,
                "actual_status": actual_status,
                "matches_expected": matches,
                "hard_gate_count": report["hard_gate_count"],
                "warning_count": report["warning_count"],
                "hard_gate_codes": [item["code"] for item in report["hard_gates"]],
                "warning_codes": [item["code"] for item in report["warnings"]],
            }
        )
    return {
        "schema_id": VALIDATOR_SCHEMA_ID,
        "sample": str(path),
        "status": "PASS" if all_match else "FAIL",
        "fixture_count": len(fixture_results),
        "fixture_results": fixture_results,
        "authority_boundary": {
            "validator_is_project_control_only": True,
            "physics_claim_authority_created": False,
        },
    }


def read_csv_rows(repo_root: Path, registry_name: str) -> list[dict[str, str]]:
    path = repo_root / "registries" / registry_name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_completion(repo_root: Path, path_text: str) -> dict[str, Any]:
    if not path_text:
        return {}
    path = repo_root / path_text
    if not path.is_file():
        return {}
    try:
        payload = load_yaml(path)
    except StrictYamlError:
        return {}
    return payload if isinstance(payload, dict) else {}


def live_opt_in_records(repo_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in read_csv_rows(repo_root, "AGENT_JOB_REGISTRY.csv"):
        completion = load_completion(repo_root, row.get("completion_path", ""))
        minimum = dict_value(completion.get("minimum_payload_record"))
        if not minimum:
            continue
        record = dict(minimum)
        record.setdefault("task_id", row.get("task_id", ""))
        record.setdefault("job_id", row.get("job_id", ""))
        record.setdefault("role_id", row.get("role_id", ""))
        records.append(record)
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture-dir", type=Path, help="Evaluate fixture files and expected statuses.")
    parser.add_argument("--live", action="store_true", help="Evaluate live opt-in minimum_payload_record completions.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a compact text summary.")
    parser.add_argument("--write-json", type=Path, help="Write the JSON report to this path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.fixture_dir:
        report = evaluate_fixture_dir(args.fixture_dir)
        exit_status = 0 if report["status"] == "PASS" else 1
    else:
        records = live_opt_in_records(REPO_ROOT) if args.live else []
        report = evaluate_records(records, sample="live-opt-in" if args.live else "empty")
        exit_status = 0 if report["status"] in {"PASS", "WARN"} else 1

    if args.write_json:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"minimum physics payload validation: {report['status']}")
    return exit_status


if __name__ == "__main__":
    raise SystemExit(main())
