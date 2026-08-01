#!/usr/bin/env python3
"""Validate the bounded P13-T02 planner-authoritative cutover contract."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.project_control.classify_project_changes import classify_paths  # noqa: E402
from scripts.validation.executor import ExecutionContext  # noqa: E402
from scripts.validation.plan import canonical_manifest_sha256, load_manifest  # noqa: E402
from scripts.validation.profiles import resolve_profile  # noqa: E402
from scripts.validation.run import load_adapters  # noqa: E402


TASK_ID = "RT-20260801-007"
JOB_ID = "AJ-RT-20260801-007-001"
ARTIFACT_DIR = ROOT / "research_control/tasks" / TASK_ID / "artifacts"
DEFAULT_OUTPUT = ARTIFACT_DIR / "p13_t02_planner_cutover_receipt.json"
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"
CATALOG_PATH = ROOT / "research_control/design/validation_obligation_catalog_v1.yaml"
BINDINGS_PATH = ROOT / "research_control/design/validation_adapter_bindings_v1.json"
PROJECT_WORKFLOW_PATH = ROOT / ".github/workflows/project-control-validation.yml"
SCHEDULED_WORKFLOW_PATH = ROOT / ".github/workflows/scheduled-full-validation.yml"
CHECKPOINT_PATH = ROOT / "scripts/research_control/checkpoint_research_transaction.py"
SKILL_PATHS = (
    ROOT / ".codex/skills/continue-research/SKILL.md",
    ROOT / ".codex/skills/improve-project-system/SKILL.md",
    ROOT / ".codex/skills/project-memory-system/SKILL.md",
    ROOT / ".codex/skills/user-modified-project/SKILL.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout.strip()


def load_checkpoint_module():
    name = "p13_t02_checkpoint_contract"
    specification = importlib.util.spec_from_file_location(name, CHECKPOINT_PATH)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load checkpoint module")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def make_plan(target: str) -> str:
    completed = subprocess.run(
        ["make", "-n", "PYTHON=.venv/bin/python", target],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(f"make -n {target} failed: {completed.stderr.strip()}")
    return completed.stdout


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main() -> int:
    args = parse_args()
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, evidence: Any) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "evidence": evidence,
            }
        )

    manifest = load_manifest(MANIFEST_PATH)
    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    bindings_document = json.loads(BINDINGS_PATH.read_text(encoding="utf-8"))
    adapters = load_adapters(BINDINGS_PATH, manifest)
    by_id = {str(gate["gate_id"]): gate for gate in manifest["gates"]}

    check(
        "live_authority_pair",
        manifest["migration_epoch"] == "planner_authoritative"
        and manifest["execution_authority"] == "manifest_planner",
        {
            "migration_epoch": manifest["migration_epoch"],
            "execution_authority": manifest["execution_authority"],
        },
    )
    check(
        "obligation_catalog_authority_pair",
        catalog["migration_epoch"] == "planner_authoritative"
        and catalog["execution_authority"] == "manifest_planner",
        {
            "migration_epoch": catalog["migration_epoch"],
            "execution_authority": catalog["execution_authority"],
        },
    )
    check(
        "adapter_binding_active",
        bindings_document["status"] == "active" and bool(adapters),
        {
            "status": bindings_document["status"],
            "adapter_count": len(adapters),
        },
    )

    full = resolve_profile(
        manifest,
        classify_paths([]),
        requested_profile="full",
    ).plan
    required_full = {
        gate_id
        for gate_id, gate in by_id.items()
        if gate["severity"] == "blocking" and gate_id != "checkpoint_transaction"
    }
    missing_full = sorted(required_full - set(full.selected_gate_ids))
    missing_full_adapters = sorted(
        gate_id
        for gate_id in full.selected_gate_ids
        if by_id[gate_id]["adapter"] not in adapters
    )
    check(
        "unfiltered_full_blocking_coverage",
        not missing_full and "test_shard_repository" in full.selected_gate_ids,
        {
            "required_blocking_gate_count": len(required_full),
            "selected_gate_count": len(full.selected_gate_ids),
            "missing_gate_ids": missing_full,
        },
    )
    check(
        "selected_full_adapter_coverage",
        not missing_full_adapters,
        {"missing_adapter_gate_ids": missing_full_adapters},
    )

    affected_cases = {
        "claim_language": (
            ("README.md",),
            "claim_language_changed",
        ),
        "targeted_pdf": (
            ("legacy_ontology/tex/aether_flow_consistency.tex",),
            "targeted_pdf_build",
        ),
        "mermaid": (
            (
                "markdown/html-explainer-specs/project-overview-explainer.md",
                "README.md",
            ),
            "mermaid_sources",
        ),
        "obligation_catalog": (
            ("research_control/design/validation_obligation_catalog_v1.yaml",),
            "research_control_diff",
        ),
    }
    affected_evidence: dict[str, Any] = {}
    affected_pass = True
    for case_id, (paths, required_gate_id) in affected_cases.items():
        classification = classify_paths(paths)
        plan = resolve_profile(
            manifest,
            classification,
            requested_profile="affected",
        ).plan
        missing_case_adapters = sorted(
            gate_id
            for gate_id in plan.selected_gate_ids
            if by_id[gate_id]["adapter"] not in adapters
        )
        case_pass = (
            not plan.unknown_paths
            and required_gate_id in plan.selected_gate_ids
            and by_id[required_gate_id]["adapter"] in adapters
            and not missing_case_adapters
        )
        affected_pass = affected_pass and case_pass
        affected_evidence[case_id] = {
            "paths": list(paths),
            "path_tags": list(plan.path_tags),
            "required_gate_id": required_gate_id,
            "selected": required_gate_id in plan.selected_gate_ids,
            "unknown_paths": list(plan.unknown_paths),
            "missing_adapter_gate_ids": missing_case_adapters,
        }
    check("affected_special_gate_coverage", affected_pass, affected_evidence)

    targeted_pdf_gate = by_id["targeted_pdf_build"]
    targeted_pdf_adapter = adapters[targeted_pdf_gate["adapter"]]
    with tempfile.TemporaryDirectory() as directory:
        temporary_root = Path(directory)
        stdout_path = temporary_root / "stdout"
        stderr_path = temporary_root / "stderr"
        empty_target_result = targeted_pdf_adapter.run(
            ExecutionContext(
                gate_id="targeted_pdf_build",
                timeout_seconds=5,
                stdout_path=stdout_path,
                stderr_path=stderr_path,
                cancellation=threading.Event(),
                changed_paths=(),
                scopes=("repository",),
            )
        )
        empty_target_stdout = stdout_path.read_text(encoding="utf-8")
    required_pdf_outputs = {
        "legacy_ontology/pdfs/**",
        "manuscripts/pdfs/**",
        "ontology/pdfs/**",
        "registries/**",
        "wiki/**",
    }
    check(
        "targeted_pdf_contract_and_empty_set_safety",
        empty_target_result.exit_code == 0
        and "no changed TeX paths" in empty_target_stdout
        and required_pdf_outputs <= set(targeted_pdf_gate["output_globs"]),
        {
            "declared_output_globs": targeted_pdf_gate["output_globs"],
            "empty_target_exit_code": empty_target_result.exit_code,
            "empty_target_stdout": empty_target_stdout.strip(),
        },
    )

    make_authoritative = make_plan("validate-project-control")
    make_legacy = make_plan("validate-project-control-legacy")
    check(
        "make_authoritative_owner",
        make_authoritative.count("scripts.validation.cli run --profile full --paths") == 1
        and "validate_research_control.py --check-diff" not in make_authoritative,
        {"planner_full_execution_count": make_authoritative.count("scripts.validation.cli run --profile full --paths")},
    )
    check(
        "make_legacy_rollback",
        "validate_research_control.py --check-diff" in make_legacy
        and "unittest discover -s tests" in make_legacy,
        {"target": "validate-project-control-legacy"},
    )

    project_workflow = PROJECT_WORKFLOW_PATH.read_text(encoding="utf-8")
    scheduled_workflow = SCHEDULED_WORKFLOW_PATH.read_text(encoding="utf-8")
    project_yaml = yaml.safe_load(project_workflow)
    scheduled_yaml = yaml.safe_load(scheduled_workflow)
    check(
        "project_workflow_single_owner",
        set(project_yaml["jobs"]) == {"quality_portability_matrix", "validate_project_control"}
        and "make PYTHON=.venv/bin/python validate-project-control" in project_workflow
        and "validation_plan_shadow:" not in project_workflow
        and "validation_shards_shadow:" not in project_workflow,
        {"job_ids": sorted(project_yaml["jobs"])},
    )
    check(
        "scheduled_unfiltered_full",
        set(scheduled_yaml["jobs"]) == {"scheduled_assurance", "scheduled_full_validation"}
        and "make PYTHON=.venv/bin/python validate-project-control" in scheduled_workflow
        and "paths-ignore:" not in scheduled_workflow
        and "branches-ignore:" not in scheduled_workflow,
        {"job_ids": sorted(scheduled_yaml["jobs"])},
    )

    skill_failures: list[str] = []
    for path in SKILL_PATHS:
        text = path.read_text(encoding="utf-8")
        if not all(
            fragment in text
            for fragment in (
                "scripts.validation.cli run --profile <fast|affected|full>",
                "checkpoint_research_transaction.py --job-id <agent-job-id>",
                "validate-project-control-legacy",
                "--legacy-validation",
                "planner_authoritative",
            )
        ):
            skill_failures.append(path.relative_to(ROOT).as_posix())
    check("skill_entrypoint_cutover", not skill_failures, {"failures": skill_failures})

    checkpoint = load_checkpoint_module()
    check(
        "checkpoint_default_and_rollbacks",
        checkpoint.parse_args([]).validation_mode == "planner"
        and checkpoint.parse_args(["--legacy-validation"]).validation_mode == "legacy"
        and checkpoint.parse_args(["--compare-validation"]).validation_mode == "compare",
        {
            "default": checkpoint.parse_args([]).validation_mode,
            "legacy": checkpoint.parse_args(["--legacy-validation"]).validation_mode,
            "compare": checkpoint.parse_args(["--compare-validation"]).validation_mode,
        },
    )

    failures = [item["check_id"] for item in checks if item["status"] != "PASS"]
    receipt = {
        "schema_id": "p13_t02_planner_cutover_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_commit": git("rev-parse", "HEAD"),
        "status": "PASS" if not failures else "FAIL",
        "manifest_sha256": canonical_manifest_sha256(manifest),
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): sha256(path)
            for path in (
                MANIFEST_PATH,
                CATALOG_PATH,
                BINDINGS_PATH,
                PROJECT_WORKFLOW_PATH,
                SCHEDULED_WORKFLOW_PATH,
                CHECKPOINT_PATH,
            )
        },
        "counts": {
            "check_count": len(checks),
            "pass_count": len(checks) - len(failures),
            "fail_count": len(failures),
        },
        "failed_check_ids": failures,
        "checks": checks,
        "authority": {
            "operational_validation_only": True,
            "scientific_claims_changed": False,
            "distance_to_gr_changed": False,
            "physics_claim_authority": False,
            "ontology_authority": False,
            "benchmark_authority": False,
            "proof_authority": False,
            "gate_chair_authority": False,
            "publication_authorized": False,
            "push_performed": False,
            "hosted_workflow_dispatch_performed": False,
        },
    }
    if args.write_report:
        atomic_write(args.output, receipt)
    if args.json:
        print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    else:
        print(
            f"{receipt['status']} checks={receipt['counts']['check_count']} "
            f"failures={receipt['counts']['fail_count']}"
        )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
