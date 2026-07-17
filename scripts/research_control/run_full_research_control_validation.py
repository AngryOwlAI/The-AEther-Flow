#!/usr/bin/env python3
"""Compatibility wrapper for the shared full validation profile.

The shared planner owns gate selection. During the ``shadow_planner`` epoch,
the legacy Make target remains execution-authoritative. This wrapper only
coordinates those two surfaces and emits operational receipt evidence; it does
not establish physics proof authority or change scientific claim status.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.validation.plan import load_manifest  # noqa: E402


DEFAULT_MANIFEST = REPO_ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
REPORT_SCHEMA_ID = "research_control_local_full_wrapper_report_v2"
PLAN_SCHEMA_ID = "research_control_local_full_wrapper_plan_v2"
CLAIM_SUPERSEDENCE_PREDICATE_ID = "rc_diff_satisfies_claim_language_same_scope_v1"
DEPRECATION_MESSAGE = (
    "DEPRECATED_COMPATIBILITY_WRAPPER: use the shared validation profile targets; "
    "this entry point remains a shadow-planner compatibility surface."
)
LEGACY_COMPATIBILITY_LABELS = {
    "research_control_diff": "research_control_diff_validation",
}


def python_bin() -> str:
    return ".venv/bin/python"


def planner_command() -> list[str]:
    return [
        python_bin(),
        "-m",
        "scripts.validation.cli",
        "plan",
        "--profile",
        "full",
        "--paths",
        "--json",
    ]


def legacy_command() -> list[str]:
    return [
        "make",
        "--no-print-directory",
        f"PYTHON={python_bin()}",
        "validate-project-control-legacy",
    ]


def tail(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    return text[-limit:]


def claim_language_summary(stdout: str) -> dict[str, Any]:
    try:
        payload = json.loads(stdout)
    except (json.JSONDecodeError, TypeError):
        hard_ids = re.findall(r"claim-language hard failure ([a-z0-9_]+)", stdout)
        warning_ids = re.findall(r"claim-language warning ([a-z0-9_]+)", stdout)
        if not hard_ids and not warning_ids and "Research-control validation" not in stdout:
            return {
                "status": "UNAVAILABLE",
                "finding_count": 0,
                "hard_fail_count": 0,
                "warning_count": 0,
                "finding_ids": [],
            }
        return {
            "status": "FAIL" if hard_ids else "PASS",
            "finding_count": len(hard_ids) + len(warning_ids),
            "hard_fail_count": len(hard_ids),
            "warning_count": len(warning_ids),
            "finding_ids": sorted(
                {f"claim_language_changed:{class_id}" for class_id in hard_ids + warning_ids}
            ),
        }
    findings = [
        finding
        for finding in payload.get("findings", [])
        if finding.get("gate_id") == "claim_language_changed"
    ]
    hard_findings = [
        finding
        for finding in findings
        if str(finding.get("severity", "")).startswith("hard_fail_")
        or finding.get("severity") == "blocking"
    ]
    return {
        "status": "FAIL" if hard_findings else "PASS",
        "finding_count": len(findings),
        "hard_fail_count": len(hard_findings),
        "warning_count": len(findings) - len(hard_findings),
        "finding_ids": sorted(
            {str(finding.get("finding_id", "")) for finding in findings if finding.get("finding_id")}
        ),
    }


def run_process(
    command: list[str],
    *,
    repo_root: Path,
    tail_chars: int,
    label: str,
    purpose: str,
    authority_level: str,
) -> tuple[dict[str, Any], str]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    return (
        {
            "label": label,
            "command": command,
            "purpose": purpose,
            "authority_level": authority_level,
            "required": True,
            "advisory": False,
            "returncode": completed.returncode,
            "status": "PASS" if completed.returncode == 0 else "FAIL",
            "stdout_tail": tail(stdout, tail_chars),
            "stderr_tail": tail(stderr, tail_chars),
        },
        stdout,
    )


def run_shared_planner(
    repo_root: Path,
    tail_chars: int,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    result, stdout = run_process(
        planner_command(),
        repo_root=repo_root,
        tail_chars=tail_chars,
        label="validation_plan_full",
        purpose="Select the canonical full profile through the shared validation planner CLI.",
        authority_level="selection-only",
    )
    if result["returncode"] != 0:
        return result, None
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as error:
        result["returncode"] = 2
        result["status"] = "FAIL"
        result["planner_parse_error"] = str(error)
        return result, None
    if not isinstance(payload, dict):
        result["returncode"] = 2
        result["status"] = "FAIL"
        result["planner_parse_error"] = "shared planner did not emit a JSON object"
        return result, None
    return result, payload


def command_plan(
    include_smoke_tests: bool = False,
    shared_plan: dict[str, Any] | None = None,
    *,
    repo_root: Path = REPO_ROOT,
) -> list[dict[str, Any]]:
    """Return a deprecated manifest-derived compatibility projection.

    This function remains for callers that inspect the former runner API. It
    does not select gates or own an executable command chain: selection comes
    from the shared CLI and command metadata comes from the shared manifest.
    """

    del include_smoke_tests
    if shared_plan is None:
        result, shared_plan = run_shared_planner(repo_root.resolve(), 4000)
        if result["returncode"] != 0 or shared_plan is None:
            return []
    manifest_path = repo_root / DEFAULT_MANIFEST.relative_to(REPO_ROOT)
    manifest = load_manifest(manifest_path)
    gate_records = {
        str(gate.get("gate_id", "")): gate
        for gate in manifest.get("gates", [])
        if isinstance(gate, dict)
    }
    selected_gate_ids = [str(gate_id) for gate_id in shared_plan.get("selected_gate_ids", [])]
    compatibility_omissions = (
        {"research_control_core"}
        if "research_control_diff" in selected_gate_ids
        else set()
    )
    projection: list[dict[str, Any]] = []
    for gate_id in selected_gate_ids:
        if gate_id in compatibility_omissions:
            continue
        gate = gate_records.get(str(gate_id), {})
        compatible = gate.get("command_compatibility", [])
        command = shlex.split(str(compatible[0])) if compatible else []
        projection.append(
            {
                "gate_id": str(gate_id),
                "label": LEGACY_COMPATIBILITY_LABELS.get(str(gate_id), str(gate_id)),
                "command": command,
                "purpose": str(gate.get("description", "")),
                "authority_level": "legacy-authoritative",
                "required": str(gate.get("severity", "")) == "blocking",
                "advisory": str(gate.get("severity", "")) in {"advisory", "local_only"},
                "satisfies_obligations": list(gate.get("satisfies_obligations", [])),
            }
        )
    return projection


def _declared_advisory_diagnostic(
    gate_id: str,
    command_fragment: str,
    *,
    repo_root: Path,
) -> bool:
    """Confirm an explicit diagnostic remains available outside ordinary full."""

    manifest_path = repo_root / DEFAULT_MANIFEST.relative_to(REPO_ROOT)
    manifest = load_manifest(manifest_path)
    gate = next(
        (
            item
            for item in manifest.get("gates", [])
            if isinstance(item, dict) and item.get("gate_id") == gate_id
        ),
        None,
    )
    if not isinstance(gate, dict):
        return False
    commands = gate.get("command_compatibility", [])
    profiles = gate.get("profiles", [])
    obligations = gate.get("satisfies_obligations", [])
    return (
        gate.get("severity") == "advisory"
        and gate.get("mutating") is False
        and isinstance(commands, list)
        and any(command_fragment in str(command) for command in commands)
        and isinstance(profiles, list)
        and "doctor" in profiles
        and isinstance(obligations, list)
        and gate_id in obligations
    )


def coverage_map(
    commands: list[dict[str, Any]],
    *,
    repo_root: Path = REPO_ROOT,
) -> dict[str, bool]:
    """Return the deprecated coverage view derived from shared manifest data.

    Direct advisory diagnostics count as compatibility-covered when they
    remain explicitly declared for Doctor or role-obligation use, even though
    P8-T07 intentionally omits their execution from the ordinary full plan.
    """

    gate_ids = {str(command.get("gate_id", "")) for command in commands}
    obligations = {
        str(obligation)
        for command in commands
        for obligation in command.get("satisfies_obligations", [])
    }
    research_control_diff = "research_control_diff" in gate_ids
    return {
        "registry_referential_integrity": research_control_diff,
        "active_state_sidecar_validation": research_control_diff
        and "compact_frontier_freshness" in gate_ids,
        "claim_language_lint": research_control_diff,
        "research_control_validation": research_control_diff,
        "research_control_core_obligation": "research_control_core" in obligations
        or research_control_diff,
        "research_control_diff_obligation": "research_control_diff" in obligations,
        "current_frontier_check": "current_frontier_freshness" in gate_ids,
        "compact_current_frontier_check": "compact_frontier_freshness" in gate_ids,
        "generated_derivative_drift_check": {
            "memory_core",
            "current_frontier_freshness",
            "compact_frontier_freshness",
            "dependency_graph_freshness",
        }.issubset(gate_ids),
        "task_index_validation": "task_index_freshness" in gate_ids,
        "claim_graph_validation": "claim_graph_validation" in gate_ids,
        "route_signature_extraction_if_implemented": _declared_advisory_diagnostic(
            "route_signature_diagnostic",
            "extract_route_signatures.py",
            repo_root=repo_root,
        ),
        "no_bare_accepted_high_risk_rows": research_control_diff,
        "no_premature_efe_route": research_control_diff,
        "documentation_impact": "documentation_impact" in gate_ids,
        "diff_allowlist_check": research_control_diff,
        "route_orbit_advisory": _declared_advisory_diagnostic(
            "route_orbit_diagnostic",
            "validate_route_orbits.py --advisory-only",
            repo_root=repo_root,
        ),
        "whitespace_diff_check": "git_diff_check" in gate_ids,
    }


def build_report(
    planner_result: dict[str, Any],
    shared_plan: dict[str, Any] | None,
    legacy_result: dict[str, Any] | None,
    *,
    include_smoke_tests: bool,
    plan_only: bool,
    repo_root: Path,
) -> dict[str, Any]:
    results = [planner_result]
    if legacy_result is not None:
        results.append(legacy_result)
    required_failures = [
        result["label"]
        for result in results
        if result["returncode"] != 0 and result["required"] and not result["advisory"]
    ]
    compatibility_plan = (
        command_plan(shared_plan=shared_plan, repo_root=repo_root)
        if shared_plan is not None
        else []
    )
    legacy_stdout = str((legacy_result or {}).get("stdout_tail", ""))
    return {
        "schema_id": PLAN_SCHEMA_ID if plan_only else REPORT_SCHEMA_ID,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "PASS" if not required_failures else "FAIL",
        "repo_root": str(repo_root),
        "requested_profile": "full",
        "effective_profile": (shared_plan or {}).get("effective_profile", ""),
        "manifest_hash": (shared_plan or {}).get("manifest_hash", ""),
        "selected_gate_ids": (shared_plan or {}).get("selected_gate_ids", []),
        "execution_authority": (shared_plan or {}).get("execution_authority", "legacy"),
        "planner_executes_commands": False,
        "plan_only": plan_only,
        "include_smoke_tests": include_smoke_tests,
        "include_smoke_tests_compatibility": "accepted_no_op_full_profile_already_selects_repository_tests",
        "compatibility_wrapper_deprecated": True,
        "deprecation_message": DEPRECATION_MESSAGE,
        "replacement_entry_points": [
            "make validate-full",
            ".venv/bin/python -m scripts.validation.cli plan --profile full --paths --json",
        ],
        "legacy_execution_status": (
            "NOT_RUN" if legacy_result is None else legacy_result["status"]
        ),
        "ci_equivalent": False,
        "ci_equivalence_status": "not_equivalent_until_v19_p11_centralization",
        "operational_receipt_only": True,
        "no_physics_delta": True,
        "physics_proof_authority": False,
        "distance_to_gr_delta": "none",
        "required_failure_labels": required_failures,
        "advisory_failure_labels": [],
        "required_check_coverage": coverage_map(
            compatibility_plan,
            repo_root=repo_root,
        ),
        "claim_language_obligation": {
            "predicate_id": CLAIM_SUPERSEDENCE_PREDICATE_ID,
            "satisfied_by": "legacy_validate_project_control",
            "same_scope_required": True,
            "summary": claim_language_summary(legacy_stdout),
        },
        "shared_plan": shared_plan or {},
        "compatibility_command_projection": compatibility_plan,
        "commands": results,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output", type=Path, help="Optional JSON report path.")
    parser.add_argument("--json", action="store_true", help="Print the JSON report to stdout.")
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Request the shared full profile without running the legacy executor.",
    )
    parser.add_argument(
        "--include-smoke-tests",
        action="store_true",
        help="Deprecated no-op; the full profile already selects repository tests.",
    )
    parser.add_argument("--tail-chars", type=int, default=4000, help="Maximum stdout/stderr characters retained per command.")
    return parser.parse_args(argv)


def write_report(report: dict[str, Any], output: Path | None) -> None:
    if not output:
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    print(DEPRECATION_MESSAGE, file=sys.stderr)
    planner_result, shared_plan = run_shared_planner(repo_root, args.tail_chars)
    legacy_result: dict[str, Any] | None = None
    if planner_result["returncode"] == 0 and not args.plan_only:
        legacy_result, _ = run_process(
            legacy_command(),
            repo_root=repo_root,
            tail_chars=args.tail_chars,
            label="legacy_validate_project_control",
            purpose="Execute the existing full project-control chain under legacy shadow authority.",
            authority_level="legacy-authoritative",
        )
    report = build_report(
        planner_result,
        shared_plan,
        legacy_result,
        include_smoke_tests=args.include_smoke_tests,
        plan_only=args.plan_only,
        repo_root=repo_root,
    )
    write_report(report, args.output)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    if planner_result["returncode"] != 0:
        return int(planner_result["returncode"])
    if legacy_result is not None:
        return int(legacy_result["returncode"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
