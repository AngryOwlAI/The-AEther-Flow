#!/usr/bin/env python3
"""Validate the P4-T01 receipt contract example and malformed fixtures."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


RUN_SCHEMA = "validation_run_receipt_v1"
GATE_SCHEMA = "validation_gate_result_v1"
FINDING_SCHEMA = "validation_finding_v1"
ARTIFACT_SCHEMA = "validation_artifact_reference_v1"

STATUSES = (
    "PASS",
    "FAIL",
    "WARN",
    "SKIP_NOT_APPLICABLE",
    "SKIP_SUPERSEDED",
    "CACHE_HIT",
    "BLOCKED_CONFIGURATION",
)
SEVERITIES = {"blocking", "advisory", "diagnostic"}
CACHE_STATUSES = {"NOT_ELIGIBLE", "MISS", "HIT", "BYPASSED"}
MODES = {"legacy", "shadow", "planner"}
LEVELS = {"ERROR", "WARN", "INFO"}
FINDING_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
HASH_RE = re.compile(r"^(?:sha256:[0-9a-f]{64}|git-tree-sha1:[0-9a-f]{40})$")
FORBIDDEN_RAW_KEYS = {"stdout", "stderr", "stdout_tail", "stderr_tail"}

RUN_KEYS = {
    "schema_id",
    "schema_version",
    "run_id",
    "mode",
    "profile",
    "scope",
    "base_ref",
    "tree_hash",
    "planner_version",
    "manifest_hash",
    "environment_fingerprint",
    "started_at",
    "finished_at",
    "duration_ms",
    "status",
    "authority",
    "output_policy",
    "selected_gate_ids",
    "executed_gate_ids",
    "superseded_gate_ids",
    "counts",
    "gate_results",
    "artifacts",
}

GATE_KEYS = {
    "schema_id",
    "gate_id",
    "severity",
    "status",
    "cache_status",
    "input_fingerprint",
    "implementation_fingerprint",
    "started_at",
    "finished_at",
    "duration_ms",
    "error_count",
    "warning_count",
    "finding_count",
    "shown_finding_count",
    "findings_truncated",
    "shown_findings",
    "full_receipt",
    "satisfied_obligation_ids",
    "child_gate_ids",
    "mutated_paths",
    "artifact_refs",
}

AUTHORITY_KEYS = {
    "scope",
    "source_authoritative",
    "full_receipts_authoritative",
    "physics_claim_authority",
    "ontology_authority",
    "benchmark_authority",
    "gate_chair_authority",
}


def add(errors: list[dict[str, str]], finding_id: str, message: str) -> None:
    errors.append({"finding_id": finding_id, "message": message})


def nonnegative_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def unique_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and bool(item) for item in value)
        and len(value) == len(set(value))
    )


def safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and str(path) == value


def parse_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return None


def validate_interval(
    obj: dict[str, Any], errors: list[dict[str, str]], finding_id: str, label: str
) -> None:
    started = parse_utc(obj.get("started_at"))
    finished = parse_utc(obj.get("finished_at"))
    duration = obj.get("duration_ms")
    if started is None or finished is None or not nonnegative_integer(duration):
        add(errors, finding_id, f"{label} has an invalid UTC interval")
        return
    observed = round((finished - started).total_seconds() * 1000)
    if observed != duration or observed < 0:
        add(errors, finding_id, f"{label} duration does not match its timestamps")


def validate_hash(value: Any) -> bool:
    return isinstance(value, str) and HASH_RE.fullmatch(value) is not None


def validate_authority(value: Any, errors: list[dict[str, str]]) -> None:
    if not isinstance(value, dict) or set(value) != AUTHORITY_KEYS:
        add(errors, "VRR-E-AUTHORITY", "authority boundary is incomplete or extended")
        return
    if value.get("scope") != "operational_validation_only":
        add(errors, "VRR-E-AUTHORITY", "authority scope is not operational only")
    for key in AUTHORITY_KEYS - {"scope"}:
        if value.get(key) is not False:
            add(errors, "VRR-E-AUTHORITY", f"{key} must be false")


def validate_full_receipt(value: Any, errors: list[dict[str, str]], gate_id: str) -> None:
    keys = {"artifact_id", "path", "content_hash", "local_only", "authoritative"}
    if not isinstance(value, dict) or set(value) != keys:
        add(errors, "VRR-E-FULL-RECEIPT", f"{gate_id} full receipt is missing or malformed")
        return
    if not isinstance(value.get("artifact_id"), str) or not value["artifact_id"]:
        add(errors, "VRR-E-FULL-RECEIPT", f"{gate_id} full receipt artifact ID is invalid")
    if not safe_relative_path(value.get("path")):
        add(errors, "VRR-E-PATH", f"{gate_id} full receipt path is unsafe")
    if not validate_hash(value.get("content_hash")):
        add(errors, "VRR-E-HASH", f"{gate_id} full receipt hash is invalid")
    if value.get("local_only") is not True or value.get("authoritative") is not False:
        add(errors, "VRR-E-FULL-RECEIPT", f"{gate_id} full receipt boundary is invalid")


def validate_finding(
    value: Any,
    errors: list[dict[str, str]],
    all_finding_ids: list[str],
    artifact_ids: set[str],
) -> None:
    keys = {"schema_id", "finding_id", "level", "code", "message", "artifact_ref"}
    if not isinstance(value, dict) or set(value) != keys:
        add(errors, "VRR-E-FINDING-SHAPE", "shown finding has an invalid shape")
        return
    if value.get("schema_id") != FINDING_SCHEMA:
        add(errors, "VRR-E-FINDING-SHAPE", "shown finding schema ID is invalid")
    finding_id = value.get("finding_id")
    if not isinstance(finding_id, str) or FINDING_ID_RE.fullmatch(finding_id) is None:
        add(errors, "VRR-E-FINDING-ID", "shown finding ID is not stable-form")
    else:
        all_finding_ids.append(finding_id)
    if value.get("level") not in LEVELS:
        add(errors, "VRR-E-FINDING-SHAPE", "shown finding level is invalid")
    if not isinstance(value.get("code"), str) or not value["code"]:
        add(errors, "VRR-E-FINDING-SHAPE", "shown finding code is invalid")
    if not isinstance(value.get("message"), str) or not value["message"].strip():
        add(errors, "VRR-E-FINDING-SHAPE", "shown finding message is invalid")
    artifact_ref = value.get("artifact_ref")
    if artifact_ref is not None and artifact_ref not in artifact_ids:
        add(errors, "VRR-E-ARTIFACT", "shown finding artifact reference is unresolved")


def validate_artifacts(value: Any, errors: list[dict[str, str]]) -> set[str]:
    artifact_ids: set[str] = set()
    if not isinstance(value, list):
        add(errors, "VRR-E-ARTIFACT", "artifacts must be an array")
        return artifact_ids
    keys = {
        "schema_id",
        "artifact_id",
        "kind",
        "path",
        "content_hash",
        "local_only",
        "authoritative",
        "description",
    }
    for artifact in value:
        if not isinstance(artifact, dict) or set(artifact) != keys:
            add(errors, "VRR-E-ARTIFACT", "artifact reference has an invalid shape")
            continue
        artifact_id = artifact.get("artifact_id")
        if artifact.get("schema_id") != ARTIFACT_SCHEMA:
            add(errors, "VRR-E-ARTIFACT", "artifact schema ID is invalid")
        if not isinstance(artifact_id, str) or not artifact_id or artifact_id in artifact_ids:
            add(errors, "VRR-E-ARTIFACT", "artifact ID is missing or duplicated")
        else:
            artifact_ids.add(artifact_id)
        if not isinstance(artifact.get("kind"), str) or not artifact["kind"]:
            add(errors, "VRR-E-ARTIFACT", "artifact kind is invalid")
        if not safe_relative_path(artifact.get("path")):
            add(errors, "VRR-E-PATH", "artifact path is unsafe")
        if not validate_hash(artifact.get("content_hash")):
            add(errors, "VRR-E-HASH", "artifact hash is invalid")
        if not isinstance(artifact.get("local_only"), bool):
            add(errors, "VRR-E-ARTIFACT", "artifact local-only flag is invalid")
        if artifact.get("authoritative") is not False:
            add(errors, "VRR-E-AUTHORITY", "artifact must be non-authoritative")
        if not isinstance(artifact.get("description"), str) or not artifact["description"].strip():
            add(errors, "VRR-E-ARTIFACT", "artifact description is invalid")
    return artifact_ids


def aggregate_status(statuses: list[str]) -> str:
    if not statuses:
        return "BLOCKED_CONFIGURATION"
    if "BLOCKED_CONFIGURATION" in statuses:
        return "BLOCKED_CONFIGURATION"
    if "FAIL" in statuses:
        return "FAIL"
    if "WARN" in statuses:
        return "WARN"
    return "PASS"


def validate_receipt(receipt: Any) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(receipt, dict):
        add(errors, "VRR-E-RUN-SHAPE", "run receipt must be an object")
        return errors

    raw_keys = FORBIDDEN_RAW_KEYS & set(receipt)
    if raw_keys:
        add(errors, "VRR-E-RAW-OUTPUT", "raw stdout or stderr keys are forbidden")
    if set(receipt) != RUN_KEYS:
        add(errors, "VRR-E-RUN-SHAPE", "run receipt fields do not match schema v1")
    if receipt.get("schema_id") != RUN_SCHEMA or receipt.get("schema_version") != 1:
        add(errors, "VRR-E-SCHEMA-ID", "unknown run schema ID or version")

    for key in ("run_id", "profile", "scope", "base_ref", "planner_version"):
        if not isinstance(receipt.get(key), str) or not receipt[key].strip():
            add(errors, "VRR-E-RUN-SHAPE", f"{key} must be nonblank")
    if receipt.get("mode") not in MODES:
        add(errors, "VRR-E-RUN-SHAPE", "mode is invalid")
    for key in ("tree_hash", "manifest_hash", "environment_fingerprint"):
        if not validate_hash(receipt.get(key)):
            add(errors, "VRR-E-HASH", f"{key} is invalid")
    validate_interval(receipt, errors, "VRR-E-RUN-INTERVAL", "run")
    validate_authority(receipt.get("authority"), errors)

    policy = receipt.get("output_policy")
    policy_keys = {
        "default_shown_findings_per_gate",
        "hard_max_shown_findings_per_gate",
        "raw_stdout_stderr_embedded",
    }
    hard_max = -1
    if not isinstance(policy, dict) or set(policy) != policy_keys:
        add(errors, "VRR-E-OUTPUT-POLICY", "output policy is invalid")
    else:
        default = policy.get("default_shown_findings_per_gate")
        hard_max = policy.get("hard_max_shown_findings_per_gate")
        if not nonnegative_integer(default) or default > 5:
            add(errors, "VRR-E-OUTPUT-POLICY", "default shown-finding limit is invalid")
        if not nonnegative_integer(hard_max) or not 1 <= hard_max <= 10 or hard_max < default:
            add(errors, "VRR-E-OUTPUT-POLICY", "hard shown-finding limit is invalid")
        if policy.get("raw_stdout_stderr_embedded") is not False:
            add(errors, "VRR-E-RAW-OUTPUT", "raw output policy must be false")

    selected = receipt.get("selected_gate_ids")
    executed = receipt.get("executed_gate_ids")
    superseded = receipt.get("superseded_gate_ids")
    for label, value in (
        ("selected", selected),
        ("executed", executed),
        ("superseded", superseded),
    ):
        if not unique_strings(value):
            add(errors, "VRR-E-GATE-SETS", f"{label} gate IDs are invalid")
    if all(isinstance(value, list) for value in (selected, executed, superseded)):
        if not set(executed).issubset(set(selected)) or not set(superseded).issubset(set(selected)):
            add(errors, "VRR-E-GATE-SETS", "executed or superseded gates were not selected")
        if set(executed) & set(superseded):
            add(errors, "VRR-E-GATE-SETS", "executed and superseded gates overlap")

    artifact_ids = validate_artifacts(receipt.get("artifacts"), errors)
    gate_results = receipt.get("gate_results")
    if not isinstance(gate_results, list):
        add(errors, "VRR-E-GATE-SHAPE", "gate results must be an array")
        gate_results = []
    gate_result_ids: list[str] = []
    all_finding_ids: list[str] = []
    statuses: list[str] = []
    error_total = warning_total = finding_total = 0

    for gate in gate_results:
        if not isinstance(gate, dict) or set(gate) != GATE_KEYS:
            add(errors, "VRR-E-GATE-SHAPE", "gate result fields do not match schema v1")
            continue
        gate_id = gate.get("gate_id")
        if gate.get("schema_id") != GATE_SCHEMA or not isinstance(gate_id, str) or not gate_id:
            add(errors, "VRR-E-GATE-SHAPE", "gate schema ID or gate ID is invalid")
            gate_id = "unknown_gate"
        gate_result_ids.append(gate_id)
        if gate.get("severity") not in SEVERITIES:
            add(errors, "VRR-E-GATE-SHAPE", f"{gate_id} severity is invalid")
        status = gate.get("status")
        if status not in STATUSES:
            add(errors, "VRR-E-GATE-STATUS", f"{gate_id} status is invalid")
        else:
            statuses.append(status)
        cache_status = gate.get("cache_status")
        if cache_status not in CACHE_STATUSES:
            add(errors, "VRR-E-CACHE-STATUS", f"{gate_id} cache status is invalid")
        if status == "CACHE_HIT" and cache_status != "HIT":
            add(errors, "VRR-E-CACHE-STATUS", f"{gate_id} cache-hit result lacks HIT")
        if status != "CACHE_HIT" and cache_status == "HIT":
            add(errors, "VRR-E-CACHE-STATUS", f"{gate_id} HIT cache lacks cache-hit result")
        for key in ("input_fingerprint", "implementation_fingerprint"):
            if not validate_hash(gate.get(key)):
                add(errors, "VRR-E-HASH", f"{gate_id} {key} is invalid")
        validate_interval(gate, errors, "VRR-E-GATE-INTERVAL", gate_id)

        for key in ("error_count", "warning_count", "finding_count", "shown_finding_count"):
            if not nonnegative_integer(gate.get(key)):
                add(errors, "VRR-E-GATE-COUNT", f"{gate_id} {key} is invalid")
        shown = gate.get("shown_findings")
        if not isinstance(shown, list):
            add(errors, "VRR-E-GATE-COUNT", f"{gate_id} shown findings must be an array")
            shown = []
        if gate.get("shown_finding_count") != len(shown):
            add(errors, "VRR-E-GATE-COUNT", f"{gate_id} shown finding count is inconsistent")
        if hard_max >= 0 and len(shown) > hard_max:
            add(errors, "VRR-E-FINDING-BUDGET", f"{gate_id} exceeds the hard display budget")
        full_count = gate.get("finding_count")
        truncated = gate.get("findings_truncated")
        if isinstance(full_count, int) and full_count < len(shown):
            add(errors, "VRR-E-GATE-COUNT", f"{gate_id} full finding count is too small")
        if not isinstance(truncated, bool) or truncated is not (full_count > len(shown)):
            add(errors, "VRR-E-GATE-COUNT", f"{gate_id} truncation flag is inconsistent")
        validate_full_receipt(gate.get("full_receipt"), errors, gate_id)
        for finding in shown:
            validate_finding(finding, errors, all_finding_ids, artifact_ids)

        for key in ("satisfied_obligation_ids", "child_gate_ids", "artifact_refs"):
            if not unique_strings(gate.get(key)):
                add(errors, "VRR-E-GATE-SHAPE", f"{gate_id} {key} is invalid")
        for artifact_ref in gate.get("artifact_refs", []):
            if artifact_ref not in artifact_ids:
                add(errors, "VRR-E-ARTIFACT", f"{gate_id} artifact reference is unresolved")
        paths = gate.get("mutated_paths")
        if not unique_strings(paths) or any(not safe_relative_path(path) for path in paths or []):
            add(errors, "VRR-E-PATH", f"{gate_id} mutated paths are invalid")
        if status == "SKIP_SUPERSEDED" and gate_id not in (superseded or []):
            add(errors, "VRR-E-GATE-SETS", f"{gate_id} supersedence is not declared")

        if nonnegative_integer(gate.get("error_count")):
            error_total += gate["error_count"]
        if nonnegative_integer(gate.get("warning_count")):
            warning_total += gate["warning_count"]
        if nonnegative_integer(gate.get("finding_count")):
            finding_total += gate["finding_count"]

    if len(all_finding_ids) != len(set(all_finding_ids)):
        add(errors, "VRR-E-FINDING-ID", "finding IDs are not unique across the run")
    if isinstance(executed, list) and gate_result_ids != executed:
        add(errors, "VRR-E-GATE-ORDER", "gate result order differs from executed gate order")

    counts = receipt.get("counts")
    count_keys = {
        "selected_gate_count",
        "executed_gate_count",
        "superseded_gate_count",
        "error_count",
        "warning_count",
        "finding_count",
        "status_counts",
    }
    if not isinstance(counts, dict) or set(counts) != count_keys:
        add(errors, "VRR-E-RUN-COUNT", "aggregate counts have an invalid shape")
    else:
        expected = {
            "selected_gate_count": len(selected) if isinstance(selected, list) else 0,
            "executed_gate_count": len(executed) if isinstance(executed, list) else 0,
            "superseded_gate_count": len(superseded) if isinstance(superseded, list) else 0,
            "error_count": error_total,
            "warning_count": warning_total,
            "finding_count": finding_total,
        }
        for key, expected_value in expected.items():
            if counts.get(key) != expected_value:
                add(errors, "VRR-E-RUN-COUNT", f"aggregate {key} is inconsistent")
        status_counts = counts.get("status_counts")
        computed = Counter(statuses)
        if not isinstance(status_counts, dict) or set(status_counts) != set(STATUSES):
            add(errors, "VRR-E-RUN-COUNT", "status counts have an invalid shape")
        elif any(status_counts[key] != computed[key] for key in STATUSES):
            add(errors, "VRR-E-RUN-COUNT", "status counts are inconsistent")

    if receipt.get("status") not in STATUSES:
        add(errors, "VRR-E-RUN-STATUS", "run status is outside the exact vocabulary")
    elif receipt.get("status") != aggregate_status(statuses):
        add(errors, "VRR-E-RUN-STATUS", "run status is not the deterministic aggregate")
    return errors


def malformed_fixtures(example: dict[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    fixtures: list[tuple[str, str, dict[str, Any]]] = []

    unknown_schema = copy.deepcopy(example)
    unknown_schema["schema_version"] = 2
    fixtures.append(("unknown_schema_version", "VRR-E-SCHEMA-ID", unknown_schema))

    bad_status = copy.deepcopy(example)
    bad_status["gate_results"][1]["status"] = "SUCCESS"
    fixtures.append(("unknown_gate_status", "VRR-E-GATE-STATUS", bad_status))

    raw_output = copy.deepcopy(example)
    raw_output["stdout"] = "raw output is forbidden"
    fixtures.append(("embedded_raw_stdout", "VRR-E-RAW-OUTPUT", raw_output))

    duplicate_finding = copy.deepcopy(example)
    gate = duplicate_finding["gate_results"][1]
    gate["shown_findings"].append(copy.deepcopy(gate["shown_findings"][0]))
    gate["shown_finding_count"] = 2
    gate["finding_count"] = 2
    gate["warning_count"] = 2
    duplicate_finding["counts"]["finding_count"] = 2
    duplicate_finding["counts"]["warning_count"] = 2
    fixtures.append(("duplicate_finding_id", "VRR-E-FINDING-ID", duplicate_finding))

    over_budget = copy.deepcopy(example)
    gate = over_budget["gate_results"][1]
    original = gate["shown_findings"][0]
    gate["shown_findings"] = []
    for index in range(11):
        finding = copy.deepcopy(original)
        finding["finding_id"] = f"VRR-EXAMPLE-RCD-WARN-{index + 1:03d}"
        gate["shown_findings"].append(finding)
    gate["shown_finding_count"] = 11
    gate["finding_count"] = 11
    gate["warning_count"] = 11
    over_budget["counts"]["finding_count"] = 11
    over_budget["counts"]["warning_count"] = 11
    fixtures.append(("shown_findings_over_budget", "VRR-E-FINDING-BUDGET", over_budget))

    missing_full = copy.deepcopy(example)
    missing_full["gate_results"][1]["full_receipt"] = None
    fixtures.append(("missing_full_receipt", "VRR-E-FULL-RECEIPT", missing_full))

    authority_escalation = copy.deepcopy(example)
    authority_escalation["authority"]["physics_claim_authority"] = True
    fixtures.append(("physics_authority_escalation", "VRR-E-AUTHORITY", authority_escalation))
    return fixtures


def build_report(example_path: Path, validator_path: Path) -> dict[str, Any]:
    root = validator_path.parents[4]
    try:
        example = json.loads(example_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "schema_id": "validation_receipt_schema_validation_report_v1",
            "status": "FAIL",
            "errors": [{"finding_id": "VRR-E-EXAMPLE-READ", "message": str(exc)}],
        }

    example_errors = validate_receipt(example)
    fixture_results: list[dict[str, Any]] = []
    for fixture_id, expected_finding_id, fixture in malformed_fixtures(example):
        findings = validate_receipt(fixture)
        finding_ids = sorted({finding["finding_id"] for finding in findings})
        fixture_results.append(
            {
                "fixture_id": fixture_id,
                "expected_finding_id": expected_finding_id,
                "rejected": bool(findings),
                "expected_finding_observed": expected_finding_id in finding_ids,
                "finding_ids": finding_ids,
            }
        )
    fixtures_pass = all(
        result["rejected"] and result["expected_finding_observed"] for result in fixture_results
    )
    status = "PASS" if not example_errors and fixtures_pass else "FAIL"
    return {
        "schema_id": "validation_receipt_schema_validation_report_v1",
        "status": status,
        "validated_schema_id": RUN_SCHEMA,
        "example_path": example_path.relative_to(root).as_posix(),
        "validator_path": validator_path.relative_to(root).as_posix(),
        "gate_ids": [
            "validation_receipt_schema_shape",
            "validation_receipt_example_conformance",
            "validation_receipt_malformed_fixtures",
            "validation_receipt_authority_boundary",
        ],
        "counts": {
            "example_error_count": len(example_errors),
            "malformed_fixture_count": len(fixture_results),
            "rejected_fixture_count": sum(result["rejected"] for result in fixture_results),
            "expected_finding_match_count": sum(
                result["expected_finding_observed"] for result in fixture_results
            ),
        },
        "example_errors": example_errors,
        "malformed_fixtures": fixture_results,
        "authority": {
            "scope": "operational_validation_only",
            "physics_claim_authority": False,
            "ontology_authority": False,
            "benchmark_authority": False,
            "gate_chair_authority": False,
        },
    }


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[4]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--example",
        type=Path,
        default=root / "research_control/design/validation_run_receipt_example_v1.json",
    )
    parser.add_argument(
        "--write-report",
        type=Path,
        default=root
        / "research_control/tasks/RT-20260716-001/artifacts/validation_receipt_schema_validation.json",
    )
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator_path = Path(__file__).resolve()
    report = build_report(args.example.resolve(), validator_path)
    args.write_report.parent.mkdir(parents=True, exist_ok=True)
    args.write_report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Validation receipt schema review: {report['status']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
