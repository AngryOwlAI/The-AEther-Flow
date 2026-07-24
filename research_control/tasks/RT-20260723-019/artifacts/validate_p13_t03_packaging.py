#!/usr/bin/env python3
"""Validate the bounded v21 P13-T03 packaging and dependency contract."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260723-019"
JOB_ID = "AJ-RT-20260723-019-001"
ARTIFACTS = ROOT / "research_control/tasks" / TASK_ID / "artifacts"
LOCK = ARTIFACTS / "requirements.lock"
REPORT = ARTIFACTS / "p13_t03_packaging_receipt.json"
LOCAL = ROOT / ".local/v21_p13_t03"
PYPROJECT = ROOT / "pyproject.toml"
RUNTIME_WRAPPER = ROOT / "requirements.txt"
DEV_WRAPPER = ROOT / "requirements-dev.txt"
MAKEFILE = ROOT / "Makefile"
WORKFLOWS = (
    ROOT / ".github/workflows/project-control-validation.yml",
    ROOT / ".github/workflows/scheduled-full-validation.yml",
)
POLICY = ARTIFACTS / "packaging_environment_policy_v1.md"
MIGRATION = ARTIFACTS / "packaging_migration_guide.md"
CLASSIFIER = ROOT / "scripts/project_control/classify_project_changes.py"
NOTICES = ROOT / "NOTICES"

EXPECTED_DISTRIBUTIONS = {
    "PyMuPDF": "1.27.2.3",
    "PyYAML": "6.0.3",
}
EXPECTED_LOCK_COMMAND = (
    "uv pip compile pyproject.toml --all-extras --universal "
    "--generate-hashes --output-file "
    "research_control/tasks/RT-20260723-019/artifacts/requirements.lock"
)
FOCUSED_TESTS = (
    "tests.test_project_change_classifier",
    "tests.test_validation_orchestration",
    "tests.test_ci_validation_plan",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalized_lock_body(path: Path) -> bytes:
    lines = path.read_bytes().splitlines(keepends=True)
    while lines and (lines[0].startswith(b"#") or not lines[0].strip()):
        lines.pop(0)
    return b"".join(lines)


def record_check(
    checks: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    evidence: str,
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "evidence": evidence,
        }
    )


def run_command(
    label: str,
    command: list[str],
    *,
    python_path: Path | None = None,
    timeout: int = 900,
) -> dict[str, Any]:
    LOCAL.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )
    duration = time.monotonic() - started
    stdout_path = LOCAL / f"{label}.stdout.log"
    stderr_path = LOCAL / f"{label}.stderr.log"
    stdout_path.write_text(completed.stdout or "", encoding="utf-8")
    stderr_path.write_text(completed.stderr or "", encoding="utf-8")
    result: dict[str, Any] = {
        "label": label,
        "command": command,
        "returncode": completed.returncode,
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "duration_seconds": round(duration, 6),
        "stdout": {
            "path": stdout_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(stdout_path),
            "bytes": stdout_path.stat().st_size,
        },
        "stderr": {
            "path": stderr_path.relative_to(ROOT).as_posix(),
            "sha256": sha256(stderr_path),
            "bytes": stderr_path.stat().st_size,
        },
    }
    if python_path is not None and completed.returncode == 0:
        version = subprocess.run(
            [
                python_path.as_posix(),
                "-c",
                (
                    "import importlib.metadata, json, platform, sys; "
                    "print(json.dumps({"
                    "'implementation': platform.python_implementation(), "
                    "'python_series': f'{sys.version_info.major}.{sys.version_info.minor}', "
                    "'pymupdf': importlib.metadata.version('PyMuPDF'), "
                    "'pyyaml': importlib.metadata.version('PyYAML')"
                    "}, sort_keys=True))"
                ),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        result["environment_probe"] = (
            json.loads(version.stdout) if version.returncode == 0 else {}
        )
    return result


def validate_static_contract(checks: list[dict[str, Any]]) -> dict[str, Any]:
    pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    project = pyproject["project"]
    tool = pyproject["tool"]
    environment = tool["aether-flow"]["environment"]

    record_check(
        checks,
        "python_series",
        project["requires-python"] == ">=3.12,<3.13",
        f"requires-python={project['requires-python']}",
    )
    record_check(
        checks,
        "direct_dependency",
        project["dependencies"]
        == [
            f"{name}=={version}"
            for name, version in EXPECTED_DISTRIBUTIONS.items()
        ],
        f"dependencies={project['dependencies']}",
    )
    expected_groups = {"validation", "test", "proof", "documentation"}
    optional_groups = project["optional-dependencies"]
    record_check(
        checks,
        "named_dependency_groups",
        set(optional_groups) == expected_groups
        and all(optional_groups[group] == [] for group in expected_groups)
        and pyproject["dependency-groups"] == {"dev": []},
        "validation,test,proof,documentation,dev groups declared",
    )
    record_check(
        checks,
        "lock_metadata",
        environment["lock-file"]
        == "research_control/tasks/RT-20260723-019/artifacts/requirements.lock"
        and environment["lock-maintenance-command"] == EXPECTED_LOCK_COMMAND
        and environment["ordinary-install-command"]
        == "python -m pip install --require-hashes -r requirements-dev.txt",
        "pyproject environment commands and lock path match policy",
    )
    external_names = {
        entry["name"] for entry in tool["aether-flow"]["external-tools"]
    }
    record_check(
        checks,
        "external_tool_metadata",
        external_names
        == {"git", "make", "uv", "Lean", "TeX", "Node.js and Playwright"}
        and all(
            entry["managed-by-python-lock"] is False
            for entry in tool["aether-flow"]["external-tools"]
        ),
        f"external_tools={sorted(external_names)}",
    )

    lock_text = LOCK.read_text(encoding="utf-8")
    lock_requirement_lines = [
        line for line in lock_text.splitlines()
        if line and not line[0].isspace() and not line.startswith("#")
    ]
    hashes = re.findall(r"--hash=sha256:([0-9a-f]{64})", lock_text)
    record_check(
        checks,
        "exact_hash_lock",
        lock_requirement_lines
        == [
            f"{name.lower()}=={version} \\"
            for name, version in EXPECTED_DISTRIBUTIONS.items()
        ]
        and len(hashes) >= 1
        and len(hashes) == len(set(hashes)),
        (
            f"requirements={lock_requirement_lines}; "
            f"unique_sha256_hashes={len(set(hashes))}"
        ),
    )
    record_check(
        checks,
        "compatibility_wrappers",
        RUNTIME_WRAPPER.read_text(encoding="utf-8").splitlines()[-1]
        == "-r research_control/tasks/RT-20260723-019/artifacts/requirements.lock"
        and DEV_WRAPPER.read_text(encoding="utf-8").splitlines()[-1]
        == "-r requirements.txt",
        "runtime wrapper includes lock; dev wrapper includes runtime wrapper",
    )

    make_text = MAKEFILE.read_text(encoding="utf-8")
    record_check(
        checks,
        "make_parity",
        (
            "VALIDATION_REQUIRED_DISTRIBUTIONS := "
            + " ".join(
                f"{name}=={version}"
                for name, version in EXPECTED_DISTRIBUTIONS.items()
            )
        )
        in make_text
        and "pip install --require-hashes -r requirements-dev.txt" in make_text
        and all(
            path in make_text
            for path in (
                "pyproject.toml",
                "research_control/tasks/RT-20260723-019/artifacts/requirements.lock",
                "requirements.txt",
                "requirements-dev.txt",
            )
        ),
        "Make setup and validation environment use the exact contract",
    )

    workflow_text = "\n".join(
        workflow.read_text(encoding="utf-8") for workflow in WORKFLOWS
    )
    provisioning_lines = [
        line.strip()
        for line in workflow_text.splitlines()
        if "pip install" in line and "-r requirements.txt" in line
    ]
    record_check(
        checks,
        "ci_dependency_parity",
        len(provisioning_lines) == 6
        and all("--require-hashes" in line for line in provisioning_lines),
        f"hash_enforced_ci_provisioning_steps={len(provisioning_lines)}",
    )

    classifier_text = CLASSIFIER.read_text(encoding="utf-8")
    record_check(
        checks,
        "classifier_coverage",
        "DEPENDENCY_ENVIRONMENT_PATHS" in classifier_text
        and "path in DEPENDENCY_ENVIRONMENT_PATHS" in classifier_text,
        "root dependency surfaces have an explicit classifier family",
    )
    record_check(
        checks,
        "policy_and_migration",
        POLICY.exists()
        and MIGRATION.exists()
        and "Failure behavior" in POLICY.read_text(encoding="utf-8")
        and "Rollback" in MIGRATION.read_text(encoding="utf-8"),
        "task-local policy and migration guide are present",
    )
    notice_text = " ".join(NOTICES.read_text(encoding="utf-8").split())
    record_check(
        checks,
        "license_boundary",
        "package dependencies remain under their own licenses" in notice_text,
        "no new dependency; repository third-party notice remains explicit",
    )

    return {
        "pyproject_sha256": sha256(PYPROJECT),
        "lock_sha256": sha256(LOCK),
        "lock_body_sha256": sha256_bytes(normalized_lock_body(LOCK)),
        "lock_hash_count": len(hashes),
        "requirements_sha256": sha256(RUNTIME_WRAPPER),
        "requirements_dev_sha256": sha256(DEV_WRAPPER),
    }


def reproduce_lock(checks: list[dict[str, Any]]) -> dict[str, Any]:
    uv = shutil.which("uv")
    if uv is None:
        record_check(checks, "lock_reproducibility", False, "uv not found")
        return {"status": "FAIL", "reason": "uv_not_found"}
    with tempfile.TemporaryDirectory(prefix="aether-p13-t03-lock-") as directory:
        output = Path(directory) / "requirements.lock"
        result = run_command(
            "lock-reproduction",
            [
                uv,
                "pip",
                "compile",
                "pyproject.toml",
                "--all-extras",
                "--universal",
                "--generate-hashes",
                "--no-header",
                "--output-file",
                output.as_posix(),
            ],
        )
        matches = (
            result["returncode"] == 0
            and output.exists()
            and normalized_lock_body(output) == normalized_lock_body(LOCK)
        )
        record_check(
            checks,
            "lock_reproducibility",
            matches,
            (
                "uv resolution matches committed normalized lock body"
                if matches
                else "uv resolution differs or failed"
            ),
        )
        result["committed_lock_body_sha256"] = sha256_bytes(
            normalized_lock_body(LOCK)
        )
        result["reproduced_lock_body_sha256"] = (
            sha256_bytes(normalized_lock_body(output)) if output.exists() else ""
        )
        return result


def clean_install(checks: list[dict[str, Any]]) -> dict[str, Any]:
    if platform.python_implementation() != "CPython" or sys.version_info[:2] != (3, 12):
        record_check(
            checks,
            "clean_install",
            False,
            (
                f"requires CPython 3.12; observed "
                f"{platform.python_implementation()} "
                f"{sys.version_info.major}.{sys.version_info.minor}"
            ),
        )
        return {"status": "FAIL", "reason": "unsupported_bootstrap_python"}

    with tempfile.TemporaryDirectory(prefix="aether-p13-t03-env-") as directory:
        environment = Path(directory) / ".venv"
        create = run_command(
            "clean-venv-create",
            [sys.executable, "-m", "venv", environment.as_posix()],
        )
        python_path = environment / "bin/python"
        if create["returncode"] != 0:
            record_check(checks, "clean_install", False, "venv creation failed")
            return {"status": "FAIL", "create": create}
        install = run_command(
            "clean-hash-install",
            [
                python_path.as_posix(),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--require-hashes",
                "-r",
                "requirements-dev.txt",
            ],
            python_path=python_path,
        )
        tests = run_command(
            "clean-focused-tests",
            [
                python_path.as_posix(),
                "-m",
                "unittest",
                "-v",
                *FOCUSED_TESTS,
            ],
        )
        observed = install.get("environment_probe", {})
        passed = (
            install["returncode"] == 0
            and tests["returncode"] == 0
            and observed.get("implementation") == "CPython"
            and observed.get("python_series") == "3.12"
            and observed.get("pymupdf") == EXPECTED_DISTRIBUTIONS["PyMuPDF"]
            and observed.get("pyyaml") == EXPECTED_DISTRIBUTIONS["PyYAML"]
        )
        record_check(
            checks,
            "clean_install",
            passed,
            (
                f"environment={observed}; "
                f"install_exit={install['returncode']}; "
                f"focused_tests_exit={tests['returncode']}"
            ),
        )
        return {
            "status": "PASS" if passed else "FAIL",
            "create": create,
            "install": install,
            "focused_tests": tests,
            "environment": observed,
        }


def main() -> int:
    args = parse_args()
    checks: list[dict[str, Any]] = []
    static = validate_static_contract(checks)
    lock_reproduction = reproduce_lock(checks)
    clean_environment = clean_install(checks)
    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    report: dict[str, Any] = {
        "schema_id": "p13_t03_packaging_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": status,
        "scope": "project_system",
        "scientific_claims_changed": False,
        "distance_to_gr_delta_changed": False,
        "dependency_delta": {
            "new_operational_distributions": [],
            "newly_declared_existing_distributions": ["PyYAML"],
            "removed_distributions": [],
            "exact_distributions": [
                f"{name}=={version}"
                for name, version in EXPECTED_DISTRIBUTIONS.items()
            ],
            "license_waiver": False,
        },
        "static_contract": static,
        "lock_reproduction": lock_reproduction,
        "clean_environment": clean_environment,
        "checks": checks,
        "authority_limits": {
            "physics_progress_inferred": False,
            "proof_authority": False,
            "publication_or_push_authority": False,
        },
    }
    if args.write_report:
        REPORT.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    else:
        print(f"P13-T03 packaging validation: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
