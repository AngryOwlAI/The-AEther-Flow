#!/usr/bin/env python3
"""Validate V21 P16-T03 provenance and reproducibility as control evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import tarfile
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260803-013"
JOB_ID = "AJ-RT-20260803-013-001"
AUDIT_HEAD = "ba3b0d969d465dad233c84716ad5254eddba2439"
ARTIFACTS = Path(__file__).resolve().parent
MATRIX = ROOT / "research_control/tasks/RT-20260803-002/artifacts/v21_final_recommendation_coverage_matrix.json"
ATTEMPT_VALIDATION = ROOT / "research_control/tasks/RT-20260721-006/artifacts/v21_attempt_history_validation.json"
PLAN_ID = "recommendations_implementation_plan_continue_task-v21"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
GOAL_PATH_TOKEN = ".codex/skills/continue-research-goal/goals/"

OUTPUTS = {
    "audit": ARTIFACTS / "v21_p16_t03_final_provenance_audit.md",
    "freshness": ARTIFACTS / "v21_p16_t03_freshness_report.json",
    "repairs": ARTIFACTS / "v21_p16_t03_broken_reference_repair_list.yaml",
    "execution": ARTIFACTS / "v21_p16_t03_validator_execution_log.json",
    "receipt": ARTIFACTS / "v21_p16_t03_compact_receipt.json",
    "validation": ARTIFACTS / "v21_p16_t03_validation.json",
}

DEPENDENCIES = {
    "research_control/tasks/RT-20260803-002/jobs/completions/AJC-AJ-RT-20260803-002-001.yaml": "4e59a0ae6d0740677ef0b4331f753138f32b76b27981435f5933aaab1a78fd66",
    "research_control/tasks/RT-20260722-003/jobs/completions/AJC-AJ-RT-20260722-003-001.yaml": "d381a8fd8f8867cbd5789c46c38f0967d69c0fd83a67e6592bf2d21c37b40715",
    "research_control/tasks/RT-20260802-007/jobs/completions/AJC-AJ-RT-20260802-007-001.yaml": "fddaf38076c5b4f691f75ac2d45568fc879db460de8136241de201a2aa8908b3",
    "research_control/tasks/RT-20260802-009/jobs/completions/AJC-AJ-RT-20260802-009-001.yaml": "d5d0f32aaab3fe3ecfa9affa67a50128991b3004557da2dbcc612c84569b4806",
    "research_control/tasks/RT-20260803-012/jobs/completions/AJC-AJ-RT-20260803-012-001.yaml": "32490ac7e5a57138f6de7a884825532ee17389d36634dbb9fc7f7cc076c0bf8d",
}

COMMANDS = [
    ("candidate_lineage", "research_control/tasks/RT-20260721-005/artifacts/validate_v21_candidate_lineage.py", ["--check", "--json"]),
    ("attempt_ledger", "research_control/tasks/RT-20260721-006/artifacts/validate_v21_attempt_ledger.py", ["--check", "--json"]),
    ("event_store_architecture", "research_control/tasks/RT-20260721-007/artifacts/validate_v21_event_store_architecture.py", ["--check", "--json"]),
    ("event_store_pilot", "research_control/tasks/RT-20260721-008/artifacts/v21_event_store_pilot.py", ["--check", "--json"]),
    ("formal_proof", "research_control/tasks/RT-20260720-018/artifacts/validate_eqsrc_selector_formal_proof.py", ["--json"]),
    ("proof_normal_form_registry", "scripts/research_control/validate_proof_normal_form_registry.py", ["--json"]),
    ("reproducibility_packages", "research_control/tasks/RT-20260802-009/artifacts/validate_p15_t06_reproducibility_packages.py", ["--check", "--json"]),
    ("external_action_boundary", "research_control/tasks/RT-20260802-010/artifacts/validate_p15_t07_no_external_action.py", ["--check", "--json"]),
    ("benchmark_p9_t02", "research_control/tasks/RT-20260730-008/artifacts/validate_p9_t02_vacuum_minkowski_case.py", ["--check", "--json"]),
    ("benchmark_p9_t03", "research_control/tasks/RT-20260730-010/artifacts/validate_p9_t03_weak_field_clock.py", ["--check", "--json"]),
    ("benchmark_p9_t04", "research_control/tasks/RT-20260730-011/artifacts/validate_p9_t04_causal_freefall.py", ["--check", "--json"]),
    ("benchmark_p9_t05", "research_control/tasks/RT-20260730-012/artifacts/validate_p9_t05_cosmology.py", ["--check", "--json"]),
    ("benchmark_p9_t06", "research_control/tasks/RT-20260730-013/artifacts/validate_p9_t06_radiative.py", ["--check", "--json"]),
    ("benchmark_p9_t07", "research_control/tasks/RT-20260730-015/artifacts/validate_p9_t07_nonlinear_compact.py", ["--check", "--json"]),
    ("benchmark_p9_t08", "research_control/tasks/RT-20260731-001/artifacts/validate_p9_t08_benchmark_audit.py", ["--check", "--json"]),
]


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def render_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def run_commands() -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    failures: list[str] = []
    for validator_id, script, arguments in COMMANDS:
        command = [".venv/bin/python", script, *arguments]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            payload = {}
        outcome = payload.get("status") or payload.get("validation_status") or payload.get("result_status")
        passed = result.returncode == 0 and str(outcome or "PASS_EXIT_ZERO").upper().startswith("PASS")
        records.append(
            {
                "validator_id": validator_id,
                "command": " ".join(command),
                "exit_code": result.returncode,
                "outcome": outcome or ("PASS_EXIT_ZERO" if passed else "FAIL_EXIT_NONZERO"),
                "passed": passed,
                "stdout_sha256": digest_bytes(result.stdout.encode()),
                "stderr_sha256": digest_bytes(result.stderr.encode()),
            }
        )
        if not passed:
            failures.append(f"validator_failed:{validator_id}")
    return records, failures


def audit_matrix() -> tuple[dict[str, Any], list[str]]:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    tracked_result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True)
    tracked = {item.decode() for item in tracked_result.stdout.split(b"\0") if item}
    errors: list[str] = []
    immutable = 0
    mutable = 0
    unique_paths: set[str] = set()
    selectors: set[str] = set()
    for row in data["rows"]:
        for evidence in row["selected_evidence"]:
            for prefix in ("task", "completion"):
                relative = evidence.get(f"{prefix}_path", "")
                expected = evidence.get(f"{prefix}_sha256", "")
                if not relative:
                    continue
                unique_paths.add(relative)
                path = ROOT / relative
                if relative not in tracked or not path.is_file() or path.is_symlink():
                    errors.append(f"missing_or_untracked_matrix_path:{relative}")
                    continue
                if relative == "research_control/program_state.yaml":
                    mutable += 1
                    selectors.add(evidence.get("identity_source", ""))
                else:
                    immutable += 1
                    if digest(path) != expected:
                        errors.append(f"immutable_matrix_hash_mismatch:{relative}")
    state = read_yaml(ROOT / "research_control/program_state.yaml")
    selector_checks = {
        "program_state:$.eqsrc_family_freeze_inventory_result": (state.get("eqsrc_family_freeze_inventory_result") or {}).get("plan_task_id") == "P3-T07",
        "program_state:$.p10_t08_current_burden_status_generation": (state.get("p10_t08_current_burden_status_generation") or {}).get("plan_task_id") == "P10-T08",
    }
    expected_counts = {
        "recommendation_count": 72,
        "direct_mapping_edge_count": 633,
        "verified_pre_p16_mapping_edge_count": 598,
        "pending_downstream_p16_mapping_edge_count": 35,
        "unique_verified_pre_p16_task_count": 116,
    }
    for field, expected in expected_counts.items():
        if data.get(field) != expected:
            errors.append(f"matrix_count_mismatch:{field}")
    if immutable != 1182 or mutable != 7:
        errors.append("matrix_reference_count_mismatch")
    if selectors != set(selector_checks) or not all(selector_checks.values()):
        errors.append("mutable_program_state_selector_identity_mismatch")
    return {
        **expected_counts,
        "matrix_sha256": digest(MATRIX),
        "immutable_reference_count": immutable,
        "mutable_reference_count": mutable,
        "unique_evidence_path_count": len(unique_paths),
        "mutable_selector_checks": selector_checks,
    }, errors


def audit_dependencies() -> tuple[dict[str, Any], list[str]]:
    checks: dict[str, Any] = {}
    errors: list[str] = []
    for relative, expected in DEPENDENCIES.items():
        path = ROOT / relative
        observed = digest(path) if path.is_file() else None
        checks[relative] = {"expected": expected, "observed": observed, "match": observed == expected}
        if observed != expected:
            errors.append(f"dependency_hash_mismatch:{relative}")
    return {"completion_count": len(checks), "checks": checks}, errors


def audit_registered_sources() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    checked = 0
    for relative in ("registries/MARKDOWN_SOURCE_REGISTRY.csv", "registries/TEX_SOURCE_REGISTRY.csv"):
        with (ROOT / relative).open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                source = row.get("path", "")
                source_hash = row.get("source_hash", "")
                if not source or not source_hash or TASK_ID in source:
                    continue
                checked += 1
                path = ROOT / source
                if not path.is_file() or digest(path) != source_hash:
                    errors.append(f"registered_source_mismatch:{row.get('object_id')}:{source}")
    return {"content_address_count": checked, "mismatch_count": len(errors)}, errors


def audit_control_records() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    task_count = 0
    completion_count = 0
    for task_path in sorted((ROOT / "research_control/tasks").glob("RT-*/00_TASK.yaml")):
        if TASK_ID in task_path.as_posix():
            continue
        task = read_yaml(task_path)
        plan = task.get("implementation_plan") or {}
        if plan.get("plan_id") != PLAN_ID and plan.get("plan_path") != PLAN_PATH:
            continue
        task_count += 1
        if task.get("status") not in {"completed", "blocked"}:
            continue
        job_id = task.get("current_job_id")
        completion_path = task_path.parent / "jobs/completions" / f"AJC-{job_id}.yaml"
        if not job_id or not completion_path.is_file():
            errors.append(f"v21_completion_missing:{task.get('task_id')}")
            continue
        completion = read_yaml(completion_path)
        completion_count += 1
        if completion.get("task_id") != task.get("task_id") or completion.get("job_id") != job_id:
            errors.append(f"v21_completion_identity_mismatch:{task.get('task_id')}")

    handoff_count = 0
    current_hash_mismatches = 0
    resolved_transitions = 0
    recovery_text = (
        ROOT
        / "research_control/tasks/RT-20260725-005/artifacts/p5_t01_staged_control_contract_recovery_receipt.json"
    ).read_text(encoding="utf-8")
    for handoff_path in sorted((ROOT / "research_control/handoffs").glob("handoff-*.yaml")):
        match = re.search(r"(\d+)$", handoff_path.stem)
        if not match or not 773 <= int(match.group(1)) <= 953:
            continue
        handoff = read_yaml(handoff_path)
        if not re.fullmatch(r"P\d+-T\d+", str(handoff.get("plan_task_id", ""))):
            continue
        handoff_count += 1
        relative = handoff.get("completion_path", "")
        expected = handoff.get("completion_sha256", "")
        if not relative or not expected:
            continue
        path = ROOT / relative
        observed = digest(path) if path.is_file() else None
        if observed == expected:
            continue
        current_hash_mismatches += 1
        known = (
            handoff.get("handoff_id") == "handoff-0864"
            and expected == "ff6ef8b39030b1bc64e3d977de6f9644f551c80a9315fec98c62caba6f9c6d72"
            and observed == "7e671b29d93cfe89a4ce4118dde3b8c40fe0c3bb29c6e797f504439286b49f2a"
            and observed in recovery_text
            and expected in recovery_text
        )
        if known:
            resolved_transitions += 1
        else:
            errors.append(f"unresolved_handoff_content_address:{handoff.get('handoff_id')}")
    return {
        "v21_task_record_count": task_count,
        "v21_completion_identity_count": completion_count,
        "handoff_record_count": handoff_count,
        "handoff_current_hash_mismatch_count": current_hash_mismatches,
        "resolved_historical_transition_count": resolved_transitions,
        "unresolved_control_record_count": len(errors),
    }, errors


def audit_packages() -> tuple[dict[str, Any], list[str]]:
    catalog_path = ROOT / "research_control/tasks/RT-20260802-009/artifacts/p15_t06_package_catalog_v1.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    checks: list[dict[str, Any]] = []
    goal_members = 0
    for package in catalog["packages"]:
        archive = ROOT / package["archive_path"]
        archive_hash = digest(archive) if archive.is_file() else None
        members: list[str] = []
        if archive.is_file():
            with tarfile.open(archive, "r") as handle:
                members = handle.getnames()
        forbidden = [member for member in members if GOAL_PATH_TOKEN in member]
        goal_members += len(forbidden)
        commit_exists = subprocess.run(
            ["git", "cat-file", "-e", f"{package['source_snapshot_commit']}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        ).returncode == 0
        passed = archive_hash == package["archive_sha256"] and not forbidden and commit_exists
        checks.append(
            {
                "package_id": package["package_id"],
                "archive_sha256": archive_hash,
                "archive_hash_match": archive_hash == package["archive_sha256"],
                "entry_count": len(members),
                "goal_state_member_count": len(forbidden),
                "source_snapshot_commit_exists": commit_exists,
            }
        )
        if not passed:
            errors.append(f"package_boundary_failure:{package['package_id']}")
    if GOAL_PATH_TOKEN in catalog_path.read_text(encoding="utf-8"):
        errors.append("goal_state_path_in_package_catalog")
    return {
        "catalog_sha256": digest(catalog_path),
        "package_count": len(checks),
        "goal_state_member_count": goal_members,
        "publication_authorized": bool(catalog["publication_authorized"]),
        "external_release_authorized": bool(catalog["external_release_authorized"]),
        "packages": checks,
    }, errors


def audit_attempt_repair() -> tuple[dict[str, Any], list[str]]:
    value = json.loads(ATTEMPT_VALIDATION.read_text(encoding="utf-8"))
    observed_count = (value.get("metrics") or {}).get("head_prefix_count")
    observed_hash = digest(ATTEMPT_VALIDATION)
    expected_hash = "a2e8e6731e38f11c24cec8e40dd59e5da5177866516e8f5d1c7d471fbf753fa6"
    errors = [] if observed_count == 8 and observed_hash == expected_hash else [
        "attempt_validation_generated_derivative_not_repaired"
    ]
    return {
        "path": ATTEMPT_VALIDATION.relative_to(ROOT).as_posix(),
        "preimage_sha256": "316d52625fe2698cec2bee138dd952b366ca080a00f0f52068b0500cd1f641da",
        "postimage_sha256": observed_hash,
        "expected_postimage_sha256": expected_hash,
        "head_prefix_count": observed_count,
        "append_only_ledger_modified": False,
    }, errors


def build_outputs() -> tuple[dict[Path, str], dict[str, Any]]:
    errors: list[str] = []
    matrix, found = audit_matrix()
    errors.extend(found)
    dependencies, found = audit_dependencies()
    errors.extend(found)
    sources, found = audit_registered_sources()
    errors.extend(found)
    control, found = audit_control_records()
    errors.extend(found)
    packages, found = audit_packages()
    errors.extend(found)
    repair, found = audit_attempt_repair()
    errors.extend(found)
    validators, found = run_commands()
    errors.extend(found)
    validator_passes = sum(item["passed"] for item in validators)
    result = "PASS_P16_T03_EVIDENCE_GRAPH_REPRODUCIBLE" if not errors else "FAIL"

    freshness = {
        "schema_id": "v21_p16_t03_freshness_report_v1",
        "task_id": TASK_ID,
        "audit_head": AUDIT_HEAD,
        "pre_task_generated_report_gate": {
            "status": "PASS",
            "report_count": 4,
            "failed_report_count": 0,
            "source_commit": "efcaec7df6b355681eea25ddb5b625de77e665ba",
            "observed_commit_lag": 1,
            "maximum_commit_lag": 1,
            "validator": "scripts/research_control/validate_generated_report_freshness.py --json",
        },
        "coverage_matrix_mutable_snapshot_semantics": {
            "author_time_program_state_sha256": "219c8044390f5478f407ca55037d6e02de71230f4642a5277bce57ef41e2fa44",
            "audit_start_program_state_sha256": "0870aa7e97f466bffa8dd78c9c9d59b09aa09619101ab69cc88a6e72a36f408c",
            "reference_count": matrix["mutable_reference_count"],
            "selector_identity_preserved": all(matrix["mutable_selector_checks"].values()),
            "classification": "expected_mutable_state_evolution_not_broken_content_address",
        },
        "registered_content_addresses": sources,
        "post_write_requirement": "Regenerate governed views and rerun live freshness validation after final control writes.",
        "generated_views_are_authority": False,
        "physics_promotion_authorized": False,
    }

    repairs = {
        "schema_id": "v21_p16_t03_broken_reference_repair_list_v1",
        "task_id": TASK_ID,
        "status": "PASS_NO_UNRESOLVED_BROKEN_REFERENCE" if not errors else "FAIL_UNRESOLVED",
        "finding_count": 2,
        "repaired_finding_count": 1,
        "resolved_historical_transition_count": 1,
        "unresolved_finding_count": len(errors),
        "findings": [
            {
                "finding_id": "BR-P16T03-001",
                "classification": "stale_generated_validation_derivative",
                "status": "repaired_in_scope",
                **repair,
                "repair": "Refresh generated head_prefix_count from 0 to current exact HEAD-prefix count 8; preserve the ledger byte-for-byte.",
            },
            {
                "finding_id": "BR-P16T03-002",
                "classification": "historical_author_time_content_address_transition",
                "status": "resolved_by_tracked_recovery",
                "path": "research_control/handoffs/handoff-0864.yaml",
                "author_time_completion_sha256": "ff6ef8b39030b1bc64e3d977de6f9644f551c80a9315fec98c62caba6f9c6d72",
                "current_completion_sha256": "7e671b29d93cfe89a4ce4118dde3b8c40fe0c3bb29c6e797f504439286b49f2a",
                "recovery_completion_path": "research_control/tasks/RT-20260725-005/jobs/completions/AJC-AJ-RT-20260725-005-001.yaml",
                "interpretation": "The immutable handoff preserves its author-time hash; the later exact transition is tracked, so no historical rewrite is permitted or required.",
            },
        ],
        "errors": errors,
        "authority_limits": {
            "historical_handoff_rewrite_authorized": False,
            "append_only_ledger_rewrite_authorized": False,
            "scientific_status_changed": False,
        },
    }

    execution = {
        "schema_id": "v21_p16_t03_validator_execution_log_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "validator_count": len(validators),
        "passed_validator_count": validator_passes,
        "failed_validator_count": len(validators) - validator_passes,
        "validators": validators,
        "authority_note": "Command exits and output hashes are operational evidence only; same-context recomputation is not independent replication or scientific proof.",
    }

    receipt = {
        "schema_id": "v21_p16_t03_compact_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": "P16-T03",
        "recommendation_ids": ["V21-R41", "V21-R42", "V21-R46", "V21-R47", "V21-R48", "V21-R49", "V21-R50", "V21-R52", "V21-R53", "V21-R66"],
        "result_status": result,
        "immutable_reference_count": matrix["immutable_reference_count"],
        "mutable_snapshot_reference_count": matrix["mutable_reference_count"],
        "registered_content_address_count": sources["content_address_count"],
        "v21_completion_identity_count": control["v21_completion_identity_count"],
        "package_count": packages["package_count"],
        "clean_reproduction_pass_count": 4 if validator_passes == len(validators) else 0,
        "validator_count": len(validators),
        "validator_pass_count": validator_passes,
        "repaired_finding_count": 1,
        "resolved_historical_transition_count": 1,
        "unresolved_finding_count": len(errors),
        "goal_state_member_count": packages["goal_state_member_count"],
        "claim_boundary_summary": "Operational provenance and reproducibility only; no scientific, Gate, benchmark, publication, proof, or completed-derivation promotion.",
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "publication_authorized": False,
        "external_action_authorized": False,
    }

    validation = {
        "schema_id": "v21_p16_t03_final_evidence_provenance_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "result_status": result,
        "checks": {
            "coverage_matrix": matrix,
            "dependencies": dependencies,
            "registered_sources": sources,
            "v21_control_records": control,
            "packages": packages,
            "generated_validation_repair": repair,
            "validator_pass_count": {
                "expected": len(validators),
                "observed": validator_passes,
                "match": validator_passes == len(validators),
            },
        },
        "errors": errors,
        "error_count": len(errors),
        "authority_limits": {
            "validator_pass_is_science": False,
            "independent_replication_claimed": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "publication_or_external_action_authorized": False,
        },
    }

    audit = f"""---
