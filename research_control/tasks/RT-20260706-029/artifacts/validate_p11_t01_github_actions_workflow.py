#!/usr/bin/env python3
"""Validate the v17 P11-T01 GitHub Actions workflow artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
WORKFLOW_PATH = REPO_ROOT / ".github/workflows/project-control-validation.yml"

REQUIRED_SNIPPETS = {
    "workflow name": "name: Project Control Validation",
    "push trigger": "push:",
    "pull request trigger": "pull_request:",
    "manual trigger": "workflow_dispatch:",
    "read-only contents permission": "contents: read",
    "project-control job": "validate_project_control:",
    "memory read-only job": "validate_memory_read_only:",
    "python setup action": "actions/setup-python@v5",
    "checkout action": "actions/checkout@v4",
    "python 3.12": 'python-version: "3.12"',
    "venv creation": "python -m venv .venv",
    "requirements install": ".venv/bin/python -m pip install -r requirements.txt",
    "make entrypoint": "make PYTHON=.venv/bin/python validate-project-control",
    "memory validate-only command": ".venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only",
}

FORBIDDEN_SNIPPETS = {
    "write-all permission": "write-all",
    "write contents permission": "contents: write",
    "local cache output": ".local/",
    "physics proof claim": "physics proof",
    "benchmark promotion": "benchmark promotion",
    "completed derivation": "completed derivation",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def job_block(text: str, job_name: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line == f"  {job_name}:":
            start = index
            break
    if start is None:
        return ""

    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("  ") and not line.startswith("    ") and line.endswith(":"):
            end = index
            break
    return "\n".join(lines[start:end])


def validate() -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    text = WORKFLOW_PATH.read_text(encoding="utf-8") if WORKFLOW_PATH.exists() else ""
    lower = text.lower()

    if not WORKFLOW_PATH.exists():
        errors.append(f"missing workflow: {WORKFLOW_PATH.relative_to(REPO_ROOT)}")

    for label, snippet in REQUIRED_SNIPPETS.items():
        if snippet not in text:
            errors.append(f"missing required snippet for {label}: {snippet}")

    for label, snippet in FORBIDDEN_SNIPPETS.items():
        if snippet.lower() in lower:
            errors.append(f"forbidden snippet present for {label}: {snippet}")

    project_job = job_block(text, "validate_project_control")
    memory_job = job_block(text, "validate_memory_read_only")
    if "make PYTHON=.venv/bin/python validate-project-control" not in project_job:
        errors.append("validate_project_control job does not call make validate-project-control with the CI PYTHON wrapper")
    if "bootstrap_memory_system.py --validate-only" not in memory_job:
        errors.append("validate_memory_read_only job does not run bootstrap_memory_system.py --validate-only")
    if "make " in memory_job:
        warnings.append("validate_memory_read_only job invokes make; expected a narrow read-only validation command")

    return {
        "schema_id": "p11_t01_github_actions_workflow_report_v1",
        "status": "PASS" if not errors else "FAIL",
        "workflow_path": str(WORKFLOW_PATH.relative_to(REPO_ROOT)),
        "workflow_hash": sha256(WORKFLOW_PATH) if WORKFLOW_PATH.exists() else "",
        "required_snippet_count": len(REQUIRED_SNIPPETS),
        "forbidden_snippet_count": len(FORBIDDEN_SNIPPETS),
        "project_control_job_present": bool(project_job),
        "memory_read_only_job_present": bool(memory_job),
        "operational_receipt_only": True,
        "physics_proof_authority": False,
        "no_physics_delta": True,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = validate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
