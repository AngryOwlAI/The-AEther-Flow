#!/usr/bin/env python3
"""Run the v15 P11 local CI-equivalent research-control validation sequence.

This script is operational receipt evidence only. A PASS result means the
configured control, registry, claim-language, render-freshness, and drift gates
completed successfully in the local repository state. It does not establish
physics proof authority, promote a physics claim, authorize a source-law
adoption, or change Distance-to-GR status.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
REPORT_SCHEMA_ID = "research_control_local_ci_equivalent_report_v1"


@dataclass(frozen=True)
class ValidationCommand:
    label: str
    command: tuple[str, ...]
    purpose: str
    authority_level: str
    required: bool = True
    advisory: bool = False


def python_bin() -> str:
    return ".venv/bin/python"


def base_command_plan(include_smoke_tests: bool = False) -> list[ValidationCommand]:
    py = python_bin()
    commands = [
        ValidationCommand(
            label="memory_validate_only",
            command=(
                py,
                ".codex/skills/project-memory-system/scripts/bootstrap_memory_system.py",
                "--validate-only",
            ),
            purpose="Confirm generated memory, wiki, semantic, and registry derivative surfaces are fresh.",
            authority_level="required-gate",
        ),
        ValidationCommand(
            label="current_frontier_check",
            command=(py, "scripts/research_control/render_current_frontier.py", "--check"),
            purpose="Confirm the current-frontier report is fresh relative to tracked control state.",
            authority_level="required-render-check",
        ),
        ValidationCommand(
            label="dependency_graph_check",
            command=(py, "scripts/research_control/render_dependency_graph.py", "--check"),
            purpose="Confirm dependency graph JSON, Markdown, and DOT artifacts are fresh.",
            authority_level="required-render-check",
        ),
        ValidationCommand(
            label="claim_language_changed_lint",
            command=(py, "scripts/project_control/validate_claim_language.py", "--json", "--changed"),
            purpose="Lint changed claim-language gate surfaces, including high-risk accepted wording.",
            authority_level="required-gate",
        ),
        ValidationCommand(
            label="documentation_impact_validation",
            command=(py, "scripts/project_control/validate_documentation_impact.py", "--json"),
            purpose="Validate documentation-impact receipts for the current transaction.",
            authority_level="required-gate",
        ),
        ValidationCommand(
            label="project_improvement_signal_validation",
            command=(py, "scripts/project_control/collect_project_improvement_signals.py", "--validate-emitted", "--json"),
            purpose="Validate emitted project-improvement signals and bridge sidecars.",
            authority_level="required-gate",
        ),
        ValidationCommand(
            label="research_control_validation",
            command=(py, "scripts/research_control/validate_research_control.py"),
            purpose="Validate research-control task, decision, job, handoff, role, and registry consistency.",
            authority_level="required-gate",
        ),
        ValidationCommand(
            label="research_control_diff_validation",
            command=(py, "scripts/research_control/validate_research_control.py", "--check-diff"),
            purpose="Validate current changed paths against the active AgentJob allowlist.",
            authority_level="required-gate",
        ),
        ValidationCommand(
            label="route_signature_extraction",
            command=(py, "scripts/research_control/extract_route_signatures.py", "--sample", "recent-matter-coupling", "--json"),
            purpose="Exercise implemented v15 route-signature extraction as diagnostic control evidence.",
            authority_level="advisory-diagnostic",
            advisory=True,
        ),
        ValidationCommand(
            label="route_orbit_advisory",
            command=(
                py,
                "scripts/research_control/validate_route_orbits.py",
                "--sample",
                "recent-matter-rr-e",
                "--json",
                "--advisory-only",
            ),
            purpose="Run route-orbit diagnostics without converting advisory evidence into a physics verdict.",
            authority_level="advisory-diagnostic",
            advisory=True,
        ),
        ValidationCommand(
            label="whitespace_diff_check",
            command=("git", "diff", "--check"),
            purpose="Detect whitespace errors in the current transaction diff.",
            authority_level="required-gate",
        ),
    ]
    if include_smoke_tests:
        commands.append(
            ValidationCommand(
                label="repository_smoke_tests",
                command=(py, "-m", "unittest", "discover", "-s", "tests"),
                purpose="Run the repository test suite as an opt-in broad local CI smoke layer.",
                authority_level="ci-smoke",
            )
        )
    return commands


def command_plan(include_smoke_tests: bool = False) -> list[dict[str, Any]]:
    return [
        {
            "label": command.label,
            "command": list(command.command),
            "purpose": command.purpose,
            "authority_level": command.authority_level,
            "required": command.required,
            "advisory": command.advisory,
        }
        for command in base_command_plan(include_smoke_tests=include_smoke_tests)
    ]


def tail(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    return text[-limit:]


def run_command(command: ValidationCommand, repo_root: Path, tail_chars: int) -> dict[str, Any]:
    completed = subprocess.run(
        command.command,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "label": command.label,
        "command": list(command.command),
        "purpose": command.purpose,
        "authority_level": command.authority_level,
        "required": command.required,
        "advisory": command.advisory,
        "returncode": completed.returncode,
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "stdout_tail": tail(completed.stdout, tail_chars),
        "stderr_tail": tail(completed.stderr, tail_chars),
    }


def coverage_map(commands: list[dict[str, Any]]) -> dict[str, bool]:
    labels = {command["label"] for command in commands}
    return {
        "registry_referential_integrity": "research_control_validation" in labels,
        "claim_language_lint": "claim_language_changed_lint" in labels,
        "research_control_validation": "research_control_validation" in labels,
        "current_frontier_check": "current_frontier_check" in labels,
        "generated_derivative_drift_check": {
            "memory_validate_only",
            "current_frontier_check",
            "dependency_graph_check",
        }.issubset(labels),
        "route_signature_extraction_if_implemented": "route_signature_extraction" in labels,
        "no_bare_accepted_high_risk_rows": "claim_language_changed_lint" in labels,
        "no_premature_efe_route": "claim_language_changed_lint" in labels and "research_control_validation" in labels,
        "documentation_impact": "documentation_impact_validation" in labels,
        "diff_allowlist_check": "research_control_diff_validation" in labels,
        "route_orbit_advisory": "route_orbit_advisory" in labels,
        "whitespace_diff_check": "whitespace_diff_check" in labels,
    }


def build_report(
    results: list[dict[str, Any]],
    *,
    include_smoke_tests: bool,
    repo_root: Path,
) -> dict[str, Any]:
    commands = [
        {
            "label": result["label"],
            "command": result["command"],
            "purpose": result["purpose"],
            "authority_level": result["authority_level"],
            "required": result["required"],
            "advisory": result["advisory"],
        }
        for result in results
    ]
    required_failures = [
        result["label"]
        for result in results
        if result["returncode"] != 0 and result["required"] and not result["advisory"]
    ]
    advisory_failures = [
        result["label"]
        for result in results
        if result["returncode"] != 0 and result["advisory"]
    ]
    return {
        "schema_id": REPORT_SCHEMA_ID,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "PASS" if not required_failures else "FAIL",
        "repo_root": str(repo_root),
        "include_smoke_tests": include_smoke_tests,
        "operational_receipt_only": True,
        "no_physics_delta": True,
        "physics_proof_authority": False,
        "distance_to_gr_delta": "none",
        "required_failure_labels": required_failures,
        "advisory_failure_labels": advisory_failures,
        "required_check_coverage": coverage_map(commands),
        "commands": results,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output", type=Path, help="Optional JSON report path.")
    parser.add_argument("--json", action="store_true", help="Print the JSON report to stdout.")
    parser.add_argument("--plan-only", action="store_true", help="Print or write the command plan without executing it.")
    parser.add_argument("--include-smoke-tests", action="store_true", help="Append the full repository unittest smoke suite.")
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
    plan = base_command_plan(include_smoke_tests=args.include_smoke_tests)
    if args.plan_only:
        report: dict[str, Any] = {
            "schema_id": "research_control_local_ci_equivalent_plan_v1",
            "status": "PASS",
            "repo_root": str(repo_root),
            "include_smoke_tests": args.include_smoke_tests,
            "operational_receipt_only": True,
            "no_physics_delta": True,
            "required_check_coverage": coverage_map(command_plan(args.include_smoke_tests)),
            "commands": command_plan(args.include_smoke_tests),
        }
        write_report(report, args.output)
        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    results = [run_command(command, repo_root, args.tail_chars) for command in plan]
    report = build_report(results, include_smoke_tests=args.include_smoke_tests, repo_root=repo_root)
    write_report(report, args.output)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