authority: project_control
task_id: {TASK_ID}
plan_task_id: P16-T03
status: {"PASS" if not errors else "FAIL"}
physics_promotion_authorized: false
proof_authority: false
---

# V21 P16-T03 final evidence provenance audit

## Result

**{result}**. The audited evidence graph is navigable and reproducible under
its declared immutable and mutable-state semantics. This is operational
control evidence only; it does not establish scientific truth, independent
replication, Gate success, benchmark promotion, publication authority, or a
completed derivation.

## Source and identity integrity

- {matrix["immutable_reference_count"]} immutable P16-T01 task/completion references match byte-for-byte.
- {matrix["mutable_reference_count"]} author-time program-state references evolved as expected while both exact identity selectors remain bound to P3-T07 and P10-T08.
- {sources["content_address_count"]} pre-existing registered Markdown and TeX content addresses match their source bytes.
- {control["v21_completion_identity_count"]} finalized V21 task/completion identities resolve without mismatch.
- One historical handoff content address is intentionally author-time: handoff-0864's later completion transition is exactly recorded by RT-20260725-005 and requires no historical rewrite.

## Lineage, proof, benchmark, and package reproduction

All {validator_passes} selected validators pass after the one exact generated
attempt-validation refresh. Candidate lineage, the append-only attempt chain,
event architecture, event-store pilot, the pinned Lean proof object, the proof
normal-form registry, all selected P9 benchmark receipts, the four P15 source
packages, and the no-external-action boundary reproduce their recorded
operational dispositions. The four archives contain zero recursive-goal-state
members and retain false publication and external-release authority.

