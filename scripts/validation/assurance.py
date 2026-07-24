#!/usr/bin/env python3
"""Evaluate bounded coverage, mutation, and security evidence.

The evaluator consumes tool-native or normalized JSON and emits a compact,
deterministic gate result.  It does not run tools, infer scientific truth, or
treat a score as proof of correctness.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "validation_assurance_evaluation_v1"
SEVERITIES = ("LOW", "MEDIUM", "HIGH")
MUTATION_STATES = (
    "killed",
    "survived",
    "suspicious",
    "timeout",
    "untested",
    "skipped",
)
MUTMUT_STATES = {
    "killed": "killed",
    "survived": "survived",
    "suspicious": "suspicious",
    "timeout": "timeout",
    "no tests": "untested",
    "skipped": "skipped",
    "not checked": "skipped",
}
MUTMUT_RESULT_RE = re.compile(r"^\s+(?P<name>\S+): (?P<state>[^:]+)\s*$")


class AssuranceEvidenceError(ValueError):
    """Raised when evidence is malformed or outside the bounded contract."""


def _mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AssuranceEvidenceError(f"{field} must be an object")
    return value


def _sequence(value: object, field: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise AssuranceEvidenceError(f"{field} must be an array")
    return value


def _nonnegative_int(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise AssuranceEvidenceError(f"{field} must be a nonnegative integer")
    return value


def _percentage(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AssuranceEvidenceError(f"{field} must be numeric")
    percentage = float(value)
    if not math.isfinite(percentage) or not 0.0 <= percentage <= 100.0:
        raise AssuranceEvidenceError(f"{field} must be between 0 and 100")
    return percentage


def _result(kind: str, status: str, **payload: object) -> dict[str, object]:
    return {
        "schema_id": SCHEMA_ID,
        "kind": kind,
        "status": status,
        **payload,
        "authority": {
            "operational_evidence_only": True,
            "proof_authority": False,
            "scientific_claim_authority": False,
        },
    }


def evaluate_coverage(
    report: Mapping[str, Any],
    *,
    minimum_percent: float,
) -> dict[str, object]:
    """Evaluate a coverage.py JSON report against an incremental floor."""

    floor = _percentage(minimum_percent, "minimum_percent")
    totals = _mapping(report.get("totals"), "totals")
    statements = _nonnegative_int(totals.get("num_statements"), "totals.num_statements")
    branches = _nonnegative_int(totals.get("num_branches", 0), "totals.num_branches")
    percent = _percentage(totals.get("percent_covered"), "totals.percent_covered")
    status = "PASS" if statements > 0 and percent >= floor else "FAIL"
    return _result(
        "coverage",
        status,
        minimum_percent=floor,
        observed_percent=percent,
        num_statements=statements,
        num_branches=branches,
        evidence_nonempty=statements > 0,
    )


def evaluate_mutation(
    report: Mapping[str, Any],
    *,
    minimum_percent: float,
) -> dict[str, object]:
    """Evaluate a normalized mutation report and its explicit dispositions."""

    floor = _percentage(minimum_percent, "minimum_percent")
    counts = _mapping(report.get("counts"), "counts")
    normalized_counts = {
        state: _nonnegative_int(counts.get(state, 0), f"counts.{state}")
        for state in MUTATION_STATES
    }
    measured = sum(
        normalized_counts[state]
        for state in ("killed", "survived", "suspicious", "timeout", "untested")
    )
    score = 100.0 * normalized_counts["killed"] / measured if measured else 0.0
    unresolved = (
        normalized_counts["survived"]
        + normalized_counts["suspicious"]
        + normalized_counts["timeout"]
        + normalized_counts["untested"]
    )
    dispositions = _sequence(report.get("survivor_dispositions", []), "survivor_dispositions")
    disposition_count = len(dispositions)
    status = (
        "PASS"
        if measured > 0 and score >= floor and unresolved <= disposition_count
        else "FAIL"
    )
    return _result(
        "mutation",
        status,
        minimum_percent=floor,
        observed_percent=score,
        measured_mutants=measured,
        unresolved_mutants=unresolved,
        disposition_count=disposition_count,
        counts=normalized_counts,
    )


def normalize_mutmut_results(
    text: str,
    *,
    target_prefix: str,
) -> dict[str, object]:
    """Normalize `mutmut results --all true` for one exact function prefix."""

    if not target_prefix:
        raise AssuranceEvidenceError("target_prefix must be nonempty")
    counts = {state: 0 for state in MUTATION_STATES}
    matched_names: list[str] = []
    for line in text.splitlines():
        match = MUTMUT_RESULT_RE.match(line)
        if match is None or not match.group("name").startswith(target_prefix):
            continue
        state = match.group("state")
        try:
            normalized_state = MUTMUT_STATES[state]
        except KeyError as exc:
            raise AssuranceEvidenceError(f"unknown mutmut state: {state}") from exc
        counts[normalized_state] += 1
        matched_names.append(match.group("name"))
    if not matched_names:
        raise AssuranceEvidenceError("no mutmut results matched target_prefix")
    return {
        "schema_id": "normalized_mutmut_result_v1",
        "target_prefix": target_prefix,
        "mutant_count": len(matched_names),
        "counts": counts,
        "survivor_dispositions": [],
    }


def bandit_finding_key(finding: Mapping[str, Any]) -> str:
    """Return a stable key for one Bandit finding."""

    test_id = finding.get("test_id")
    filename = finding.get("filename")
    line_number = finding.get("line_number")
    if (
        not isinstance(test_id, str)
        or not test_id
        or not isinstance(filename, str)
        or not filename
        or isinstance(line_number, bool)
        or not isinstance(line_number, int)
        or line_number < 1
    ):
        raise AssuranceEvidenceError("Bandit finding identity is malformed")
    return f"{test_id}:{filename}:{line_number}"


def evaluate_bandit(
    report: Mapping[str, Any],
    *,
    dispositions: Mapping[str, Any] | None = None,
) -> dict[str, object]:
    """Count Bandit findings and fail closed on undispositioned high severity."""

    disposition_map = dispositions or {}
    results = _sequence(report.get("results"), "results")
    counts = {severity: 0 for severity in SEVERITIES}
    finding_keys: list[str] = []
    unresolved_high: list[str] = []
    for value in results:
        finding = _mapping(value, "results[]")
        severity = finding.get("issue_severity")
        if severity not in SEVERITIES:
            raise AssuranceEvidenceError("Bandit finding severity is invalid")
        counts[str(severity)] += 1
        key = bandit_finding_key(finding)
        finding_keys.append(key)
        if severity == "HIGH" and key not in disposition_map:
            unresolved_high.append(key)
    status = "PASS" if not unresolved_high else "FAIL"
    return _result(
        "bandit",
        status,
        finding_count=len(results),
        finding_counts=counts,
        disposition_count=sum(key in disposition_map for key in finding_keys),
        unresolved_high=sorted(unresolved_high),
    )


def dependency_finding_key(dependency: str, vulnerability_id: str) -> str:
    """Return a stable key for one dependency vulnerability."""

    if not dependency or not vulnerability_id:
        raise AssuranceEvidenceError("dependency finding identity is malformed")
    return f"{dependency}:{vulnerability_id}"


def evaluate_pip_audit(
    report: Mapping[str, Any],
    *,
    dispositions: Mapping[str, Any] | None = None,
) -> dict[str, object]:
    """Count pip-audit vulnerabilities and require an explicit disposition."""

    disposition_map = dispositions or {}
    dependencies = _sequence(report.get("dependencies"), "dependencies")
    finding_keys: list[str] = []
    for value in dependencies:
        dependency = _mapping(value, "dependencies[]")
        name = dependency.get("name")
        if not isinstance(name, str) or not name:
            raise AssuranceEvidenceError("dependency name is malformed")
        vulnerabilities = _sequence(dependency.get("vulns", []), "dependencies[].vulns")
        for vulnerability_value in vulnerabilities:
            vulnerability = _mapping(vulnerability_value, "dependencies[].vulns[]")
            vulnerability_id = vulnerability.get("id")
            if not isinstance(vulnerability_id, str):
                raise AssuranceEvidenceError("vulnerability id is malformed")
            finding_keys.append(dependency_finding_key(name, vulnerability_id))
    unresolved = sorted(key for key in finding_keys if key not in disposition_map)
    status = "PASS" if not unresolved else "FAIL"
    return _result(
        "pip_audit",
        status,
        dependency_count=len(dependencies),
        finding_count=len(finding_keys),
        disposition_count=sum(key in disposition_map for key in finding_keys),
        unresolved_vulnerabilities=unresolved,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "kind",
        choices=("coverage", "mutation", "mutmut", "bandit", "pip-audit"),
        help="evidence kind to evaluate",
    )
    parser.add_argument("--input", type=Path, required=True, help="tool report JSON")
    parser.add_argument(
        "--dispositions",
        type=Path,
        help="optional JSON object keyed by stable finding ID",
    )
    parser.add_argument("--minimum-percent", type=float, default=0.0)
    parser.add_argument(
        "--target-prefix",
        help="exact mangled function prefix for mutmut result normalization",
    )
    return parser.parse_args(argv)


def _load_object(path: Path, field: str) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AssuranceEvidenceError(f"cannot read {field}: {exc}") from exc
    return _mapping(value, field)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        if args.kind == "mutmut":
            if args.target_prefix is None:
                raise AssuranceEvidenceError("mutmut requires --target-prefix")
            try:
                text = args.input.read_text(encoding="utf-8")
            except OSError as exc:
                raise AssuranceEvidenceError(f"cannot read input: {exc}") from exc
            mutation_report = normalize_mutmut_results(
                text,
                target_prefix=args.target_prefix,
            )
            result = evaluate_mutation(
                mutation_report,
                minimum_percent=args.minimum_percent,
            )
        else:
            json_report = _load_object(args.input, "input")
            dispositions = (
                _load_object(args.dispositions, "dispositions")
                if args.dispositions is not None
                else None
            )
            if args.kind == "coverage":
                result = evaluate_coverage(
                    json_report,
                    minimum_percent=args.minimum_percent,
                )
            elif args.kind == "mutation":
                result = evaluate_mutation(
                    json_report,
                    minimum_percent=args.minimum_percent,
                )
            elif args.kind == "bandit":
                result = evaluate_bandit(json_report, dispositions=dispositions)
            else:
                result = evaluate_pip_audit(json_report, dispositions=dispositions)
    except AssuranceEvidenceError as exc:
        print(json.dumps({"schema_id": SCHEMA_ID, "status": "ERROR", "error": str(exc)}))
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