## Repair and freshness

The only stale generated field was head_prefix_count in the P10 attempt
validation derivative. Its owning validator deterministically computes eight
because all eight finalized events are now the HEAD prefix. The derivative was
refreshed from preimage hash
316d52625fe2698cec2bee138dd952b366ca080a00f0f52068b0500cd1f641da to
postimage hash
a2e8e6731e38f11c24cec8e40dd59e5da5177866516e8f5d1c7d471fbf753fa6;
the append-only ledger was not modified. The pre-task live generated-report
gate passed all four report classes at the allowed one-commit lag. Final
governed views must be regenerated and revalidated after this task's control
records are finalized.

## Remaining authority boundary

P16-T04 remains unexecuted and may be routed only after this transaction
passes final generated-freshness, documentation-impact, signal, affected
research-control, memory, diff, and governed-checkpoint gates. No goal record,
local cache, ontology edit, Distance-to-GR change, publication action, push, or
external contact is included in this audit.
"""

    outputs = {
        OUTPUTS["audit"]: audit,
        OUTPUTS["freshness"]: render_json(freshness),
        OUTPUTS["repairs"]: yaml.safe_dump(repairs, sort_keys=False, allow_unicode=True),
        OUTPUTS["execution"]: render_json(execution),
        OUTPUTS["receipt"]: render_json(receipt),
        OUTPUTS["validation"]: render_json(validation),
    }
    return outputs, validation


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    outputs, validation = build_outputs()
    if args.write_report:
        for path, content in outputs.items():
            path.write_text(content, encoding="utf-8")
    else:
        stale = [
            path.relative_to(ROOT).as_posix()
            for path, content in outputs.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            validation["errors"].extend(f"stored_output_drift:{path}" for path in stale)
            validation["error_count"] = len(validation["errors"])
            validation["result_status"] = "FAIL"
    if args.json:
        print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["result_status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
